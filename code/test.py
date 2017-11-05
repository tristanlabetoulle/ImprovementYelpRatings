from sklearn.feature_extraction import DictVectorizer
import json
import flatdict

a = {0:"bouffon",1:"oui"}
b = {2:"ett",3:"aaa"}
print a
a.update(b)
print a

measurements = [
    {'city': 'Dubai', 'temperature': 33.,'allah':'tttre'},
    {'city': 'London', 'temperature': 12., 'allah':'whhh'},
    {'city': 'San Fransisco', 'temperature': 18.,'allah':'tttre'}]

from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()

print vec.fit_transform(measurements).toarray()

print vec.get_feature_names()

array_dictionary_features = []
with open('../data/filtered/business.json','rb') as infile:
    for line in infile:
        data = json.loads(line)
        flat_attributes = flatdict.FlatDict(data['attributes'])
        for key,value in flat_attributes.iteritems():
            if type(value)==bool:
                    pass
            else:
                print "ERROR {} {}".format(key,value)

