import pandas as pd
import numpy as np
from unicodedata import normalize
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher
import csv

def similarity(word):
    searcher = Searcher(db, CosineMeasure())
    return np.array(searcher.search(normalize('NFKC', word), 0.7))

def set_similarity_strings(passed_list, word):
    """
    wordに指定した文字列に類似するものを抽出し、passed_listに追加する
    """
    passed_list.extend([word])
    similarity_strings = similarity(word)
    diff_list = np.setdiff1d(similarity_strings, np.array(passed_list))

    if len(diff_list) == 0:
        return

    for d in diff_list:
        set_similarity_strings(passed_list, d)

def main():
    file = open('similarity_grouping_result.csv', 'w')

    writer = csv.writer(file, lineterminator='\n')
    writer.writerow(['total_count', 'combined_passed_name'])

    df = pd.read_csv('janome_result.csv')
    keys = df['name'].ravel()

    print("Start. target keys: {}".format(len(keys)))

    for index, row in df.iterrows():
        db.add(normalize('NFKC', row['name']))

    for index, row in df.iterrows():
        name = row['name']
        if name not in keys:
    #         print("Detected passed key: {}".format(name))
            continue

        passed_list = []
        set_similarity_strings(passed_list, name)
        total_count = df[df['name'].isin(passed_list)]['count'].sum()
        combined_passed_name = ': '.join(passed_list)
#         print("Count: {}, Names: {}".format(total_count, combined_passed_name))
        writer.writerow([total_count, combined_passed_name])

        keys = np.delete(keys, np.where(np.isin(keys, passed_list) == True))
    #     print("Grouping keys... size: {}, keys: {}. Unpassed keys... size: {}".format(len(passed_list), passed_list, len(keys)))

    file.close()
    print("End")

if __name__ == "__main__":
    db = DictDatabase(CharacterNgramFeatureExtractor(2))
    main()
