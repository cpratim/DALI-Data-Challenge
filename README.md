# Website for DALI Data Challenge

## Challenge:

(https://github.com/dali-lab/dali-challenges/blob/master/docs/DataChallenge.md)

## Temporary Website:

(https://dali-data-challenge.herokuapp.com/)


## Backend:

## Webserver

The webserver was coded using the Flask framework for backend programming
allowing access to python code spanning many files and libraries and the easy
display of that information on the front end. 

All the graphs and visuals located on the /demographics page were made from 
scratch using a combination of Flask dynamic element loading and HTML + CSS. 
All loaded in realtime from the original JSON files and could work with any
data as long as it follows the same structure. 

## Machine Learning Engine

The machine learning processing was done using PyTorch (https://pytorch.org/). 
The network for predictions was a 1D convolutional neural network trained to 
maximize the correlation between n-1 features and the feature you wanted to predict. 
This was then repeated for every single feature in the dataset, using every other
feature besides that in the training set, and the target feature in the y set. 
For high value prediction such as the Height or Year it was scaled down, but other
than that the correlations were high for every other output. 

Feature | Year | Gender | Height | Happiness | Stressed | Speep | Social Dinners | Alcohol Drinks | Caffeine Rating | Affiliated | Num Languages | Gym | Screen Hours | Phone Type |
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |---
Correlation | .200 | 0.857 | .513 | .324 | .230 | .185 | .0714 | .286 | .786 | .435 | .482 | .646 | .418 |

