#!python
import copy

##Author: Lijun 
#
#History:
#V0.4   2022-01-05
#增加功能：1）在运行过程中增加“自动完成”功能，自动模拟完成操作。
#
#V0.3   2021-12-18
#增加功能：增加初始场景，游戏可以从多个初始场景中选择1个。
#
#V0.2   2021-12-16
#增加功能：返回上一步；返回上一步后，删除本步骤、上一步变为最后一步；如果没有上一步则菜单不显示
#V0.1   2021-12-15
#实现基础功能：一种初始化图形，可以人工操作游戏，游戏成功有提示
#
#
#
#
#Guanyu=11 (*1) ;关羽2*1（水平*竖直，下同) 横条，1个
#zhang/zhao/ma/huang = x
#                      x   (*4,2-5) ;张飞/赵云/马超/黄忠 1*2竖条，4个 
#zu = x (*4,6-9)    ;小卒， 1*1块，4个
#caocao = 00
#         00 (*1)   ;曹操，2*2块，1个
#
#
#数据结构：
#
#role[id,name,width,height,loc_row,loc_col]
#代号，名字，水平宽度，竖直高度，左上角行位置，左上角列位置
#
#result[row][col]
#各行各列的角色
#
#
#
#初始化角色位置


#初始化游戏设置
def init_conf():
    global role
    global history 
    global auto_play
    global opened
    global closed
    role = []        #角色清单，用于保存各角色属性（长宽、位置等）
    history=[]       #历史角色清单的历史动作列表，用于游戏返回上一步
    auto_play=False  #设置是否自动游戏，如果自动，则会使用opened表、closed表
    opened=[]
    closed=[]

#初始化游戏地图，设定各角色的位置。
def init_map():
    while True:
        map = input('''Welcome to HuaRongDao, Please choose a map to play:
    1、横刀立马
    2、齐头并前
    3、兵分三路
    4、屯兵东路
    5、左右布兵
    6、前挡后阻
    请输入(1-6)：''')

        try:
            map=int(map)
        except:
            pass
#        print("Map is",map)
        if(map==1):        
            #1、地图“横刀立马”
            #张曹曹马
            #飞操操超
            #赵关羽黄
            #云卒卒忠
            #卒    卒
            #口门门口
            role.append(['0','Caocao',2,2,1,2])
            role.append(['1','Guanyu',2,1,3,2])
            role.append(['2','Zhangfei',1,2,1,1])
            role.append(['3','Zhaoyun',1,2,3,1])
            role.append(['4','Machao',1,2,1,4])
            role.append(['5','Huangzhong',1,2,3,4])
            role.append(['6','xiaozu',1,1,4,2])
            role.append(['7','xiaozu',1,1,4,3])
            role.append(['8','xiaozu',1,1,5,1])
            role.append(['9','xiaozu',1,1,5,4])
            break
        elif(map==2):            
            #2、地图“齐头并前”
            #张曹曹赵
            #飞操操云
            #卒卒卒卒
            #马关羽黄
            #超    忠
            #口门门口
            role.append(['0','Caocao',2,2,1,2])
            role.append(['1','Guanyu',2,1,4,2])
            role.append(['2','Zhangfei',1,2,1,1])
            role.append(['3','Zhaoyun',1,2,1,4])
            role.append(['4','Machao',1,2,4,1])
            role.append(['5','Huangzhong',1,2,4,4])
            role.append(['6','xiaozu',1,1,3,1])
            role.append(['7','xiaozu',1,1,3,2])
            role.append(['8','xiaozu',1,1,3,3])
            role.append(['9','xiaozu',1,1,3,4])
            return
        elif(map==3):
            #3、地图“兵分三路”
            #卒曹曹卒
            #张操操赵
            #飞关羽云
            #马卒卒黄
            #超    忠
            #口门门口
            role.append(['0','Caocao',2,2,1,2])
            role.append(['1','Guanyu',2,1,3,2])
            role.append(['2','Zhangfei',1,2,2,1])
            role.append(['3','Zhaoyun',1,2,2,4])
            role.append(['4','Machao',1,2,4,1])
            role.append(['5','Huangzhong',1,2,4,4])
            role.append(['6','xiaozu',1,1,1,1])
            role.append(['7','xiaozu',1,1,1,4])
            role.append(['8','xiaozu',1,1,4,2])
            role.append(['9','xiaozu',1,1,4,3])
            return
        elif(map==4):
            #4、地图“屯兵东路”
            #曹曹张赵
            #操操飞云
            #关羽卒卒
            #马黄卒卒
            #超忠
            #口门门口
            role.append(['0','Caocao',2,2,1,1])
            role.append(['1','Guanyu',2,1,3,1])
            role.append(['2','Zhangfei',1,2,1,3])
            role.append(['3','Zhaoyun',1,2,1,4])
            role.append(['4','Machao',1,2,4,1])
            role.append(['5','Huangzhong',1,2,4,2])
            role.append(['6','xiaozu',1,1,3,3])
            role.append(['7','xiaozu',1,1,3,4])
            role.append(['8','xiaozu',1,1,4,3])
            role.append(['9','xiaozu',1,1,4,4])
            return
        elif(map==5):
            #5、地图“左右布兵”
            #张曹曹赵
            #飞操操云
            #  马黄
            #卒超忠卒
            #卒关羽卒
            #口门门口
            role.append(['0','Caocao',2,2,1,2])
            role.append(['1','Guanyu',2,1,5,2])
            role.append(['2','Zhangfei',1,2,1,1])
            role.append(['3','Zhaoyun',1,2,1,4])
            role.append(['4','Machao',1,2,3,2])
            role.append(['5','Huangzhong',1,2,3,3])
            role.append(['6','xiaozu',1,1,4,1])
            role.append(['7','xiaozu',1,1,4,4])
            role.append(['8','xiaozu',1,1,5,1])
            role.append(['9','xiaozu',1,1,5,4])
            return
        elif(map==6):
            #6、地图“前挡后阻”
            #曹曹关羽
            #操操马卒
            #赵黄超卒
            #卒超忠卒
            #卒关羽卒
            #口门门口
            role.append(['0','Caocao',2,2,1,2])
            role.append(['1','Guanyu',2,1,5,2])
            role.append(['2','Zhangfei',1,2,1,1])
            role.append(['3','Zhaoyun',1,2,1,4])
            role.append(['4','Machao',1,2,3,2])
            role.append(['5','Huangzhong',1,2,3,3])
            role.append(['6','xiaozu',1,1,4,1])
            role.append(['7','xiaozu',1,1,4,4])
            role.append(['8','xiaozu',1,1,5,1])
            role.append(['9','xiaozu',1,1,5,4])
            return
        else:
            print("\nWrong selection!")

#根据地图位置更新各角色站位结果
def updatelocation(role):    
    result = [['x' for i in range(5)] for j in range(7)]
    result[6][1]=' '
    result[6][4]=' '    
    for x in role:
    #    print(x)
        row = x[4]
        for rowcnt in range(x[3]):
            col = x[5]
            for colcnt in range(x[2]):
    #            print(row,col)
                result[row][col]=x[0]
                col = col +1
            row = row +1
    return(result)

#打印各角色站位结果
def prtresult(result):
    print("\n")
    for row in range(1,7):
        for col in range(1,5):
            print(result[row][col],end="")
        print('')

'''def prtmenu():
    while True:
        print('0-----begin game')
        print('1-----exit')
        print('\n\n Please input 0/1')
        select = input()
        if(select == '1'):
            break
        elif (select =='0'):
            print('game start')
            break
'''

#判断是否可以移动,返回可以移动的方向left，right，up，down
#获取移动角色的左上角初始位置，以及宽度、高度
#代号，名字，宽度，高度，左上角行位置，左上角列位置
def move_judge(master,role,result):
#获取各角色的xy坐标、以及宽度、高度
    pos_row=role[master][4]
    pos_col=role[master][5]
    pos_row_cnt=role[master][2]
    pos_col_cnt=role[master][3]

#初始化角色可以移动方向的结果
    direct=[]
    
#判断是否能向左移动
    left_flag='F'
#第一列的不能左移
    if(pos_col<=1):
        pass
#        print('不能向左移动')
    else:
#只有当左边列、与角色相同高度行的所有格子都是x时才可以左移
        for row in range(pos_col_cnt):
            if(result[pos_row+row][pos_col-1]=='x'):
                pass
                left_flag='T'
            else:
                left_flag='F'
                break
    if(left_flag=='T'):
        print("can move left!")
        direct.append("left")
#        return("left")

#判断是否能向右移动
    right_flag='F'
#角色的当前x坐标加上宽度大于4则不能右移
    if(pos_col+pos_row_cnt>4):
        pass
#        print('不能向右移动')
    else:
#只有当右边列、与角色相同高度行的所有格子都是x时才可以右移
        for row in range(pos_col_cnt):
            if(result[pos_row+row][pos_col+pos_row_cnt]=='x'):
                pass
                right_flag='T'
            else:
                right_flag='F'
                break
    if(right_flag=='T'):
        print("can move right!")
        direct.append("right")
#        return("right")

#判断是否能向上移动
    up_flag='F'
#第一行的不能上移
    if(pos_row<=1):
        pass
#        print('不能向上移动')
    else:
#只有当上边行、与角色相同高度列的所有格子都是x时才可以上移
        for col in range(pos_row_cnt):
            if(result[pos_row-1][pos_col+col]=='x'):
                pass
                up_flag='T'
            else:
                up_flag='F'
                break
    if(up_flag=='T'):
        print("can move up!")
        direct.append("up")
#        return("up")

#判断是否能向下移动
    down_flag='F'
#角色的当前y坐标加上高度大于6则不能下移
    if(pos_row+pos_col_cnt>6):
        pass
#        print('不能向下移动')
    else:
#只有当下边行、与角色相同高度列的所有格子都是x时才可以下移
        for col in range(pos_row_cnt):
            if(result[pos_row+pos_col_cnt][pos_col+col]=='x'):
                down_flag='T'
            else:
                down_flag='F'
                break
    if(down_flag=='T'):
        print("can move down!")
        direct.append("down")
    return(direct)

#移动
def move(master,role,direct,result):
#    print("Move"+ str(master))
#    pass
#数据结构：
#role[id,name,width,height,loc_row,loc_col]
#代号，名字，宽度，高度，左上角行位置，左上角列位置

#打印可移动的方向
    prtstr=""
    for yy in range(len(direct)):
#        print(yy,direct[yy],end='   ')
        prtstr=prtstr+str(yy)+"-"+direct[yy]
        if(yy != len(direct)-1):
            prtstr=prtstr+","
        else:
            prtstr=prtstr+",x to exit):"

    if len(direct) >= 2:
        inputx=input("\n please choose direct("+prtstr)
        if(inputx=='x' or inputx=='X'):
            exit
        else:
            direct = direct[int(inputx)]
    else:
        direct = direct[0]

    last_role=role
    if (direct == 'left'):
        role[master][5]=role[master][5]-1
    if (direct == 'right'):
        role[master][5]=role[master][5]+1
    if (direct == 'up'):
        role[master][4]=role[master][4]-1
    if (direct == 'down'):
        role[master][4]=role[master][4]+1
    print(role)
    return(role)
    
'''
for i in range(10):
    x=move_judge(i,role,result)
    print(x)

'''

def check_win(role):
    if(role[0][4]==5 and role[0][5]==2):
        return("Success!")



#主程序    
#result=updatelocation(role)
#prtresult(result)
print('\n')
init_conf()
init_map()
while True:
    history.append(copy.deepcopy(role))
    result=updatelocation(role)
    prtresult(result)
    print("\n\n")
    if(len(history)>1):
        select = input('Target: Move Caocao--0000--block to exit\n Choose an item to move，x to exit, b to back: ')
    else:
        select = input('Target: Move Caocao--0000--block to exit\n Choose an item to move，x to exit')
    if(select=='b' or select=='B'):
        if(len(history)>1):
            print('before:',history)
            history.pop()
            print('after:',history)
            role=copy.deepcopy(history[-1])
            print('last:',role)
        else:
            print("\n cannot go back, please choose again")
    elif(select in "0123456789"):
       direct = move_judge(int(select),role,result)
       if(direct!=[]):
            role=move(int(select),role,direct,result)
            history.append(copy.deepcopy(role))
            if(check_win(role)=="Success!"):
                print("\n Congratulations! You Win!")
                break
       else:
           print("\n cannot move, please choose again")
    elif (select =='x' or select=='X'):
        print('good bye')
        break
