#!python
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
result = [['x' for i in range(5)] for j in range(7)]

#初始化武将位置
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

#根据位置更新站位结果
def updatelocation(role,result):
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

#打印站位结果
def prtresult(result):
    for row in range(1,7):
        for col in range(1,5):
            print(result[row][col],end="")
        print('')
    return

def prtmenu():
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
prtmenu()            
updatelocation(role,result)
prtresult(result)
