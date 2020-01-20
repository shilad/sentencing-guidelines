import numpy as np
import pandas as pd

# Instructions from Chad:
# office <- tmp$OFFICE
# yr <- substr(tmp$CASLGKY,6,7)
# sequence <- substr(tmp$CASLGKY,8,12)
# feddoc <- paste0(office,":",yr,"-cr-",sequence)


# csv = pd.read_csv('./mergedData.csv', dtype=np.str, low_memory=False)
# print(sorted(csv['DISTRICT'].unique().tolist()))
# print(sorted(csv['CIRCDIST'].unique().tolist()))
# print(csv['CIRCUIT']).value_counts()
# print(csv['OFFICE'].value_counts())
# sys.exit(1)


dist_df = pd.read_csv('districts.csv')
rows = {}

dist_map = dict(zip(dist_df['DISTRICT'], dist_df['distcode']))
chunk_size = 100000
found = 0
total = 0
rows = []
row_nums = []

for i, chunk in enumerate(pd.read_csv('./mergedData.csv', chunksize=chunk_size, dtype=np.str, low_memory=False)):
    print('found %d of %d districts' % (found, total))
    for j, row in chunk.iterrows():
        total += 1
        dist = int(row['DISTRICT'])
        if dist not in dist_map:
            continue
        found += 1
        row_num = total
        row_id = row['USSCIDN']
        office = row['OFFICE']
        caslgky = row['CASLGKY']
        year = caslgky[5:7]
        seq  = caslgky[7:12]
        query = office + ":" + year + "-cr-" + seq

        row_nums.append(row_num)
        rows.append([row_id, caslgky, dist_map[dist], query])

pd.DataFrame(rows, index=row_nums, columns=['usscidn', 'caslgky', 'dist', 'query']).to_csv('./case_queries.csv')





