# -*- coding: utf-8 -*-
import emoji.unicode_codes as codes
import re


class UnicodeEmojiProvider(object):

    def __iter__(self):
        ws_patt = re.compile(r'\s+')
        source = codes.EMOJI_UNICODE.items()
        emojis = sorted(source, key=len, reverse=True)
        for name, emoji_ in emojis:
            yield (ws_patt.sub('', emoji_), 'emoji:' + name)
