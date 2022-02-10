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
        
    role = []        #角色清单，用于保存各角色属性（长宽、位置等）
    history=[]       #历史角色清单的历史动作列表，用于游戏返回上一步
    orig=[]          #自动游戏时的初始局面
#    auto_play=False  #设置是否自动游戏，如果自动，则会使用openeded表、closed表


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
def prtresult(resultx):
    print("\n")
    for row in range(1,7):
        for col in range(1,5):
            print(resultx[row][col],end="")
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

    last_role=copy.deepcopy(role)
    if (direct == 'left'):
        last_role[master][5]=role[master][5]-1
    if (direct == 'right'):
        last_role[master][5]=role[master][5]+1
    if (direct == 'up'):
        last_role[master][4]=role[master][4]-1
    if (direct == 'down'):
        last_role[master][4]=role[master][4]+1
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
               next_role_list.append([next_role, this_role, x, direct, '', this_nodeid])
               
                     
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

def check_win(role):
    if(role[0][4]==5 and role[0][5]==2):
        return("Success!")

def check_match(orig,dest):
#作用：比较两种局型是否一致，包括6/7/8/9的位置，如果0-5位置相同，且6/7/8/9的组合位置相同，也认为两个局型一致，返回True。
#orig,dest的结构即role的结构
#如果orig与dest的0-5相同，但orig的6/7位置与dest8/9位置对调，也认为orig与dest相同。
    if(orig == dest):
        return True
    else:
        return False
    
def autoplay(role):
    global max_nodeid
    max_nodeid = 1
    global opened
    global closed
    opened =[]
    closed=[]
    opened.append([copy.deepcopy(role),'NULL','','',1,0])
    handleOpen()

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
    
    while True:
        if len(opened)==0:
                break
#        x=0
        for x in range(len(opened)):
#          print('opened updated, now is node No.:', opened[x][5])
#打印当前处理的node形状
#          result=updatelocation(opened[x][0])
#          prtresult(result)
          this_node = copy.deepcopy(opened[x])
          tmp = move_mult(this_node)
#          print(tmp)
#          print(opened)
#          print('tmp length is',len(tmp))
          for y in range(len(tmp)):
                  flag=False
                  
#检查新节点是否已经在open表中，如在将不添加
                  for jj in range(len(opened)):
#                        print('tmp[y][0]is',tmp[y][0])
#                        print('opened[x][0]is',opened[x][0])

#                        if tmp[y][0]==opened[jj][0]:
#原有判断还不够精细，需要增加同等项6/7/8/9四个小卒组合位置相同的，也认为是同一局型。
                        if(check_match（tmp[y][0],opened[jj][0]）==True):
                            flag=True
#                            print('falg opened set to True')


#检查新节点是否已经在closed表中，如在将不添加
                  for kk in range(len(closed)):
#                         print('tmp[',y,'][0]is',tmp[y][0])
#                         print('closed[',kk,'][0]is',closed[kk][0])

#                         if tmp[y][0]==closed[kk][0]:
#改为使用函数check_match
                        if(check_match（tmp[y][0],closed[kk][0]）==True):
                            flag=True
#                                print('falg close set to True')
                  if flag==False:
                      max_nodeid = max_nodeid +1
#统计分析的节点数量
#                      if max_nodeid%50>=0 and max_nodeid%50 < 1:
#                        print(int(max_nodeid/50)*50,'nodes get!')
#                        print('已完成：',len(closed),'剩余:',len(opened))                      
                      tmp[y][4]=max_nodeid
                      opened.append(tmp[y])
#                     print('新增节点',next_role, this_role, x, direct, max_nodeid, this_nodeid)
#                      print('新增open节点', tmp[y][5],':----',tmp[y][2],'move',tmp[y][3],'---->',tmp[y][4])
#                      tmp_pos=updatelocation(tmp[y][1])
#                      prtresult(tmp_pos)
#                      tmp_pos2=updatelocation(tmp[y][0])
#                      prtresult(tmp_pos2)
#                        print('add opened node',opened[-1])
#                  else:
#                        print('node',tmp[y][0], 'already exists in opened or closed!')

#检查是否成功
                  if(check_win(tmp[y])=="Success!"):
                    closed.append(opened[x])
                    closed.append(opened[-1])
                    opened.remove(opened[x])
#                    print('add close node',opened[x])
                    print('Totally',max_nodeid,'nodes ayalyzed,find the result.')
                    prtAnswer()
                    print('Success!')
                    exit("We find it!")
          closed.append(opened[x])
#          print(len(closed),'nodes closed!')
#          print('add close node',opened[x][5])
#          print('节点分析完毕，移入closed节点：', opened[x][4],'已完成：',len(closed),'剩余:',len(opened))
          if len(closed)%200>=0 and len(closed)%200 < 1:
              print('已完成：',len(closed),'剩余:',len(opened))   
              tmp_pos=updatelocation(opened[x][0])
              prtresult(tmp_pos)


#打印结果，方法是从close表最后一条开始，查找其前一个节点，
#直到前一节点为0，并将所有查到的序列写入step，打印出step
#即得到所有的变化过程。
def prtAnswer():
      step=[closed[-1]]
      nodePrt=closed[-1][4]
      while True:
            for x in range(len(closed)):
                  if nodePrt==closed[x][3]:
                        step.insert(0,closed[x])
                        nodePrt=closed[x][4]
            if nodePrt==0:
                  break            
      for x in range(len(step)):
            print('Step',x,':')
            prtNum(step[x][0])
      print('Finished!')
      time.sleep(10)
  

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
        select = input('Target: Move Caocao--0000--block to exit\n Choose an item to move，x to exit, b to back, a to autoplay: ')
    else:
        select = input('Target: Move Caocao--0000--block to exit\n Choose an item to move，x to exit, a to autoplay: ')
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
