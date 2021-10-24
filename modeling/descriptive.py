import numpy as np
from modeling.load import load_descriptive
from pprint import pprint
from util.states import state_regions, abbreviations, region_abbv
from util.colors import bar_colors
from random import choice
import requests

data = load_descriptive()

dataT = {
	k: [p[k] for p in data] for k in data[0]
}

color_dist = {'d': {'d': bar_colors[0]}}

majors = []
for k in dataT['major']:
	majors.extend([i.strip() for i in k.split(',')])
dataT['major'] = majors

regions = []
for k in dataT['home']:
	try:
		ab = (k.split(',')[-1]).strip()
		if ab not in state_regions:
			ab = abbreviations[ab]
		state = state_regions[ab]
	except:
		state = 'I'

	regions.append(region_abbv[state])
dataT['region'] = regions

raw_dist = {}
for k in dataT:
	raw_dist[k] = {}
	for v in dataT[k]:
		if v not in raw_dist[k]:
			raw_dist[k][v] = 0
		raw_dist[k][v] += 1

for k in raw_dist:
	n = sum(list(raw_dist[k].values()))
	for v in raw_dist[k]:
		raw_dist[k][v] = (raw_dist[k][v] / n) * 100

def web_distribution(var, min_p = 2):
	
	d, dist = [], {}
	raw = raw_dist[var]
	other = raw['Other'] if 'Other' in raw else 0
	color_dist[var.upper()] = {}
	for k in raw:
		if k == 'Other': continue
		if raw[k] < min_p:
			other += raw[k]
		else:
			d.append((k, raw[k]))

	if other != 0: d.append(('Other', other))
	for n, (k, p) in enumerate(
		sorted(d, key=lambda x: x[1], reverse=True)
	):	
		color_dist[var.upper()][k] = bar_colors[n]
		dist[k] = {'percentage': '{:.2f}'.format(p), 'color': bar_colors[n], 'pf': p}
	return dist

default_vars = ['year', 'race', 'gender', 'major', 'phoneType', 'region', 'age', 'favoriteColor', 'role']

def load_web_distributions(vars = default_vars):
	dist = {}
	for var in vars:
		dist[var.upper()] = web_distribution(var)
	return dist

def create_member_attributes(member, vars, chance_ignore=['favoriteColor', 'age', 'role']):
	chance = 1
	for v in vars:
		
		c = choice(dataT[v])
		member[v.upper()] = c
		if v not in chance_ignore:
			chance *= raw_dist[v][c] / 100
	return member, chance * 100

def create_new_member(vars=default_vars[1:], thresh=.5):
	name = choice(dataT['name']).split(' ')[0] + ' ' + choice(dataT['name']).split(' ')[-1]

	#picture = requests.get('https://randomuser.me/api').json()['results'][0]['picture']['large']
	#picture = requests.get('https://randomfox.ca/floof/').json()['image']
	
	picture = requests.get('https://dog.ceo/api/breeds/image/random').json()['message']
	member = {
		'picture': picture,
		'name': name,
	}	

	chance = 0
	while (chance < thresh):
		member, chance = create_member_attributes(member, vars)
	return member, chance
	

if __name__ == '__main__':
	pprint(distribution('region'))
