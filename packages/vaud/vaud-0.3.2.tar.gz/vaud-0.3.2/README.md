# VK audio url decoder [![Build Status](https://travis-ci.org/yuru-yuri/vk-audio-url-decoder.svg?branch=master)](https://travis-ci.org/yuru-yuri/vk-audio-url-decoder)

[![PyPI - License](https://img.shields.io/pypi/l/vaud.svg)](https://pypi.org/project/vaud/)
[![GitHub issues](https://img.shields.io/github/issues/yuru-yuri/vk-audio-url-decoder.svg)](https://github.com/yuru-yuri/vk-audio-url-decoder/issues)
[![PyPI](https://img.shields.io/pypi/v/vaud.svg)](https://pypi.org/project/vaud/)


[![Maintainability](https://api.codeclimate.com/v1/badges/f88a8b485070badb584b/maintainability)](https://codeclimate.com/github/yuru-yuri/vk-audio-url-decoder/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f88a8b485070badb584b/test_coverage)](https://codeclimate.com/github/yuru-yuri/vk-audio-url-decoder/test_coverage)

## Usage:

### Decode urls:

```python

import vaud

uid = 1
url = 'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC'
decoded_url = vaud.decode(uid, url)  # One track

```

```python

import vaud

uid = 1
urls = [
    'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC',
    'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC',
    'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC',
]
decoder = vaud.Decoder(uid)  # Multiple tracks
decoded_urls = []
for url in urls:
    decoded_urls.append(decoder.decode(url))

```

```python

import vaud

# DO NOT DO THIS! :
# (This creates a lot of unnecessary classes for the loop)
# For loop use previous example 

uid = 1
urls = []
decoded_urls = [
    'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC',
    'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC',
    'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC',
]

for url in urls:
    decoded_urls.append(vaud.decode(uid, url))

```

### Get all audio (not auto-decode):

```python

import vaud

my_vk = MyVkClass()  # Own class for vk.com
cookies = my_vk.cookies # Get site cookies. dict()
uid = my_vk.uid  # User id

audio_parser = vaud.AlAudio(uid, cookies)
all_urls = audio_parser.main()  [('encoded_url', 'Track name', 'Author'), ('encoded_url', 'Track name', 'Author')]

decoded_urls = []  # Look before examples

```
