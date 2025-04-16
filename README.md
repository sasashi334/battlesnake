# バトルスネーク（ソロ用）

## 概要
大学のグループワークで、グループ対抗で作ったバトルスネークのコード。Python指定だったのでPythonで書いた。意見をみんなで出し合い、私がコードを書いた。最終結果は15班中2位だった(私の班は3班)。
![Image](https://github.com/user-attachments/assets/c6d14529-3b84-4f0c-a65b-5f91d9f2979b)


## 実行環境
windows 11
ubuntu
Python 3.10.12

## 実行方法
フォルダをダウンロードし、ターミナルを二つ用意する。
一つ目のターミナルで  
```
python3 main.py
```
を実行する。
その後、二つ目のターミナルで  
```
./battlesnake play --url http://localhost:8000 -W 6 -H 6 --foodSpawnChance 0 --minimumFood 3 --browser
```
を実行するとヘビが動き出す。



