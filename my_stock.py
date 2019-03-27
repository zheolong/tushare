#-*- coding:utf-8 -*-

import sys
import tushare as ts
import pandas as pd

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

csv_file_name = sys.argv[1]

ts.set_token('be824752c259de2aa58d4551f693a3c1aa17754cdf4cb779c9030ed9')

pro = ts.pro_api()
#查询当前所有正常上市交易的股票列表
stocks = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

# Create the pandas DataFrame
df_all = pd.DataFrame({}, columns = ['sequence', 'scene', 'amount'])

is_first_df = True

open(csv_file_name, 'w').close()

csv_file = open(csv_file_name, 'a')

for index, row in stocks.iterrows():
    #print(row)
    #sys.exit(0)
    symbol = row['symbol']
    industry = row['industry']

    his_data = ts.get_hist_data(symbol) #一次性获取全部数据
    if his_data is None:
        continue

    
    his_data = his_data.reset_index()
    #print(his_data.columns)
    #sys.exit(0)

    df_tmp = pd.DataFrame({}, columns = ['sequence', 'scene', 'amount'])
    df_tmp[['sequence','amount']] = his_data[['date','open']]
    df_tmp['scene'] = symbol + "_" + industry

    if is_first_df:
        df_tmp.to_csv(csv_file, header = True, index = False)
        is_first_df = False
    else:
        df_tmp.to_csv(csv_file, mode = 'a', header = False, index = False)

csv_file.close()

#print(type(stocks))
#print(stocks)
