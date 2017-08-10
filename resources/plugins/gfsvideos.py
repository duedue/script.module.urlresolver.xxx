'''
    urlresolver XBMC Addon
    Copyright (C) 2016 Gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import re, urlparse
from urlresolver import common
from urlresolver.plugins.lib import helpers
from urlresolver.resolver import UrlResolver, ResolverError

class GFSVideosResolver(UrlResolver):
    name = 'gfsvideos'
    domains = ['gfsvideos.com']
    pattern = '(?://|\.)(gfsvideos\.com)/video/([\w-]+-\d+\.html)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        html = self.net.http_GET(web_url, headers=headers).content

        if html:
            try:
                file = re.search('''<source\s*src=['"]([^"']+)''', html, re.DOTALL).groups()[0]
                headers.update({'Referer': web_url, \
                                'Accept-Encoding': 'identity;q=1, *;q=0', \
                                'chrome-proxy': 'frfr', \
                                'Accept': '*/*', \
                                'Accept-Language': 'en-US,en;q=0.8'})
                return file + helpers.append_headers(headers)
            except:
                raise ResolverError('File not found')

        raise ResolverError('File not found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='http://www.{host}/video/{media_id}')

    @classmethod
    def _is_enabled(cls):
        return True
