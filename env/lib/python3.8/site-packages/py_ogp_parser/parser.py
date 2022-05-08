#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

def __parse_ogp(metas):
    """
    Extract meta tag contents data having `property`.

    Arguments:
        metas: Extracted meta tag data having `contents`
    Return:
        [dict] results: Extracted meta tag contents data having `property`
    """
    ogps = list(filter(lambda x: x.has_attr('property'), metas))
    results = {}
    for ogp in ogps:
        prop = str(ogp['property'])
        content = str(ogp['content'])
        if prop not in results:
            results[prop] = []
        results[prop].append(content)
    return results


def __parse_seo(metas):
    """
    Extract meta tag contents data having `name`.

    Arguments:
        metas: Extracted meta tag data having `contents`
    Return:
        [dict] results: Extracted meta tag contents data having `name`
    """
    ogps = list(filter(lambda x: x.has_attr('name'), metas))
    results = {}
    for ogp in ogps:
        prop = str(ogp['name'])
        content = str(ogp['content'])
        if prop not in results:
            results[prop] = []
        results[prop].append(content)
    return results

def domparser(dom):
    """
    Get Opengraph data or SEO data.

    Arguments:
        dom: BeautifulSoup4 Object
    
    Return:
        [dict] Page title and OpenGraph data and SEO data
    """
    metas = dom.select('meta')
    metas = list(filter(lambda x: x.has_attr('content'), metas))

    title = str(dom.find('head').find('title').string)
        
    return {
        'title': title,
        'ogp': __parse_ogp(metas),
        'seo': __parse_seo(metas)
    }

def request(url, apparent_encoding=False):
    """
    HTTP Request And Dom parsing.

    Arguments: 
        url: Request URL
        apparent_encoding: if True: use apparent_encoding, else: no apparent_encoding
    Return:
        [int]  status_code: HTTP Status Code
        [dict] ogp_data: Extracted `Page title`, `Opengraph` and `SEO` meta data, 
    """
    res = requests.get(url)
    if apparent_encoding:
        res.encoding = res.apparent_encoding
    return res.status_code, domparser(BeautifulSoup(res.text, 'html.parser'))
