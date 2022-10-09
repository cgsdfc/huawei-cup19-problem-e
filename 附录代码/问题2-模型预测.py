import tensorflow.keras as keras
import pickle
import plotly.express as px
import pandas as pd
from pathlib import Path as P
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei',
                                   'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

seqlen = 1

scaler = pickle.load(P('问题2-MinMaxScaler-训练数据.pkl').open('rb'))
# df=pd.read_csv('问题2-训练数据-归一化.csv',index_col='time', parse_dates=True)
df = pd.read_csv('问题2-训练数据-归一化.csv').drop(columns='time')
model = keras.models.load_model('./problem2_checkpoint.h5')

df_test = df.iloc[-seqlen:, :]
test = df_test.values.reshape([1, seqlen, -1])
df_test.shape, test.shape

INDEX = pd.period_range(pd.Period(year=2022, month=4, freq='1M'), pd.Period(
    year=2023, month=12, freq='1M'))
INDEX = INDEX.to_timestamp()

def predict(model, df_test: pd.DataFrame, index, seqlen: int):
    n = len(index)
    for i in range(n):
        test = df_test.iloc[-seqlen:, :].values.reshape([1, seqlen, -1])
        pred = model.predict(test)
        df_pred = pd.DataFrame(pred, columns=df.columns)
        df_test = pd.concat([df_test, df_pred])

    df_test = df_test.iloc[seqlen:, :]
    df_test.index = index

    return df_test

df_pred = predict(model, df_test, INDEX, seqlen=seqlen)
data = scaler.inverse_transform(df_pred.values)
df_pred = pd.DataFrame(data=data, columns=df_pred.columns, index=df_pred.index)
df_pred = df_pred[['10cm湿度(kg/m2)', '40cm湿度(kg/m2)',
                   '100cm湿度(kg/m2)', '200cm湿度(kg/m2)']]
df_pred = df_pred.applymap(lambda x: round(x, 2))
df_pred.to_excel('问题2-预测结果.xlsx')

px.line(df_pred).update_layout(xaxis_title='时间', yaxis_title='湿度取值',
                               title='问题2 模型预测2022-04至2023-12共21个月的土壤湿度', legend_title='不同深度的土壤湿度')
