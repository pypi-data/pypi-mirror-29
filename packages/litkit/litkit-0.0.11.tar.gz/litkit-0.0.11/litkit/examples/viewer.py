from beeprint import pp
from sklearn.linear_model import Lasso, LinearRegression, ElasticNet, Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import pandas as pd

from litkit.dash.viewer import view
from litkit.data import get_baseball_df
from litkit.inspect import info


p = Pipeline([
    ('estimator', Lasso())
])

pg = [
    {'estimator': [Lasso(), LinearRegression(), ElasticNet(), Ridge()]}
]

gs = GridSearchCV(estimator=p, param_grid=pg, n_jobs=1, return_train_score=True)

df = get_baseball_df()

y = df['RS']
X = df[['RA', 'W', 'OBP', 'SLG']]

gs.fit(X, y)

r_df = pd.DataFrame(gs.cv_results_)

del r_df['params']
r_df['param_estimator'] = r_df['param_estimator'].apply(lambda x: x.__class__.__name__)

view(r_df)

pp(p.named_steps["estimator"])

