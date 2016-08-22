"""Module for reading, preprocessing, and enriching the raw dataset
"""

import pandas as pd
import os
import requests

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

if __name__ == "__main__":
    df = read_data()
    print df.head()
