import pip
pip.main(['install','flatdict'])

from sklearn.feature_extraction import DictVectorizer
import json
import flatdict
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import pylab as plt
import pickle
from sklearn.cluster import AgglomerativeClustering
import os

index_to_id = {}
array_dictionary_features = []
for count,line in enumerate(open(os.path.join('..','data','filtered','restaurant.json'),'rb')):
    restaurant = json.loads(line)
    index_to_id[count]=restaurant['business_id']
    dictionary_features = {}
    for element in restaurant['categories']:
        dictionary_features[element]=True
    flat_attributes = flatdict.FlatDict(restaurant['attributes'])
    dictionary_features.update(flat_attributes)
    array_dictionary_features.append(dictionary_features)

print "--DICTIONARY BUILT--"
vectorizer = DictVectorizer()
restaurant_features_matrix = vectorizer.fit_transform(array_dictionary_features)

restaurant_features_matrix = PCA(n_components=20).fit_transform(restaurant_features_matrix.todense())
print "--DIMENSIONS REDUCED TO 20 USING PCA--"
print "Number of restaurants : {}".format(restaurant_features_matrix.shape[0])
print "Number of features : {}".format(restaurant_features_matrix.shape[1])

aggclus = AgglomerativeClustering(n_clusters=10).fit_predict(restaurant_features_matrix)
print "--AGGLOMERATIVE CLUSTERING FINISHED--"

#We use TSNE to visualize the result
tsne = TSNE(n_components=2,random_state=0).fit_transform(restaurant_features_matrix)
print "--TSNE FINISHED--"
restaurant_to_cluster={}
category_to_color = {
    0:'b',
    1:'g',
    2:'r',
    3:'c',
    4:'m',
    5:'y',
    6:'k',
    7:'w',
    8:'xkcd:brown',
    9:'xkcd:pink',
    10:'xkcd:silver',
    11:'xkcd:orange',
    12:'xkcd:wheat'
}
color = []
for i in range(0, tsne.shape[0]):
    pred = aggclus[i]
    restaurant_to_cluster[index_to_id[i]]=pred
    color.append(category_to_color[pred%13])    
plt.scatter(tsne[:,0],tsne[:,1],c=color,marker='o',alpha=0.1)

plt.savefig(os.path.join('..','results','restaurants_clustering_agglomerative_clustering.png'))

print "--SAVING THE RESTAURANTS' CATEGORIES IN DICT--"
pickle.dump(restaurant_to_cluster,open(os.path.join('..','results','restaurant_to_cluster.pkl'),'wb'))

plt.show()
