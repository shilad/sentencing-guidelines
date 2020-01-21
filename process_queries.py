import json
import random
import time
from random import shuffle

import pandas as pd

import logging
import os
import re
import sys
import traceback

from xmljson import BadgerFish

PATH_CRED = 'pacer_credentials.txt'

logging.basicConfig(level=logging.WARN)

from juriscraper.pacer import PacerSession, PossibleCaseNumberApi


def die(*args):
    logging.fatal(*args)
    sys.exit(1)


def read_credentials():
    """
    Reads PACER username and password from PATH_CRED file.
    If the file doesn't exist it makes a dummy file.
    :return: (username, password)
    """
    # Create a dummy file if it doesn't exist
    if not os.path.isfile(PATH_CRED):
        with open(PATH_CRED, 'w') as f:
            f.write('username: XXXXX\npassword: XXXXX\n\n')
    with open(PATH_CRED) as f:
        cred_str = f.read()
        m = re.match(
            'username:\\s*(\\S+)\\s*password:\\s*(\\S+)\\s*',
            cred_str,
            flags=re.MULTILINE)
        if not m:
            die('invalid credentials file: %s', repr(cred_str))
        username = m.group(1).strip()
        password = m.group(2).strip()
        if username == 'XXXXX' or password == 'XXXXX':
            die('Username and password not configured. Please edit %s', PATH_CRED)
        return (username, password)


def main(in_path, out_path):
    (username, password) = read_credentials()
    session = PacerSession(username=username, password=password)
    df_in = pd.read_csv(in_path)

    processed_rows = set()
    if os.path.isfile(out_path):
        for line in open(out_path):
            data = json.loads(line)
            processed_rows.add(data['row_num'])

    js_clients = {}
    def get_juris_scraper(court_id):
        if court_id not in js_clients:
            js_clients[court_id] = PossibleCaseNumberApi(court_id, session)
        return js_clients[court_id]

    # Shuffle the ordering to mix up the sites and avoid hammering any one of them.
    records = df_in.to_dict(orient='records')
    random.Random(10).shuffle(records)

    for i, row in enumerate(records):
        result = dict(row)
        result['row_num'] = result['Unnamed: 0']    # index has a weird name
        del result['Unnamed: 0']

        if result['row_num'] in processed_rows:
            continue

        if i % 10 == 0:
            print('processing row %d' % i)

        try:
            js = get_juris_scraper(row['dist'])
            js.query(row['query'])
            result['response'] = xml_to_str(js.tree)
            result['status'] = 'ok'
            time.sleep(0.5)
        except:
            result['status'] = 'error'
            result['error'] = traceback.format_exc()
            traceback.print_exc()
            time.sleep(2)

        with open(out_path, 'a') as f:
            f.write(json.dumps(result) + '\n')



BF = BadgerFish(xml_fromstring=False)
def xml_to_str(xml):
    return BF.data(xml)


def append_to_csv(path, df):
    """
    From https://stackoverflow.com/a/53773275
    """
    with open(path, 'a') as f:
        df.to_csv(f, header=f.tell() == 0)


if __name__ == '__main__':
    main('case_queries.csv', 'pacer_results.json')


