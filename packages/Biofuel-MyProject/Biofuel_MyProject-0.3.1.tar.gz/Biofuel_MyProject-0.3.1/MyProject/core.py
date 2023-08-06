import matplotlib.pyplot as plt
from neupy import algorithms, layers, environment, estimators
import numpy as np
import openbabel
import pandas as pd
import pubchempy as pcp
import pybel
from pybel import Smarts, readstring
from sklearn import linear_model, metrics
from sklearn.cross_decomposition import PLSRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV, ShuffleSplit, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPRegressor


def Database():
    """compile data sets into a data library, the output will be a DataFrame"""
    data_1 = pd.read_excel('data/Flash Point and Cetane Number Predictions for Fuel Compounds.xls', skiprows=3) ###load data
    data = data_1[['Name','Family', 'FP Exp.', 'CN Exp.']]  ###select columns
    result_1 = data.drop(index=0)   ###rearrange the index
    result_1.reset_index(drop=True, inplace=True)
    names = ['Name','Family', 'Flash Point', 'Cetane Number']   ###rename columns
    result_1.columns = names
    data_2 = pd.read_excel('data/Flash Point and Cetane Number Predictions for Fuel Compounds.xls', skiprows=4)
    result_2 = data_2.loc[: , '-H': 'aaCa']   ###select specific columns
    smarts = ["[H]", "[CX4H3]", "[CX4H2]", "[CX4H1]", "[CX4H0]", "[CX3H2]", "[CX3H1]", "[CX3H0]", "[CX2H1]","[CX2H0]", 
"[CX4H2R]", "[CX4H1R]", "[CX4H0R]","[CX3H1R]","[CX3H0R]","[cX3H1](:*):*", "[cX3H0](:*)(:*)*", "[OX2H1]", "[OX2H1][cX3]:[c]", 
"[OX2H0]", "[OX2H0R]", "[oX2H0](:*):*", "[CX3H0]=[O]", "[CX3H0R]=[O]", "[CX3H1]=[O]", "[CX3H0](=[O])[OX2H1]", 
"[CX3H0](=[O])[OX2H0]", "[cX3H0](:*)(:*):*"]   ###rename functional groups to SMARTS
    result_2.columns = smarts
    result = pd.concat([result_1, result_2], axis=1)   ###combine two dataframes into one dataframe
    return result


def SMILES(CID):
    """
    Description:
    This function produces a SMILES from CID number input 
    """
    #CID number can be gained from URL:https://pubchem.ncbi.nlm.nih.gov/
    c = pcp.Compound.from_cid(CID)
    SMILES = c.canonical_smiles  ###create SMILES structure
    return SMILES


def descriptor_generator(CID):
    """Generate the number of each functional group for specific compound according to input CID"""
    fg = ["[H]", "[CX4H3]", "[CX4H2]", "[CX4H1]", "[CX4H0]", "[CX3H2]", "[CX3H1]", "[CX3H0]", "[CX2H1]", 
              "[CX2H0]", "[CX4H2R]", "[CX4H1R]", "[CX4H0R]","[CX3H1R]","[CX3H0R]","[cX3H1](:*):*", 
              "[cX3H0](:*)(:*)*", "[OX2H1]", "[OX2H1][cX3]:[c]", "[OX2H0]", "[OX2H0R]", "[oX2H0](:*):*", 
              "[CX3H0]=[O]", "[CX3H0R]=[O]", "[CX3H1]=[O]", "[CX3H0](=[O])[OX2H1]", "[CX3H0](=[O])[OX2H0]", 
              "[cX3H0](:*)(:*):*"]  ###define SMARTS of functional groups list
    counts = []   ###count functional groups
    result = SMILES(CID)  ###generate SMILES of compound
    mol = readstring("smi", result)   ###load SMILES
    for i in range(len(fg)):
        smarts = Smarts(fg[i])   ###load SMARTS
        n = smarts.findall(mol)  ###find specific functional group, return will be tuples in a list
        counts.append(len(n))    ###record number of functional group
    X = pd.DataFrame(np.array(counts).reshape(1, -1))  ###reshape the counts
    return X


def df_prediction(family, prop):
    """
    This function is used to create train and test data for prediction.
    """
    test_size = 0.1   ###define test size 
    data = Database()   ###load, select, clear NaN data
    data_f = data[data.Family == family]
    df = data_f[np.isfinite(data_f[prop])]
    if df.shape == (0, 32):
        raise Exception ('shape', 'We are short of data!')
        return
    else:
        train, test = train_test_split(df, test_size=test_size, random_state=17)  ###split data
        return train, test


def plot(model, prop, family):
    """
    This function is used to make parity plot, mse vs. bootstrap samples, r_2 vs. bootstrap samples.
    """
    iteration = 10  ###define iteration for bootstrap samples
    
    train, test = df_prediction(family, prop)
    X_train = train[train.columns[4:]]  ###select functional groups
    X_test = test[test.columns[4:]]
    n = np.arange(1, iteration+1)       ###set bootstrap sample
    mses = []    ###place mse
    r2s = []     ###place r2
    
    fig = plt.figure(figsize=(18, 6))   ###adjust the figsize
    plt.subplot(131)                    ###make parity plot
    plt.scatter(train[prop], model.predict(X_train), label='training data')
    plt.scatter(test[prop], model.predict(X_test), color='r', label='testing data')
    plt.xlabel(prop, fontsize=16)
    plt.ylabel(prop, fontsize=16)
    plt.legend(fontsize=16)
    plt.title('Parity Plot', fontsize=16)
    
    for i in n:
        mse, r2 = bootstrap(prop, i, family, model)  ###get mse and r2 average for different samples
        mses.append(mse)
        r2s.append(r2)
    
    plt.subplot(132)    ###make mse vs. bootstrap samples
    plt.plot(n, mses)
    plt.xlabel('Number of Bootstrap Samples', fontsize=16)
    plt.ylabel('Mean Squared Error (MSE)', fontsize=16)
    plt.title('Number of Bootstrap Samples vs. MSE', fontsize=16)
    
    plt.subplot(133)    ###make r2 vs. bootstrap samples
    plt.plot(n, r2s)
    plt.xlabel('Number of Bootstrap Samples', fontsize=16)
    plt.ylabel('$R^2$', fontsize=16)
    plt.title('Number of Bootstrap Samples vs. $R^2$', fontsize=16)
    return fig


def bootstrap(prop, iteration, family, model):
    """
    This function is used to validate model by resampling method, it will generate mse and r2 average.
    """
    fraction = 0.8  ###define resample fraction
    data = Database()  ###load dataframe
    data_f = data[data.Family == family]  ###select specific family to resample
    df = data_f[np.isfinite(data_f[prop])]  ###clear the data is NaN
    mse = []   ###place mse values
    r2 = []    ###place r2 values
    for i in range(iteration):
        sample = df.sample(frac=fraction, replace=True)   ###sample from data
        X = sample[sample.columns[4:]]  ###select functional groups
        y = sample[prop]     ###select properties
        y_pred = model.predict(X)   ###build model and predict
        mse.append(mean_squared_error(y, y_pred))   ###compute mse
        r2.append(r2_score(y, y_pred))   ###compute r2
    mse_avg = np.mean(mse)    ###average mse
    r2_avg = np.mean(r2)      ###average r2
    return mse_avg, r2_avg


def OLS_train(family, prop):
    """
    This function is used to train model according to Ordinary Least Squares(linear model). 
    """
    train, test = df_prediction(family, prop)  ###create data for train and test
    OLS = linear_model.LinearRegression()   ###build model
    train_X = train[train.columns[4:]]   ###select functional groups
    OLS.fit(train_X, train[prop])    ###train model
    return OLS     ###return model

def OLS_test(family, prop):
    """
    This function is used to test and make plots according to OLS model.
    """
    model= OLS_train(family, prop)
    fig = plot(model, prop, family)  ###make plots
    return fig

def OLS_pred(family, prop, fg):
    """
    This function is used to predict properties according to OLS model.
    """
    model= OLS_train(family, prop)
    result = model.predict(fg)[0]
    return result


def PLS_train(family, prop):
    """
    This function is used to train model according to Partial Least Squares(linear model).
    """
    train, test = df_prediction(family, prop)  ###create data for train and test
    PLS = PLSRegression()          ###build model
    train_X = train[train.columns[4:]]   ###select functional groups
    PLS.fit(train_X, train[prop])   ###train model
    return PLS     ###return model

def PLS_test(family, prop):
    """
    This function is used to test and make plots according to PLS model.
    """
    model = PLS_train(family, prop)
    fig = plot(model, prop, family)  ###make plots
    return fig

def PLS_pred(family, prop, fg):
    """
    This function is used to predict properties according to PLS model.
    """
    model = PLS_train(family, prop)
    result = model.predict(fg)[0][0]
    return result


def PNR_train(family, prop):
    """
    This function is used to train model according to Polynomial Regression(nonlinear model). 
    """
    train, test = df_prediction(family, prop)    ###create data for train and test
    PNR = make_pipeline(PolynomialFeatures(), Ridge())   ###build model
    train_X = train[train.columns[4:]]   ###select functional groups
    PNR.fit(train_X, train[prop])    ###train model
    return PNR         ###return model

def PNR_test(family, prop):
    """
    This function is used to test and make plots according to PNR model.
    """
    model = PNR_train(family, prop)
    fig = plot(model, prop, family)  ###make plots
    return fig

def PNR_pred(family, prop, fg):
    """
    This function is used to predict properties according to PNR model.
    """
    model = PNR_train(family, prop)
    result = model.predict(fg)[0]
    return result


def GRNN_train(family, prop):
    """This function is used to predict properties by using the General Regression Neural Network model."""
    train, test = df_prediction(family, prop)  ###create data for train and test
    x_train = train[train.columns[4:]]   ###select functional groups
    y_train = train[prop]    ###select prop groups

    scaler = MinMaxScaler(feature_range=(0, 1))  #Rescale model
    rescaledX = scaler.fit_transform(x_train)   #Rescale x
    np.set_printoptions(precision=4) # summarize transformed data for x,, and also set up the descimal place of the value
    
    grnn = algorithms.GRNN(std=0.4,verbose=False,)    #Set up the model
    grnn.train(x_train, y_train)  #Train the model
    return grnn

def GRNN_test(family, prop):
    """
    This function is used to make plots according to GRNN model.
    """
    model= GRNN_train(family, prop)
    fig = plot(model, prop, family)  ###make plots
    return fig

def GRNN_pred(family, prop, fg):
    """
    This function is used to predict properties according to GRNN model.
    """
    model = GRNN_train(family, prop)
    result = model.predict(fg)[0][0]
    return result


def MLPR_train(family, prop):
    """This function is used to predict properties by using the Multiple Layers Perception Regression model."""
    # Input data and define the parameters
    data = Database()
    data_f = data[data.Family == family]
    df = data_f[np.isfinite(data_f[prop])]
    x = df.loc[:,'[H]':'[cX3H0](:*)(:*):*']
    y = df[prop]
    
    array_x = x.values
    array_y = y.values
    
    scaler = MinMaxScaler(feature_range=(0, 1))   #Rescale model
    rescaledX = scaler.fit_transform(array_x)   #Rescale x
    np.set_printoptions(precision=4) # summarize transformed data for x,, and also set up the descimal place of the value
    
    x_train, x_test, y_train, y_test = train_test_split(rescaledX, array_y, test_size=0.1, random_state=17)
        
    mlpr = MLPRegressor(hidden_layer_sizes=(1000,),activation='identity', solver='sgd', learning_rate='adaptive', 
max_iter=4000, verbose=False)   #Set up the model
    mlpr.fit(x_train, y_train)   #Train the model
    return mlpr, x_train, x_test, y_train, y_test

def MLPR_test(family, prop):
    """
    This function is used to make plots according to MLPR model.
    """
    model, x_train, x_test, y_train, y_test = MLPR_train(family, prop)
    y_predict = model.predict(x_test)
    y_predict_train = model.predict(x_train)
    
    fig = plt.figure(figsize=(18, 6))
    plt.scatter(y_test, y_predict, color='r', label='testing data')
    plt.scatter(y_train, y_predict_train,  label='training data')
    plt.xlabel(prop+'_Actual', fontsize=16)
    plt.ylabel(prop+'_Predict', fontsize=16)
    plt.title('Parity Plot', fontsize=16)
    plt.legend()
    return fig

def MLPR_pred(family, prop, fg):
    """
    This function is used to predict properties according to MLPR model.
    """
    model = MLPR_train(family, prop)[0]
    result = model.predict(fg)[0]
    return result


def data_clean():
    """split data and generate train & test subset"""
    df = Database()
    train, test = train_test_split(df, test_size=0.1, random_state=2)
    a = train.loc[:,'[H]': '[cX3H0](:*)(:*):*']
    X_train = a.mask(a>0, 1)# transfer the descriptor numbers into 1/0
    y_train = train['Family']

    b = test.loc[:,'[H]': '[cX3H0](:*)(:*):*']
    X_test = b.mask(b>0, 1)
    y_test = test['Family']
    return X_train, y_train, X_test, y_test


def train_knn(k, X_train, y_train):
    """use knn method to train data"""
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    return knn

def test_knn():
    """give classification accuracy"""
    X_train, y_train, X_test, y_test = data_clean()
    k = 5 # fix k at 5
    knn = train_knn(k, X_train, y_train)
    test_pred = knn.predict(X_test)
    train_pred = knn.predict(X_train)
    acc = metrics.accuracy_score(y_test, test_pred)
    print('k =', k)
    print('Accuracy =', acc)
    return acc
    
def predict_family_knn(X):
    """predit family of import molecule X"""
    X_train, y_train, X_test, y_test = data_clean()
    k = 5 # fix k at 5
    knn = train_knn(k, X_train, y_train)
    y_pred = knn.predict(X)
    return y_pred

def plot_knn(y_pred):
    """plot a y_pred vs. y_actual figure and show the prediction on it"""
    X_train, y_train, X_test, y_test = data_clean()
    k = 5 # fix k at 5
    knn = train_knn(k, X_train, y_train)
    test_pred = knn.predict(X_test)
    train_pred = knn.predict(X_train)
    acc = metrics.accuracy_score(y_test, test_pred)
    ax = plt.figure(figsize=(9,4))
    plt.plot([0,7], [0,7], color='k')
    plt.scatter(y_train, train_pred, marker='s', s=100,c='c', label='train')
    plt.scatter(y_test, test_pred, marker='d', s=100, c='orange', label='test')
    plt.scatter(y_pred, y_pred, marker='*', s=100, c='r', label='prediction') # plot the predictoin dot
    plt.xticks(rotation='40')
    plt.xlabel('Actual Family', fontsize=15)
    plt.ylabel('Predicted Family', fontsize=15)
    plt.title('Knn Classification (k=%d, Accuracy=%.5f)' % (k, acc),fontsize=20)
    plt.legend()
    return ax


def train_lda(X_train, y_train):
    """use lda method to train data"""
    lda = LinearDiscriminantAnalysis()
    lda.fit(X_train, y_train)
    return lda

def test_lda():
    """give classification accuracy"""
    X_train, y_train, X_test, y_test = data_clean()
    lda = train_lda(X_train, y_train)
    test_pred = lda.predict(X_test)
    acc = metrics.accuracy_score(y_test, test_pred)
    print('Accuracy = ', acc)
    return acc

def predict_family_lda(X):
    """predit family of import molecule X"""
    X_train, y_train, X_test, y_test = data_clean()
    lda = train_lda(X_train, y_train)
    y_pred = lda.predict(X)
    return y_pred

def plot_lda(y_pred):
    """plot a y_pred vs. y_actual figure and show the prediction on it"""
    X_train, y_train, X_test, y_test = data_clean()
    lda = train_lda(X_train, y_train)
    test_pred = lda.predict(X_test)
    train_pred = lda.predict(X_train)
    acc = metrics.accuracy_score(y_test, test_pred)
    ax = plt.figure(figsize=(9,4))
    plt.plot([0,7], [0,7], color='k')
    plt.scatter(y_train, train_pred, marker='s', s=100,c='c', label='train')
    plt.scatter(y_test, test_pred, marker='d', s=100, c='orange', label='test')
    plt.scatter(y_pred, y_pred, marker='*', s=100, c='r', label='prediction')# plot the predictoin dot
    plt.xticks(rotation='40')
    plt.xlabel('Actual Family', fontsize=15)
    plt.ylabel('Predicted Family', fontsize=15)
    plt.title('LDA Classification (Accuracy=%.5f)' % (acc),fontsize=20)
    plt.legend()
    return ax


def train_svm(X_train, y_train):
    """use lda method to train data"""
    svm = LinearSVC(random_state=0)
    svm.fit(X_train, y_train)
    return svm

def test_svm():
    """give classification accuracy"""
    X_train, y_train, X_test, y_test = data_clean()
    svm = train_svm(X_train, y_train)
    test_pred = svm.predict(X_test)
    acc = metrics.accuracy_score(y_test, test_pred)
    print('Accuracy = ', acc)
    return acc

def predict_family_svm(X):
    """predit family of import molecule X"""
    X_train, y_train, X_test, y_test = data_clean()
    svm = train_svm(X_train, y_train)
    y_pred = svm.predict(X)
    return y_pred

def plot_svm(y_pred):
    """plot a y_pred vs. y_actual figure and show the prediction on it"""
    X_train, y_train, X_test, y_test = data_clean()
    svm = train_svm(X_train, y_train)
    test_pred = svm.predict(X_test)
    train_pred = svm.predict(X_train)
    acc = metrics.accuracy_score(y_test, test_pred)
    ax = plt.figure(figsize=(9,4))
    plt.plot([0,7], [0,7], color='k')
    plt.scatter(y_train, train_pred, marker='s', s=100,c='c', label='train')
    plt.scatter(y_test, test_pred, marker='d', s=100, c='orange', label='test')
    plt.scatter(y_pred, y_pred, marker='*', s=100, c='r', label='prediction')# plot the predictoin dot
    plt.xticks(rotation='40')
    plt.xlabel('Actual Family', fontsize=15)
    plt.ylabel('Predicted Family', fontsize=15)
    plt.title('SVM Classification (Accuracy=%.5f)' % (acc),fontsize=20)
    plt.legend()
    return ax

