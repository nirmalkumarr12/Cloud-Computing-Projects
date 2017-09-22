from sklearn import datasets
from sklearn.cluster import KMeans
import sklearn.metrics as sm
import pandas as pd
import numpy as np

index_cont='''
<form method='POST' action='/kmean_cent'>
<input type='text' name='clusters'/>
<input type='submit' value='Print Centroid'/>
</form><br>
<form method='POST' action='/kmean_model'>
<input type='text' name='clusters'/>
<input type='submit' value='Print Model'/>
</form>

'''





@app.route('/')
def index():
	return index_cont

@app.route('/kmean_cent',methods=['POST'])
def kmean_perform():
	iris=datasets.load_iris()
	df_x=pd.DataFrame(iris.data)
	df_x.columns=['sepal-length','sepal-width','petal-length','petal-width']
	df_y=pd.DataFrame(iris.target)
	df_y.columns=['targets']

	model=KMeans(n_clusters=3)

	model.fit(df_x)
	centroids,_ = kmeans(df_x,2)
	return "Centroid : {0}".format(centroids

@app.route('/kmean_model',methods=['POST'])
def kmean_perform_model():
	iris=datasets.load_iris()
	df_x=pd.DataFrame(iris.data)
	df_x.columns=['sepal-length','sepal-width','petal-length','petal-width']
	df_y=pd.DataFrame(iris.target)
	df_y.columns=['targets']

	model=KMeans(n_clusters=3)

	model.fit(df_x)

	return model