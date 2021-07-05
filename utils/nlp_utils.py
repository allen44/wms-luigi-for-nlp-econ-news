import re
import pickle
import unicodedata
import requests
import os
import pickle

import requests_cache
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import spacy

# Load contraction map
from contractions import CONTRACTION_MAP

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from tqdm.notebook import tqdm


from pprint import pprint

import stanza

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import model_evaluation_utils as meu


def scrap_static_website(**kwargs):
  # Unpack kwargs
  url_root = kwargs.get('url_root', 'https://www.prnewswire.com/news/institute-for-supply-management')
  urls = kwargs.get('urls', [ f'{url_root}/?page={p}&pagesize=100' \
        for p in (1, 2, 3, 4)])
  session = kwargs.get('session', requests_cache.CachedSession('news_cache'))
  headers = kwargs.get('headers', {'User-Agents': 'Mozilla/5.0',
          'referer': url_root})
  
  # Identify links of interest
  links = []
  links_suffixes = []
  for url in urls:
    # Use requests to retrieve data from a given URL
    news_response = session.get(url, headers=headers)
    # Parse the whole HTML page using BeautifulSoup
    news_soup = BeautifulSoup(news_response.text, 'html.parser')
    # Get a list of all the links
    for link in news_soup.find_all('a'):
      # print(link.get('href'))
      # print(type(link.get('href')))
      href = str(link.get('href'))
      if 'news-release' in href:
        # Filter the links to include the phrase 'PMI-at'
        if 'pmi-at' in href \
        and 'hospital' not in href \
        and 'services' not in href: 
          suffix = link.get('href').replace('/news-releases', '')
          links.append(f'{url_root}{suffix}')
          links_suffixes.append(suffix)
        # elif 'nmi-at' in str(link.get('href')):
        # links.append(link.get('href'))
  direct_links = ['https://www.prnewswire.com/news-releases'+ suffix for suffix in links_suffixes ]

  # Parse results
  res = session.get(direct_links[0])
  soup = BeautifulSoup(res.text, 'html.parser')

  return links, links_suffixes, direct_links, session, soup
