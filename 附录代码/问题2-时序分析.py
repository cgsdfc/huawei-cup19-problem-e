import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei',
                                   'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 这里对问题2的诸多变量进行了分组（比如降水组，温度组，风速组），然后每组进行时序图的可视化。
#
# 对变量分组的说明如下：
# 1. 同一组的变量具有相同的单位和相似的取值范围，比如气温组的单位都是摄氏度，且取值范围也都在10-40度之间，方便可视化；
# 2. 同一组的变量有某种近似性和趋同性，不同组的变量则可能具有趋同性或者互异性。比如天数组（即不同温度范围在一个月里录得的天数）和温度组（即平均气温或者最大最小气温）是具有趋同性的；
# 3. 这种分类可以看做手工进行的、对变量的聚类，而不是传统的对样本的聚类；

df = pd.read_csv('./附件3-湿度-预处理.csv', index_col='time')
df_H = df

YCOLS = ['10cm湿度(kg/m2)', '40cm湿度(kg/m2)', '100cm湿度(kg/m2)', '200cm湿度(kg/m2)']
H_COLS = YCOLS
fig = px.line(df, y=YCOLS)
fig.update_layout(xaxis_title='年份',
                  yaxis_title='湿度(kg/m2)',
                  title='附件3、土壤湿度2022—2012年',
                  legend_title='土壤深度')

# 对不同深度的土壤湿度进行可视化。观察得出如下结论：
#
# 1. 最深层的土壤（即200cm）湿度随着时间的推移，其变化很小，可见深层土壤的湿度是比较稳定的。
# 2. 不同深度的土壤，其湿度有着严格的单调关系，即土壤深度越大，其湿度也越大，其中的原因可能有：
#     1. 浅层的土壤更容易受到蒸发作用的影响，而深层的土壤受到浅层土壤的遮挡，蒸发作用相对较弱。
#     2. 由于重力的作用，水分从浅层土壤向深层土壤渗透，导致深层土壤的湿度更大；
# 3. 10cm，40cm和100cm的土壤湿度变化趋势有一定的相似性，但也有变化趋势相反的时候；

df = pd.read_csv('./附件4-土壤蒸发量-预处理.csv', index_col='time')
df_SoilEvap = df

YCOLS = ['土壤蒸发量(W/m2)', '土壤蒸发量(mm)']
SOIL_EVAP_COLS = YCOLS
fig = px.line(df, y=YCOLS)
fig.update_layout(xaxis_title='年份',
                  yaxis_title='取值',
                  title='附件4、土壤蒸发量2012—2022年',
                  legend_title='土壤蒸发量单位')

# 这里可以看到，土壤蒸发量的两种单位（W/m2 mm）的变量的变化趋势是几乎完全一致的。
# 因此在搭建预测模型时，只需要选择其中一种单位即可。

df = pd.read_csv('附件8-气候-预处理.csv', index_col='time')
df_Climate = df

# 温度组（气温组）变量

TEMP_COLS = [col for col in df.columns if col.endswith('(℃)')]
df_Temp = df_Climate[TEMP_COLS]
TEMP_COLS

# 风速组变量

WIND_COLS = [col for col in df.columns if col.endswith('(knots)')]
df_Wind = df_Climate[WIND_COLS]
WIND_COLS

# 能见度组变量

VIS_COLS = [col for col in df.columns if col.endswith('(km)')]
df_Vis = df_Climate[VIS_COLS]
VIS_COLS

# 气压组变量

PRESS_COLS = [col for col in df.columns if col.endswith('(hPa)')]
df_Press = df_Climate[PRESS_COLS]
PRESS_COLS

# 天数组变量

DAYS_COLS = [col for col in df.columns if col.endswith('天数')]
df_Days = df_Climate[DAYS_COLS]
DAYS_COLS

# 降水组变量

RAIN_COLS = [col for col in df.columns if col.endswith('(mm)')]
df_Rain = df_Climate[RAIN_COLS]
RAIN_COLS

len(TEMP_COLS) + len(WIND_COLS) + len(VIS_COLS) + len(PRESS_COLS) + len(
    DAYS_COLS) + len(RAIN_COLS), len(df.columns)

VAR_GROUP = [TEMP_COLS, WIND_COLS, VIS_COLS, PRESS_COLS, DAYS_COLS, RAIN_COLS]
len(VAR_GROUP)

# 一共是6组变量。下面分别对每组变量进行时序图的可视化。

fig = px.line(df, y=RAIN_COLS)
fig.update_layout(title='附件8、锡林郭勒盟气候2012-2022（降水量）',
                  xaxis_title='年份',
                  yaxis_title='降水量(mm)',
                  legend_title='降水量指标')

# 1. 降水量在某些月份出现了高出其他月份很多的取值，比如2017年1月891.79mm和2022年2月的769.04mm。
# 由于最近全球极端天气频繁，在没有更多气象方面的证据的情况下，不能简单地认为这些过大的值是异常值。
# 2. 降水量和最大单日降水量的总体变化趋势很接近，但降水量的变化幅度更大，而最大单日降水量的变化幅度相对稳定，
# 这可能是由于该地区的气候导致的，即特大的暴雨是不常见的，但降水天数可能较多。

fig = px.line(df, y=TEMP_COLS)
fig.update_layout(title='附件8、锡林郭勒盟气候2012-2022（温度）',
                  xaxis_title='年份',
                  yaxis_title='温度(℃)',
                  legend_title='温度指标')

# 1. 各种气温指标的变化趋势非常一致，在每年的5,6,7,8月份迎来一个高峰，其他月份则是低谷，这是典型的季节性变化；
# 2. 由于气温指标的高度正相关，我们可以选取较为简单的平均气温作为模型输入；

fig = px.line(df, y=WIND_COLS)
fig.update_layout(title='附件8、锡林郭勒盟气候2012-2022（风速）',
                  xaxis_title='年份',
                  yaxis_title='风速(knots)',
                  legend_title='风速指标')

fig = px.line(df, y=VIS_COLS)
fig.update_layout(title='附件8、锡林郭勒盟气候2012-2022（能见度）',
                  xaxis_title='年份',
                  yaxis_title='能见度(km)',
                  legend_title='能见度指标')

fig = px.line(df, y=PRESS_COLS)
fig.update_layout(title='附件8、锡林郭勒盟气候2012-2022（气压）',
                  xaxis_title='年份',
                  yaxis_title='气压(hPa)',
                  legend_title='气压指标')

fig = px.line(df, y=DAYS_COLS)
fig.update_layout(title='附件8、锡林郭勒盟气候2012-2022（天数）',
                  xaxis_title='年份',
                  yaxis_title='天数',
                  legend_title='天数指标')
