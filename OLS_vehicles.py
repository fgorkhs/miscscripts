import matplotlib.pyplot as plt
from statistics import mean
import numpy as np
import scipy as sp
from math import sqrt
import pandas as pd
from pprint import pprint
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.compat import lzip

#loads df from file
df = pd.read_csv("vehicle.csv", index_col='Year', thousands=",")

# This calculates each one independently.
# However, it was still good practice, I suppose.

# Defines variables
df['y'] = df['Vehicle']
df['x1'] = df['GDP']
df['x2'] = df['Population']

#Means of each variable
mean_y = mean(df['y'])
mean_x1 = mean(df['x1'])
mean_x2 = mean(df['x2'])

# Variance from mean for each variable
df['var_y'] = df['y'] - mean_y
df['var_x1'] = df['x1'] - mean_x1
df['var_x2'] = df['x2'] - mean_x2

#products of variance
df['product_of_var_x1'] = df['var_y'] * df['var_x1']
df['product_of_var_x2'] = df['var_y'] * df['var_x2']

#Predicted slope (beta)
beta_x1 = sum(df['product_of_var_x1']) / sum([n * n for n in df['var_x1']])
beta_x2 = sum(df['product_of_var_x2']) / sum([n * n for n in df['var_x2']])

#intercept (alpha, or sometimes beta zero)
alpha_x1 = mean_y - (beta_x1 * mean_x1)
alpha_x2 = mean_y - (beta_x2 * mean_x2)

#print(df.drop(['Vehicle', 'GDP', 'Population'], axis =1))

with open("prelimdata.csv", "w") as file:
    df.drop(['Vehicle', 'GDP', 'Population'], axis =1).to_csv(file)

df['predicted_y1'] = alpha_x1 + (beta_x1 * df['x1'])
df['predicted_y2'] = alpha_x2 + (beta_x2 * df['x2'])


plt.plot(df['x1'], df['predicted_y1'], color='red')
plt.plot(df['x1'], df['y'], marker='o', linewidth=0, markersize = 1.6, color='black')
plt.title("Vehicles vs GDP")
plt.xlabel("GDP")
plt.ylabel("Vehicles")
# plt.savefig("gdp_explore.png")
plt.show()

plt.plot(df['x2'], df['predicted_y2'], color='red')
plt.plot(df['x2'], df['y'], marker='o', linewidth=0, markersize = 1.6, color='black')
plt.title("Vehicles vs Population")
plt.xlabel("Population")
plt.ylabel("Vehicles")
# plt.savefig("pop_explore.png")
plt.show()

# This uses some Python to complete the actual thing.
# I wanted to do this all manually to better understand the material,
# But every guide wanted me to use some library or another.

X = df[['GDP', "Population"]]
y = df['Vehicle']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
predictions = model.predict(X)


print(model.summary())
print(model.fvalue)
print(model.f_pvalue)

plt.plot(df['GDP'], predictions, color='teal')
plt.title("Vehicles vs GDP")
plt.xlabel("GDP")
plt.plot(df['GDP'], y, marker='o', linewidth=0, markersize = 1.6, color='black')
# plt.savefig("stats_gdp.png")
plt.show()

plt.plot(df['Population'], predictions, color='teal')
plt.title("Vehicles vs Population")
plt.xlabel("Population")
plt.plot(df['Population'], y, marker='o', linewidth=0, markersize = 1.6, color='black')
# plt.savefig("stats_pop.png")
plt.show()

vif_df = pd.DataFrame()
vif_df["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif_df["features"] = X.columns
print(vif_df)

name = ['Lagrange multiplier statistic', 'p-value',
        'f-value', 'f p-value']
test = sm.stats.het_breuschpagan(model.resid, model.model.exog)
test = lzip(name, test)

pprint(test)