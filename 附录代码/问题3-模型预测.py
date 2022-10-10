import tensorflow.keras as keras
import pickle
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei',
                                   'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 用回归模型预测2022年各个放牧强度不同放牧小区的五种土壤化学性质的量。
YEAR, INTENSITY, BLOCK, SOC, SIC, STC, ALLN, CN = ['year', '放牧强度（intensity）', '放牧小区（plot）', 'SOC土壤有机碳', 'SIC土壤无机碳',
                                                   'STC土壤全碳', '全氮N', '土壤C/N比']

df_NUMERIC = pd.read_csv('./问题3-因变量.csv')  # 训练集的Y
scaler = pickle.load(open('./问题3-scaler.pkl', 'rb'))
df_INPUT = pd.read_csv('./问题3-自变量.csv')  # 训练集的X（预处理）
df_INDEX = pd.read_csv('./问题3-索引.csv')  # 训练集的X（原始）
model = keras.models.load_model('./problem3_checkpoint.h5')

df_Block = df_INDEX[[INTENSITY, BLOCK]].drop_duplicates()
df_Block = pd.DataFrame(data=df_Block, columns=[INTENSITY, BLOCK])
df_Test = pd.get_dummies(df_Block[BLOCK])
df_year = pd.Series(data=10, name=YEAR, index=df_Test.index)
df_Test = pd.concat([df_year, df_Test], axis=1)

# 获取测试集的输入数据，即2022年（用10表示）和各个小区。以及相应的索引。
df_TestIndex = pd.concat([df_year, df_Block], axis=1)
df_INPUT.columns, df_INPUT.year.iloc[-1]  # df_Test 的列顺序要和df_INPUT保持一致。

pred = model.predict(df_Test.values)
df_pred = pd.DataFrame(data=pred, columns=df_NUMERIC.columns)
df_pred[:] = scaler.inverse_transform(df_pred.values)
df_pred = pd.concat([df_TestIndex, df_pred], axis=1).drop(columns=YEAR)
df_pred.to_excel('问题3-最终结果.xlsx')
df_pred.to_csv('问题3-最终结果.csv', index=False)

# 这就是问题3的最终结果了，索引的顺序和题目的有不一致。
df_pred['year'] = 2022
df = pd.read_csv('问题3-附件14.csv')
df = pd.concat([df, df_pred])
df.to_csv('问题3-附件14-加预测数据.csv', index=False)

# ## 将预测数据连接到原始数据上，看看趋势是否一致
#
# 原始数据为不同小区，相同放牧强度的平均值和错误棒，模型预测的各小区的平均值（2022年）应该符合原始数据的时间变化趋势。
# 比如，SOC随着时间推移而上升，则2022年各放牧强度下的平均SOC应该比2021年的高；
# 同理，SIC随着时间推移而下降，则2022年各放牧强度下的平均SIC应该比2021年的低；
df_std = df.groupby([YEAR, INTENSITY]).std().reset_index()
df_mean = df.groupby([YEAR, INTENSITY]).mean().reset_index()

def plotVarTime(y):
    fig = px.line(df_mean, x=YEAR, y=y, color=INTENSITY, error_y=df_std[y])
    fig.update_layout(xaxis_title='年份', title='不同放牧强度下{}的逐年变化趋势'.format(y))
    return fig

plotVarTime(SOC)
plotVarTime(SIC)
plotVarTime(STC)
plotVarTime(ALLN)
plotVarTime(CN)
