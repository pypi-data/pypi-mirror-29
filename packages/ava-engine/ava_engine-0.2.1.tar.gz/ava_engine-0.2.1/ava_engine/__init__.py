#!/usr/bin/env python
# -*- coding: utf-8 -*-
import grpc

from ava_engine.ava.api_engine_ping_pb2 import PingRequest
from ava_engine.ava.api_engine_detect_pb2 import DetectRequest, DetectResponse, ImageItem
from ava_engine.ava.api_engine_get_detect_pb2 import GetDetectResponse

from ava_engine.ava.api_model_sync_pb2 import ModelSyncRequest
from ava_engine.ava.api_model_load_pb2 import ModelLoadRequest
from ava_engine.ava.api_model_download_pb2 import ModelDownloadRequest

from ava_engine.ava.service_api_pb2_grpc import EngineApiDefStub
from ava_engine.ava.service_api_pb2_grpc import ModelApiDefStub


class Client:
    """Client class encapsulates all API calls to the Ava Engine."""

    def __init__(self, host, port):
        self._host = host
        self._port = port

        self._channel = grpc.insecure_channel('{host}:{port}'.format(host=host, port=port))
        self._engine_stub = EngineApiDefStub(self._channel)
        self._model_stub = ModelApiDefStub(self._channel)

    def ping(self):
        """Invokes the `Ping` request, returning a `ava_engine_ava.api_ping_pb2.PingResponse`."""
        return self._engine_stub.Ping(PingRequest())

    def detect(self, model_key, images):
        """Given an list of image objects, performs image detection on each image.

        `images` are expected to be an array of objects where each object has a `data` key
        to represent image bytes and an optional, free form `custom_id`. For example:

        >>> import uuid
        >>> client = Client('localhost', 50051)
        >>> detection_images = [
        ...     {'data': open('...').read(), 'custom_id': uuid.uuid4()},
        ...     {'data': open('...').read(), 'custom_id': uuid.uuid4()},
        ...     {'data': open('...').read(), 'custom_id': uuid.uuid4()},
        ...     {'data': open('...').read(), 'custom_id': uuid.uuid4()},
        ...     {'data': open('...').read()},
        ... ]
        >>> client.detect('person_day', detection_images)

        Args:
            model_key (str): The name or id of the model that has been previously loaded.
            images (list[dict]): A list of image dictionaries, each dict has a data key and an
                optional custom_id key.

        Returns:
            ava_engine.ava.api_detect_pb2.DetectResponse: An instance of DetectResponse.

        """
        if not images:
            return DetectResponse(id=None, results=[])

        detection_images = []
        for image in images:
            detection_images.append(ImageItem(data=image['data'], custom_id=image.get('custom_id')))
        return self._engine_stub.Detect(DetectRequest(model_key=model_key, images=detection_images))

    def get_detect(self, detection_id):
        """Given a `detection_id` from a previous `detect` call, retrieve historical results.

        Args:
            detection_id (str): The id from a previous detection call

        Returns:
            ava_engine.ava.api_get_detect_pb2.GetDetectResponse: An instance of GetDetectResponse.

        """
        return self._engine_stub.GetDetect(GetDetectResponse(id=detection_id))

    def sync_models(self):
        """Syncs latest models between this client and our model update server."""
        return self._model_stub.Sync(ModelSyncRequest())

    def load_model(self, id=None, name=None, memory_percentage=None):
        """Loads a model given the `name` or `id` into memory if it exists in storage."""
        message = ModelLoadRequest()
        if id:
            message.id = id
        if name:
            message.name = name
        if memory_percentage:
            message.memory_percentage = memory_percentage
        return self._model_stub.Load(message)

    def download_model(self, id_):
        """Download the a model given the model `id_` if it exists."""
        return self._model_stub.Download(ModelDownloadRequest(id=id_))


def connect(host='localhost', port=50051):
    """Creates a `Client` instance, allowing connections to the ava-engine daemon.

    Args:
        host (str, optional): The server address (without port, including protocol).
        port (int, optional): The server's exposed port

    Returns
        ava_engine.Client: An instance of `ava_engine.Client`.

    """
    return Client(host, port)
