#!python
import copy
import time

##Author: Lijun 
#
#History:
#V0.5   2022-01-19
#1)修订此前的地图错误，标准华容道只能是5行4列，出口在第6行2/3列，但游戏中角色不可以通过那两个中转，
#因此需要相应修改计算办法。如可以中转则经典‘横刀立马’只需38步即可完成，而不是标准的81步。
#2)完成上述修订后，发现当前算法得到的“横道立马”需要的步数比标准的81步多，不是最优解，需要修改相应算法。
#解决办法是：
#A、增加一个字典，保存每个role状态的对应的距离初始状态的移动步数、以及当前步数条件下的上一个role。
#key值是role，因为字典key不支持list形式，因此考虑将role类型变为字符串形式；value的值是当前role距离初始值的最小
#步数（距离值），在当前最小步数情况下的前一role，以及从前一role到本role需要移动的角色和移动方向。
#B、在处理open表的时候，每次从前一role产生一个新role的时候，则检查字典，如果该role在字典中不存在，则根据前一
#role的距离值+1算得新role的距离值，存入字典；如果已在字典中存在、且新距离值比role小，则更新字典中的距离和前一role
#C、等所有节点全都计算完成后，从字典中最后成功状态role（可能有多个）中找出距离值最小的一个，然后由这个role在字典中
#倒查出到初始状态的最短路径，将相关内容存储成列表即得到最短的路径。
#D、原有的node数据结构仍可保留，但原有流程在找到一个成功结果即停止计算的方式需要改变，变为计算完所有节点再比较后
#得到最短路径。
#涉及修改内容：1、引入字典结构；2、处理open表时，新生成node情况下，更新字典结构；3、修改open表处理方式，需要处理
#完所有node；4、修改产生和打印最终结果的方式（基于字典而不是基于closed表）。
#
#
#V0.4   2022-01-18
#增加功能：1）在运行过程中增加“自动完成”功能，可以自动模拟完成并打印结果。
#
#V0.3   2021-12-18
#增加功能：增加初始场景，游戏可以从多个初始场景中选择1个。
#
#V0.2   2021-12-16
#增加功能：返回上一步；返回上一步后，删除本步骤、上一步变为最后一步；如果没有上一步则菜单不显示
#V0.1   2021-12-15
#实现基础功能：一种初始化图形，可以人工操作游戏，游戏成功有提示
##
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
        
    role = []        #角色清单，用于保存各角色属性（长宽、位置等）
    history=[]       #历史角色清单的历史动作列表，用于游戏返回上一步
    orig=[]          #自动游戏时的初始局面
#    auto_play=False  #设置是否自动游戏，如果自动，则会使用openeded表、closed表


#初始化游戏地图，设定各角色的位置。
def init_map():
    while True:
        map = input('''Welcome to HuaRongDao, Please choose a map to play:
    1、横刀立马(81)
    2、齐头并前
    3、兵分三路
    4、屯兵东路
    5、左右布兵
    6、前挡后阻
    7、测试地图
    8、测试地图2
    9、测试地图3
    请输入(1-9)：''')

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
            #操操马张
            #赵黄超飞
            #云忠卒卒
            #卒    卒
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
        elif(map==7):
            #7、测试地图
            #关羽马张    
            #赵黄超飞
            #云忠
            #卒曹曹卒
            #卒操操卒
            role.append(['0','Caocao',2,2,4,2])
            role.append(['1','Guanyu',2,1,1,1])
            role.append(['2','Zhangfei',1,2,1,4])
            role.append(['3','Zhaoyun',1,2,2,1])
            role.append(['4','Machao',1,2,1,3])
            role.append(['5','Huangzhong',1,2,2,2])
            role.append(['6','xiaozu',1,1,4,1])
            role.append(['7','xiaozu',1,1,4,4])
            role.append(['8','xiaozu',1,1,5,1])
            role.append(['9','xiaozu',1,1,5,4])
            return
        elif(map==8):
            #8、测试地图2
            #关羽马张    
            #赵黄超飞
            #云忠
            #曹曹卒卒
            #操操卒卒
            role.append(['0','Caocao',2,2,4,1])
            role.append(['1','Guanyu',2,1,1,1])
            role.append(['2','Zhangfei',1,2,1,4])
            role.append(['3','Zhaoyun',1,2,2,1])
            role.append(['4','Machao',1,2,1,3])
            role.append(['5','Huangzhong',1,2,2,2])
            role.append(['6','xiaozu',1,1,4,3])
            role.append(['7','xiaozu',1,1,4,4])
            role.append(['8','xiaozu',1,1,5,3])
            role.append(['9','xiaozu',1,1,5,4])
            return
        elif(map==9):
            #9、测试地图3
            #关羽马张    
            #赵黄超飞
            #云忠
            #曹曹卒卒
            #操操卒卒
            role.append(['0', 'Caocao', 2, 2, 1, 2])
            role.append(['1', 'Guanyu', 2, 1, 3, 2])
            role.append(['2', 'Zhangfei', 1, 2, 1, 1])
            role.append(['3', 'Zhaoyun', 1, 2, 3, 1])
            role.append(['4', 'Machao', 1, 2, 1, 4])
            role.append(['5', 'Huangzhong', 1, 2, 3, 4])
            role.append(['6', 'xiaozu', 1, 1, 6, 3])
            role.append(['7', 'xiaozu', 1, 1, 5, 3])
            role.append(['8', 'xiaozu', 1, 1, 6, 2])
            role.append(['9', 'xiaozu', 1, 1, 5, 4])
            return
        else:
            print("\nWrong selection!")

#根据地图位置更新各角色站位结果
def updatelocation(rolex):    
    result = [['x' for i in range(5)] for j in range(6)]
    for x in rolex:
    #    print(x)
#        print('rolex is:',rolex)
        row = x[4]
        for rowcnt in range(x[3]):
            col = x[5]
            for colcnt in range(x[2]):
    #            print(row,col)
                result[row][col]=x[0]
                col = col +1
            row = row +1
    return(result)

#根据role打印各角色站位结果
def prtresult(resultx):
    print("\n")
    for row in range(1,6):
        for col in range(1,5):
            print(resultx[row][col],end="")
        print('')

#根据role_to_str结果打印各角色站位结果
def prtresult_str(role_to_str):
    print("\n")
    for i in range(5):
        for j in range(4):
            print(role_to_str[i*4+j],end='')
        print()

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
def move_judge(master,rolex):
#获取各角色的xy坐标、以及宽度、高度
    pos_row=rolex[master][4]
    pos_col=rolex[master][5]
    pos_row_cnt=rolex[master][2]
    pos_col_cnt=rolex[master][3]

#更新节点位置
    result=updatelocation(rolex)
#    prtresult(result)

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
#        print(master, "can move left!")
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
#        print(master,"can move right!")
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
#        print(master,"can move up!")
        direct.append("up")
#        return("up")

#判断是否能向下移动
    down_flag='F'
#角色的当前y坐标加上高度大于6则不能下移
    if(pos_row+pos_col_cnt>5):
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
#        print(master,"can move down!")
        direct.append("down")
        
#    if(len(direct)>0):
#        print('this time:',master,'can move',direct)
    return(direct)


#移动
def move(master,rolex,direct,result):
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

    last_role=copy.deepcopy(rolex)
    if (direct == 'left'):
        last_role[master][5]=rolex[master][5]-1
    if (direct == 'right'):
        last_role[master][5]=rolex[master][5]+1
    if (direct == 'up'):
        last_role[master][4]=rolex[master][4]-1
    if (direct == 'down'):
        last_role[master][4]=rolex[master][4]+1
    print(last_role)
    return(last_role)

def move_mult(posit):
#用于自动化情况下,从过一种局面产生该局面下可移动角色变成的几种后续局面
#输入是opened表中的一个数据，如下，
#[当前role，前一role，移动角色，移动方向，当前局面nodeid，前一局面nodeid]
#输出数据结构也是上面结构形成的list，list的任一元素也即opened表的数据元素形式：
#其中role局面的数据结构：
#role[id,name,width,height,loc_row,loc_col]
#代号，名字，宽度，高度，左上角行位置，左上角列位置
#id范围0-9分别代表各种角色

#0、初始化
    global opened
    global closeed
    next_role_list=[]
    this_role = copy.deepcopy(posit[0])  #当前局面
    this_nodeid = posit[4]  #当前局面nodeid
    
#1、检查各角色哪些可以移动，分别向什么方向移动
    for x in range(0,10):
        all_direct=move_judge(x,this_role)
        if(len(all_direct)<1):
           pass

#2、如果可以移动，则执行移动，并生成所有新局面列表
        else:
           for y in range(len(all_direct)):
               next_role = copy.deepcopy(this_role)
               direct = all_direct[y]
               if (direct == 'left'):
                   next_role[x][5]=next_role[x][5]-1
               if (direct == 'right'):
                   next_role[x][5]=next_role[x][5]+1
               if (direct == 'up'):
                   next_role[x][4]=next_role[x][4]-1
               if (direct == 'down'):
                   next_role[x][4]=next_role[x][4]+1
               next_role_list.append([next_role, this_role, x, direct, '', this_nodeid,0]) #next nodeid set to null
                             
                     
#3、返回当前局面所有下一条局面清单
#    print('next_role_list:')
#    for x in range(len(next_role_list)):
#        print(next_role_list[x])
    return(next_role_list)   

'''
for i in range(10):
    x=move_judge(i,role)
    print(x)

'''

def check_win(rolex):
    if(rolex[0][4]==4 and rolex[0][5]==2):
        return("Success!")
    else:
        return("Fail!")

def check_match(orig,dest):
#作用：比较两种局型是否一致，
#包括2/3/4/5(关张马黄）的位置，如果1-2相同，但2/3/4/5组合相同，也认为等价相同。
#包括6/7/8/9的位置，如果0-5等价相同，且6/7/8/9的组合位置相同，也认为两个局型一致，返回True。
#orig,dest的结构即role的组结构,由0-9共10个如下的单个角色的list构成：
#role[id,name,width,height,loc_row,loc_col]
#代号，名字，宽度，高度，左上角行位置，左上角列位置

#v0:粗略的比较方式
    if(orig == dest):
        return(True)
    else:
        return(False)
#v1:精确对比
'''
#v1:增加了2-9准确匹配的方式方式
    chkflag = True
#先看0-1（曹操关羽）是否一致，如果有一个不同直接返回不一致
    for cnt in range(0,2):
       if(orig[cnt] != dest[cnt]):
#            print('orig is: dest is:',orig[cnt],dest[cnt])
            chkflag = False
            return(chkflag)

#然后看2-5，方法是取2-5所有4个元素的xy坐标位置，然后获得乘数，如果乘数相同则4个位置的组合是匹配的
    product1 = 1
    product2 = 1
    for cnt in range(2,6):
#            print(orig[cnt][4]*10+orig[cnt][5],dest[cnt][4]*10+orig[cnt][5])
            product1 = product1 * (orig[cnt][4]*10+orig[cnt][5])
            product2 = product2 * (dest[cnt][4]*10+dest[cnt][5])
#    print('product1,product2',product1,product2)
    if(product1 != product2):
            chkflag = False
            return(chkflag)
    
#然后看6-9，方法是取6-9所有4个元素的xy坐标位置，然后获得乘数，如果乘数相同则4个位置的组合是匹配的
    product1 = 1
    product2 = 1
    for cnt in range(6,10):
#            print(orig[cnt][4]*10+orig[cnt][5],dest[cnt][4]*10+orig[cnt][5])
            product1 = product1 * (orig[cnt][4]*10+orig[cnt][5])
            product2 = product2 * (dest[cnt][4]*10+dest[cnt][5])
#    print('product1,product2',product1,product2)
    if(product1 != product2):
            chkflag = False
#    if(orig!=dest):
#       print('two equals\n',orig,'\n',dest)
    return(chkflag)
'''
def diff(node):
#这是一个判决函数，用来判断当前node与最终结果的差距，差值越小表明效果越好
#输入类型是role
#思路：
#1、曹操（role的第0条）的位置越接近目标位置（6,2）越好，考虑x或y每差1增加150.
#当曹操y<4时，曹操最好在边上、方便往下移动，因此x为2时额外增加100（1/3不用）.
#2、关羽（role的第1条）的位置，靠边比中间好，也就是x=1或x=3时，值为0；为2时，增加200.
#3、如果关羽在曹操的下方，则增加150（关羽横坐标与曹操相同）
#4、张赵马黄越靠上越好，考虑每向下1格，增加50
#5、如果出口的两个格子的任意一个被占用，则增加10（两个则增加20）
    
    diff_value = 0
#    print('node[0],node[1]',node[0],node[1])
    cc_loc_x = node[0][4]
    cc_loc_y = node[0][5]
    gy_loc_x = node[1][4]
    gy_loc_y = node[1][5]
    zf_loc_x = node[2][4]
    zy_loc_x = node[3][4]
    mc_loc_x = node[4][4]
    hz_loc_x = node[5][4]
    
    diff_value = diff_value + (4-cc_loc_x)*300
    diff_value = diff_value + gy_loc_x * 150
    diff_value = diff_value + (zf_loc_x+zy_loc_x+mc_loc_x+hz_loc_x)*50

    if(cc_loc_x <= 4):
        if(cc_loc_y==2):
            diff_value= diff_value + 50
    else:
        if(cc_loc_y==1):
            diff_value = diff_value + 50
        elif(cc_loc_y==3):
            diff_value = diff_value + 50
#判断出口两个格子是否被占用,只有在曹操比较靠下的时候才判断
        result = updatelocation(node)
        for col in range(2,4):
    #        print(result[6][col])
            if(result[6][col]!='x'):
                  diff_value = diff_value + 25        
#如果关羽在曹操下层，则关羽的位置很重要
    if(gy_loc_x > cc_loc_x):          
        if(gy_loc_x==cc_loc_x+1 and gy_loc_y==cc_loc_y):
            diff_value = diff_value + 100
        if(gy_loc_y==2):
            diff_value = diff_value + 100
        
    return(diff_value)
	
def autoplay(role):
    global max_nodeid
    max_nodeid = 1
    global opened
    global closed
    global distance
    global oklist   #计算最短距离时，保存多个成功结果的node局型
    global distance #计算最短距离时，保存各role距离初始值信息的字典
    opened =[]
    closed=[]
    oklist=[]
    distance={}
#节点的定义：
#包含局势role（0-9共10个角色信息构成的list，）（列表）、前一局势role（列表）、前面到本局势的移动角色\
#角色的移动方向(字符串）、当前局势nodeid（数值）、前一局面nodeid（数值）、局势diff值(数值，diff函数计算）
    orig_node = [copy.deepcopy(role),'','','',1,0,diff(copy.deepcopy(role))]
    opened.append(orig_node)
#    print('add to opened:',opened[-1])
#添加到字典
    handleDict(orig_node)
    handleOpen()

#A*算法，根据diff值将diff值小的内容插入到open表的前面，node的最后一项就是diff值
def addOpen(node):
#    print('node diff, last diff',node[6], opened[-1][6])
    if(len(opened)==0 or node[6]>=opened[-1][6]):
        opened.append(node)
#        print('append opened',node)
#        print('new opened is:',opened)
#        result=updatelocation(node[0])
#        prtresult(result)            
    else:
        for i in range(len(opened)):
            if(node[6]<opened[i][6]):
#                print('lenth is opened is:',len(opened),'this node is:',node[0],'nodeid is:',node[4],'diff is:',node[6])
#                print('insert opened',node)
                opened.insert(i,node)
                break

#A*算法，通过定义字典保存不同role距离初始role的步数距离,随时更新各role的最小距离，以帮助得到最短路径
#字典数据结构定义：{role_str:[从初始role到当前role的最小步数(数字),最小步数情况下的前一role(字符串形式),前一role到本role的
#移动角色(字符串形式），角色的移动方向(字符串）
#输入参数是新局型的node
#需要用到role_to_str函数，实际是通过updatelocation(role)得到二位数组result，然后将其每一位取出合并变为字符串，例如：
#2004
#2004
#3115
#3675
#8xx9
#变为：'20042004311536758xx9'
def role_to_str(rolex):
    if(rolex==''):
        return('')        
    result = updatelocation(rolex)
#    print('result is:',result)
    result_new = ''
    for i in range(1,6):
        for j in range(1,5):
            result_new = result_new + result[i][j]
#    print('result_new is:',result_new,type(result_new))
    return(result_new)

def handleDict(nodex):
    global distance
    new_role_str=role_to_str(nodex[0])
#    print('new_role_str is:',new_role_str)
    if(nodex[1]!=''):
        old_role_str=role_to_str(nodex[1])
    else:
        old_role_str=''        
    if((new_role_str in distance) == False):
#如果新role在字典不存在，则添加进distance字典.如字典为空，则第一个加入的距离为0；否则距离是该节点的前一节点距离+1.
#        print('here')
        if(len(distance)==0):
#            print('here1')
            distance[new_role_str]=[0,old_role_str,nodex[2],nodex[3]]  #将第一个role的距离设置为0
#            print('distance is:',distance)
        else:
#            print('here 2')
            distance[new_role_str]=[distance[old_role_str][0]+1,old_role_str,nodex[2],nodex[3]] #更新距离为前一节点+1（假设前节点存在）
    else:
#        print('there')
#        print('distance is:',distance)
#        print('distance[new_role_str][0] and distance[old_role_str][0]+1 are:', distance[new_role_str][0],distance[old_role_str][0]+1)
        if (distance[new_role_str][0]>distance[old_role_str][0]+1):
#如果新role在字典存在、但distance比新计算的大，则更新字典
            print('distance update, from',distance[new_role_str][0], 'to', distance[old_role_str][0]+1)
            distance[new_role_str]=[distance[old_role_str][0]+1,old_role_str,nodex[2],nodex[3]]
            

#用于处理Open表
#方法是：如果Open表非空，则：
#1）按照顺序对open表的每个角色进行所有方向的移动，
#将移动后的新状态节点添加进open表；如果过程中找到了满足条件
#的目的状态节点，则停止处理并返回打印结果；
#如果新获得的序列已存在与open、close表，则不再添加。
#2）将该节点加入close表；
#3）从open表中删除该节点；
#
#open表格式：当前role，前一role，移动角色，移动方向，当前局面nodeid，前一局面nodeid
def handleOpen():
    global opened
    global closed
    global max_nodeid
    global begin_time
    global end_time
    global oklist

    begin_time = int(time.time())
    
    while True:
          if len(opened)==0:
                break

#如果用A* 算法，就每次从0开始，否则用下句的for循环
          x=0
#        for x in range(len(opened)):
          tmpOpen=copy.deepcopy(opened[x])

#          print('opened updated, now is node No.:', opened[x][5])
#打印当前处理的node形状
#          result=updatelocation(opened[x][0])
#          prtresult(result)
          this_node = copy.deepcopy(opened[x])

#tmp包含的是当前被分析节点可能的所有后续node的列表
          tmp = move_mult(this_node)
#          print(tmp)
#          print(opened)
#          print('tmp length is',len(tmp))
          remove_flag = False
          for y in range(len(tmp)):
#将每个新的node更新到dict。
                  handleDict(tmp[y])
#flag是是否添加到open表的标记。
                  flag=False
                  
#检查新节点是否已经在open表中，如在将不添加
                  for jj in range(len(opened)):
#                        print('tmp[y][0]is',tmp[y][0])
#                        print('opened[x][0]is',opened[x][0])

#                        if tmp[y][0]==opened[jj][0]:
#原有判断还不够精细，需要增加同等项6/7/8/9四个小卒组合位置相同的，也认为是同一局型。
                        if(check_match(tmp[y][0],opened[jj][0])==True):
                            flag=True
#                            print('flag opened set to True','tmp =','open[',jj,']=',tmp[y][0])
#                            print('role is',role)
#                            print('opened is',opened)
                        
#检查新节点是否已经在closed表中，如在将不添加
                  for kk in range(len(closed)):
#                         print('tmp[',y,'][0]is',tmp[y][0])
#                         print('closed[',kk,'][0]is',closed[kk][0])
#                         if tmp[y][0]==closed[kk][0]:
#改为使用函数check_match
                        if(check_match(tmp[y][0],closed[kk][0])==True):
                            flag=True
#                            print('falg close set to True')
                
                  if(flag==False):
                      max_nodeid = max_nodeid +1
#统计分析的节点数量
#                      if max_nodeid%50>=0 and max_nodeid%50 < 1:
#                        print(int(max_nodeid/50)*50,'nodes get!')
#                        print('已完成：',len(closed),'剩余:',len(opened))                      
                      tmp[y][4]=max_nodeid      #将新生成的节点赋上nodeid编号
                      tmp[y][6]=diff(tmp[y][0]) #将新生成的节点的最后一位补充上diff值
#参考前行“next_role_list.append([next_role, this_role, x, direct, '', this_nodeid,0]) #next nodeid set to null"

#A*算法用addOpen，A算法用open.append
#                      opened.append(tmp[y])
#                      print('tmp[y] is:',tmp[y])
                      addOpen(tmp[y])
#                     print('新增节点',next_role, this_role, x, direct, max_nodeid, this_nodeid)
#                      print('新增open节点', tmp[y][5],':----',tmp[y][2],'move',tmp[y][3],'---->',tmp[y][4])
#                      tmp_pos=updatelocation(tmp[y][1])
#                      prtresult(tmp_pos)
#                      tmp_pos2=updatelocation(tmp[y][0])
#                      prtresult(tmp_pos2)
#                      print('add opened node',tmp[y][0])
#                  else:
#                      print('node',tmp[y][0], 'already exists in opened or closed!')
#检查是否成功
                  if(check_win(tmp[y][0])=="Success!"):
                    print('Success，find one result!ID:',tmp[y][5])
                    tmp_pos=updatelocation(tmp[y][0])
                    prtresult(tmp_pos)
                    oklist.append(tmp[y])
#                    print('final is:',tmp[y])
#                    print('opened[0] is:',opened[0])
#                    closed.append(tmpOpen)
##                    print('add to closed:',opened[0])
                    opened.remove(tmp[y])
                    closed.append(tmp[y])
#                    print('add to closed:',tmp[y])                    

#需要分析得到最短路径时，下面部分注释掉，如只要得到第一个结果，这部分保留
#                    opened.remove(opened[0])
##                    print('add close node',opened[x])
#                    print('Totally',max_nodeid,'nodes ayalyzed,find the result.')
#                    print('已完成：',len(closed),'剩余:',len(opened),'diffold:',tmpOpen[6],'diffnew:',tmp[y][6])
#                    print('closed is:',closed)
#                    prtAnswer(closed)
#                    print('Success!')
#                    end_time = int(time.time())
#                    print('Caculating time:',end_time-begin_time,'seconds.')
#                    exit("We find it!")

           
          closed.append(tmpOpen)
          opened.remove(tmpOpen)
          if(len(oklist)>=1):
              break
#          print(len(closed),'nodes closed!')
#          print('add close node',opened[x][5])
#          print('节点分析完毕，移入closed节点：', opened[x][4],'已完成：',len(closed),'剩余:',len(opened))
          if((len(closed)+len(opened))%100>=0 and (len(closed)+len(opened))%100<1):
              print('已完成：',len(closed),'剩余:',len(opened),'diffold:',tmpOpen[6],'diffnew:',opened[0][6])   
              tmp_pos=updatelocation(tmpOpen[0])
              prtresult(tmp_pos)
##需要分析得到最短路径时，下面部分注释掉，如只要得到第一个结果，这部分保留
#'''
#    else:
#        print('No answer!')
#        end_time = int(time.time())
#        print('Caculating time:',end_time-begin_time)
#'''
    end_time = int(time.time())
    print('Caculating time:',end_time-begin_time)
    if(len(oklist)==0):
        print('No answer!')
    else:
        print(len(oklist),'result(s) found!')
        prtAnswerShort(oklist,distance)        

#打印结果，方法是从close表最后一条开始，查找其前一个节点，
#直到前一节点为0，并将所有查到的序列写入step，打印出step
#即得到所有的变化过程。
#node: [当前role，前一role，移动角色，移动方向，当前局面nodeid，前一局面nodeid,diff]
def prtAnswer(closed):
      step=[closed[-1]]
#      print('closed is:',closed)
#      print('Step is:',step)
      nodePrt=closed[-1][5]   #最后节点父节点的ID
#      print('prt nodeid is:',nodePrt)
      while True:
            for x in range(len(closed)):
                  if(nodePrt==closed[x][4]):    #从closed表找上一节点的父节点，即节点ID等于后一节点父节点ID
                        step.insert(0,closed[x])
#                        print('Step is:',step)
                        nodePrt=closed[x][5]    #更新父节点ID
            if(nodePrt==0):
                  break
      print('\n Totally',len(step),' steps, as below:')
      for x in range(len(step)):
            print('\nStep',x,', id:',step[x][4],end='')
            if(x==0):
                print('(Begin)',end='')
            if(x==len(step)-1):
                print('(Final)')
            if(x%5==0 or x==len(step)-1):
                result = updatelocation(step[x][0])
                prtresult(result)
            if(x<len(step)-1):
                print('     ----',step[x+1][2],'move', step[x+1][3],'---->',end='')
#      print('Finished!')


#打印最短路径，方法是从oklist找出所有的成功最终状态，然后从distance中找出从这些最终状态到最初状态的序列、并打印出来。
def prtAnswerShort(oklist,distance):
#找到每个成功状态的序列，把序列的role_to_str存入solution数组
    solution = []
    for i in range(len(oklist)):
#        print('distance is',distance)
#        print('solution is:',solution)
        solution.append([])
#        print('solution is:',solution)
        print('oklist[',i,'] is', oklist[i])
        current_role_str = role_to_str(oklist[i][0])
        print('current_role_is:',current_role_str)
        while True:
            solution[i].insert(0,current_role_str)
#            print('i=',i,'solution[',i,'is:',solution[i])
            if(distance[current_role_str][1] in distance):
#                print('last_role_str is in distance')
                last_role_str = distance[current_role_str][1]
                current_role_str = last_role_str
            else:
#                print('last_role_str:',distance[current_role_str][1],'is not in distance')
#                if(distance[current_role_str][0]!=0):
#                    print('ditance[',current_role_str,']=',distance[current_role_str][0],'but no last_role found!')
#                    print('Something Wrong, first step is not orig.')
                break
#打印所有成功序列
    max_length = 999
    max_length_no = 999                        
    for i in range(len(oklist)):
        print('Solution No.',i,':')
        if len(oklist[i]) < max_length:
            max_length = len(oklist[i])-1
            max_length_no = i
        for j in range(len(solution[i])):
            print('\nStep',j,end='')
            if(j==0):
                print('(Begin)',end='')
            if(j==len(solution[i])-1):
                print('(Final)')
            if(j%5==0 or j==len(solution[i])-1):
                prtresult_str(solution[i][j])
            if(j<len(solution[i])-1):
                print('     ----',distance[solution[i][j+1]][2],'move', distance[solution[i][j+1]][3],'---->',end='')
    print('Solution No.',max_length_no, 'is the shortest solution,totally',max_length,'steps!')   

#主程序    
#result=updatelocation(role)
#prtresult(result)
print('\n')
init_conf()
init_map()
while True:
    result=updatelocation(role)
    prtresult(result)
    role_to_str(role)
    print("\n\n")
    if(len(history)>1):
        select = input('Target: Move Caocao--0000--block to exit\n Choose an item to move，x to exit, b to back, a to autoplay: ')
    else:
        select = input('Target: Move Caocao--0000--block to exit\n Choose an item to move，x to exit, a to autoplay: ')
    if(select=='b' or select=='B'):
        if(len(history)>1):
            print('before:',history)
            history.pop()
            print('after:',history)
            rolex=copy.deepcopy(history[-1])
            print('last:',rolex)
        else:
            print("\n cannot go back, please choose again")
    elif(select in "0123456789"):
       direct = move_judge(int(select),role)
       if(direct!=[]):
            role=move(int(select),role,direct,result)
            history.append(copy.deepcopy(role))
            if(check_win(role)=="Success!"):
                print("\n Congratulations! You Win!")
                break
       else:
           print("\n cannot move, please choose again")
    elif(select=='a' or select=='A'):
        auto_play=True
        autoplay(role)
        break
    elif (select =='x' or select=='X'):
        print('good bye')
        break
