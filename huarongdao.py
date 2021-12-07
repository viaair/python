#!python
import copy

#
#Guanyu=11 (*1)
#zhang/zhao/ma/huang = x
#                      x   (*4,2-5)
#zu = x (*4,6-9)
#caocao = 00
#         00 (*1)
#
#数据结构：
#role[id,name,width,height,loc_row,loc_col]
#代号，名字，宽度，高度，左上角行位置，左上角列位置
#
#result[row][col]
#各行各列的角色
#
#初始化角色位置
role = []
role.append(['0','caocao',2,2,1,2])
role.append(['1','Guanyu',2,1,3,2])
role.append(['2','Zhangfei',1,2,1,1])
role.append(['3','Zhaoyun',1,2,3,1])
role.append(['4','Machao',1,2,1,4])
role.append(['5','Huangzhong',1,2,3,4])
role.append(['6','xiaozu',1,1,4,2])
role.append(['7','xiaozu',1,1,4,3])
role.append(['8','xiaozu',1,1,5,1])
role.append(['9','xiaozu',1,1,5,4])

'''
用如下部分测试成功判断功能
role[0][4]=4
role[0][5]=2
role[6][4]=1
role[6][5]=2
role[7][4]=1
role[7][5]=3
'''

#根据位置更新站位结果
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

#打印站位结果
def prtresult(result):
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
    pos_row=role[master][4]
    pos_col=role[master][5]
    pos_row_cnt=role[master][2]
    pos_col_cnt=role[master][3]

#初始化结果
    direct=[]
    
#判断是否能向左移动
    left_flag='F'
    if(pos_col<=1):
        pass
#        print('不能向左移动')
    else:
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
    if(pos_col+pos_row_cnt>4):
        pass
#        print('不能向右移动')
    else:
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
    if(pos_row<=1):
        pass
#        print('不能向上移动')
    else:
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
    if(pos_row+pos_col_cnt>6):
        pass
#        print('不能向下移动')
    else:
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
    for yy in range(len(direct)):
        print(yy,direct[yy],end=' ')
    if len(direct) >= 2:
        direct = direct[int(input("\n please choose direct"))]
    else:
        direct = direct[0]

    if (direct == 'left'):
        role[master][5]=role[master][5]-1
    if (direct == 'right'):
        role[master][5]=role[master][5]+1
    if (direct == 'up'):
        role[master][4]=role[master][4]-1
    if (direct == 'down'):
        role[master][4]=role[master][4]+1
    return(role)


'''
for i in range(10):
    x=move_judge(i,role,result)
    print(x)

'''

def check_win(role):
    if(role[0][4]==5 and role[0][5]==2):
        return("Success!")
    
result=updatelocation(role)
prtresult(result)
while True:
    print('\n'*3)
    result=updatelocation(role)
    prtresult(result)
    print("\n\n")
    select = input('choose a item to move')
    if(select in "0123456789"):
       direct = move_judge(int(select),role,result)
       if(direct!=[]):
            role=move(int(select),role,direct,result)
            if(check_win(role)=="Success!"):
                print("\n Congratulations! You Win!")
                break
       else:
           print("cannot move, please choose again")
    elif (select =='x'):
        print('good bye')
        break
