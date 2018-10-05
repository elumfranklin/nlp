# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 10:59:53 2018

@author: endy franklin
this code predicts if a passenger would survive or not from the titanic
ship wreck
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

dataset= pd.read_csv('train.csv')
#using seaborn to visualize colums with more missing values
null_value=sns.heatmap(dataset.isnull(), yticklabels=False, cmap='viridis', cbar=False)


#using seaborn to count the number of survivors based on sex
sns.countplot(x='Survived', hue='Sex', data=dataset)

#using seaborn to count the number of survivors based on class
sns.countplot(x='Survived', hue='Pclass', data=dataset)

#distribution plot of ages
dataset['Age'].plot.hist()

#using seaborn to count the sibling/spouse
sns.countplot(x='SibSp', data=dataset)

#distribution plot of fare
dataset['Fare'].plot.hist()




#find the missing age based on the Pclass
dataset.groupby('Pclass').mean()

def get_age(cols):
    Age=cols[0]
    Pclass=cols[1]
    
    if pd.isnull(Age):
        if Pclass ==1:
            return 38
        elif Pclass == 2:
            return 29
        else:
            return 25
    else:
        return Age
    
dataset['Age'] = dataset[['Age', 'Pclass']].apply(get_age, axis=1)


#drop this column since there are so many missing values
dataset.drop('Cabin', axis=1, inplace=True)

#converting categorical variables to dummy or indicator variables
sex=pd.get_dummies(dataset['Sex'], drop_first=True)
embark=pd.get_dummies(dataset['Embarked'], drop_first=True)
dataset=pd.concat([dataset, sex, embark], axis=1)

dataset.drop(['Sex', 'Embarked', 'Name', 'Ticket', 'PassengerId'], axis=1, inplace=True)

#get the dependent and independent variable
y=dataset['Survived']
x=dataset.drop('Survived', axis=1)

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state =101)

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(x_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(x_test)

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))


#using confusion metrics
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, y_pred))





