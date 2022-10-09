import pandas as pd
import plotly.express as px

# SOC: 土壤有机碳
# SIC: 土壤无机碳
# STC: 土壤全碳
# TN: 全N
# C/N: 土壤C/N比
#

excel = pd.ExcelFile(
    './数据集/监测点数据/附件14：内蒙古自治区锡林郭勒盟典型草原不同放牧强度土壤碳氮监测数据集（2012年8月15日-2020年8月15日）/内蒙古自治区锡林郭勒盟典型草原不同放牧强度土壤碳氮监测数据集（2012年8月15日-2020年8月15日）.xlsx')
df = excel.parse(sheet_name='data')

# 注意：相同的年份，小区和放牧强度下，有重复的数据，先看看这些数据是不是差别很小，如果是，说明是重复实验，则取平均值即可。
# 有三组变量：
# 1. X变量，即表格的行，是放牧强度和小区；
# 2. Y变量，即表格的列，待预测的值，那四个化学性质；、
# 3. 时间变量，即年份；

YEAR, BLOCK, INTENSITY, SOC, SIC, STC, ALLN, CN = df.columns
X_LIST = [BLOCK, INTENSITY]
Y_LIST = [SOC, SIC, STC, ALLN, CN]
df.info()  # 没有空值，所给的列都是需要的

df = df.groupby([YEAR, INTENSITY, BLOCK]).mean().reset_index()
df.to_csv('问题3-附件14.csv', index=False)

df_std = df.groupby([YEAR, INTENSITY]).std().reset_index()
df_mean = df.groupby([YEAR, INTENSITY]).mean().reset_index()

# 错误棒（error bar）由同一年份的不同小区或者重复实验计算而来。
def plotVarTime(y):
    fig = px.line(df_mean, x=YEAR, y=y, color=INTENSITY, error_y=df_std[y])
    fig.update_layout(xaxis_title='年份', title='不同放牧强度下{}的逐年变化趋势'.format(y))
    return fig

# ## 不同放牧强度下，各变量随年份变化趋势
#
# 这是参考数据附带的说明文件画的（一模一样的）。
plotVarTime(SOC)
plotVarTime(SIC)
plotVarTime(STC)
plotVarTime(ALLN)
plotVarTime(CN)
