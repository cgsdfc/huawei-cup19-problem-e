import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

# 建模的思路：
# 1. 小区作为哑巴变量，和时间一起作为自变量；
# 2. 化学性质是因变量；
# 3. 用一个两层的MLP模型；
df = pd.read_csv('./问题3-附件14.csv')
YEAR, INTENSITY, BLOCK, SOC, SIC, STC, ALLN, CN = ['year', '放牧强度（intensity）', '放牧小区（plot）', 'SOC土壤有机碳', 'SIC土壤无机碳',
                                                   'STC土壤全碳', '全氮N', '土壤C/N比']

NUMERIC = [SOC, SIC, STC, ALLN, CN]
scaler = StandardScaler()
scaler.fit(df[NUMERIC])
df[NUMERIC] = scaler.transform(df[NUMERIC])
df_NUMERIC = df[NUMERIC]

df_NUMERIC.to_csv('问题3-因变量.csv', index=False)
pickle.dump(scaler, open('问题3-scaler.pkl', 'wb'))


# 对因变量，即土壤的化学性质，进行归一化。
df_Year = df[YEAR] - df[YEAR].min()
df_Block = pd.get_dummies(df[BLOCK])
df_INPUT = pd.concat([df_Year, df_Block], axis=1)
df_INPUT.to_csv('问题3-自变量.csv', index=False)

# 对自变量，即年份和小区，进行归一化和哑巴化（Dummy）。
df_Index = df[[YEAR, INTENSITY, BLOCK]]
df_Index.to_csv('问题3-索引.csv', index=False)
