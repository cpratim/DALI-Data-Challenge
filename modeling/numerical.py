from modeling.load import load_numerical
import numpy as np
from scipy.stats import mode
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def correlation(x, y):
	return np.corrcoef(x, y)[0, 1]

test_size = .2
X, features = load_numerical()

datasets = {}

p = X.T
for n, f in enumerate(features):
	y = p[n]
	p = np.delete(p, n, axis=0)
	XTr, XTe, yTr, yTe = train_test_split(p.T, y, test_size=test_size)
	datasets[f] = {
		'X_train': XTr, 
		'X_test': XTe,
		'y_train': yTr,
		'y_test': yTe,
	}
	p = X.T
	
for f in datasets:
	m = datasets[f]
	reg = RandomForestRegressor(n_jobs=-1)
	
	reg.fit(m['X_train'], m['y_train'])

	pred = reg.predict(m['X_test'])
	y_test =  m['y_test']
	
	print(f'{f} | Correlation: {round(correlation(pred, y_test), 3)}')
