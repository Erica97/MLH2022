'''
python3 main.py INTEGRATED-DATASET.csv <minSupport> <minConfidence>
'''
import os
import pathlib

from flask import Flask, request, render_template
import sys
import itertools
import csv
from io import StringIO

app = Flask(__name__, template_folder='templates')
PARENT_PATH = str(pathlib.Path(__file__).parent.resolve())
UPLOAD_FOLDER = PARENT_PATH + '\static'

# Upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Apriori algorithm from paper section 2.1
def Apriori(allRows, allItems, minSupp, minConf):
    # setCount stores the frequency for each given row
    set_count = {}
    large_by_row = {}
    large_sets_per_iter = {}
    k = 1
    # first iteration when k=1
    current_large = generate_can(allRows, allItems, minSupp, set_count)
    # row_id is row ID in the csv file
    row_id = 0
    num_items = 0

    for row in allRows:
        ordered_can = []
        num_items = len(row)
        row_id += 1

        for item in row:
            for candidate in current_large:
                if item in candidate:
                    ordered_can.append(item)
                large_by_row[row_id] = ordered_can

    while (k <= num_items):
        subsets = []
        for key, value in large_by_row.items():
            # use itertools to get all possible combinations of subsets of size k
            for subset in itertools.combinations(value, k):
                subsets.append(tuple(subset))

        # pruning is done in candidate generation step
        current_large = generate_can(allRows, subsets, minSupp, set_count)
        # key: current iteration k; values: all sets of size k
        large_sets_per_iter[k] = current_large
        k += 1

    # get item-support list across all iterations
    item_support = []
    # rule-support-confidence
    rules = []
    for key, sets in large_sets_per_iter.items():
        for s in sets:
            item_support.append((list(s), float(set_count[s]) / len(allRows)))
            LHS = s[0]
            RHS = list(s[1:])
            support = float(set_count[s]) / len(allRows)
            confidence = float(set_count[s]) / float(set_count[LHS])

            if confidence >= minConf and RHS:  # Right hand side not empty
                rules.append(((LHS, RHS), confidence, support))

    return item_support, rules


# This function generates candidate items that are above minSupp threshold and returns in a list form
def generate_can(allRows, allItems, minSupp, set_count):
    new_can = []
    # item frequency dict for current iteration
    current = {}
    # remove duplicates
    unique_items = list(set(allItems))
    for item in unique_items:
        for row in allRows:
            if (item in row) or all(i in row for i in item):  # if the row list contains all element in item list
                # if we encountered item in current iteration
                if item in current.keys():
                    current[item] += 1
                else:
                    current[item] = 1

                if item in set_count.keys():
                    set_count[item] += 1
                else:
                    set_count[item] = 1
    # Add candidates with support >= minSupp to the new_can
    for item, count in current.items():
        supp = float(count) / len(allRows)
        if supp >= minSupp:
            new_can.append(item)
    return new_can

def readCSV(csvfile):
    csvreader = open(csvfile, encoding='utf-8')
    for line in csvreader:
        row = list(line.strip().rstrip(',').split(','))
        yield row

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['myFile']
        file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        # Read in file and get a generator using itertools
        data = readCSV(file_path)
            
        minSupp = float(request.form.get('minSupport'))
        minConf = float(request.form.get('minConf'))

        allRows = []
        allItems = []
        for row in data:
            # allRows is a list of lists for rows in csv file
            allRows.append(row)
            for item in row:
                allItems.append(item)

        items, rules = Apriori(allRows, allItems, minSupp, minConf)
        # output results

        add1 = "\n==Frequent itemsets (min_sup = %.2f%%" % (minSupp * 100) + ")"
        temp = list()
        temp.append(add1)
        for item, supp in sorted(items, key=lambda x: x[1], reverse=True):
            temp.append("\n%s , %.2f%%" % (str(item), supp * 100))

        add2 = "\n==High-confidence association rules (min_conf = %.2f%%" % (minConf * 100) + ")"

        temp2 = list()
        temp2.append(add2)
        for rule, confidence, support in sorted(rules, key=lambda x: x[1], reverse=True):
            LHS, RHS = str([rule[0]]), str(rule[1])
            temp2.append(
                "\n%s ==> %s" % (LHS, RHS) + " (Conf: %.2f%% " % (confidence * 100) + ", Supp: %.2f%%)" % (support * 100))

        return render_template('index.html', tem=temp, tem2=temp2)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
