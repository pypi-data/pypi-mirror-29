# ava_engine

**Welcome to ava_engine!**

This is the official Python client library for Image Intelligence's Ava Engine (AI edge solution).

## Installation & usage

```bash
pip install ava-engine
```

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import ava_engine


def main():
    client = ava_engine.connect('localhost', 50051)
    print(client.ping())
    print(client.sync_models())

    client.load_model(name='person_day')

    detection_results = client.detect([
        {'data': open('./data/images/test_image_1.jpg', 'rb').read(), 'custom_id': str(uuid.uuid4())},
        {'data': open('./data/images/test_image_2.jpg', 'rb').read(), 'custom_id': str(uuid.uuid4())},
        {'data': open('./data/images/test_image_3.jpg', 'rb').read(), 'custom_id': str(uuid.uuid4())},
        {'data': open('./data/images/test_image_4.jpg', 'rb').read(), 'custom_id': str(uuid.uuid4())},
        {'data': open('./data/images/test_image_5.jpg', 'rb').read()},
        {'data': open('./data/images/test_image_6.jpg', 'rb').read()},
        {'data': open('./data/images/test_image_7.jpg', 'rb').read()},
    ])
    print(detection_results)
    print(client.get_detect(detection_results.id))


if __name__ == '__main__':
    main()
```
