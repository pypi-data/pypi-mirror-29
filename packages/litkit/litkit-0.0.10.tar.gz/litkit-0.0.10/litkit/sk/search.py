from sklearn.cross_decomposition import CCA, PLSCanonical, PLSRegression
from sklearn.feature_selection import VarianceThreshold, SelectKBest, SelectPercentile, GenericUnivariateSelect, SelectFromModel
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.linear_model import BayesianRidge, ARDRegression, ElasticNet, ElasticNetCV, HuberRegressor, Lars, LarsCV, Lasso, LassoCV, LassoLars, LassoLarsCV, LassoLarsIC, LinearRegression, MultiTaskElasticNet, MultiTaskElasticNetCV, MultiTaskLasso, MultiTaskLassoCV, OrthogonalMatchingPursuit, \
    OrthogonalMatchingPursuitCV, PassiveAggressiveRegressor, Ridge, RidgeCV, SGDRegressor, TheilSenRegressor
from sklearn.model_selection import *
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import LinearSVR, NuSVR, SVR
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor


def get_all_single_task_regressors():
    return [ARDRegression(), BayesianRidge(), CCA(), DecisionTreeRegressor(), ElasticNet(), ElasticNetCV(), ExtraTreeRegressor(), GaussianProcessRegressor(), HuberRegressor(), KNeighborsRegressor(), KernelRidge(), Lars(), LarsCV(), Lasso(), LassoCV(), LassoLars(),
            LassoLarsCV(), LassoLarsIC(), LinearRegression(), LinearSVR(), MLPRegressor(), NuSVR(), OrthogonalMatchingPursuit(), OrthogonalMatchingPursuitCV(), PLSCanonical(), PLSRegression(),
            PassiveAggressiveRegressor(), Ridge(), RidgeCV(), SGDRegressor(), SVR(), TheilSenRegressor()]


def get_kfolds():
    return [KFold(), StratifiedKFold(), RepeatedKFold(), RepeatedStratifiedKFold(), GroupKFold()]


def get_feature_selection():
    return [VarianceThreshold(), SelectKBest(), SelectPercentile(), SelectFromModel(estimator=None)]