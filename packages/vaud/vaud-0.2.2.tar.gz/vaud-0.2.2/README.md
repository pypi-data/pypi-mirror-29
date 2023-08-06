# VK audio url decoder [![Build Status](https://travis-ci.org/yuru-yuri/vk-audio-url-decoder.svg?branch=master)](https://travis-ci.org/yuru-yuri/vk-audio-url-decoder)

[![PyPI - License](https://img.shields.io/pypi/l/vaud.svg)](https://pypi.org/project/vaud/)
[![GitHub issues](https://img.shields.io/github/issues/yuru-yuri/vk-audio-url-decoder-php.svg)](https://github.com/yuru-yuri/vk-audio-url-decoder-php/issues)
[![PyPI](https://img.shields.io/pypi/v/vaud.svg)](https://pypi.org/project/vaud/)


[![Maintainability](https://api.codeclimate.com/v1/badges/f88a8b485070badb584b/maintainability)](https://codeclimate.com/github/yuru-yuri/vk-audio-url-decoder/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f88a8b485070badb584b/test_coverage)](https://codeclimate.com/github/yuru-yuri/vk-audio-url-decoder/test_coverage)

## Usage:

```python

import vaud

uid = 1
url = 'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC'
decoded_url = vaud.decode(uid, url)

```

```python
 
import vaud

uid = 1
urls = [
    'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC',
    'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC',
    'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC',
]
decoder = vaud.Decoder(uid)
decoded_urls = []
for url in urls:
    decoded_urls.append(decoder.decode(url))

```
