import pandas as pd
import numpy as np
import pickle

data = pd.read_csv('be_ml.csv')

x = data.drop(['close'],axis=1)
y= data['close']

from sklearn.model_selection import train_test_split
x_train, x_test , y_train ,y_test = train_test_split(x,y,test_size = 0.2,random_state = 0)

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(x_train, y_train)

pickle.dump(model, open('model.pkl', "wb"))