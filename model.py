import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

from parse_player_stats import ROLES

# Train a random forest model
def randomForest(train_X, train_y, test_X, test_y):
    print("\n\n")
    print(f"###Random Forest###")
    print("\n")
    
    '''Cross Validation'''
    n_estimators = [int(x) for x in np.linspace(start = 500, stop = 2000, num = 100)]
    max_features = ['auto', 'sqrt']
    max_depth = [int(x) for x in np.linspace(10, 100, num = 10)]
    max_depth.append(None)
    min_samples_split = [2, 5, 10]
    min_samples_leaf = [1, 2, 4]
    bootstrap = [True, False]
    random_grid = {'n_estimators': n_estimators,
                   'max_features': max_features,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf,
                   'bootstrap': bootstrap       
                  }
    rf = RandomForestRegressor(random_state = 69)
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 200, cv = 5, verbose = 1, random_state = 69, n_jobs = -1)
    rf_random.fit(train_X, train_y)
    pred = rf_random.predict(test_X)
    rf_best_params = rf_random.best_params_
    rf_mse = metrics.mean_squared_error(test_y, pred)
    print("Best parameters for random forest: ", rf_best_params)
    print("Mean Squared Error for Random Forest = ", rf_mse)

    return (rf_random.best_estimator_, rf_mse)

# Train a gradient boosting model
def gradientboosting(train_X, train_y, test_X, test_y):
    print("\n\n")
    print(f"###Gradient Boosting###")
    print("\n")

    '''Cross validation'''
    n_estimators = [int(x) for x in np.linspace(start = 500, stop = 2000, num = 100)]
    learning_rate = [0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 1]
    max_features = ['auto', 'sqrt']
    max_depth = [int(x) for x in np.linspace(10, 100, num = 10)]
    max_depth.append(None)
    min_samples_split = [2, 5, 10]
    min_samples_leaf = [1, 2, 4]
    random_grid = {'n_estimators': n_estimators,
                   'max_features': max_features,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf,
                   'learning_rate': learning_rate       
                  }
    gb = GradientBoostingRegressor(random_state = 69)
    gb_random = RandomizedSearchCV(estimator = gb, param_distributions = random_grid, n_iter = 200, cv = 5, verbose = 1, random_state = 69, n_jobs = -1)
    gb_random.fit(train_X, train_y)
    pred = gb_random.predict(test_X)
    gb_best_params = gb_random.best_params_
    gb_mse = metrics.mean_squared_error(test_y, pred)
    print("Best parameters for Gradient Boosting: ", gb_best_params)
    print("Mean Squared Error for Gradient Boosting = ", gb_mse)

    return (gb_random.best_estimator_, gb_mse)

# Train a KNN model
def KNN(train_X, train_y, test_X, test_y):
    print("\n\n")
    print(f"###KNN###")
    print("\n")

    n_neighbors = [int(x) for x in np.linspace(start = 5, stop = 50, num = 10)]
    weights = ['uniform', 'distance']
    algorithm = ['auto', 'ball_tree', 'kd_tree', 'brute']
    p = [1, 2]
    leaf_size = [int(x) for x in np.linspace(start = 10, stop = 100, num = 10)]
    random_grid = {'n_neighbors': n_neighbors,
                   'weights': weights,
                   'algorithm': algorithm,
                   'p': p,
                   'leaf_size': leaf_size,       
                  }
    scaler = StandardScaler()
    train_X_scaled = scaler.fit_transform(train_X)
    test_X_scaled = scaler.transform(test_X)
    knn = KNeighborsRegressor()
    knn_random = RandomizedSearchCV(estimator = knn, param_distributions = random_grid, n_iter = 200, cv = 5, verbose = 1, random_state = 69, n_jobs = -1)
    knn_random.fit(train_X_scaled, train_y)
    pred = knn_random.predict(test_X_scaled)
    knn_best_params = knn_random.best_params_
    knn_mse = metrics.mean_squared_error(test_y, pred)
    print("Best parameters for KNN: ", knn_best_params)
    print("Mean Squared Error for KNN = ", knn_mse)

    return (knn_random.best_estimator_, knn_mse)


if __name__ == "__main__":
    tank_train_X = pickle.load(open("aggregated/tank_train_X.pickle", "rb")) 
    tank_train_y = pickle.load(open("aggregated/tank_train_y.pickle", "rb")) 
    tank_test_X = pickle.load(open("aggregated/tank_test_X.pickle", "rb")) 
    tank_test_y = pickle.load(open("aggregated/tank_test_y.pickle", "rb")) 

    damage_train_X = pickle.load(open("aggregated/damage_train_X.pickle", "rb")) 
    damage_train_y = pickle.load(open("aggregated/damage_train_y.pickle", "rb")) 
    damage_test_X = pickle.load(open("aggregated/damage_test_X.pickle", "rb")) 
    damage_test_y = pickle.load(open("aggregated/damage_test_y.pickle", "rb")) 

    support_train_X = pickle.load(open("aggregated/support_train_X.pickle", "rb")) 
    support_train_y = pickle.load(open("aggregated/support_train_y.pickle", "rb")) 
    support_test_X = pickle.load(open("aggregated/support_test_X.pickle", "rb")) 
    support_test_y = pickle.load(open("aggregated/support_test_y.pickle", "rb")) 
    
    data = {"tank": (tank_train_X, tank_train_y, tank_test_X, tank_test_y),
            "damage": (damage_train_X, damage_train_y, damage_test_X, damage_test_y),
            "support": (support_train_X, support_train_y, support_test_X, support_test_y)}

    for role in ROLES:
        rf_best_model, rf_mse = randomForest(*data[role])
        gb_best_model, gb_mse = gradientboosting(*data[role])
        knn_best_model, knn_mse = KNN(*data[role])

        result = [rf_best_model, rf_mse, gb_best_model, gb_mse, knn_best_model, knn_mse]
        print(f"\n###RESULT###\n{role}: {result}\n")
        with open(f"{role}_result.pickle", "wb") as handle:
            pickle.dump(result, handle)