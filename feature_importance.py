import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

from parse_player_stats import ROLES

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
    
    tank_rf = RandomForestRegressor(bootstrap=False, ccp_alpha=0.0, criterion='mse', max_depth=33, max_features='sqrt', max_leaf_nodes=None, max_samples=None, 
                                   min_impurity_decrease=0.0, min_impurity_split=None, min_samples_leaf=1, min_samples_split=5, min_weight_fraction_leaf=0.0, 
                                   n_estimators=1419, n_jobs=None, oob_score=False, random_state=69, verbose=0, warm_start=False)
    print("Fitting...")
    tank_rf.fit(tank_train_X, tank_train_y)
    print("Calculating...")
    tank_result = permutation_importance(tank_rf, tank_test_X, tank_test_y, random_state=69)
    tank_idx = tank_result.importances_mean.argsort()
    print("Plotting...")
    fig, ax = plt.subplots()
    fig.tight_layout()
    ax.boxplot(tank_result.importances[tank_idx].T, vert=False, labels=tank_test_X.columns[tank_idx])
    ax.set_title("[TANK] Permutation Feature Importances (on Test Set)")

    damage_gb = GradientBoostingRegressor(alpha=0.9, ccp_alpha=0.0, criterion='friedman_mse', init=None, learning_rate=0.01, loss='ls', max_depth=41, max_features='sqrt', max_leaf_nodes=None, 
                                          min_impurity_decrease=0.0, min_impurity_split=None, min_samples_leaf=4, min_samples_split=10, min_weight_fraction_leaf=0.0,
                                          n_estimators=1449, n_iter_no_change=None, random_state=69, subsample=1.0, tol=0.0001, validation_fraction=0.1, verbose=0, warm_start=False)
    print("Fitting...")
    damage_gb.fit(damage_train_X, damage_train_y)
    print("Calculating...")
    damage_result = permutation_importance(damage_gb, damage_test_X, damage_test_y, random_state=69)
    damage_idx = damage_result.importances_mean.argsort()
    print("Plotting...")
    fig2, ax2 = plt.subplots()
    fig2.tight_layout()
    ax2.boxplot(damage_result.importances[damage_idx].T, vert=False, labels=damage_test_X.columns[damage_idx])
    ax2.set_title("[DAMAGE] Permutation Feature Importances (on Test Set)")

    support_gb = GradientBoostingRegressor(alpha=0.9, ccp_alpha=0.0, criterion='friedman_mse', init=None, learning_rate=0.01, loss='ls', max_depth=17, max_features='sqrt', max_leaf_nodes=None, 
                                           min_impurity_decrease=0.0, min_impurity_split=None, min_samples_leaf=1, min_samples_split=10, min_weight_fraction_leaf=0.0,
                                           n_estimators=742, n_iter_no_change=None, random_state=69, subsample=1.0, tol=0.0001, validation_fraction=0.1, verbose=0, warm_start=False)
    print("Fitting...")
    support_gb.fit(support_train_X, support_train_y)
    print("Calculating...")
    support_result = permutation_importance(support_gb, support_test_X, support_test_y, random_state=69)
    support_idx = support_result.importances_mean.argsort()
    print("Plotting...")
    fig3, ax3 = plt.subplots()
    fig3.tight_layout()
    ax3.boxplot(support_result.importances[support_idx].T, vert=False, labels=support_test_X.columns[support_idx])
    ax3.set_title("[SUPPORT] Permutation Feature Importances (on Test Set)")

    plt.show(block=True)


