import sys
import json
import re
import math
import numpy as np
from collections import Counter
from collections import defaultdict
from nltk.stem.porter import PorterStemmer

### Global variables ###
events = []

def main():

    # Get command-line arguments
    args = sys.argv

    if len(args) < 2:
        print("Please provide event description.")
        quit()

    # First argument is event description
    event_desc = args[1]

    # Load events from events json file
    with open("events.json") as events_json:
        events_dict = json.load(events_json)
        events = [event["description"] for event in events_dict if event["description"]]

    # Print top events based on cosine similarity
    ranked_events = get_cos_sim_ranked_events(event_desc, events)
    print_top_events(event_desc, ranked_events, events_dict, 10)

### Helper Functions ###

# Tokenize text into list of words and stem words
def tokenize(text):
    return stem(re.findall(r'[a-z]+', text.lower()) if text else [])

# Stem each word in word list using Porter Stemming Algorithm
def stem(words):
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in words]

# Build inverted index dictionary
def build_inverted_index(events):
    inv_idx = defaultdict(list)

    for idx, event in enumerate(events):
        # Dict format: {word: # of times word appears in event description}
        word_counts = Counter(tokenize(event))

        # Update list of (event_id, tf) for each word in event
        for word in word_counts:
            inv_idx.setdefault(word, []).append((idx, word_counts[word]))

    return inv_idx

# Compute IDF using inverted index
def compute_idf(inv_idx, n_events, min_df=5, max_df_ratio=0.95):
    idf_dict = {}

    # Ignore too specific and too common words
    pruned_inv_idx = {k:v for k,v in inv_idx.items()
                        if len(v) >= min_df and
                        ((len(v)/float(n_events)) <= max_df_ratio)}

    # Compute IDF for each word in filtered_inv_idx
    for word, doc_tf in pruned_inv_idx.items():
        # TODO: Optimize this so we don't store number of events
        idf = math.log(n_events / float(1 + len(doc_tf)), 2)
        idf_dict[word] = idf

    return idf_dict

# Compute norm of each event using inverted index
def compute_doc_norms(inv_idx, idf, n_events):
    norms = np.zeros(n_events)

    # Compute norm of each event
    for word, doc_tf in inv_idx.items():
        for event_id, tf in doc_tf:
            norms[event_id] += pow((tf * idf[word]), 2)

    return np.sqrt(norms)

# Get most similar events using cosine similarity
def get_cos_sim_list(query, inv_idx, idf, doc_norms):
    # Dict format: {event_id: unnormalized_score}
    scores = defaultdict(int)

    query_words = tokenize(query)
    query_counts = Counter(query_words)

    # Compute the vectors product
    for word in query_words:
        # Ignore words that don't appear in event descriptions
        if word not in inv_idx: continue
        doc_tf_list = inv_idx[word]
        for event_id, doc_tf in doc_tf_list:
            doc_weight = idf[word] * doc_tf
            query_weight = query_counts[word] * idf[word]
            scores[event_id] += query_weight * doc_weight

    # Normalize the scores
    for event_id, score in scores.items():
        doc_norm = float(doc_norms[event_id])
        idf_tf_sum = 0

        for term, tf in query_counts.items():
            if term not in idf: continue
            idf_tf_sum += math.pow(idf[term]*tf, 2)

        query_norm = math.sqrt(idf_tf_sum)
        scores[event_id] = float(score) / (doc_norm * query_norm)

    results = sorted(scores.items(), key=lambda x: -x[1])
    results = [(s, d) for d,s in results]

    return results

# Get ranked list of events
def get_cos_sim_ranked_events(query, events):
    inv_idx = build_inverted_index(events)
    idf = compute_idf(inv_idx, len(events))
    inv_idx = {k:v for k, v in inv_idx.items() if k in idf}
    doc_norms = compute_doc_norms(inv_idx, idf, len(events))

    return get_cos_sim_list(query, inv_idx, idf, doc_norms)

# Print out ranked list
def print_top_events(query, ranked_events, events_dict, top_k):
    print("#" * len(query))
    print(query)
    print("#" * len(query))

    for score, event_id in ranked_events[:top_k]:
        print("[{:.2f}] {}".format(
            score,
            events_dict[event_id]['name'].encode('utf-8')))

# Get cosine similarity between two vectors
def get_cos_sim(vec1, vec2):
    vec_prod = np.dot(vec1, vec2)
    vec_norm_prod = np.linalg.norm(vec1) * np.linalg.norm(vec2)

    return vec_prod / float(vec_norm_prod)

if __name__ == '__main__':
    main()
