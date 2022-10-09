import pandas as pd
from pathlib import Path as P
import plotly.express as px


# ### 处理附件3：不同深度的土壤湿度数据
#
# 1. 剔除经纬度，因为都是一样的；
# 2. 把月份和年份合并为`pandas.DatetimeIndex`，然后剔除；
# 3. 数据中不存在空值，无须处理；


df = pd.ExcelFile('./数据集/基本数据/附件3、土壤湿度2022—2012年.xls')
df = df.parse(0)

YCOLS = ['10cm湿度(kg/m2)', '40cm湿度(kg/m2)',
         '100cm湿度(kg/m2)', '200cm湿度(kg/m2)']
TIMECOLS = ['month', 'year', 'day']


NAMEMAP = {
    '月份': 'month', '年份': 'year', '10cm湿度(kg/m2)': '10cm湿度(kg/m2)', '40cm湿度(kg/m2)': '40cm湿度(kg/m2)',
    '100cm湿度(kg/m2)': '100cm湿度(kg/m2)', '200cm湿度(kg/m2)': '200cm湿度(kg/m2)'
}
COLS = list(NAMEMAP.values())


def renameAndExtract(df: pd.DataFrame, map: dict) -> pd.DataFrame:
    return df.rename(columns=map)[list(map.values())]


def yearMonthToDate(df: pd.DataFrame) -> pd.DataFrame:
    TIMECOLS = ['month', 'year', 'day']
    df['day'] = 1
    df['time'] = pd.to_datetime(df[TIMECOLS])
    df = df.set_index('time').drop(columns=['day']).sort_index()
    return df


df = renameAndExtract(df, NAMEMAP)
df = yearMonthToDate(df)


df.to_csv('./附件3-湿度-预处理.csv')


# ### 处理附件4：土壤蒸发量数据
#
# 处理过程和附件3基本相同。


df = pd.ExcelFile('./数据集/基本数据/附件4、土壤蒸发量2012—2022年.xls')
df = df.parse(0)
# Soil evaporation


YCOLS = ['土壤蒸发量(W/m2)', '土壤蒸发量(mm)']


NAMEMAP = {
    '月份': 'month', '年份': 'year', '土壤蒸发量(W/m2)': '土壤蒸发量(W/m2)', '土壤蒸发量(mm)': '土壤蒸发量(mm)'
}


df = renameAndExtract(df, NAMEMAP)
df = yearMonthToDate(df)

fig = px.line(df, y=YCOLS)
fig.update_layout(xaxis_title='年份', yaxis_title='取值',
                  title='附件4、土壤蒸发量2012—2022年', legend_title='土壤蒸发量单位')
df.to_csv('./附件4-土壤蒸发量-预处理.csv')


# ### 处理附件8：气候数据
#
# 1. 将不同年份的文件合并为一个DataFrame方便分析；
# 2. 删除只有一种取值的列：`['站点号', '海拔高度(m)', '经度', '纬度', '平均气温≥35℃的天数']`；
# 3. 删除空值过多的列（在127行中，只有33行为非空的那些列，意义不大），有：
#
# `['积雪深度(mm)','平均最大瞬时风速(knots)','最大瞬时风速极值(knots)']`；
#


d = P('./数据集/基本数据/附件8、锡林郭勒盟气候2012-2022/')
file_list = list(d.rglob('*年.xls'))
df_list = [pd.read_excel(f) for f in file_list]
df = pd.concat(df_list)


# 删除只有一个值的列。
BAD_COLS = [col for col in df.columns if len(df[col].unique()) == 1]
df = df.drop(columns=BAD_COLS)
df.info()  # 有些列na太多，删掉。


BAD_COLS = ['积雪深度(mm)', '平均最大瞬时风速(knots)', '最大瞬时风速极值(knots)']
df = df.drop(columns=BAD_COLS)
df.isna().any().any()

df = df.rename(columns={'年份': 'year', '月份': 'month'})
df = yearMonthToDate(df)
df.to_csv('附件8-气候-预处理.csv')
