import pickle
import json

def clustered_average_rating(business_id,user_cluster):
    user_to_cluster = pickle.load(open('../results/user_to_cluster.pkl','rb'))
    rating = 0
    count = 0
    for line in open('../data/filtered/review.json','rb'):
        review = json.loads(line)
        if review['business_id']==business_id and review['user_id'] in user_to_cluster and user_to_cluster[review['user_id']]==user_cluster :
            rating = rating + review['stars']
            count = count + 1
    return [None,None] if count==0 else [float(rating)/count,count];

restaurant_id = 'ABRgXNwdOX_JyqChNr8IYw'
print '{} restaurant'.format('Swatow')
print '-----------------'
for i in range(7):
    average,count = clustered_average_rating(restaurant_id,i)
    print 'Average rating for cluster {} : {} ({} reviews)'.format(i,average,count)
