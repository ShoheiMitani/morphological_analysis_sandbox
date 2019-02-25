import csv
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *

output = open('wakati.txt', 'w', newline="\n")

char_filters = [UnicodeNormalizeCharFilter()]

token_filters = [
    POSKeepFilter(['名詞']),
    LowerCaseFilter(),
    ExtractAttributeFilter('surface'),
]

tokenizer = Tokenizer("userdic.csv", udic_enc="utf8")

analyzer = Analyzer(char_filters, tokenizer, token_filters)

with open('input.csv', 'r') as f:
    """
    CSVファイルを読み込み、形態素に分解し名詞のみを抽出した結果を保存する
    """
    reader = csv.reader(f)

    for row in reader:
        text = row[0]
        nouns = [surface for surface in analyzer.analyze(text)]
        output.writelines("{}\n".format(' '.join(nouns)))

output.close()
