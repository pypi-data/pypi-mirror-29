import sys
sys.path.append('../..')

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC

from MyProject import core


def test_Database():
    '''Check the shape of the database'''
    result = core.Database()
    assert result.shape == (1159, 32), "The database is not right"  ##test the shape of the database
    return

def test_SMILES():
    """Check the SMILES function could generate the correct molecular structure,based on input CID number"""
    result1 = core.SMILES(175854)  ##check SMILES structures
    result2 = core.SMILES(13526104)
    result3 = core.SMILES(887)
    
    assert result1 == 'C(C=CCO)O', 'The chemcial (2E)-but-2-ene-1,4-diol converts wrong!'
    assert result2 == 'CCCCC(CC)(CO)C(C)O', 'The chemcial 2-Butyl-2-ethylbutane-1,3-diol converts wrong!'
    assert result3 == 'CO', 'The chemcial methanol converts wrong'
    return

def test_descriptor_generator():
    """Check descriptor_generator can generate correct numbers of functional groups for 
    specific compound according to CID"""
    result1 = core.descriptor_generator(887).values.T.tolist()  ##test methane
    result2 = core.descriptor_generator(175854).values.T.tolist()   ##test 2-Butene-1,4-diol, (2E)-
    result3 = core.descriptor_generator(61038).values.T.tolist()   ##test 2-Ethyl-2-butyl-1,3-propanediol

    assert result1 == [[4],[1],[0],[0],[0], [0], [0],[0],[0],[0], [0],[0], [0], [0],[0], [0],[0], [1], [0],[0], [0], [0], [0], [0], [0], [0], [0], [0]], (
                      "The descriptor_generator does not work properly")
    assert result2 == [[8], [0], [2], [0],[ 0],[ 0], [2], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [2], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], (
                      "The descriptor_generator does not work properly")
    assert result3 == [[20], [2], [6], [0], [1], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [2], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], (
                      "The descriptor_generator does not work properly")
    return

def test_df_prediction():
    """
    This function is used to test df_prediction.
    """
    family = 'Alcohols'   ###define parameters
    prop = 'Flash Point'
    train = core.df_prediction(family, prop)[0]
    test = core.df_prediction(family, prop)[1]
    assert train.shape == (60, 32), "The training data are not right"  ###test the shape of training data
    assert test.shape == (7, 32), "The testing data are not right"    ### test the shape of testing data
    return

def test_bootstrap():
    """Check the type of outputs are correct"""
    result1 = type(core.bootstrap('Flash Point', 10, 'Esters', core.OLS_train('Esters', 'Flash Point')))
    result2 = type(core.bootstrap('Flash Point', 10, 'Esters', core.OLS_train('Esters', 'Flash Point'))[0])
    assert result1 == tuple, 'The output is wrong'
    assert result2 == np.float64, 'The output is wrong'
    return

def test_plot():
    """Check the type of outputs are correct"""
    assert type(core.plot(core.OLS_train('Esters','Cetane Number'), 'Cetane Number', 'Esters')) == matplotlib.figure.Figure, 'The output is wrong :('
    return

def test_model():
    result1 = type(core.OLS_pred('Esters', 'Flash Point', core.descriptor_generator(887)))
    result2 = type(core.OLS_pred('Esters', 'Cetane Number', core.descriptor_generator(65115)))
    assert result1 == np.float64, 'The output is wrong'
    assert result2 == np.float64, 'The output is wrong'
    return

X_train, y_train, X_test, y_test = core.data_clean()
X=X_train.iloc[0:1,:]
y_pred = 'Esters'

def test_data_clean():
    # four results of data sets should be provided
    assert len(core.data_clean()) == 4, "clean_data() breaks"
    assert type(core.data_clean()) == tuple, "clean_data() breaks"
    return 

def test_train_knn():
    k = 5
    knn = core.train_knn(k, X_train, y_train)
    # knn should be a classifier
    type(knn) == KNeighborsClassifier, "train_knn() breaks"
    return 

def test_test_knn():
    k = 5
    # accuarcy should be possitive
    assert core.test_knn() > 0, "test_knn() breaks"
    return
    

def test_predict_family_knn():
    # prediction should be an array of family
    assert type(core.predict_family_knn(X)) == np.ndarray, "predict_family_knn() breaks"
    return

def test_plot_knn():
    # this fuction should provide a figure
    assert type(core.plot_knn(y_pred)) == plt.Figure, "plot_knn() breaks"
    return 

def test_train_lda():
    # lda should be a classifier
    lda = core.train_lda(X_train, y_train)
    type(lda) == LinearDiscriminantAnalysis, "train_lda() breaks"
    return 

def test_test_lda():
    # accuarcy should be possitive
    assert core.test_lda() > 0, "test_lda() breaks"
    return
    

def test_predict_family_lda():
    # prediction should be an array of family
    assert type(core.predict_family_lda(X)) == np.ndarray, "predict_family_lda() breaks"
    return

def test_plot_lda():
    # this fuction should provide a figure
    assert type(core.plot_lda(y_pred)) == plt.Figure, "plot_lda() breaks"
    return

def test_train_svm():
    # svm should be a classifier
    svm = core.train_svm(X_train, y_train)
    type(svm) == LinearSVC, "train_svm() breaks"
    return 

def test_test_svm():
    # accuarcy should be possitive
    assert core.test_svm() > 0, "test_svm() breaks"
    return
    
def test_predict_family_svm():
    # prediction should be an array of family
    assert type(core.predict_family_svm(X)) == np.ndarray, "predict_family_svm() breaks"
    return

def test_plot_svm():
    # this fuction should provide a figure
    assert type(core.plot_svm(y_pred)) == plt.Figure, "plot_svm() breaks"
    return 
