Hello, before get to use the code need to know several conditions

1. change the path of file :

   import os
for dirname, _, filenames in os.walk('C:/Folder Arya/Study/BAU Doc/Fall SMT/Artificial İntelligence/Term Project'): 
    for filename in filenames:
        print(os.path.join(dirname, filename))

   #Reading the dataset from path files
data = 'C:/Folder Arya/Study/BAU Doc/Fall SMT/Artificial İntelligence/Term Project/adult.csv'
df = pd.read_csv(data, header=None, sep=',\s')

change into specific location of data set that has been obtained. then it can run well 


the dataset links : https://www.kaggle.com/datasets/garymk/movielens-25m-dataset
