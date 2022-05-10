# Association Rules Extrator (Data Mining Flask Web App)

This is the sample code prepared by Jiawen Li for the MLH summer 2022 fellowship program.


## Motivation: Apriori algorithm for association rule learning problems

Association Rule Learning is a data mining technique which allows us to get interesting insights of relationship among the items. If I have to define it in one line I can simply say,

Association Rule Learning is simply about finding association between two different things. For example, People who bought Bread also bought Butter or, People who watched 3 Idiots also watched Chhichhore etc.

Apriori Algorithm is one of the algorithm used for transaction data in Association Rule Learning. It allows us to mine the frequent itemset in order to generate association rule between them.
Example: list of items purchased by customers, details of website which are frequently visited etc.

This algorithm was introduced by Agrawal and Srikant in 1994.

## Tech stack

Programming languages: Python, JavaScript, HTML, CSS

Framework: Flask

Deployed on: Heroku

## Demo & How to use

```Working demo link```: https://mlh2022.herokuapp.com/ 


To use this web app, upload your preprocessed .csv file, and input 2 parameters, both in [0, 1]: ```<minSupport>```, ```<minConfidence>```.


### Parameter Definitions

```<minSupport>``` : Minimum support, where 

Support(I)= (Number of transactions containing item I) / (Total number of transactions)

```<minConfidence>```: Minimum confidence, where 

Confidence(I1 -> I2) = (Number of transactions containing items I1 and I2) / (Number of transactions containing item I1)


### Dependencies

gunicorn

bidict

click

colorama

Flask

itsdangerous

Jinja2

MarkupSafe

python-engineio

python-socketio

Werkzeug


## Data source for the test .csv file

Link to dataset: https://data.cityofnewyork.us/Business/NYCgov-Poverty-Measure-Data-2014-/aqqw-n6ec

The dataset is the  NYC Open Data NYCgov 2014 Poverty Measure Data File. This file contains poverty rates and related data from theNYCgov poverty measure data. For the purpose of this project we chose to focus on the following categories: Borough, Citizen Status, Education Level, Ethnicity, and Poverty Status.

Extractions from this poverty dataset are compelling and meaningful. Using this data, we can see the various relationships between boroughs, ethnicity, citizenship, education, and poverty level. This may help to see the discrepancies in all these factors and poverty levels. This includes trends in level of education and ethnicity, levels of education and poverty, citizenship status and poverty, and borough and poverty levels. Given the current politics in NYC, extracting and understanding these relationships is extremely important and relevant to see discrepencies and how we need to better support marginalized groups in NYC.


## Apriori Algorithm Implementation
The set of functions in `main.py` include Apriori, generate_can, output and main. The apriori algorithm is based on the pseudocode provided in the paper section 2.1. 

In the ```index``` function, we read in the data in the csv file to mine, as well as the values for minimum support and minimum confidence threshold. Each row in the csv file is represented as a list, and the ```allRows``` variable is a list of lists storing all rows. The list ```allItems``` is a list where each item in the list is an item from each row, making this a list of every market basket item that appears. We pass both lists to the ```Apriori``` function, along with the minimum support and minimum confidence level parameters.

In the ```Apriori``` function, we first create the ```current_large``` using the ```generate_can``` function. This function takes in ```allRows``` and ```allItems``` lists, and returns a list of frequent items: ```current_large```. It iterates through each item in the ```allItems``` list, and if the item exists in a row, we increases its frequency(count) by 1, thus we can calculate its support. If its support > ```minSupp```, the item will be a candidate.

In order to generate all possible combinations of subsets, we use a dictionary ```large_by_row``` to store all subsets of items in a given row which have at least ```minSupp```, and the key is the row number (```row_id```). The candidate subsets are therefore sorted by the row number, and we can use Itertools to generate subset permutations to avoid duplicate association rules. Next we calls to the ```generate_can``` function to get ```current_large``` which stores all large sets of size k (k=current number of iterations), and we store ```current_large``` in a dictionary ```large_sets_per_iter``` with key being k.

To get the list of frequent items, we iterate through each item in ```large_sets_per_iter``` and calculate its support by dividing its counts(stored in ```set_count```) by the total number of rows/transactions. Comparison with ```minSupp``` is done before so we do need to evaluate against it again. The (item, support) pairs are stored in the list ```item_support```.
Meanwhile, to get the list of rules, we pop the first item in each sets as the "left hand side" of a rule, and the remaining items as the "right hand side"; we then compute the confidence of the given rule by dividing the support of the entire item by the support of the LHS. The rules above ```minConf``` are stored in the list ```rules```.

Pruning is done in the ```generate_can``` function. It generates candidate items(subsets) that are above ```minSupp``` threshold and returns a list a new candidates. This is also where ```set_count``` is updated to record all potential candidate subsets and their counts(frequency) in the entire dataset.


## Compelling sample run


Details of the run is in ```example-run.txt```. The frequent items revealed some interesting facts about the population in NYC. The most frequent items depict the portray of the most common NYC citizens: not in poverty, white, citizen by birth, 18 to 64 years old who live in Brooklyn or Queens; have bachelors degree or higher.

The association rules illustrate how education level is related to poverty. 'Bachelors Degree or Higher' > 'Some College' > 'High School Degree' in terms of the confidence scores for their association with 'Not in Poverty'; this implies that the more education one gets, the more likely he/she will be rich. It also shows that 'Queens' and 'Manhattan' associates with 'Not in Poverty' stronger compared to 'Brooklyn'. This finding aligns with our intuition since those two boroughs are more expensive to live in compared to Brooklyn.
