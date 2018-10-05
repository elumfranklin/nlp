# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:41:46 2018

@author: endy franklin
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('C:/Users/endy franklin/Desktop/Machine Learning A-Z Template Folder/Part 3 - Classification/Section 15 - K-Nearest Neighbors (K-NN)/K_Nearest_Neighbors/Social_Network_Ads.csv')
X = dataset.iloc[:, [2, 3]].values
y = dataset.iloc[:, 4].values

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting K-NN to the Training set
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 4)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

#classification report and confusion matrix
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

#using the elbow method
error_rate=[]
for i in range(1,10):
    classifier=KNeighborsClassifier(n_neighbors = i)
    classifier.fit(X_train, y_train)
    pred_i=classifier.predict(X_test)
    error_rate.append(np.mean(pred_i !=y_test))
    
error_rate

plt.plot(range(1,10), error_rate, color='blue', linestyle='dashed', marker='o', markerfacecolor='red',)
plt.title('error_rate vs k value')
plt.xlabel('k')
plt.ylabel('error_rate')
plt.show()
    
    
