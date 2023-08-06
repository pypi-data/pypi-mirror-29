# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import re


# Refer: http://stackoverflow.com/questions/26568722/remove-unicode-emoji-using-re-in-python
# Refer: http://stackoverflow.com/questions/22706522/python-remove-ios-emoji-characters-in-a-unicode-str-to-avoid-databaseerror-in
# Refer: https://stackoverflow.com/questions/13729638/how-can-i-filter-emoji-characters-from-my-input-so-i-can-save-in-mysql-5-5
try:
    # Wide UCS-4 build
    emoji_regex = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
except re.error:
    # Narrow UCS-2 build
    emoji_regex = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
