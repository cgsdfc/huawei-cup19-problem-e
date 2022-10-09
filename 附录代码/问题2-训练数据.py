import pickle
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import plotly.express as px
import pandas as pd
from pathlib import Path as P
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei',
                                   'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# ## 获取数据集

# 这里是要把问题所需的训练数据整理出来，基本上就是一个机器学习的数据集获取的过程。

# 这是土壤湿度W，每月的数据。注意：代码里面用符号H表示，实际上是W。

df = pd.read_csv('./附件3-湿度-预处理.csv', index_col='time')
df_H = df.drop(columns=['month', 'year'])
df_H.columns

# 这是土壤蒸发量E，每月的数据，和湿度W是对齐的（数据的时间范围完全相同），注意：代码里面用符号SoilEvap表示，实际上是E。

df = pd.read_csv('./附件4-土壤蒸发量-预处理.csv', index_col='time')
df_SoilEvap = df.drop(columns=['month', 'year'])
df_SoilEvap.columns

# 这是气候条件，有很多变量，但大部分变量和要预测的湿度相关性不大（见相关性分析）。
# 筛选了4个相关性比较大的变量：
# ```
# ['土壤蒸发量(mm)', '平均露点温度(℃)', '最低气温极值(℃)', '平均最低气温(℃)']
# ```

df = pd.read_csv('附件8-气候-预处理.csv', index_col='time')
df_Climate = df.drop(columns=['month', 'year'])

df_All = df_Climate.join([df_H, df_SoilEvap])
# 对所有自变量、因变量合并为一个df

Y_COLS = ['10cm湿度(kg/m2)', '40cm湿度(kg/m2)', '100cm湿度(kg/m2)', '200cm湿度(kg/m2)']
X_COLS = ['土壤蒸发量(mm)', '降水量(mm)', '平均气温(℃)']

# 这里定义了4个因变量和3个自变量。

df = df_All[Y_COLS + X_COLS].dropna()
df.to_csv('问题2-原训练数据.csv')

# 这里获取了模型预测所需要的数据，即3个自变量和3个因变量。

scaler = MinMaxScaler()
# df_val=scaler.fit_transform(df)
scaler.fit(df)
df_val = scaler.transform(df)
df = pd.DataFrame(data=df_val, index=df.index, columns=df.columns)
df.to_csv('问题2-训练数据-归一化.csv')
pickle.dump(scaler, P('问题2-MinMaxScaler-训练数据.pkl').open('wb'))


# 对变量进行最小最大值归一化（MinMaxScale），把变量的范围映射到0-1区间。

px.line(df).update_layout(xaxis_title='时间',
                          yaxis_title='取值',
                          legend_title='变量',
                          title='问题2 自变量和因变量的时序图')
