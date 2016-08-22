"""Module for reading, preprocessing, and enriching the raw dataset"""

import pandas as pd
import os
import requests
import urllib
import BeautifulSoup

base_uri = "http://dashboard.healthit.gov/datadashboard/data"
data_fname = "systematic-lit-review-appendix.csv"
tmp_dir = "tmp"
out_fp = os.path.join(tmp_dir, data_fname)


def read_data():
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    if not os.path.exists(out_fp):
        df = pd.read_csv(os.path.join(base_uri, data_fname))
        df.to_csv(out_fp, index=False)
    else:
        df = pd.read_csv(out_fp)
    return df


def clean_text(t):
    return t.replace("&amp;apos;", "")


def preprocess_data(df):
    df.loc[:, "author"] = df["author"].apply(clean_text)
    df.loc[:, "article_title"] = df["article_title"].apply(clean_text)
    df.loc[:, "google_scholar_search_term"] = \
        df["author"] + " " + df["article_title"]
    return df


def get_google_scholar(payload):
    '''payload is a dictionary'''
    gscholar_base_uri = "https://scholar.google.com/scholar"
    return requests.get(gscholar_base_uri, params=payload).text


def parse_gres_html(gres_html):
    s = BeautifulSoup.BeautifulSoup(gres_html)
    gs_bdy = s.find("div", {"id": "gs_bdy"})
    gs_r = gs_bdy.findAll("div", {"class": "gs_r"})
    return gs_r


if __name__ == "__main__":
    df = preprocess_data(read_data())

    # data check 1
    msg_1 = "article_title contains '&' characters"
    assert len(df["article_title"][
        df["article_title"].str.contains("&")]) == 0, msg_1

    search_term = df['google_scholar_search_term'].iloc[0]
    gres = get_google_scholar({'q': search_term})
    gres_text = parse_gres_html(gres)
    print gres_text
