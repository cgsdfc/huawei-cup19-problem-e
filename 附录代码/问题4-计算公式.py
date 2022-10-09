import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei',
                                   'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

WIND = '暖季平均风速(m/s)'
RAIN = '暖季降水量(mm)'
TEMP = '暖季平均气温(℃)'
CLIMATE_COLS = [WIND, RAIN, TEMP]

PLANT = '夏季植被盖度'
WATER = '夏季地表水资源量(104m3/km2)'
UNDER_WATER = '夏季地下水埋深(m)'
GND_COLS = [PLANT, WATER, UNDER_WATER]

PERSON = '人口密度(person/km2)'
SHEEP = '牲畜密度(sheep unit/km2)'
MONEY = '人均家庭经营纯收入(yuan)'
HUMAN_COLS = [PERSON, SHEEP, MONEY]

FACTOR_COLS = CLIMATE_COLS+HUMAN_COLS
PLOT = '监测点'

UPPER = {
    WIND: 2.61,
    RAIN: 100,
    TEMP: 35,
    PLANT: 50,
    WATER: 21.47,
    UNDER_WATER: 7.7,
    PERSON: 60,
    SHEEP: 25,
    MONEY: 1100,
}
LOWER = {
    WIND: 1.43,
    RAIN: 10,
    TEMP: 5,
    PLANT: 10,
    WATER: 1.22,
    UNDER_WATER: 4.85,
    PERSON: 7,
    SHEEP: 5,
    MONEY: 450,
}

# 这里按照参考文献，把各个因子的上限和下限记录下来（抄下来）。
# 每个因子的原始数值按照一定的规则转变为0-1区间内的值，这里的规则就依赖于这些上限和下限。
# 下面的函数就是定义的规则。
def Q_Wind(x):
    if x >= UPPER[WIND]:
        return 1
    if x < LOWER[WIND]:
        return 0
    val = (x-LOWER[WIND])/(UPPER[WIND]-LOWER[WIND])
    return val

def Q_Rain(x):
    if x < 10:
        return 1
    if x > 100:
        return 0
    val = (100-x)/(100-10)
    return val

def Q_Temp(x):
    if 25 <= x <= 30:
        return 0
    if x < 5 or x > 35:
        return 1
    if 5 <= x <= 25:
        return (25-x)/(25-5)
    if 30 < x <= 35:
        return (x-30)

def Q_Plant(x):
    if x >= 50:
        return 0
    if x < 10:
        return 1
    return (50-x)/(50-10)

def Q_Water(x):
    pass

def Q_UnderWater(x):
    if x > UPPER[UNDER_WATER]:
        return 1
    if x < LOWER[UNDER_WATER]:
        return 0
    return (x-LOWER[UNDER_WATER])/(UPPER[UNDER_WATER]-LOWER[UNDER_WATER])

def Q_Person(x):
    if x >= 60:
        return 1
    if x < 7:
        return 0
    return (x-7)/(60-7)

def Q_Sheep(x):
    if x < 5:
        return 0
    if x >= 25:
        return 1
    return (x-5)/(25-5)

def Q_Money(x):
    if x >= 1100:
        return 1
    if x < 450:
        return 0
    return (x-450)/(1100-450)

Q_map = {
    WIND: Q_Wind,
    RAIN: Q_Rain,
    TEMP: Q_Temp,
    PLANT: Q_Plant,
    WATER: Q_Water,
    UNDER_WATER: Q_UnderWater,
    PERSON: Q_Person,
    SHEEP: Q_Sheep,
    MONEY: Q_Money,
}

WEIGHT_COEFF = {
    WIND: 0.1802,
    RAIN: 0.0787,
    TEMP: 0.0685,
    PLANT: 0.2036,
    WATER: 0.0808,
    UNDER_WATER: 0.1282,
    PERSON: 0.0509,
    SHEEP: 0.1282,
    MONEY: 0.0808,
}

# 这里是每个因子的权重，也是文献里面直接给出的，搬运过来。
# 权重的总和为1。

def judge_SM(x):
    if 0 <= x < 0.2:
        return '非沙漠化'
    if 0.2 < x <= 0.4:
        return '轻度沙漠化'
    if 0.4 < x <= 0.6:
        return "中度沙漠化"
    if 0.6 < x <= 0.8:
        return '重度沙漠化'
    return '极度沙漠化'

def compute_SM(Q_raw: dict, eta: float):
    Q1 = {key: Q_map[key](val) for key, val in Q_raw.items()}
    Q2 = {key: val*WEIGHT_COEFF[key] for key, val in Q1.items()}
    SM1 = sum(Q2.values())
    SM2 = SM1*eta

    return Q1, Q2, SM1, SM2, judge_SM(SM2)


df_Climate = pd.read_csv('./问题4-气候因素-预处理.csv')
df_Human = pd.read_csv('./问题4-人文因素-预处理.csv')


df = df_Human.set_index('year').join(
    df_Climate.set_index('year')).drop(columns='time')

# 把我们获取到的两组因子（气候因子，人文因子）合并起来，准备计算SM值了。
# SM的计算包括：
# 1. 沙漠化指数SM，是一个0-1之间的无量纲数；代码中是SM1；
# 2. 沙漠化程度，是根据SM值得到的五档等级；代码中是SM2；

SM1_COL, SM2_COL = '沙漠化指数', '沙漠化程度'


def compute_SM_series(s: pd.Series):
    *_, SM1, SM2 = compute_SM(s.to_dict(), eta=1)
    return {
        SM1_COL: SM1,
        SM2_COL: SM2,
    }

df_SM = df[FACTOR_COLS].apply(compute_SM_series, axis=1, result_type='expand')
df_ = pd.concat([df, df_SM], axis=1)

df_res = df_[[PLOT, SM1_COL, SM2_COL]]
df_res.to_csv('问题4-不同监测点的沙漠化程度（2018-2020）')
df_res

px.line(df_res, x=df.index, y=SM1_COL, color=PLOT).update_layout(
    xaxis_title='年份', title='不同监测点的沙漠化指数随时间的变化情况')
