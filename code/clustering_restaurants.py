from sklearn.feature_extraction import DictVectorizer
import json
import flatdict
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
import pylab as pl

array_dictionary_features = []
for line in open('../data/filtered/business.json','rb'):
    business = json.loads(line)
    dictionary_features = {}
    for element in business['categories']:
        dictionary_features[element]=True
    flat_attributes = flatdict.FlatDict(business['attributes'])
    dictionary_features.update(flat_attributes)
    array_dictionary_features.append(dictionary_features)

print "--DICTIONARY BUILT--"
vectorizer = DictVectorizer()
restaurant_features_matrix = vectorizer.fit_transform(array_dictionary_features)

kmeans = KMeans(n_clusters = 3, random_state=0).fit(restaurant_features_matrix)
print "--KMEANS FINISHED--"
#We use PCA to visualize the result

pca = TruncatedSVD(n_components=2).fit_transform(restaurant_features_matrix)
print "--PCA FINISHED--"
for i in range(0, pca.shape[0]):
    pred = kmeans.predict(restaurant_features_matrix[i])[0]
    if pred == 0:
        c1 = pl.scatter(pca[i,0],pca[i,1],c='r',marker='o')
    elif pred == 1:
        c2 = pl.scatter(pca[i,0],pca[i,1],c='g',marker='o')
    elif pred == 2:
        c3 = pl.scatter(pca[i,0],pca[i,1],c='b',marker='o')

pl.show()
