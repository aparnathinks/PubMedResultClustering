from util import get_df, denotation_label, preprocess_text, get_label, DISEASE_IDS, group_error



from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

'''
============================================================================
Labeled set clustering 
using K-means++
without using the labels in the process of clustering
self generated label names from Mesh ids
the labels in training set used only for accuracy calculation
============================================================================
'''
print("\n#################   Labeled Set  #################\n\n")

#Create data frames for the data sets
set1_df= get_df('data/set1.json')
set2_df= get_df('data/set2.json')

X_set1=list()
Y_set1=list()
X_set2=list()
Y_set2=list()

# prune, lemmatize and prepare text
for i in range(len(set1_df)):
    denote=' '.join(set1_df.loc[i]['denotations'])
    string=' '.join(preprocess_text(set1_df.loc[i]['text']))
    X_set1.append(set1_df.iloc[i]['sourceid']+ string+' '+denote)


#Encode labels for cross verification
le=LabelEncoder()
Y_set1=le.fit_transform(get_label()[1])
label_set1=set1_df['sourceid']


#TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
hash_matrix=vectorizer.fit_transform(X_set1)


# CLUSTER
# Split data into 6 clusters because data analysis shows an elbow at 6 and we also know that there are 6 labels
kmeans = KMeans(n_clusters=6, init='k-means++', max_iter=1000).fit(hash_matrix)


# get Cluster labels.
clusters = kmeans.labels_

print("Generated diseases\n\n")
for group in set(clusters):
    gp_label=list()
    disease=list()

    for i in range(len(X_set1)):
        if (clusters[i] == group):
            disease+=set1_df['denotations'][i]
    temp=denotation_label([disease])
    print(DISEASE_IDS[temp[0]])
    gp_label.append(temp)

total_error=group_error(clusters,0,23,)+group_error(clusters,23,32)+group_error(clusters,32,48)+\
            group_error(clusters,48,80)+group_error(clusters,80,86)+group_error(clusters,86,103)
accuracy=((len(clusters)-total_error)/len(clusters))*100


'''
========================================
PRINTING RESULTS
Accuarcy > 90%
========================================
'''

#original labels
print("\n\nOriginal Labels\n")
print(Y_set1)

#clustered labels
print("\n\nCluster Labels\n")
print(clusters)

#accuracy
print("\n\nAccuarcy is: %s /%",accuracy)


'''
============================================================================
Unlabeled set clustering 
using K-means++
without using the labels in the process of clustering
============================================================================
'''


print("\n\n#################   Unlabeled Set  #################\n\n")

print("\n   GROUPS \n")

#Create data frames for the data set
set3_df= get_df('data/set3.json', ordered=False)

X_set3=list()
Y_set3=list()

# prune, lemmatize and prepare text
for i in range(len(set3_df)):
    denote=' '.join(set3_df.loc[i]['denotations'])
    string=' '.join(preprocess_text(set3_df.loc[i]['text']))
    X_set3.append(set3_df.iloc[i]['sourceid']+ string+' '+denote)



#TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
hash_matrix=vectorizer.fit_transform(X_set3)



# CLUSTER
# Split data into 6 clusters because data analysis shows an elbow at n=8 but
# "Marfan's Syndrome" falls into two groups
# on repeated trials for groups with distinct labels n=5 seems to work best

kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=1000).fit(hash_matrix)


# get Cluster labels.
clusters = kmeans.labels_

result=dict()
for group in set(clusters):
    gp_label=list()
    disease=list()
    temp_dict = dict()
    print("CLUSTER ", group+1, "\n")
    for i in range(len(X_set3)):
        if (clusters[i] == group):
            disease+=set3_df['denotations'][i]
            temp_dict[set3_df['sourceid'][i]]=""
            print(set3_df['sourceid'][i])
    temp=denotation_label([disease])
    if DISEASE_IDS[temp[0]]:
        for a in temp_dict: temp_dict[a]=DISEASE_IDS[temp[0]]
        result.update(temp_dict)
        print('\n',DISEASE_IDS[temp[0]],'\n\n')
    else:
        for a in temp_dict: temp_dict[a] =temp
        result.update(temp_dict)
        print(temp,'\n\n')
    gp_label.append(temp)
print(result)
print(len(result))

with open('result.txt', 'w') as opfile:
    for k,v in result.items():
        string=k + '\t' + v + '\n'
        opfile.write(string)




