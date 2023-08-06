# -*- coding: utf-8 -*-
from . import generic


class Parser(generic.Parser):
    oembed_api_url = 'http://soundcloud.com/oembed?url={url}&format=json&visual=false&maxheight=150'

    def get_embed(self):
        response = self.fetch_oembed()

        if response:
            return {
                "id": None,
                "url": self.url,
                "type": response['type'],
                'duration': self.embed_duration(),
                "height": response['height'],
                "width": None,
                "ratio": None,
                "html_code": response['html']
            }
