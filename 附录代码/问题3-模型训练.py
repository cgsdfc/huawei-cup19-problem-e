import tensorflow.keras as keras
from sklearn.model_selection import train_test_split
import pickle
import plotly.express as px
import pandas as pd
from pathlib import Path as P
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei',
                                   'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

learning_rate = 0.0001
train_size = 0.9
bs = 1
epochs = 500

YEAR, INTENSITY, BLOCK, SOC, SIC, STC, ALLN, CN = ['year', '放牧强度（intensity）', '放牧小区（plot）', 'SOC土壤有机碳', 'SIC土壤无机碳',
                                                   'STC土壤全碳', '全氮N', '土壤C/N比']

df_NUMERIC = pd.read_csv('./问题3-因变量.csv')
scaler = pickle.load(open('./问题3-scaler.pkl', 'rb'))
df_INPUT = pd.read_csv('./问题3-自变量.csv')
df_INDEX = pd.read_csv('./问题3-索引.csv')

X_train, X_val, Y_train, Y_val = train_test_split(
    df_INPUT.values, df_NUMERIC.values, train_size=train_size, shuffle=False)

inputs = keras.layers.Input(shape=(X_train.shape[1], ))
x = keras.layers.Dense(128, activation='relu')(inputs)
x = keras.layers.Dense(128, activation='relu')(x)
outputs = keras.layers.Dense(Y_train.shape[1])(x)

model = keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer=keras.optimizers.Adam(
    learning_rate=learning_rate), loss="mse")
model.summary()

path_checkpoint = "problem3_checkpoint.h5"
es_callback = keras.callbacks.EarlyStopping(
    monitor="val_loss", min_delta=0, patience=10)

modelckpt_callback = keras.callbacks.ModelCheckpoint(
    monitor="val_loss",
    filepath=path_checkpoint,
    verbose=1,
    # 要同时保存网络结构。
    save_weights_only=False,
    save_best_only=True,
)

history = model.fit(
    X_train, Y_train,
    epochs=epochs,
    validation_data=(X_val, Y_val),
    callbacks=[es_callback, modelckpt_callback],
    batch_size=bs
)

def visualize_loss(history, title):
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]
    epochs = range(len(loss))
    plt.figure(figsize=(10, 5))
    plt.plot(epochs, loss, "b", label="Training loss")
    plt.plot(epochs, val_loss, "r", label="Validation loss")
    plt.title(title)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()

visualize_loss(history, "Training and Validation Loss")

pred = model.predict(df_INPUT.values)
df_pred = pd.DataFrame(data=pred, columns=df_NUMERIC.columns)
df_pred[:] = scaler.inverse_transform(df_pred.values)
df_gnd = pd.DataFrame(data=scaler.inverse_transform(
    df_NUMERIC), columns=df_NUMERIC.columns)
PRED, GND = '预测值', '真实值'
df = df_pred.join(df_gnd, rsuffix=GND, lsuffix=PRED).join(df_INDEX)
df.to_csv('问题3-预测结果-训练集.csv', index=False)

# ## 全体训练样本上的拟合效果
def plotPredGndSample(name, df):
    tt = f'{name}拟合效果'.replace('/', '')
    fig = px.line(df, y=[name+GND, name+PRED]
                  ).update_layout(title=tt,
                                  legend_title='预测值/真实值', yaxis_title='取值', xaxis_title='样本')
    fig.write_image(
        P('./导出/问题3/').joinpath('全体训练样本上的拟合效果').joinpath(tt+'.png'))
    return fig

plotPredGndSample(SOC, df)
plotPredGndSample(SIC, df)
plotPredGndSample(STC, df)
plotPredGndSample(ALLN, df)
plotPredGndSample(CN, df)

# ## 不同放牧强度和小区的样本上的拟合效果
df_list = list(df.groupby([INTENSITY, BLOCK]))

def plotPredGnd(i, y):
    info, df = df_list[i]
    tt = f'放牧强度{info[0]}下小区{info[1]}的{y}拟合效果'.replace('/', '')
    fig = px.line(df, x=YEAR,
                  y=[y+GND, y+PRED]).update_layout(title=tt,
                                                   yaxis_title='取值', xaxis_title='年份', legend_title='预测值/真实值')
    fig.write_image(P("./导出/问题3/不同放牧强度和小区的样本上的拟合效果/").joinpath(tt+'.png'))
    return fig

plotPredGnd(2, SOC)
plotPredGnd(2, SIC)
plotPredGnd(2, STC)
plotPredGnd(2, ALLN)
plotPredGnd(2, CN)
plotPredGnd(2, SOC)
