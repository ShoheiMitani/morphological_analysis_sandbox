import nagisa
import csv
import numpy as np
import pandas as pd

all_nouns = np.empty(0)

with open('input.csv', 'r') as f:
    """
    CSVファイルを読み込み、形態素に分解し名詞のみを抽出する
    """
    reader = csv.reader(f)

    for row in reader:
        text = row[0]
        words = nagisa.tagging(text)
        np_words = np.array(words.words)
        np_postags = np.array(words.postags)
        nouns = np_words[np.where(np_postags == '名詞')]
        all_nouns = np.hstack((all_nouns, nouns))

"""
名詞ごとの個数を計算してCSVに出力する
"""
reshaped = np.vstack((all_nouns, np.ones(all_nouns.shape[0]))).transpose()
df = pd.DataFrame({'name': all_nouns, 'count': np.ones(all_nouns.shape[0])})
grouped = df.groupby('name')
grouped.sum().sort_values(['count'], ascending=False).to_csv("nagisa_result.csv")
