import pandas as pd
import numpy as np
import zipfile
import requests
from io import BytesIO
from tqdm import tqdm
# Install the xlrd package before running this script by executing the following command in your terminal:
# pip install xlrd
import xlrd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Data loading
links = ['http://tennis-data.co.uk/2000/2000.xls', 'http://tennis-data.co.uk/2001/2001.xls', 
         'http://tennis-data.co.uk/2002/2002.xls', 'http://tennis-data.co.uk/2003/2003.xls', 
         'http://tennis-data.co.uk/2004/2004.xls', 'http://tennis-data.co.uk/2005/2005.xls', 
         'http://tennis-data.co.uk/2006/2006.xls', 'http://tennis-data.co.uk/2007/2007.xls', 
         'http://tennis-data.co.uk/2008/2008.zip', 'http://tennis-data.co.uk/2009/2009.xls', 
         'http://tennis-data.co.uk/2010/2010.xls', 'http://tennis-data.co.uk/2011/2011.xls', 
         'http://tennis-data.co.uk/2012/2012.xls', 'http://tennis-data.co.uk/2013/2013.xlsx', 
         'http://tennis-data.co.uk/2014/2014.xlsx', 'http://tennis-data.co.uk/2015/2015.xlsx', 
         'http://tennis-data.co.uk/2016/2016.xlsx', 'http://tennis-data.co.uk/2017/2017.xlsx', 
         'http://tennis-data.co.uk/2018/2018.xlsx', 'http://tennis-data.co.uk/2019/2019.xlsx', 
         'http://tennis-data.co.uk/2020/2020.xlsx', 'http://tennis-data.co.uk/2021/2021.xlsx', 
         'http://tennis-data.co.uk/2022/2022.xlsx', 'http://tennis-data.co.uk/2023/2023.xlsx',
         'http://tennis-data.co.uk/2024/2024.xlsx', 'http://tennis-data.co.uk/2025/2025.xlsx']

# Merge files into one DataFrame
# df = pd.DataFrame()
# for i, elem in enumerate(links):
#     if elem[-4:] == '.zip':
#         content = requests.get(elem)
#         zf = zipfile.ZipFile(BytesIO(content.content))
#         temp = pd.read_excel(zf.open(zf.namelist()[0])) 
#     else:
#         temp = pd.read_excel(elem) 
#         with open(f"year_stats/{elem[-8:-4]}", 'w') as f:
#             f.write(temp.to_csv())

#     df = pd.concat([df, temp], ignore_index=True)

for link in links:
    if "2008" in link:
        content = requests.get(link)
        zf = zipfile.ZipFile(BytesIO(content.content))
        temp = pd.read_excel(zf.open(zf.namelist()[0]))
        with open(f"year_stats/2008", 'w') as f:
             f.write(temp.to_csv())
