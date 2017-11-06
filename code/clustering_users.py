import pickle
from sklearn.feature_extraction import DictVectorizer
import json
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pylab as pl

business_to_category = pickle.load(open('../results/business_to_category.pkl','rb'))

index_to_id={}
dictionary_users = {}
count = 0
for line in open('../data/filtered/review.json','rb'):
    review = json.loads(line)
    index_to_id[count]=review['user_id']
    count = count+1
    if not review['user_id'] in dictionary_users:
        dictionary_users[review['user_id']] = {}
    cluster = business_to_category[review['business_id']]
    if not cluster in dictionary_users[review['user_id']]:
        dictionary_users[review['user_id']][cluster]= []
    dictionary_users[review['user_id']][cluster].append(float(review['stars']))

array_dictionary_users = []
for _,user in dictionary_users.iteritems():
    dictionary_features = {}
    for cluster,ratings in user.iteritems():
        dictionary_features[cluster]=sum(ratings)/len(ratings)
    array_dictionary_users.append(dictionary_features)

vectorizer = DictVectorizer()
user_ratings_matrix = vectorizer.fit_transform(array_dictionary_users)
print "--USERS VECTORIZED--"
print "Number of users : {}".format(user_ratings_matrix.shape[0])
print "Number of type of restaurants : {}".format(user_ratings_matrix.shape[1])

kmeans = KMeans(n_clusters = 6, random_state=0, n_init=100).fit(user_ratings_matrix)
print "--KMEANS FINISHED--"

#We use PCA to visualize the result
pca = PCA(n_components=2,random_state=0).fit_transform(user_ratings_matrix.todense())
print "--PCA FINISHED--"
user_to_category={}
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
    pred = kmeans.predict(user_ratings_matrix[i])[0]
    user_to_category[index_to_id[i]]=pred
    color.append(category_to_color[pred])    
pl.scatter(pca[:,0],pca[:,1],c=color,marker='o',alpha=0.1)

pl.savefig('../results/users_clustering.png')

print "--SAVING THE USERS' CATEGORIES IN DICT--"
pickle.dump(user_to_category,open('../results/user_to_category.pkl','wb'))

pl.show()

