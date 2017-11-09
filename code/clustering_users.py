import pickle
from sklearn.feature_extraction import DictVectorizer
import json
from sklearn.cluster import AgglomerativeClustering
import pylab as plt
from sklearn.manifold import TSNE
import os

def filtered_users(threshold):
    if not os.path.exists(os.path.join('..','results','user_to_number_reviews.pkl')):
        user_to_number_reviews = {}
        for line in open(os.path.join('..','data','filtered','review.json'),'rb'):
            review = json.loads(line)
            if not review['user_id'] in user_to_number_reviews:
                user_to_number_reviews[review['user_id']]=1
            else:
                user_to_number_reviews[review['user_id']] = user_to_number_reviews[review['user_id']]+1
        pickle.dump(user_to_number_reviews,open('../results/user_to_number_reviews.pkl','wb'))
    else:
        user_to_number_reviews = pickle.load(open(os.path.join('..','results','user_to_number_reviews.pkl'),'rb'))
    return [key for key,value in user_to_number_reviews.iteritems() if value>=threshold]

restaurant_to_cluster = pickle.load(open(os.path.join('..','results','restaurant_to_cluster.pkl'),'rb'))
id_user = []
filtered_users_array = filtered_users(20);
pickle.dump(filtered_users_array,open(os.path.join('..','results','filtered_users.pkl'),'wb'))

dictionary_users = {}
for line in open(os.path.join('..','data','filtered','review.json'),'rb'):
    review = json.loads(line)
    if review['user_id'] in filtered_users_array:
        if not review['user_id'] in dictionary_users:
            dictionary_users[review['user_id']] = {}
        cluster = restaurant_to_cluster[review['business_id']]
        if not cluster in dictionary_users[review['user_id']]:
            dictionary_users[review['user_id']][cluster]= []
        dictionary_users[review['user_id']][cluster].append(float(review['stars']))

array_dictionary_users = []
for user_id,user in dictionary_users.items():
    dictionary_features = {}
    for cluster,ratings in user.iteritems():
        dictionary_features[cluster]=sum(ratings)/len(ratings)
    array_dictionary_users.append(dictionary_features)
    id_user.append(user_id)

vectorizer = DictVectorizer()
user_ratings_matrix = vectorizer.fit_transform(array_dictionary_users)
print "--USERS VECTORIZED--"
print "Number of users : {}".format(user_ratings_matrix.shape[0])
print "Number of type of restaurants : {}".format(user_ratings_matrix.shape[1])
print user_ratings_matrix.todense()[0:10,:]

aggclus = AgglomerativeClustering(n_clusters = 7).fit_predict(user_ratings_matrix.todense())
print "--AGGLOMERATIVE CLUSTERING FINISHED--"
#We use TSNE to visualize the result
tsne = TSNE(n_components=2,random_state=0).fit_transform(user_ratings_matrix.todense())
print "--TSNE FINISHED--"
user_to_cluster={}
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
    user_to_cluster[id_user[i]]=pred
    color.append(category_to_color[pred])
plt.scatter(tsne[:,0],tsne[:,1],c=color,marker='o',alpha=0.1)

plt.savefig('../results/users_clustering_agglomerative_clustering.png')

print "--SAVING THE USERS' CATEGORIES IN DICT--"
pickle.dump(user_to_cluster,open('../results/user_to_cluster.pkl','wb'))

plt.show()

