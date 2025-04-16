#pythonバージョン:Python 3.10.12

import random
import typing
from copy import deepcopy


"""


基本アルゴリズム: 体力あるときは上下左右を見て空き面積が広い方角に行く.空き面積が同じ場合は大回りするようにした.
                  具体的には,壁とヘビの向いてる向きから次の方角の優先度をつけた.
                  へびのしっぽの移動と距離の計算から未来の空き地を計算する.
                  エサを食べたときのしっぽの伸びも考慮に入れた.
                 
                  体力がないとき現在地からエサの場所までの経路をすべて計算.
                  その経路の中で最も体力をギリギリまで使う経路で,かつエサの湧いた後安全な確率が高いものの経路を選択.


詳細: 体力あるときは:
                    まずエサを避け、頭とシッポを1マス以上空ける.(安全)
                    無理なら頭とシッポをくっつける.(次にエサを食べるとき不安定)
                    無理ならエサをひとつずつ障害物から除外する.(体力あるのにエサを食べちゃう)
                    無理ならすべてのエサを障害物から除外する.(体力あるのにエサを連続で食べちゃう)
               
      体力ないときは:
                    食べたいエサごとに,また方角ごとに深さ優先探索を用いてすべての経路を計算.
                    求めた経路が暫定の最長経路より長い場合,その経路でエサを食べた後に湧きうるエサをすべて当てはめて,安全な確率を求める.
                    確率が一定以上のとき採用する.




"""




def info() -> typing.Dict:
    print("INFO")


    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#FF00FF",  # TODO: Choose color
        "head": "snow-worm",  # TODO: Choose head
        "tail": "block-bum",  # TODO: Choose tail
    }




# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")




# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")




#盤面をコピーしてから空き地を数える


def copyAndCount(game_state,x,y,safeZone,board,turn):
    boardCopy=deepcopy(board)
    return count(game_state,x,y,safeZone,boardCopy,turn)




#count()は座標(x,y)と地続きの空白のマス目を数える関数
#safeZoneが空白のマス目カウンタ
#戻り値は最終的なsafeZone
#エサを食べたときの遅延も考慮


def count(game_state,x,y,safeZone,board,turn):


    dx=[1,0,-1,0]
    dy=[0,1,0,-1]


    #座標(x,y)が壁の時
    if y==-1 or x==-1 or x == game_state['board']['width'] or y == game_state['board']['height']:
        return safeZone
   
    #座標(x,y)にエサがある場合
    #ターン数増やさない
    elif board[y][x]<0:
        board[y][x]=1000


        for i in range(4):
            safeZone=count(game_state,x+dx[i],y+dy[i],safeZone,board,turn)
       
        return safeZone
   
    #座標(x,y)に体がある場合かつ体が座標(x,y)から動ききってない場合
    elif board[y][x]-turn>=1 :
        return safeZone
   
    #座標(x,y)が空き地だった場合
    else :
        turn+=1
        board[y][x]=1000
        safeZone+=1
        for i in range(4):
            safeZone=count(game_state,x+dx[i],y+dy[i],safeZone,board,turn)


        return safeZone




#foodsearch()は座標(x,y)からエサまでの経路で,体力をギリギリまで使う経路を求める関数
#戻り値は最短経路の一歩目の方角と最長経路の長さ(体力以内で)
#最長経路の場合でも、エサに囲まれる可能性が高かったら避ける
#安全な確率が100%がある場合,100%の経路の中で最長なものを採用


#kakuteidist変数は安全確率100%の最長経路の長さ,kakuteidirest変数はその方角


kakuteidist=0
kakuteidirect="none"


#最長距離の初期値
distmax=0
#最初の一歩の初期値
direction="none"




def foodSearch(game_state,x,y,food,board,mode):


    global kakuteidirect,kakuteidist,distmax,firstStep


    kakuteitmp=kakuteidist




    copyState=board[food["y"]][food["x"]]


    #探索するエサだけは障害物から除外する
    board[food["y"]][food["x"]]=-1


    distPrev=distmax


    #一歩目が右の場合
    dfs(game_state,x+1,y,food,1,board,mode)
    #一歩目が右で、最長距離を更新する場合
    if distmax!=distPrev:
        firstStep="right"


    if kakuteitmp!=kakuteidist:
        kakuteidirect="right"




    kakuteitmp=kakuteidist


    distPrev=distmax
    #一歩目が左の場合
    dfs(game_state,x-1,y,food,1,board,mode)


    #一歩目が左で、最長距離を更新する場合
    if distmax!=distPrev:
        firstStep="left"


    if kakuteitmp!=kakuteidist:
        kakuteidirect="left"


    kakuteitmp=kakuteidist


    distPrev=distmax


    #一歩目が上の場合  
    dfs(game_state,x,y+1,food,1,board,mode)


    #一歩目が上で、最長距離を更新する場合
    if distmax!=distPrev:
        firstStep="up"


    if kakuteitmp!=kakuteidist:
        kakuteidirect="up"


    kakuteitmp=kakuteidist


    distPrev=distmax
    #一歩目が下の場合
    dfs(game_state,x,y-1,food,1,board,mode)


    #一歩目が下で、最長距離を更新する場合
    if distmax!=distPrev:
        firstStep="down"


    if kakuteitmp!=kakuteidist:
        kakuteidirect="down"


    board[food["y"]][food["x"]]=copyState


    return




   


   
   
   


#dfs()関数は体力が間に合い,エサにたどり着きうるすべてのルートを計算する    
#最長記録を更新しうるとき,エサに触れた瞬間の盤面の空き地にエサを一つずつ当てはめて,エサに囲まれない確率を求め,一定以上だった場合のみ最長記録を更新する


def dfs(game_state,x,y,food,dist,board,mode):


    global kakuteidist,kakuteidirect,distmax


    dx=[1,0,-1,0]
    dy=[0,1,0,-1]






    #座標が壁の場合か,体力が尽きる場合か,座標(x,y)からエサまで残りターンでは間に合わない場合


    nokori=game_state['you']["health"]-dist
    if y==-1 or x==-1 or x== game_state['board']['width'] or y== game_state['board']['height'] or nokori<0 or board[y][x]-dist>=1 or abs(y-food["y"])+abs(x-food["x"])>nokori:
        return
   
    #エサにたどり着く場合
    elif x==food["x"] and y==food["y"]:






        #最長距離を更新する場合
        if dist>distmax and dist>kakuteidist:


            #安全かどうか
            if copyAndCount(game_state,x,y,0,board,dist-1)>game_state['you']["length"]:


                prob=Exp(game_state,board,x,y,dist)


                #まずは安全な経路を探す
                if mode==0:


                    #100%安全の時


                    if prob >= 0.999:
                        if kakuteidist<dist:
                            kakuteidist=dist


                    #ヘビの長さで場合分け
                    #一定確率以上で更新


                    #長さが15以上23未満の時
                    elif game_state['you']["length"]>=15 and game_state["you"]["length"]<23:


                        if prob>=0.8:
                            distmax=dist


                        #長さが23以上30未満の時
                    elif game_state['you']["length"]>=23 and game_state["you"]["length"]<27:


                        if prob>=0.7:
                            distmax=dist


                        #長さが26以上の時


                    elif game_state["you"]["length"]>=27:


                        if prob>0.5:
                            distmax=dist


                        #長さが19未満の時
                    else:
                        if prob>=0.95:
                            distmax=dist


                #安全が無理だからギャンブル
                else:
                    if prob>=0.5:
                        distmax=dist




        return
   
    #空き地の場合
    else :


        copyState=board[y][x]
        board[y][x]=game_state['you']["length"]+dist


        for i in range(4):
            dfs(game_state,x+dx[i],y+dy[i],food,dist+1,board,mode)


        board[y][x]=copyState
        return


#Exp()関数はエサに囲まれない確率を求める
#foodSum変数は当てはめるエサの母数
#ok変数はエサに囲まれない場合の数
#戻り値は二つを割った確率、つまり安全な確率


def Exp(game_state,board,x,y,dist):
    ok=0
    foodSum=0


    for i in range(game_state['board']['width']):
        for j in range(game_state['board']['height']):
            #空き地だった場合、エサを当てはめる
            if board[j][i]>=0 and board[j][i]-dist<=0:


                foodSum+=1
                copyState=board[j][i]
                board[j][i]=1000
                #地続きの空き地が一定以上の場合ok
                if copyAndCount(game_state,x,y,0,board,dist)>20:
                    ok+=1
                board[j][i]=copyState
    if foodSum!=0:
        return ok/foodSum
   
    else :
        return 0




#グローバル変数の宣言
wall="left"
direction="up"


def move(game_state: typing.Dict) -> typing.Dict:




    is_move_safe = {"up": False, "down": False, "left": False, "right": False}
   


    my_head = game_state["you"]["body"][0]
    my_neck = game_state["you"]["body"][1]  


   
    #prevは首の向き


    if my_neck["x"] < my_head["x"]:  
        prev="right"


    elif my_neck["x"] > my_head["x"]:
        prev="left"


    elif my_neck["y"] < my_head["y"]:
        prev="up"


    elif my_neck["y"] > my_head["y"]:
        prev="down"


    else:
        prev="right"
   






    board_width = game_state['board']['width']
    board_height = game_state['board']['height']






    #wall変数は壁についた時のみ所属する壁を記録する
    #direction変数は壁についた時の首の向きを記録する
    #どちらの変数もグローバル変数のため次に壁に着くまで保持される.


    global direction,wall,kakuteidist,kakuteidirect,distmax,firstStep
    kakuteidist=0
    kakuteidirect="none"
    distmax=0
    firstStep="none"


    if my_head["x"]==0:
        direction=prev
        wall="left"
    elif my_head["x"]==board_width-1:
        direction=prev
        wall="right"
    elif my_head["y"]==0:
        direction=prev
        wall="down"
    elif my_head["y"]==board_height-1:
        direction=prev
        wall="up"
   


    my_body = game_state['you']['body']


    #boardは盤面を記録した二次元配列
    #0が空き地,1以上が障害物,-1がエサ


    board=[[0 for i in range(board_width)] for j in range(board_height)]




    #長さ3の時の事故防止
    if game_state['you']["length"]==3:
        for body in my_body:
            board[body["y"]][body["x"]]=1000


    #ヘビの体をboardに記録
    #具体的にはシッポからの距離+1をboardに記録
    else:
        #lenghtはヘビの長さ
        length=game_state['you']["length"]
        bodyCount=0
        for body in my_body:


            #体力が満タンの時にシッポの位置に体二つ存在するため、端を取り除く
            if game_state['you']['health']==100 and bodyCount==game_state['you']["length"]-1:
                continue
            board[body["y"]][body["x"]]=length-bodyCount
            bodyCount+=1


    #巡回時処理(体力が十分の時)


    #ヘビの長さ分の体力があるとき十分とみなす
    if (game_state['you']['health']>=game_state['you']["length"] and game_state['you']["length"]>10) or (game_state['you']['health']>10 and game_state['you']["length"]<=10):
        foods = game_state['board']['food']


        #まずはエサを障害物扱いし,頭とシッポを1マス以上離す
        for food in foods:
            board[food["y"]][food["x"]]=1000
           


        #count〇〇は各方角に一歩進んだ先の地続きの空き地の数            
        countUp=copyAndCount(game_state,my_head["x"],my_head["y"]+1,0,board,0)
        countRight=copyAndCount(game_state,my_head["x"]+1,my_head["y"],0,board,0)
        countDown=copyAndCount(game_state,my_head["x"],my_head["y"]-1,0,board,0)
        countLeft=copyAndCount(game_state,my_head["x"]-1,my_head["y"],0,board,0)


        #安全な方角がないなら頭とシッポをくっつける
        print(max([countRight,countLeft,countUp,countDown]))
        if max([countRight,countLeft,countUp,countDown])<20:




            countUp=copyAndCount(game_state,my_head["x"],my_head["y"]+1,0,board,1)
            countRight=copyAndCount(game_state,my_head["x"]+1,my_head["y"],0,board,1)
            countDown=copyAndCount(game_state,my_head["x"],my_head["y"]-1,0,board,1)
            countLeft=copyAndCount(game_state,my_head["x"]-1,my_head["y"],0,board,1)


            #安全な方角がないなら,1つずつエサを障害物扱いではなくする(エサの連続食いを阻止)
            if max([countRight,countLeft,countUp,countDown])<20:


                for food in foods:
                    board[food["y"]][food["x"]]=-1


                    countUp=copyAndCount(game_state,my_head["x"],my_head["y"]+1,0,board,1)
                    countRight=copyAndCount(game_state,my_head["x"]+1,my_head["y"],0,board,1)
                    countDown=copyAndCount(game_state,my_head["x"],my_head["y"]-1,0,board,1)
                    countLeft=copyAndCount(game_state,my_head["x"]-1,my_head["y"],0,board,1)


                    board[food["y"]][food["x"]]=1000


                    if max([countRight,countLeft,countUp,countDown])>=20:
                        break


                #安全な方角がないなら,全てのエサを障害物扱いでなくする
                if max([countRight,countLeft,countUp,countDown])<20:
                    for food in foods:
                        board[food["y"]][food["x"]]=-1




                    countUp=copyAndCount(game_state,my_head["x"],my_head["y"]+1,0,board,1)
                    countRight=copyAndCount(game_state,my_head["x"]+1,my_head["y"],0,board,1)
                    countDown=copyAndCount(game_state,my_head["x"],my_head["y"]-1,0,board,1)
                    countLeft=copyAndCount(game_state,my_head["x"]-1,my_head["y"],0,board,1)




        #壁に沿うように移動
        if direction=="left" and wall=="up":


            if countUp==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["up"]=True
           
            elif countLeft==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["left"]=True
       
            elif countDown==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["down"]=True


            elif countRight==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["right"]=True


        elif direction=="right" and wall=="up":


            if countUp==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["up"]=True


            elif countRight==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["right"]=True
       
            elif countDown==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["down"]=True
           
            elif countLeft==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["left"]=True






       
        elif direction=="up" and wall=="left":
       
            if countLeft==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["left"]=True
            elif countUp==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["up"]=True        
            elif countRight==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["right"]=True
            elif countDown==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["down"]=True


        elif direction=="down" and wall=="left":
       
            if countLeft==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["left"]=True
            elif countDown==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["down"]=True
            elif countRight==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["right"]=True
            elif countUp==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["up"]=True        








        elif direction=="up" and wall=="right":


            if countRight==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["right"]=True


            elif countUp==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["up"]=True    


            elif countLeft==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["left"]=True


            elif countDown==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["down"]=True


        elif direction=="down" and wall=="right":


            if countRight==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["right"]=True
           
            elif countDown==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["down"]=True




            elif countLeft==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["left"]=True


            elif countUp==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["up"]=True    


        elif direction=="left" and wall=="down":




            if countDown==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["down"]=True
       
            elif countLeft==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["left"]=True




            elif countUp==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["up"]=True    


            elif countRight==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["right"]=True
           
        elif direction=="right" and wall=="down":




            if countDown==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["down"]=True
           
            elif countRight==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["right"]=True




            elif countUp==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["up"]=True    


            elif countLeft==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["left"]=True
       
        else:
            if countDown==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["down"]=True
           
            elif countRight==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["right"]=True




            elif countUp==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["up"]=True    


            elif countLeft==max([countRight,countLeft,countUp,countDown]):
                is_move_safe["left"]=True








    #エサ探し処理


    else:
        foods = game_state['board']['food']
        #エサを障害物扱い(エサの連続食いを阻止)
        for food in foods:
            board[food["y"]][food["x"]]=1000






        #directmpは向きを記録、distmpは距離を記録
        for food in foods:


            foodSearch(game_state,my_head["x"],my_head["y"],food,board,0)


            #計算量削減(体力をギリギリまで使う経路があったら探索切り上げ)
            #if distmp>=game_state["you"]["health"]-10:
                #break




        if kakuteidirect!="none":
            is_move_safe[kakuteidirect]=True


        #エサにたどり着く場合かつ現在地から一歩先が安全な場合
        elif firstStep!="none":
            is_move_safe[firstStep]=True
       
        else:
            #エサを障害物扱いでなくする
            for food in foods:
                board[food["y"]][food["x"]]=-1






            #directmpは向きを記録、distmpは距離を記録
            for food in foods:


                foodSearch(game_state,my_head["x"],my_head["y"],food,board,1)


                #計算量削減
                if firstStep!="none":
                    break
       




            #エサにたどり着く場合
            if firstStep!="none":
                is_move_safe[firstStep]=True
       


            #諦め(最後の抵抗)
            else:




                countUp=copyAndCount(game_state,my_head["x"],my_head["y"]+1,0,board,1)
                countRight=copyAndCount(game_state,my_head["x"]+1,my_head["y"],0,board,1)
                countDown=copyAndCount(game_state,my_head["x"],my_head["y"]-1,0,board,1)
                countLeft=copyAndCount(game_state,my_head["x"]-1,my_head["y"],0,board,1)






                #壁に沿うように移動
                if direction=="left" and wall=="up":


                    if countUp==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["up"]=True
                   
                    elif countLeft==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["left"]=True
               
                    elif countDown==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["down"]=True


                    elif countRight==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["right"]=True


                elif direction=="right" and wall=="up":


                    if countUp==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["up"]=True


                    elif countRight==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["right"]=True
               
                    elif countDown==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["down"]=True
                   
                    elif countLeft==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["left"]=True






               
                elif direction=="up" and wall=="left":
               
                    if countLeft==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["left"]=True
                    elif countUp==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["up"]=True        
                    elif countRight==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["right"]=True
                    elif countDown==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["down"]=True


                elif direction=="down" and wall=="left":
               
                    if countLeft==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["left"]=True
                    elif countDown==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["down"]=True
                    elif countRight==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["right"]=True
                    elif countUp==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["up"]=True        






                elif direction=="up" and wall=="right":


                    if countRight==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["right"]=True


                    elif countUp==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["up"]=True    


                    elif countLeft==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["left"]=True


                    elif countDown==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["down"]=True


                elif direction=="down" and wall=="right":


                    if countRight==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["right"]=True
                   
                    elif countDown==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["down"]=True




                    elif countLeft==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["left"]=True


                    elif countUp==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["up"]=True    


                elif direction=="left" and wall=="down":




                    if countDown==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["down"]=True
               
                    elif countLeft==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["left"]=True




                    elif countUp==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["up"]=True    


                    elif countRight==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["right"]=True
                   
                elif direction=="right" and wall=="down":




                    if countDown==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["down"]=True
                   
                    elif countRight==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["right"]=True




                    elif countUp==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["up"]=True    


                    elif countLeft==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["left"]=True
               
                else:
                    if countDown==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["down"]=True
                   
                    elif countRight==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["right"]=True




                    elif countUp==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["up"]=True    


                    elif countLeft==max([countRight,countLeft,countUp,countDown]):
                        is_move_safe["left"]=True






###############処理ココまで######################


    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)


    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")


        return {"move": "down"}


    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)


    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']


    print(f"MOVE {game_state['turn']}: {next_move} {game_state['you']['health']} ")
    #print(f"dir {direction}: wall: {wall}")
    return {"move": next_move}




# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server


    run_server({"info": info, "start": start, "move": move, "end": end})

