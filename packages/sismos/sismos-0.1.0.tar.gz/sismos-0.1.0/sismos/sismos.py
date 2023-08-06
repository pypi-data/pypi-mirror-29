# -*- coding: utf-8 -*-

"""Main module."""

from lxml import html
import requests

def lastEarthquake():
    """ Prints last earthquake in Colombia """
    page = requests.get('http://200.119.88.135/RSNC/paginas/preliminar/detalles.php')
    tree = html.fromstring(page.content)
    # Last earthquake in Colombia
    infoIds = ['fechaL','horaL','mag','orienta','ubica']
    for id in infoIds:
            print(tree.xpath('//*[@id="'+id+'"]')[0].text)
