# -*- coding: utf-8 -*-

import os

from bio2bel.utils import get_connection, get_data_dir

MODULE_NAME = "hmdd"
DATA_DIR = get_data_dir(MODULE_NAME)
DEFAULT_CACHE_CONNECTION = get_connection(MODULE_NAME)
DATA_URL = "http://www.cuilab.cn/files/images/hmdd2/alldata.txt"
DATA_FILE_PATH = os.path.join(DATA_DIR, "hmddRawData.tsv")
col_names = ["Index", "miRNA ID", "MeSHDisease term", "PubMed ID", "Description"]