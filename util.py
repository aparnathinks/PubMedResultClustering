
import pandas as pd
import numpy as np
import json
from numpy import array

from nltk import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

import re
from nltk import bigrams
from nltk import pos_tag


DISEASE_IDS={
    'Disease:D010013':"Osteogenesis imperfecta",
    'Disease:D003550':"Cystic fibrosis",
    'Disease:D001943':"Breast Cancer",
    'Disease:D017253':'Neurofibromatosis',
    'Disease:D020788':"Bardet-Biedl syndrome",
    'Disease:D009133':"muscular atrophy",
    'Disease:C538231':"lung adenocarcinoma",
    'Disease:D008382':"Marfan's Syndrome",
    'Disease:D014424':"Turner syndrome",
    'Disease:D009634':"Noonan syndrome",
    'Disease:D003123':"Hereditary nonpolyposis colorectal cancer",
    'Disease:D003635':"Cornelia de Lange syndrome",
    'Disease:D010146':"pain",
    'Disease:D015179': "hereditary colorectal cancer"
}
# getting the most frequent denotation label from a list of denotations

def denotation_label(denotations):
    diseases = list()
    for rec in denotations:
        # print(rec)
        count_obj = dict()
        if rec:
            for item in rec:
                if item.find('Species')==-1:
                    if item in count_obj:
                        count_obj[item] += 1
                    else:
                        count_obj[item] = 1
            diseases.append(max(count_obj, key=lambda key: count_obj[key]))
        else:
            diseases.append("")
    return diseases

def get_label(file_name="data/pmids_gold_set_labeled.txt"):

    df = pd.read_csv(file_name, sep='\s+', header=None)
    df1 = df.replace(np.nan, '', regex=True)

    pmids_gold_labeled = pd.DataFrame()
    pmids_gold_labeled[0] = df1[0]

    pmids_gold_labeled[1] = df1[1] + " " + df1[2] + " " + df1[3] + " " + df1[4]


    labels = [l.strip().lower() for l in pmids_gold_labeled[1] if l.strip()]

    return (list(df1[0]),labels)

# Getting data as dataframes from json results of pubmed searches using RESTful api
def get_df(file_name, f_type='json', ordered=True):
    if ordered:
        (ids,labels)=get_label()

        if f_type=='json':
            data = pd.DataFrame(columns=['sourceid', 'text', 'denotations'])

            with open(file_name, 'r') as ipfile:
                publications = json.load(ipfile)
            for i, p in enumerate(publications.values()):
                data.loc[i]=[p['sourceid'], p['text'], ['g']]

            for i, pub in enumerate(publications.values()):

                denotations = [d['obj'] for d in pub['denotations']]
                idx=ids.index(int(pub['sourceid']))

                data.iloc[idx] = [pub['sourceid'], pub['text'], denotations]
            return data
        else:
            print("file types other than json not supported at this time")
            return False
    else:
        if f_type == 'json':


            data = pd.DataFrame(columns=['sourceid', 'text', 'denotations'])

            with open(file_name, 'r') as ipfile:
                publications = json.load(ipfile)

            # print(publications)
            for i, pub in enumerate(publications.values()):
                denotations = [d['obj'] for d in pub['denotations']]
                data.loc[i] = [pub['sourceid'], pub['text'], denotations]

            return data

        else:
            print("file types other than json not supported at this time")
            return False

train_df= get_df('data/set1.json')
#print(train_df.iloc[0])



# prune stopwords, lemmatize and return tokens
def preprocess_text(text, StopWords=["patient", "patient's", "treatment", "case", "clinical", "result"], ngram=1):
    # Get rid of punctuations
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)

    stop_words = [s.lower() for s in stopwords.words('english')]

    # get list to rid irrelevant most frequent words

    tokens = [word.lower().strip() for word in tokens]

    # get rid of stopwords
    tokens = [word.strip().lower() for word in tokens if word.strip() and word.strip().lower() not in stop_words]

    tokens = [word for word in tokens if word not in StopWords]

    # lemmetize the text
    wnl = WordNetLemmatizer()
    tokens = [wnl.lemmatize(word) for word in tokens]

    # tokens=bigrams(tokens)

    #use nouns only
    token=[token[0] for token in pos_tag(tokens) if token[1] == 'NN']

    return (tokens)

def group_error(clusters, start=0,end=0):
    cluster_count = dict()
    #print("cluster",clusters[start:end])
    for i in range(start, end):

        if clusters[i] in cluster_count:
            cluster_count[clusters[i]]+=1
        else:
            cluster_count[clusters[i]]=1
    gp_name_c=max(cluster_count, key=lambda key: cluster_count[key])

    err=sum([1 for i in range(start,end) if clusters[i]!=gp_name_c])
    return err
