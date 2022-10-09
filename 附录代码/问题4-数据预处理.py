# 这里是把文献中提到的（也是题目提到的）三组变量，即气候因素、地表因素和人文因素所对应的附件数据进行处理。
# 其中，地表因素没有找到对应的附件，其他因素都找到了不同程度的对应，如下所示：
# 1. 气候因素：附件8气候。注意暖季的定义，对原始月份数据进行筛选即可；
# 2. 任人文因素：附件13，里面有经济，人口，牲畜密度等数据，注意牲畜和钱的单位即可；
#     1. 牲畜密度要除以一年52周，看docx文档写了；
#     2. 钱的单位显然不是元（否则一年才赚30块钱？），假定为100元；

import pandas as pd
from pathlib import Path as P
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei',
                                   'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 附件8 气候因素
WIND = '暖季平均风速(m/s)'
RAIN = '暖季降水量(mm)'
TEMP = '暖季平均气温(℃)'

# 地表因素
PLANT = '夏季植被盖度'
WATER = '夏季地表水资源量(104m3/km2)'
UNDER_WATER = '夏季地下水埋深(m)'

# 人文因素
PERSON = '人口密度(person/km2)'
SHEEP = '牲畜密度(sheep unit/km2)'
MONEY = '人均家庭经营纯收入(yuan)'

# ## 气候因素
#
# 气候因素很好处理，因为数据都在附件8里面了，只要注意把暖季数据拿到即可。

df = pd.read_csv('附件8-气候-预处理.csv', index_col='time', parse_dates=True)
COLS = ['平均气温(℃)', '降水量(mm)', '平均风速(knots)', 'month', 'year']
df = df[COLS]
WARM_SEASON = list(range(3, 11))
df = df[df.month.isin(WARM_SEASON)]
df = df.resample('1Y').mean().drop(columns='month')
df['year'] = df['year'].astype(int)
df.rename(columns={
    '平均气温(℃)': TEMP,
    '降水量(mm)': RAIN,
    '平均风速(knots)': WIND,
}, inplace=True)
df.to_csv('问题4-气候因素-预处理.csv')

# ## 人文因素

f = list(P.cwd().rglob(
    '内蒙古自治区锡林郭勒盟不同示范牧户牲畜数量调查数据集（2018年7月28日-2020年9月30日）.xlsx'))[0]
df = pd.read_excel(f, sheet_name='汇总')
df.columns

YEAR, NUM_PERSON, NET_INCOME, AVE_INCOME, PLOT, NUM_SHEEP, AREA, SHEEP_DENSE =\
    ['年份', '人口数', '经济年净收入', '人均年净收入', '监测点',
        '标准羊单位（只）', '草场面积 km²', '放牧压力（只羊/km²）']

df[AREA] = df[NUM_SHEEP]/df[SHEEP_DENSE]
df[PERSON] = df[NUM_PERSON]/df[AREA]
NUM_WEEK = 52
df[SHEEP] = df[SHEEP_DENSE]/NUM_WEEK
df[MONEY] = df[AVE_INCOME]*100
df['year'] = df['年份'].apply(lambda x: int(x.replace('年', '')))

HUMAN_COLS = [PERSON, SHEEP, MONEY, 'year', PLOT]
df = df[HUMAN_COLS]
df.to_csv('问题4-人文因素-预处理.csv', index=False)
