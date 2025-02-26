import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor # where we combine different machine learning models
from sklearn.model_selection import GridSearchCV



param_grid = {  # value from sklearn website
    "n_estimators" : [100,200,30],
    #"max_features" : [2,4,6,8]
    "min_samples_split" : [2,4], # be careful about typos
    "max_depth" :[None,4,8]
}

scalar = StandardScaler()
forest = RandomForestRegressor()
data = pd.read_csv("housing.csv")
#print(data)
#print(data.info())
data.dropna(inplace= True) # Drops rows or columns containing missing values based on custom criteria.#


#data.drop(["ocean_proximity"], axis = 1,inplace = True)

x= data.drop(["median_house_value"],axis = 1)


y = data["median_house_value"]
#data.drop(["ocean_proximity"], axis = 1,inplace = True)
#print (x)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2, random_state=42)
train_data = x_train.join(y_train)

train_data.ocean_proximity.value_counts()
train_data = train_data.join(pd.get_dummies(train_data.ocean_proximity)).drop(["ocean_proximity"],axis = 1)
#print(train_data)



#train_data.hist(figsize = (15,8))
#plt.figure(figsize = (15,8))
#sns.heatmap(train_data.corr(),annot=True,cmap = "YlGnBu")  # YlGnBu is a value that cannot be changed

train_data["total_rooms"] = np.log(train_data["total_rooms"] + 1)
train_data["total_bedrooms"] = np.log(train_data["total_bedrooms"] + 1)
train_data["population"] = np.log(train_data["population"] + 1)
train_data["households"] = np.log(train_data["households"] + 1)

#train_data.join(pd.get_dummies(train_data.ocean_proximity)).drop(["ocean_proximity"],axis = 1)
#train_data.hist(figsize = (15,8))

#sns.heatmap(train_data.corr(),annot=True,cmap = "YlGnBu")  # YlGnBu is a value that cannot be changed
#plt.figure(figsize= (15,8))
#sns.scatterplot(x = "latitude", y  = "longitude",data = train_data, hue = "median_house_value",palette= "coolwarm")
#plt.show()
#train_data.ocean_proximity.value_counts()
train_data["bedroom_ratio"] = train_data["total_bedrooms"]/ train_data["total_rooms"]
train_data["households"] = train_data["total_rooms"]/ train_data["households"]
#sns.heatmap(train_data.corr(),annot=True,cmap = "YlGnBu")  # YlGnBu is a value that cannot be changed
#plt.figure(figsize= (15,8))

#plt.show()

x_train,y_train = train_data.drop(["median_house_value"],axis = 1),train_data["median_house_value"]

x_train_s = scalar.fit_transform(x_train)

#forest.fit(x_train_s,y_train)

test_data = x_test.join(y_test)
test_data["total_rooms"] = np.log(test_data["total_rooms"] + 1)
test_data["total_bedrooms"] = np.log(test_data["total_bedrooms"] + 1)
test_data["population"] = np.log(test_data["population"] + 1)
test_data["households"] = np.log(test_data["households"] + 1)
test_data = test_data.join(pd.get_dummies(test_data.ocean_proximity)).drop(["ocean_proximity"],axis = 1)
test_data["bedroom_ratio"] = test_data["total_bedrooms"]/ test_data["total_rooms"]
test_data["households"] = test_data["total_rooms"]/ test_data["households"]

x_test,y_test = test_data.drop(["median_house_value"],axis = 1),test_data["median_house_value"]

x_test_s = scalar.transform(x_test)
#print(train_data)
#print(test_data)

# this may need this {a =reg.score(x_test,y_test)}
reg = LinearRegression()
reg.fit(x_train_s, y_train)
reg_score = reg.score(x_test_s, y_test)
print(reg_score) # prints the value 0.650104186305493 which can be improved to be 1

# finding optimal model we use the ensemble
#forest.fit(x_train,y_train)

#forest.score(x_test,y_test)
# this may be used for this a = forest.score(x_test,y_test)
#forest_score = forest.score(x_test_s,y_test)
#print(forest_score)
grid_search = GridSearchCV(forest, param_grid, cv=5, scoring="r2", return_train_score=True, n_jobs=-1) # Changed to r2, n_jobs=-1 for parallel processing
grid_search.fit(x_train_s, y_train)

best_forest = grid_search.best_estimator_

forest_score = best_forest.score(x_test_s,y_test)

print(forest_score)
print(grid_search.best_params_)

