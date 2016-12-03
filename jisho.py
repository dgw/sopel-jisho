"""
jisho.py - Jisho lookup module for Sopel
Copyright 2016, dgw
Licensed under the GPL v3.0 or later
"""

from __future__ import unicode_literals
from sopel.module import commands, example
import requests

api_url = 'http://jisho.org/api/v1/search/words?keyword=%s'


@commands('jisho', 'ji')
@example('.ji onsen')
def jisho(bot, trigger):
    query = trigger.group(2) or None
    bot.say("[Jisho] %s" % fetch_result(query))


def fetch_result(query):
    if not query:
        return "No search query provided."
    try:
        r = requests.get(url=api_url % query, timeout=(10.0, 4.0))
    except requests.exceptions.ConnectTimeout:
        return "Connection timed out."
    except requests.exceptions.ConnectionError:
        return "Couldn't connect to server."
    except requests.exceptions.ReadTimeout:
        return "Server took too long to send data."
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return "HTTP error: " + e.message
    try:
        data = r.json()
    except ValueError:
        return r.content
    if data['meta']['status'] != 200:
        return "Jisho API returned error code %s" % data['meta']['status']

    try:
        entry = data['data'][0]
    except IndexError:
        return "No results."

    word = entry['japanese'][0].get('word') or ''
    furigana = [item['reading'] for item in entry['japanese'] if not word or
                (item.get('word') or query) == word and item.get('reading')]
    readings = ', '.join(furigana) if len(furigana) else ''
    if word:
        readings = " ({readings})".format(readings=readings)
    meaning = ', '.join(entry['senses'][0]['english_definitions'])
    return "{word}{readings}: {meaning}".format(word=word, readings=readings, meaning=meaning)
