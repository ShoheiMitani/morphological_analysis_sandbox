import csv
import numpy as np
import pandas as pd
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from janome_extension import PartsOfSpeechFilter

all_nouns = np.empty(0)

char_filters = [UnicodeNormalizeCharFilter(),
                RegexReplaceCharFilter('[♡❤♪⭐♥✨❗✧☺⁂➕❁#》☻】✨✨✼✲✻✨✨✨✴❁【☘◡]', ''),
                RegexReplaceCharFilter('[•#%:@-~?&!()\.\*\/\[\]\+\']', ''),
                ]

token_filters = [CompoundNounFilter(),
                 POSKeepFilter(['名詞']),
                 PartsOfSpeechFilter(['一般', '複合', '固有名詞']),
                 LowerCaseFilter(),
                 ExtractAttributeFilter('surface')]

analyzer = Analyzer(char_filters=char_filters, token_filters=token_filters)

with open('input.csv', 'r') as f:
    """
    CSVファイルを読み込み、形態素に分解し名詞のみを抽出する
    """
    reader = csv.reader(f)

    for row in reader:
        text = row[0]
        nouns = [surface for surface in analyzer.analyze(text)]
        print(nouns)
        all_nouns = np.hstack((all_nouns, nouns))

"""
名詞ごとの個数を計算してCSVに出力する
"""
reshaped = np.vstack((all_nouns, np.ones(all_nouns.shape[0]))).transpose()
df = pd.DataFrame({'name': all_nouns, 'count': np.ones(all_nouns.shape[0])})
grouped = df.groupby('name')
grouped.sum().sort_values(['count'], ascending=False).to_csv("janome_result.csv")
