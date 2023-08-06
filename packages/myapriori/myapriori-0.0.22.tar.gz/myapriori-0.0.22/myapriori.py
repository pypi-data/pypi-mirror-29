# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:19:25 2017

@author: jimmybow
"""
from __future__ import print_function
from apyori import apriori
import pandas as pd
import numpy as np
import time

# 尋找關聯規則的函數 支援兩種資料格式 
# type = 'df' 一般資料表 (皆為類別欄位)
# type = 'list' 交易資料集，格式為 list of list 或 array of list  
def run(data, supp, conf, lift, maxlen = 10, prefix_sep = '='):
  d_type = type(data)
  if d_type == pd.DataFrame:
      trans = df_to_trans(data, prefix_sep = prefix_sep)
  else: trans = data
  
  print(u'\n開始搜索關聯規則...')       
  start = time.clock() 
  results = list(apriori(trans, 
                         min_support = supp, 
                         min_confidence = conf,
                         min_lift = lift,
                         max_length = maxlen))
  end = time.clock()   
  print(u'\n完成，耗時：%0.2f秒' %(end-start))
  if len(results) > 0:
      print(u'\n整理结果...')  
      rows = []                         
      for i in results :
          for j in i.ordered_statistics:
              s = pd.Series(j)
              s[4] = i.support
              rows.append(s)    
      results = pd.DataFrame(rows)
      results.columns = ['lhs', 'rhs', 'confidence', 'lift', 'support']       
      results = results[ ['lhs', 'rhs', 'support', 'confidence', 'lift' ] ]       
      results['lhs'] = [list(results['lhs'][i]) for i in range(len(results))]     
      results['rhs'] = [list(results['rhs'][i])[0] for i in range(len(results))]  
  print(u'\n共找出 {} 條關聯規則'.format(len(results)))
  return results

def df_to_trans(data, prefix_sep = '='):
  print(u'\n轉換原始 DataFrame 至 交易資料...') 
  start = time.clock()
  trans = pd.get_dummies(data, sparse=True, prefix_sep = prefix_sep)
  col = np.array(trans.columns) 
  trans = np.array(list(map(lambda x: col[x==1] , trans.as_matrix())))
  end = time.clock() 
  print(u'\n轉換完畢，耗時：%0.2f秒' %(end-start)) 
  return trans