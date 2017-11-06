import pip
pip.main(['install','flatdict'])

from sklearn.feature_extraction import DictVectorizer
import json
import flatdict
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pylab as pl
import pickle

index_to_id = {}
array_dictionary_features = []
count = 0
for line in open('../data/filtered/business.json','rb'):
    business = json.loads(line)
    index_to_id[count]=business['business_id']
    count = count+1
    dictionary_features = {}
    for element in business['categories']:
        dictionary_features[element]=True
    flat_attributes = flatdict.FlatDict(business['attributes'])
    dictionary_features.update(flat_attributes)
    array_dictionary_features.append(dictionary_features)

print "--DICTIONARY BUILT--"
vectorizer = DictVectorizer()
restaurant_features_matrix = vectorizer.fit_transform(array_dictionary_features)
print "Number of restaurants : {}".format(restaurant_features_matrix.shape[0])
print "Number of features : {}".format(restaurant_features_matrix.shape[1])

kmeans = KMeans(n_clusters = 13, random_state=0, n_init=100).fit(restaurant_features_matrix)
print "--KMEANS FINISHED--"

#We use PCA to visualize the result
pca = PCA(n_components=2,random_state=0).fit_transform(restaurant_features_matrix.todense())
print "--PCA FINISHED--"
business_to_category={}
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
for i in range(0, pca.shape[0]):
    pred = kmeans.predict(restaurant_features_matrix[i])[0]
    business_to_category[index_to_id[i]]=pred
    color.append(category_to_color[pred])    
pl.scatter(pca[:,0],pca[:,1],c=color,marker='o',alpha=0.1)

pl.savefig('../results/restaurants_clustering.png')

print "--SAVING THE BUSINESS' CATEGORIES IN DICT--"
pickle.dump(business_to_category,open('../results/business_to_category.pkl','wb'))

pl.show()



