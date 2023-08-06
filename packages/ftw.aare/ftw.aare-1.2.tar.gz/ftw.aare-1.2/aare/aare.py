import datetime
import itertools
import locale
import pdb

import click
import requests

LANGUAGE = "en"
session = requests.Session()


def _(s):
    global LANGUAGE

    de = {"Current temperature of the aare: {}° C": "Aktuelle Temperatur der Aare: {}° C",
          "{}: min {}° C, max {}° C": "{}: min {}° C, max {}° C"}

    if LANGUAGE == "de":
        return de[s]
    else:
        return s


@click.command()
@click.option('--statistics', help='show the hottest and the coolest temperature of the last 7 days', is_flag="True")
@click.option('--language', default="", help='set the language of the output. Possible languages: "de" (German), '
                                             '"en" (English). The output is displayed in the OS language by default, '
                                             'it will also be displayed english if an invalid argument is passed.')
def aare(statistics, language):
    """A simple command which displays the current aare temperature"""
    if language != "":
        set_language(language)
    else:
        set_system_language()

    if statistics:
        display_stats()
    else:
        display_current_temp()


def set_language(lang):
    global LANGUAGE
    LANGUAGE = lang


def display_current_temp():
    api_url = 'http://aare.schwumm.ch/aare.json'
    response = session.get(api_url)
    aare_json = response.json()
    click.echo(_("Current temperature of the aare: {}° C").format(aare_json["temperature"]))


def display_stats():
    api_url = 'http://aare.schwumm.ch/api/archive'
    params = {"from": "now", "to": "-7 days"}
    # The website denies unknown user agents. So we have to impersonate a general webbrowser to gain access
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'}
    response = session.get(api_url, params=params, headers=headers)
    response_json = response.json()
    temperatures = response_json['data']['temperature']
    dates = [datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S') for item in response_json['data']['datetime']]
    data = list(zip(dates, temperatures))

    # Remove data points not having a temperature
    data = list(filter(lambda item: item[1], data))
    for key, group in itertools.groupby(data, lambda item: datetime.date(item[0].year, item[0].month, item[0].day)):
        temperatures = [item[1] for item in tuple(group)]
        min_temp = min(temperatures)
        max_temp = max(temperatures)
        day_string = key.strftime('%Y-%m-%d')
        output = _("{}: min {}° C, max {}° C").format(day_string, min_temp, max_temp)
        print(output)


def set_system_language():
    locale_tuple = locale.getdefaultlocale()
    lang = locale_tuple[0]
    if lang == "de_DE" or lang == "de_CH":
        set_language("de")


if __name__ == '__main__':
    aare()
