# kousotsu-py_v2
高卒たんメソッドをPythonで実現するスレより


セットアップスクリプトを用意しました(MAC用)
下記を実行するとDockerセットアップ後、バイナンスから初期データを取得します。

インストールは楽になったはず・・・・

```
git clone https://github.com/tyaro/kousotsu-py_v2.git

cd kousotsu-py_v2

/bin/sh setup.sh
```


現在の進捗は下記です(2021/06/22)
・通貨ペアマスタの作成
・初期データの取得
 - DBに1日足ローソク足データの格納
 - DBにBTC建て1日足ローソク足データの格納
 - DBに4時間足ローソク足データの格納
 - DBに1時間ローソク足データの格納

