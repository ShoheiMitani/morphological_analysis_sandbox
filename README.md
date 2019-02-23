pythonのnagisaとjanomeのライブラリを使い、形態素解析を試す。

# Setup

```py
pipenv install
```

```
echo '東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便 利です。' > input.csv
```

# Commands

*nagisa*

```py
pipenv run nagisa
```

*janome*

```py
pipenv run janome
```

# Function

`input.csv`に記載された文字列を形態素解析し、名刺の出現個数を数えて`**_result.csv`に出力する。

# Files

|File|意味|
|:---|:--|
|input.csv|形態素解析したい文字列|
|janome_result.csv|janomeの出力結果|
|nagisa_result.csv|nagisaの出力結果|
