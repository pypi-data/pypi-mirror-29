VK audio url decoder |Build Status|
===================================

|PyPI - License| |GitHub issues| |PyPI|

|Maintainability| |Test Coverage|

Usage:
------

.. code:: bash

    pip install vaud

Decode urls:
~~~~~~~~~~~~

.. code:: python

    import vaud

    uid = 1
    url = 'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=zuHdAgfLvxaXtd1W...CsDasdvv32yLjpy3yVBxrm#AqVYStC'
    decoded_url = vaud.decode(uid, url)  # One track

.. code:: python

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

.. code:: python

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

Get all audio (not auto-decode):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import vaud

    my_vk = MyVkClass()  # Own class for vk.com
    cookies = my_vk.cookies # Get site cookies. dict()
    uid = my_vk.uid  # User id

    audio_parser = vaud.AlAudio(uid, cookies)
    all_urls = audio_parser.main()  [('encoded_url', 'Track name', 'Author'), ('encoded_url', 'Track name', 'Author')]

    decoded_urls = []  # Look before examples

.. |Build Status| image:: https://travis-ci.org/yuru-yuri/vk-audio-url-decoder.svg?branch=master
   :target: https://travis-ci.org/yuru-yuri/vk-audio-url-decoder
.. |PyPI - License| image:: https://img.shields.io/pypi/l/vaud.svg
   :target: https://pypi.org/project/vaud/
.. |GitHub issues| image:: https://img.shields.io/github/issues/yuru-yuri/vk-audio-url-decoder.svg
   :target: https://github.com/yuru-yuri/vk-audio-url-decoder/issues
.. |PyPI| image:: https://img.shields.io/pypi/v/vaud.svg
   :target: https://pypi.org/project/vaud/
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/f88a8b485070badb584b/maintainability
   :target: https://codeclimate.com/github/yuru-yuri/vk-audio-url-decoder/maintainability
.. |Test Coverage| image:: https://api.codeclimate.com/v1/badges/f88a8b485070badb584b/test_coverage
   :target: https://codeclimate.com/github/yuru-yuri/vk-audio-url-decoder/test_coverage
