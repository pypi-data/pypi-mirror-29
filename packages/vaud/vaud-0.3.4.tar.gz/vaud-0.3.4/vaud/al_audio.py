import json
import re
import requests
import time


class AlAudio(object):
    _api_url = 'https://vk.com/al_audio.php'
    _cookies = None
    _uid = None
    _user_agent = '%s %s %s %s' % (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'AppleWebKit/537.36 (KHTML, like Gecko)',
        'Chrome/60.0.3112.101',
        'Safari/537.36'
    )
    _playlist = None
    _playlist_id = -1  # Default - all tracks
    _sleep_time = 10
    _split_audio_size = 5
    _un_parsed_tracks = None
    limit = 0
    offset = 0
    debug = False
    response_debug_callback = None
    force_data = False  # Ignore hasMore flag from response

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

    def __init__(self, uid, cookies):
        """
        :param uid: user_id
        :type uid: int
        :param cookies:
        :type cookies: dict
        """
        self._uid = int(uid)
        self._cookies = cookies
        self._playlist = []
        self._un_parsed_tracks = []

    def main(self):
        self._fill_playlist()
        response = self._parse_playlist()
        if len(response) > self.limit > 0:
            response = response[0:self.limit]
        return response

    def set_playlist_id(self, _id):
        self._playlist_id = _id

    def __get_playlist_response(self, offset):
        if offset == 0 and self.offset > 0:
            offset = self.offset

        response = self._parse_response(self._post(
            self._api_url,
            self._load_data(offset)
        ))
        if not response or len(response.get('list', [])) < 1:
            time.sleep(self._sleep_time * 2)  # spam-ban. sleeping.
            response = self._parse_response(self._post(
                self._api_url,
                self._load_data(offset)
            ))
        return response

    def _fill_playlist(self, offset=0):
        response = self.__get_playlist_response(offset)

        check_type = response.get('type', '') != 'playlist'

        if check_type or len(self._playlist) >= self.limit > 0:
            return

        self._playlist += response.get('list', [])

        if self.force_data or int(response.get('hasMore', 0)) != 0:
            time.sleep(self._sleep_time)  # spam-ban. sleeping.
            self._fill_playlist(response.get('nextOffset'))

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

    def _parse_playlist(self):
        post_load = []
        response = []
        for i in self._playlist:
            if i[2] == '':
                post_load.append(i)
            else:
                response.append((i[2], i[3], i[4], i[0]))
            if len(post_load) > self._split_audio_size:
                time.sleep(self._sleep_time / 20)
                response += self._parse_list_items(post_load)
                post_load = []
        return response

    def _parse_list_items(self, items):
        result = []
        for item in items:
            result.append('%d_%d' % (item[1], item[0]))
        return self._decode_playlist(result)

    @staticmethod
    def _get_reload_data(ids):
        return {
            'act': 'reload_audio',
            'al': 1,
            'ids': ','.join(ids)
        }

    @staticmethod
    def _get_tracks_ids(items):
        return [i[0] for i in items]

    def _check_un_parsed_tracks(self, items, response):
        idx = self._get_tracks_ids(response)
        for i in items:
            if i not in idx:
                self._un_parsed_tracks.append(i)

    def _decode_playlist(self, items):
        response = self._post(
            self._api_url,
            self._get_reload_data(items)
        )

        _ = self._parse_response(response)
        if not isinstance(_, list) or len(_) < 1:
            if self.debug:
                print('Time ban. Sleep...')

            time.sleep(self._sleep_time)

            response = self._post(
                self._api_url,
                self._get_reload_data(items)
            )

            callable(self.response_debug_callback) and self.response_debug_callback(response)

        if len(response) < len(items):
            self._check_un_parsed_tracks(items, response)

        return self._rebuild_response(response)

    def _rebuild_response(self, response):
        data = self._parse_response(response)
        if isinstance(data, list):
            return [(i[2], i[3], i[4], i[0]) for i in data]
        return []
