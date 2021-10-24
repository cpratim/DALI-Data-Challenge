from flask import (
	Flask,
	render_template, 
	url_for,
	request
)
from util.helpers import split_list
from modeling.descriptive import *
from modeling.numerical import *
import os
from util.helpers import split_list
from pprint import pprint

app = Flask(__name__)


@app.route('/')
def index():
	files = os.listdir('web/static/images')
	pics = split_list(list(enumerate(files[:64])), 8)
	return render_template('index.html', pics = pics)

@app.route('/get_demographics')
def json_demographics():
	return load_distributions()

@app.route('/demographics')
def demographics():
	distributions = load_web_distributions()
	member, chance = create_new_member()
	return render_template(
		'demographics.html', 
		distributions=distributions, 
		member=member, 
		colormap=color_dist, 
		chance= '{:.3f}'.format(chance),
	)

@app.route('/modeling', methods=['GET', 'POST'])
def modeling():
	pred = 0
	if request.method == 'POST':
		form = request.form
		feature = form['feature']
		x = {}
		for k in form:
			if k != 'feature':
				x[k] = form[k]
		pred = round(predict(feature, x)[0])
		
	features = load_features()
	ranges = load_feature_ranges()
	return render_template('modeling.html', features=features, ranges=ranges, pred=pred)
