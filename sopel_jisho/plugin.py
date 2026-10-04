"""sopel-jisho

Jisho lookup plugin for Sopel IRC bots.

Copyright 2016-2026, dgw
Licensed under the GPL v3.0 or later
"""
from __future__ import annotations

from sopel import plugin

import requests


api_url = 'https://jisho.org/api/v1/search/words?keyword=%s'
request_headers = {
    'User-Agent': 'sopel-jisho (https://github.com/dgw/sopel-jisho)',
}


@plugin.commands('jisho', 'ji')
@plugin.output_prefix('[jisho] ')
@plugin.example('.ji onsen')
def jisho(bot, trigger):
    query = trigger.group(2) or None
    try:
        results = fetch_results(query)
    except JishoError as e:
        bot.say(str(e))
        return

    try:
        entry = results['data'][0]
    except IndexError:
        bot.say("No results.")
        return

    message, link = format_output(entry)
    bot.say(message, truncation=' …', trailing=' | ' + link)


class JishoError(Exception):
    """Custom exception for Jisho API errors."""


def format_output(entry: dict) -> tuple[str, str]:
    """Expects just one "word" entry from the search response.

    Returns a tuple of (formatted message, word URL).
    """
    japanese = entry['japanese']
    word = format_words_and_readings(japanese[:1])
    meanings = []
    for number, sense in enumerate(entry['senses'], start=1):
        parts_of_speech = ', '.join(sense.get('parts_of_speech', []))
        definitions = ', '.join(sense['english_definitions'])
        part_of_speech = " ({})".format(parts_of_speech) if parts_of_speech else ''
        meanings.append("{number}.{part_of_speech} {definitions}".format(
            number=number,
            part_of_speech=part_of_speech,
            definitions=definitions))
    out = "{word} | {meanings}".format(
        word=word, meanings='; '.join(meanings))
    other_forms = format_words_and_readings(japanese[1:])
    if other_forms:
        out += " | Other forms: {forms}".format(forms=other_forms)
    return out, 'https://jisho.org/word/' + entry['slug']


# Tempted to use TypedDict and specify the expected keys, but... overkill
def format_words_and_readings(items: list[dict[str, str]]) -> str:
    forms = []
    for item in items:
        word = item.get('word') or item.get('reading') or ''
        reading = item.get('reading')
        if reading and reading != word:
            word = "{word} ({reading})".format(word=word, reading=reading)
        if word and word not in forms:
            forms.append(word)
    return ', '.join(forms)


def fetch_results(query: str | None) -> dict:
    if not query:
        raise JishoError("No search query provided.")
    try:
        r = requests.get(
            url=api_url % query,
            headers=request_headers,
            timeout=(10.0, 4.0),)
    except requests.exceptions.ConnectTimeout:
        raise JishoError("Connection timed out.")
    except requests.exceptions.ConnectionError:
        raise JishoError("Couldn't connect to server.")
    except requests.exceptions.ReadTimeout:
        raise JishoError("Server took too long to send data.")
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise JishoError("HTTP error: " + str(e))
    try:
        data = r.json()
    except ValueError:
        raise JishoError(r.content)
    if data['meta']['status'] != 200:
        raise JishoError("Jisho API returned error code %s" % data['meta']['status'])

    return data
