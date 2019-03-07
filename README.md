pythonのnagisaとjanomeのライブラリを使い、形態素解析を試す。

# Setup

```py
pipenv install
```

```
echo '東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便 利です。' > input.csv
echo '東京スカイツリー,1288,1288,4569,名詞,固有名詞,一般,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー' > userdic.csv
echo '東武スカイツリーライン,1288,1288,4700,名詞,固有名詞,一般,*,*,*,東武スカイツリーライン,トウブスカイツリーライン,トウブスカイツリーライン' > userdic.csv
echo 'とうきょうスカイツリー駅,1288,1288,4143,名詞,固有名詞,一般,*,*,*,とうきょうスカイツリー駅,トウキョウスカイツリーエキ,トウキョウスカイツリーエキ' > userdic.csv
```

# Commands

## 形態素解析

以下のコマンドで、input.csvに記載された文言を形態素解析して名詞のみを抽出し、各単語の出現回数を出力します。

*nagisaを利用する*

```py
pipenv run nagisa
#=> nagisa_result.csv
```

*janomeを利用する*

```py
pipenv run janome
#=> janome_result.csv
```

## 類義語のグルーピング

上記の各単語のうち、表記揺れや同じ意味合いのデータを検知し出力します。

```py
pipenv run similarity
#=> similarity_grouping_result.csv
```


# Function

`input.csv`に記載された文字列を形態素解析し、名刺の出現個数を数えて`**_result.csv`に出力する。

# Files

|File|意味|
|:---|:--|
|input.csv|形態素解析したい文字列|
|userdic.csv|janomeに登録する[ユーザー定義辞書](http://mocobeta.github.io/janome/#id8)|
|janome_result.csv|janomeの出力結果|
|nagisa_result.csv|nagisaの出力結果|
