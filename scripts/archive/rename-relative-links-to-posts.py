'''
rename-relative-links-to-posts.py

This script renames relative links in posts to point to new, canonical post names.
'''
import os 

filenames = [
    'posts/8020-pandas-tutorial/post.ipynb',
    'posts/hello-pyspark/hello-pyspark.ipynb',
    'posts/get-down-with-gradient-descent/get-down.ipynb',
    'posts/how-to-understand-xgboost/how-to-understand-xgboost.ipynb',
    'posts/drafts/conda-cheat-sheet/post.ipynb',
    'posts/gradient-boosting-machine-with-any-loss-function/gbm-any-loss.ipynb',
    'posts/xgboost-from-scratch/xgboost-from-scratch.ipynb',
    'posts/consider-the-decision-tree/consider-the-decision-tree.ipynb',
    'posts/decision-tree-from-scratch/decision-tree-from-scratch.ipynb',
    'posts/how-gradient-boosting-does-gradient-descent/post.ipynb',
    'posts/gradient-boosting-machine-from-scratch/gradient-boosting-machine-from-scratch.ipynb'
]
substitutions = [
            ['(/hello-world)', '(/posts/hello-world/)'],
    ['(/8020-pandas-tutorial)', '(/posts/8020-pandas-tutorial/)'],
    ['(/gradient-boosting-machine-from-scratch)', '(/posts/gradient-boosting-machine-from-scratch/)'],
    ['(/get-down-with-gradient-descent)', '(/posts/get-down-with-gradient-descent/)'],
    ['(/how-gradient-boosting-does-gradient-descent)', '(/posts/how-gradient-boosting-does-gradient-descent/)'],
    ['(/hello-pyspark)', '(/posts/hello-pyspark/)'],
    ['(/gradient-boosting-machine-with-any-loss-function)', '(/posts/gradient-boosting-machine-with-any-loss-function/)'],
    ['(/consider-the-decision-tree)', '(/posts/consider-the-decision-tree/)'],
    ['(/decision-tree-from-scratch)', '(/posts/decision-tree-from-scratch/)'],
    ['(/how-to-understand-xgboost)', '(/posts/how-to-understand-xgboost/)'],
    ['(/xgboost-from-scratch)', '(/posts/xgboost-from-scratch/)']
]


# filenames = [
#     'scripts/sample.txt'
# ]
# substitutions = [
#     ['/my-cool-post', '/posts/my-cool-post/']
# ]

for filename in filenames:

    path = filename
    with open(path, 'r') as file :
      filedata = file.read()

    for substitution in substitutions:
       filedata = filedata.replace(substitution[0], substitution[1])
    
    with open(path, 'w') as file:
        file.write(filedata)