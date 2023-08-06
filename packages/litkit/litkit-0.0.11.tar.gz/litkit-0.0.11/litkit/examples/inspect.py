from sklearn.linear_model import Lasso
from litkit.data import get_baseball_df
from litkit.inspect import info

m = Lasso()

df = get_baseball_df()

y = df['RS']
X = df[['RA', 'W', 'OBP', 'SLG']]

m.fit(X, y)

info(m)
