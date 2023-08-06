import json
import re
import requests
from time import sleep


class AlAudioBase(object):
    limit = 0
    offset = 0
    debug = False
    response_debug_callback = None
    force_data = False  # Ignore hasMore flag from response

    _api_url = 'https://vk.com/al_audio.php'
    _cookies = None
    _uid = None
    _user_agent = '%s %s %s %s' % (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'AppleWebKit/537.36 (KHTML, like Gecko)',
        'Chrome/60.0.3112.101',
        'Safari/537.36'
    )
    _playlist_id = -1  # Default - all tracks
    _sleep_time = 10
    _split_audio_size = 6
    _response_as_tuples_list = False

    _playlist = None
    _list_post_load = None
    _list_decoded_tracks = None
    _list_unparsed_tracks = None

    def __init__(self):
        self._playlist = []
        self._list_unparsed_tracks = []
        self._list_post_load = []
        self._list_decoded_tracks = []

    @property
    def _headers(self):
        return {
            'User-Agent': self._user_agent,
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Referer': 'https://vk.com/audios%d' % self._uid,
        }

    def _load_data(self, offset=0):
        return {
            'access_hash': '',
            'act': 'load_section',
            'al': 1,
            'claim': '0',
            'offset': offset,
            'owner_id': self._uid,
            'playlist_id': self._playlist_id,
            'type': 'playlist'
        }

    @staticmethod
    def _reload_data(ids):
        return {
            'act': 'reload_audio',
            'al': 1,
            'ids': ','.join(ids)
        }

    def __parse_track(self, item):
        """
        :param item:
        :type item list
        :return:
        :rtype dict
        :rtype tuple
        """
        if self._response_as_tuples_list:
            return item[2], item[3], item[4], item[0]
        return {'url': item[2], 'track': item[3], 'author': item[4], 'id': item[0]}

    def _get_playlist_response(self, offset):
        if offset == 0 and self.offset > 0:
            offset = self.offset

        response = self._parse_response(self._post(
            self._api_url,
            self._load_data(offset)
        ))

        if not response or len(response.get('list', [])) < 1:
            sleep(self._sleep_time * 2)  # spam-ban. sleeping.
            response = self._post(
                self._api_url,
                self._load_data(offset)
            )

            callable(self.response_debug_callback) and self.response_debug_callback(response)

            response = self._parse_response(response)
        return response

    def _post(self, url, data):
        response = requests.post(
            url, data=data,
            headers=self._headers,
            cookies=self._cookies
        )
        for i in response.cookies.get_dict():
            self._cookies[i] = response.cookies[i]
        return response.text

    @staticmethod
    def _parse_response(response, default=None):
        if default is None:
            default = {}
        try:
            data = re.search(r'<!json>(.+?)<!>', response).group(1)
            return json.loads(data)
        except Exception:
            return default

    def _parse_playlist_func(self, i):
        if i[2] == '':
            self._list_post_load.append(i)
        else:
            self._list_decoded_tracks.append(self.__parse_track(i))
        if len(self._list_post_load) >= self._split_audio_size:
            self._parse_list_items(self._list_post_load)
            self._list_post_load = []

    def _parse_list_items(self, items):
        result = []
        for item in items:
            result.append('%d_%d' % (item[1], item[0]))
        self._list_decoded_tracks += self._decode_playlist(result)

    def _decode_playlist(self, items):
        response = self._post(
            self._api_url,
            self._reload_data(items)
        )

        _ = self._parse_response(response)
        if not isinstance(_, list) or len(_) < 1:
            if self.debug:
                print('Time ban. Sleep...')

            sleep(self._sleep_time)

            response = self._post(
                self._api_url,
                self._reload_data(items)
            )

            callable(self.response_debug_callback) and self.response_debug_callback(response)

        if len(response) < len(items):
            self.__check_un_parsed_tracks(items, response)

        return self.__rebuild_response(response)

    @staticmethod
    def __get_tracks_ids(items):
        def __x(x):
            return x[0]
        return map(__x, items)

    def __check_un_parsed_tracks(self, items, response):
        idx = self.__get_tracks_ids(response)
        for i in items:
            if i not in idx:
                self._list_unparsed_tracks.append(i)

    def __rebuild_response(self, response):
        data = self._parse_response(response)
        if isinstance(data, list):
            return [self.__parse_track(i) for i in data]
        return []
