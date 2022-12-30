import re
from KoG2P.g2p import runKoG2P
import pandas as pd
from itertools import product
from collections import Counter
import sys
import numpy as np
from sklearn.decomposition import PCA
import pickle

# 출처: https://github.com/aparrish/phonetic-similarity-vectors/blob/a90cd24ac6efa936e9b73e82db7bda940c39afbe/featurephone.py#L58
def feature_bigrams(phones_list, phone_feature_map, include_reverse=True):
    """Takes a list of ARPAbet phones and returns a list of features.
    >>> feature_bigrams("M NG".split())
    ['blb-vel', 'blb-nas', 'nas-vel', 'nas-nas', 'vel-blb', 'vel-nas', 'nas-blb', 'nas-nas']
    >>> feature_bigrams(["OW1"])
    
    """
    # find n-grams of each successive pair
    grams = list()
    phones_list = ["^"] + phones_list + ["$"]
    for ph0, ph1 in zip(phones_list[:-1], phones_list[1:]):
        for item in product(*[phone_feature_map[ph0], phone_feature_map[ph1]]):
            grams.append('-'.join(item))

    # backwards too
    if include_reverse:
        phones_list = list(reversed(phones_list))
        for ph0, ph1 in zip(phones_list[:-1], phones_list[1:]):
            for item in \
                    product(*[phone_feature_map[ph0], phone_feature_map[ph1]]):
                grams.append('-'.join(item))

    return grams


# 출처: https://github.com/aparrish/phonetic-similarity-vectors/blob/master/generate.py
# from featurephone import feature_bigrams

def normalize(vec):
    """Return unit vector for parameter vec.
    >>> normalize(np.array([3, 4]))
    array([ 0.6,  0.8])
    """
    if np.any(vec):
        norm = np.linalg.norm(vec)
        return vec / norm
    else:
        return vec


def generate_phonetic_feature_vectors(words_file_path='data/kowords.txt', vector_size=512):

    with open(words_file_path,'r') as f:
        ko_vocabs = [line.rstrip('\n') for line in f]
    # 중복 제거 및 한글 제외 삭제 
    ko_vocabs = [re.sub('[^가-힣]','', word) for word in set(ko_vocabs)]

    # IPA to phonetic features 
    df = pd.read_csv('data/ipa_feats.csv')
    df.features = df.features.apply(lambda x: tuple(x.split()))
    phone_feature_map = dict(df.values)
    phone_feature_map['^'] = tuple(['bgn']) 
    phone_feature_map['$'] = tuple(['end']) 


    all_features = Counter()
    entries = list()

    for word in ko_vocabs:
        phones = runKoG2P(word, 'KoG2P/rulebook.txt') 
        features = Counter(feature_bigrams(phones.split(), phone_feature_map))
        entries.append((word, features))
        all_features.update(features.keys())

    for i, line in enumerate(sys.stdin):
        if line.startswith(';'):
            continue
        line = line.strip()
        word, phones = line.split("  ")
        features = Counter(feature_bigrams(phones.split(), phone_feature_map))
        entries.append((word, features))
        all_features.update(features.keys())

    print("entries:", len(entries), file=sys.stderr)

    filtfeatures = sorted([f for f, count in all_features.items() \
            if count >= 2])

    print("feature count:", len(filtfeatures), file=sys.stderr)

    print("performing PCA...", file=sys.stderr)

    # transpos of the original paper matrix 
    # cf. original paper matrix: (# of words, # of feature bigrams)
    arr = np.array([normalize([i.get(j, 0) for word, i in entries]) \
             for j in filtfeatures])

    # (# of feature bigrams, # of words)
    print(f"matrix size: {arr.shape}")

    pca = PCA(n_components=vector_size, whiten=True)
    transformed = pca.fit_transform(arr)

    feat2vec = {}
    for i in range(len(filtfeatures)):
        feature = filtfeatures[i]
        vector = transformed[i]
        feat2vec[feature] = vector
        # nums = " ".join(["%0.6f" % num for num in transformed[i]])
        # print("  ".join([word, nums]))
        
    print("done!", file=sys.stderr)


    with open('feat2vec.pickle', 'wb') as fp:
        pickle.dump(feat2vec, fp)