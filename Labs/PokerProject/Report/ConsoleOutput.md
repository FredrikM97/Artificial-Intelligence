# Attempt 0
## Params
classifiers = [
    KNeighborsClassifier(5),
    SVC(gamma=2, C=1),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1, max_iter=1000),
]

## Data
Accuracy: 0.7142857142857143    Classifier: Classifier implementing the k-nearest neighbors vote
Accuracy: 0.6326530612244898    Classifier: C-Support Vector Classification
Accuracy: 0.7551020408163265    Classifier: A random forest classifier
Accuracy: 0.7346938775510204    Classifier: Multi-layer Perceptron classifier

# Attempt 1
## Params
classifiers = [
    KNeighborsClassifier,
    SVC,
    RandomForestClassifier,
    MLPClassifier,
]
params = [
    {'n_neighbors':range(1,10),'metric':['euclidean','manhattan','chebyshev']},   
    {'C':[0.5,1.0,2.0],'kernel':['rbf', 'linear','poly','sigmoid']},
    {'max_depth':[None,2,5,10],'criterion':['gini','entropy'],'n_estimators':[10,50,100],'max_features':['auto', 2,'log2']},
    {'hidden_layer_sizes':[(100,),(60,60)],'solver':['lbfgs', 'adam'],'alpha':[0.0001,0.01,1],'max_iter':[1000,10000]}#, 'tol':[1e-4,1e-6]
]
## Data
### k-nearest neighbors vote 
Best parameters: {'n_neighbors': 6, 'metric': 'chebyshev'}
Cross valid accuracy: 0.7211764705882352 vs test accuracy: 0.5714285714285714

top 5:
(0.7211764705882352, {'n_neighbors': 6, 'metric': 'chebyshev'})
(0.709747899159664, {'n_neighbors': 8, 'metric': 'chebyshev'})
(0.7031932773109244, {'n_neighbors': 4, 'metric': 'chebyshev'})
(0.697983193277311, {'n_neighbors': 9, 'metric': 'chebyshev'})
(0.6978151260504202, {'n_neighbors': 7, 'metric': 'chebyshev'})

### C-Support Vector Classification 
Best parameters: {'C': 2.0, 'kernel': 'linear'}
Cross valid accuracy: 0.7732773109243697 vs test accuracy: 0.7959183673469388

top 5:
(0.7732773109243697, {'C': 2.0, 'kernel': 'linear'})
(0.7557983193277311, {'C': 2.0, 'kernel': 'poly'})
(0.7500840336134453, {'C': 1.0, 'kernel': 'linear'})
(0.7495798319327731, {'C': 0.5, 'kernel': 'linear'})
(0.7442016806722689, {'C': 2.0, 'kernel': 'rbf'})

### A random forest classifier 
Best parameters: {'max_depth': 10, 'criterion': 'gini', 'n_estimators': 100, 'max_features': 'auto'}
Cross valid accuracy: 0.7788235294117647 vs test accuracy: 0.7142857142857143

top 5:
(0.7788235294117647, {'max_depth': 10, 'criterion': 'gini', 'n_estimators': 100, 'max_features': 'auto'})
(0.7783193277310925, {'max_depth': 10, 'criterion': 'entropy', 'n_estimators': 50, 'max_features': 'auto'})
(0.7670588235294118, {'max_depth': 10, 'criterion': 'entropy', 'n_estimators': 100, 'max_features': 'auto'})
(0.7618487394957982, {'max_depth': 10, 'criterion': 'gini', 'n_estimators': 50, 'max_features': 'auto'})
(0.7615126050420168, {'max_depth': None, 'criterion': 'gini', 'n_estimators': 50, 'max_features': 'log2'})
'
### Multi-layer Perceptron classifier
Best parameters: {'hidden_layer_sizes': (100,), 'solver': 'lbfgs', 'alpha': 1, 'max_iter': 1000}
Cross valid accuracy: 0.7677310924369748 vs test accuracy: 0.7346938775510204

top 5:
(0.7677310924369748, {'hidden_layer_sizes': (100,), 'solver': 'lbfgs', 'alpha': 1, 'max_iter': 1000})
(0.7621848739495799, {'hidden_layer_sizes': (100,), 'solver': 'lbfgs', 'alpha': 1, 'max_iter': 10000})
(0.7620168067226891, {'hidden_layer_sizes': (100,), 'solver': 'adam', 'alpha': 1, 'max_iter': 1000})
(0.7620168067226891, {'hidden_layer_sizes': (100,), 'solver': 'adam', 'alpha': 1, 'max_iter': 10000})
(0.7618487394957982, {'hidden_layer_sizes': (60, 60), 'solver': 'adam', 'alpha': 1, 'max_iter': 1000})

# Compare Attempt 0 and 1
Accuracy: 0.7142857142857143    Classifier: Classifier implementing the k-nearest neighbors vote
Accuracy: 0.6326530612244898    Classifier: C-Support Vector Classification
Accuracy: 0.7551020408163265    Classifier: A random forest classifier
Accuracy: 0.7346938775510204    Classifier: Multi-layer Perceptron classifier

Cross valid accuracy: 0.7211764705882352 vs test accuracy: 0.5714285714285714
Cross valid accuracy: 0.7732773109243697 vs test accuracy: 0.7959183673469388
Cross valid accuracy: 0.7788235294117647 vs test accuracy: 0.7142857142857143
Cross valid accuracy: 0.7677310924369748 vs test accuracy: 0.7346938775510204

KNN is trash as expected

# Attempt 2
## Params
classifiers = [
    SVC,
    RandomForestClassifier,
    MLPClassifier,
]
params = [  
    {'C':[0.5,1.0,2.0,3.0,4.0],'kernel':['rbf', 'linear','poly']},
    {'max_depth':[None,10],'criterion':['gini','entropy'],'n_estimators':[50,100,150],'max_features':['auto','log2']},
    {'hidden_layer_sizes':[(100,),(100,50)],'solver':['lbfgs', 'adam'],'batch_size':['auto',50],'alpha':[1,2,5],'max_iter':[1000,3000]}
]
## Data
### C-Support Vector Classification 
Best parameters: {'C': 3.0, 'kernel': 'linear'}
Cross valid accuracy: 0.7850420168067227 vs test accuracy: 0.7755102040816326
top 5:
(0.7850420168067227, {'C': 3.0, 'kernel': 'linear'})
(0.7732773109243697, {'C': 2.0, 'kernel': 'linear'})
(0.7732773109243697, {'C': 3.0, 'kernel': 'rbf'})
(0.7618487394957982, {'C': 4.0, 'kernel': 'linear'})
(0.7557983193277311, {'C': 2.0, 'kernel': 'poly'})
(0.7557983193277311, {'C': 4.0, 'kernel': 'rbf'})
(0.7500840336134453, {'C': 1.0, 'kernel': 'linear'})
(0.7495798319327731, {'C': 0.5, 'kernel': 'linear'})
(0.7442016806722689, {'C': 2.0, 'kernel': 'rbf'})
(0.7440336134453781, {'C': 4.0, 'kernel': 'poly'})

### A random forest classifier 
Best parameters: {'max_depth': 10, 'criterion': 'entropy', 'n_estimators': 100, 'max_features': 'auto'}
Cross valid accuracy: 0.7729411764705882 vs test accuracy: 0.7346938775510204
top 5:
(0.7729411764705882, {'max_depth': 10, 'criterion': 'entropy', 'n_estimators': 100, 'max_features': 'auto'})
(0.7727731092436975, {'max_depth': 10, 'criterion': 'gini', 'n_estimators': 150, 'max_features': 'auto'})
(0.7613445378151261, {'max_depth': 10, 'criterion': 'gini', 'n_estimators': 150, 'max_features': 'log2'})
(0.7499159663865547, {'max_depth': 10, 'criterion': 'entropy', 'n_estimators': 150, 'max_features': 'auto'})
(0.7497478991596639, {'max_depth': None, 'criterion': 'gini', 'n_estimators': 100, 'max_features': 'auto'})
(0.7495798319327731, {'max_depth': 10, 'criterion': 'entropy', 'n_estimators': 50, 'max_features': 'auto'})
(0.7442016806722689, {'max_depth': None, 'criterion': 'gini', 'n_estimators': 50, 'max_features': 'auto'})
(0.7442016806722689, {'max_depth': None, 'criterion': 'gini', 'n_estimators': 150, 'max_features': 'auto'})
(0.7442016806722689, {'max_depth': 10, 'criterion': 'gini', 'n_estimators': 100, 'max_features': 'log2'})
(0.7438655462184874, {'max_depth': None, 'criterion': 'gini', 'n_estimators': 50, 'max_features': 'log2'})

### Multi-layer Perceptron classifier 
Best parameters: {'hidden_layer_sizes': (100, 50), 'solver': 'lbfgs', 'batch_size': 50, 'alpha': 2, 'max_iter': 1000}
Cross valid accuracy: 0.7853781512605043 vs test accuracy: 0.7755102040816326
top 5:
(0.7853781512605043, {'hidden_layer_sizes': (100, 50), 'solver': 'lbfgs', 'batch_size': 50, 'alpha': 2, 'max_iter': 1000})
(0.7794957983193278, {'hidden_layer_sizes': (100, 50), 'solver': 'adam', 'batch_size': 'auto', 'alpha': 2, 'max_iter': 3000})
(0.779327731092437, {'hidden_layer_sizes': (100,), 'solver': 'lbfgs', 'batch_size': 50, 'alpha': 2, 'max_iter': 1000})
(0.779327731092437, {'hidden_layer_sizes': (100, 50), 'solver': 'lbfgs', 'batch_size': 50, 'alpha': 2, 'max_iter': 3000})
(0.7736134453781514, {'hidden_layer_sizes': (100,), 'solver': 'lbfgs', 'batch_size': 'auto', 'alpha': 2, 'max_iter': 1000})
(0.7736134453781514, {'hidden_layer_sizes': (100,), 'solver': 'lbfgs', 'batch_size': 50, 'alpha': 1, 'max_iter': 1000})
(0.7678991596638657, {'hidden_layer_sizes': (100,), 'solver': 'lbfgs', 'batch_size': 'auto', 'alpha': 1, 'max_iter': 3000})
(0.7678991596638657, {'hidden_layer_sizes': (100,), 'solver': 'adam', 'batch_size': 'auto', 'alpha': 1, 'max_iter': 3000})
(0.7678991596638657, {'hidden_layer_sizes': (100, 50), 'solver': 'adam', 'batch_size': 'auto', 'alpha': 2, 'max_iter': 1000})
(0.7678991596638657, {'hidden_layer_sizes': (100, 50), 'solver': 'adam', 'batch_size': 50, 'alpha': 1, 'max_iter': 3000})

# Final Attempt
## Params
classifiers = [
    SVC(C=2.5, kernel='linear'),
    RandomForestClassifier(max_depth=None, criterion='gini', n_estimators=115, max_features='auto'),
    MLPClassifier(hidden_layer_sizes=(100,50), alpha=2, solver='lbfgs',batch_size=50,max_iter=1000),
]
## Data
Accuracy: 0.7959183673469388    Classifier: C-Support Vector Classification
Accuracy: 0.7346938775510204    Classifier: A random forest classifier
Accuracy: 0.7551020408163265    Classifier: Multi-layer Perceptron classifier