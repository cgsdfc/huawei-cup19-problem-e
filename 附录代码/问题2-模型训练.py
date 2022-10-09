import tensorflow.keras as keras
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei',
                                   'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

learning_rate = 0.001
train_size = 0.8
seqlen = 1
bs = 32
epochs = 200

# 这些是模型的超参数。
# - learning_rate 是学习率，控制模型收敛的快慢，太大了模型容易发散，太小了模型收敛很慢；
# - train_size 训练集占整个数据集的比例，一般是28开；
# - seqlen：序列长度，在时序建模中，就是用前几个样本来预测当前样本；
# - bs：batch size，批量大小，随机梯度下降算法SGD中，每次用来估计梯度的训练样本数量；
# 考虑到数据集本身只有100多个样本，批量不用太大；
# - epochs：训练的轮数，即迭代次数；

df = pd.read_csv('问题2-训练数据-归一化.csv', index_col='time')

df_train, df_val = train_test_split(df, train_size=train_size, shuffle=False)

# 将数据集分割为训练集和验证集，二者没有交集，训练集用来训练模型，验证集用来确保模型没有过拟合。

feature_size = df_train.shape[1]
df_train.shape, df_val.shape

dataset_train = keras.preprocessing.timeseries_dataset_from_array(
    df_train.values,
    df_train.values,
    sequence_length=seqlen,
    batch_size=bs,
    shuffle=True)
dataset_val = keras.preprocessing.timeseries_dataset_from_array(
    df_val.values,
    df_val.values,
    sequence_length=seqlen,
    batch_size=bs,
    shuffle=True)

# 利用keras的接口构造时序模型需要的时序数据集。

dataset_train, dataset_val

# 构建一个单层的LSTM模型。LSTM是一种专门用来建模时序数据的神经网络模型，即长短期记忆（Long Short Term Memory）。
# 可以展开说说理论。

inputs = keras.layers.Input(shape=(seqlen, feature_size))
lstm_out = keras.layers.LSTM(16)(inputs)
outputs = keras.layers.Dense(feature_size)(lstm_out)

model = keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              loss="mse")
model.summary()

# 训练模型：
# 1. 使用的损失函数：MSE，Mean Square Error，即均方误差；
# 2. 早停止：当验证误差经过一段时间不再改进之后，停止训练模型，这是一种停止训练循环的策略；
# 3. 检查点：当验证误差出现改进时，保存当前的模型参数；

path_checkpoint = "problem2_checkpoint.h5"
es_callback = keras.callbacks.EarlyStopping(monitor="val_loss",
                                            min_delta=0,
                                            patience=5)

modelckpt_callback = keras.callbacks.ModelCheckpoint(
    monitor="val_loss",
    filepath=path_checkpoint,
    verbose=1,
    # 要同时保存网络结构。
    save_weights_only=False,
    save_best_only=True,
)

history = model.fit(
    dataset_train,
    epochs=epochs,
    validation_data=dataset_val,
    callbacks=[es_callback, modelckpt_callback],
)

# 对模型训练过程的损失函数和验证损失函数进行可视化。
# - 基于matplotlib的可视化；
# - 基于plotly的可视化；
#
# 挑一个好看的就行。

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
