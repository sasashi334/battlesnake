# バトルスネーク（ソロ用）

## 概要
大学のグループワークで作ったバトルスネークのコード。Python指定だったためPythonで書いた。意見をみんなで出し合い、コードを私が書いた。グループ対抗で生存ターンで競ったが、私の班の最終結果は14班中2位だった。(私の班はg03)
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
を実行するとブラウザが開き、ゲームが実行される。

## ルール
ヘビが自分の体や壁に当たったり、体力が無くなったらゲームオーバーとなる。体力は1マス進むごとに1減る。盤面は6×6で、エサは確定で3つ湧く。エサを取ると体力が全回復し、体長が伸びる。1ターンごとに自分が書いたコードが実行され、上下左右で進む方向を決める。1ターンごとの実行時間制限は500msである。

## 実行映像
https://drive.google.com/file/d/1VPN0DJ60P5tH2dV3HmYmnBURzFVUqlsN/view?usp=drive_link



