import csv
import numpy as np
import pandas as pd
from janome.tokenizer import Tokenizer

all_nouns = np.empty(0)

with open('input.csv', 'r') as f:
    """
    CSVファイルを読み込み、形態素に分解し名詞のみを抽出する
    """
    reader = csv.reader(f)

    for row in reader:
        text = row[0]
        t = Tokenizer("userdic.csv", udic_enc="utf8")
        nouns = [token.surface for token in t.tokenize(text) if token.part_of_speech.startswith('名詞')]
        all_nouns = np.hstack((all_nouns, nouns))

"""
名詞ごとの個数を計算してCSVに出力する
"""
reshaped = np.vstack((all_nouns, np.ones(all_nouns.shape[0]))).transpose()
df = pd.DataFrame({'name': all_nouns, 'count': np.ones(all_nouns.shape[0])})
grouped = df.groupby('name')
grouped.sum().sort_values(['count'], ascending=False).to_csv("janome_result.csv")
