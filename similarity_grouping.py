import pandas as pd
import numpy as np
import copy
from unicodedata import normalize
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from janome_extension import PartsOfSpeechFilter, OneCharTokenFilter

import csv

def similarity(word):
    searcher = Searcher(db, CosineMeasure())
    return np.array(searcher.search(normalize('NFKC', word), 0.65))

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
    writer.writerow(['frequent_word', 'total_count', 'synonym'])

    df = pd.read_csv('janome_result.csv')
    keys = df['name'].ravel()

    char_filters = [UnicodeNormalizeCharFilter()]
    token_filters = [
        POSKeepFilter(['名詞']),
        PartsOfSpeechFilter(['固有名詞']),
        ExtractAttributeFilter('surface'),
        OneCharTokenFilter()
    ]
    analyzer = Analyzer(char_filters, Tokenizer("userdic.csv", udic_enc="utf8"), token_filters)

    print("Start. target keys: {}".format(len(keys)))

    # 全ての単語を類義語のデータベースに登録
    for index, row in df.sort_values('count', ascending=False).iterrows():
        db.add(normalize('NFKC', row['name']))

    for index, row in df.iterrows():
        name = row['name']
        if name not in keys:
            continue

        # 表記揺れと類義語を探す
        passed_list = []
        set_similarity_strings(passed_list, name)

        # 抜け漏れを少なくするため、部分一致で含まれるものを抽出する
        for word in copy.copy(passed_list):
            if len(word) <= 3:
                continue

            for key in keys:
                if key.find(word) >= 0 and key not in passed_list:
                    passed_list.extend([key])

        total_count = df[df['name'].isin(passed_list)]['count'].sum()
        combined_passed_name = ':'.join(passed_list)

        # 再頻出の単語を抽出する
        keywords = [surface for surface in analyzer.analyze(combined_passed_name)]
        frequent_word = { 'key': 'No Key', 'count': 0 }
        for key in keywords:
            if len(word) < 3:
                continue

            count = combined_passed_name.count(key)
            if count > frequent_word['count']:
                frequent_word['key'] = key
                frequent_word['count'] = count

#         print("Count: {}, Names: {}".format(total_count, combined_passed_name))
        writer.writerow([frequent_word['key'], total_count, combined_passed_name])
        keys = np.delete(keys, np.where(np.isin(keys, passed_list) == True))
    #     print("Grouping keys... size: {}, keys: {}. Unpassed keys... size: {}".format(len(passed_list), passed_list, len(keys)))

    file.close()
    print("End")

if __name__ == "__main__":
    db = DictDatabase(CharacterNgramFeatureExtractor(2))
    main()
