import json
import logging
import pandas as pd
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

TOP_LEVEL_FIELDS = {
    'row_num' : 'row',
    'usccidn' : 'usccidn',
    'query' : 'pacer_query',
    'caslgky' : 'caslgky',
    'dist' : 'district_abbrev',
}

CASE_FIELDS = {
    '@number' : 'case_number',
    '@id' : 'case_id',
    '@title' : 'case_title',
    '@sortable' : 'case_sortable',
    '@defendant' : 'case_defendant',
}

query_cases = [0] * 11
num_cases = 0
num_errors = 0
dist_errors = defaultdict(int)
dist_queries = defaultdict(int)

with open('./pacer_results.json', 'r') as f:
    rows = []
    for i, line in enumerate(f):
        if i % 50000 == 0:
            logging.info("processing line %d, found %d cases and %d errors",
                         i, num_cases, num_errors)

        js = json.loads(line)
        dist_queries[js['dist']] += 1
        if js['status'] == 'ok' and 'case' in js['response'].get('request', {}):
            cases = js['response']['request']['case']
            if type(cases) == dict:
                cases = [cases] # a single result
            num_cases += len(cases)
            query_cases[min(len(query_cases) - 1, len(cases))] += 1
            for case in cases:
                record = {}
                for (k, v) in TOP_LEVEL_FIELDS.items():
                    record[v] = js.get(k, '')
                for (k, v) in CASE_FIELDS.items():
                    record[v] = case.get(k, '')
                rows.append(record)
        else:
            num_errors += 1
            dist_errors[js['dist']] += 1
            query_cases[0] += 1

    pd.DataFrame(rows).to_csv('./pacer_results.csv', encoding='utf-8')

for (n, d) in sorted([(n, d) for (d, n) in dist_errors.items()], reverse=True):
    logging.info('district %s has %d errors (%.1f %% of queries)',
                 d, n, 100.0 * n / dist_queries[d])

for i, n in enumerate(query_cases):
    logging.info('%d cases had %d cases (%.1f%%)',
                 n, i, 100.0 * n / sum(query_cases))
