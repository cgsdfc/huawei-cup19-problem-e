import pandas as pd
from pathlib import Path as P
import plotly.express as px

TIME = '时间'
DATE = '日期'
MONTH, YEAR = '月份', '年份'
DATADIR = P('./数据集/基本数据/')

excel = pd.ExcelFile('./数据集/基本数据/附件10、叶面积指数（LAI）2012-2022年.xls')
excel.sheet_names
df = excel.parse(0)
df = df.drop(columns=['经度(lon)', '纬度(lat)', '高层植被(LAIH,m2/m2)', ])
df[DATE] = pd.to_datetime(df[DATE].astype(str)+'01')
df = df.set_index(DATE)
df = df.sort_index()

px.line(df, y=df.columns[0]).update_layout(
    yaxis_title='低层植被叶面积指数LAIL(m2/m2)', title='附件10、叶面积指数（LAI）2012-2022年', legend_title='')

df.to_csv('附件10-低层植被叶面积指数LAIL-预处理.csv')


df = pd.read_excel('./数据集/基本数据/附件6、植被指数-NDVI2012-2022年.xls')
df = df.drop(columns=['经度(lon)', '纬度(lat)'])

NDVI = '植被指数(NDVI)'
BAD = (df[NDVI] < -1) | (df[NDVI] > 1)
# NDVI 没有脏数据
BAD.any()

df.info()  # 整个df也没有空值


x = df[YEAR].astype(str)+'-'+df[MONTH].astype(str)+'-1'
df[TIME] = pd.to_datetime(x)
df = df.set_index(TIME)
df.to_csv('附件6、植被指数-NDVI2012-2022年-预处理.csv')


px.line(df.loc['2013'], y=NDVI).update_layout(title='2013年 NDVI 指数')


f = list(P('.').rglob('附件9、径流量2012-2022年*xls*'))[0]
df = pd.read_excel(f)
df = df.drop(columns=['经度(lon)', '纬度(lat)'])
x = df[YEAR].astype(str)+'-'+df[MONTH].astype(str)+'-1'
df[TIME] = pd.to_datetime(x)
df = df.set_index(TIME).sort_index()
YCOLS = ['径流量(m3/s)', '径流量(m3)']

px.line(df, y='径流量(m3/s)')
px.line(df, y='径流量(m3)')


# 两个径流量基本上趋势是一致的。
df.to_csv('附件9、径流量2012-2022年-预处理.csv')


# ### 绿植覆盖率

f_list = list(P('.').rglob('*覆盖率*xls'))
df_list = [pd.read_excel(f) for f in f_list]
df = pd.concat(df_list)
df = df.drop(columns=['经度(lon)', '纬度(lat)', '备注', ])
df[TIME] = pd.to_datetime(df[TIME])
df = df.set_index(TIME).sort_index()

px.line(df, y=df.columns[0]).update_layout(
    yaxis_title='绿植覆盖率', title='附件5、绿植覆盖率（2020-2022）')


# ### 附件7、锡林郭勒土壤基本数据


f = list(P('.').rglob('附件7、锡林郭勒土壤基本数据*'))[0]
df = pd.read_excel(f, sheet_name='data', header=None)
df = df.rename(columns=dict(enumerate(['属性', '取值'])))
df.to_csv('附件7、锡林郭勒土壤基本数据-预处理.csv')
