import queue
import copy
import time

class Node:
    data = [] #当前位置
    hash_str = ''  #唯一值
    path = [] #完整的路径信息
    parent = None
    dir_str = ''

status_queue = queue.Queue()
visit_list = []

# 向上移动 #
def move_up(parent_node, i, j):
    current_status = parent_node.data
    new_status = copy.deepcopy(current_status)
    # 先判断是否可移动
    if current_status[i+1][j] == 0:
        return
    elif current_status[i+1][j] == 1:
        if j-1 >= 0 and current_status[i][j-1] == 0:
            if current_status[i+1][j-1] == 3:
                new_status[i][j-1] = 2
                new_status[i][j] = 1
                new_status[i+1][j-1] = 0
                new_status[i+1][j] = 0
            elif current_status[i+1][j-1] ==5:
                new_status[i][j-1] = 5
                new_status[i][j] = 1
                new_status[i+1][j-1] = 1
                new_status[i+1][j] = 1
                new_status[i+2][j-1] = 0
                new_status[i+2][j] = 0
            else:
                return
    elif current_status[i+1][j] == 2:
        new_status[i][j] = 2
        new_status[i+1][j] = 0
    elif current_status[i+1][j] == 4:
        if j+1 <= 3 and current_status[i][j+1] == 0:
            new_status[i][j] = 4
            new_status[i][j+1] = 1
            new_status[i+1][j+1] = 0
            new_status[i+1][j] = 0
        else:
            return
    elif current_status[i+1][j] == 3:
        new_status[i][j] = 3
        new_status[i+1][j] = 1
        new_status[i+2][j] = 0
    elif current_status[i+1][j] == 5:
        if j+1 <= 3 and current_status[i][j+1] == 0:
            new_status[i][j] = 5
            new_status[i][j+1] = 1
            new_status[i+1][j] = 1
            new_status[i+1][j+1] = 1
            new_status[i+2][j] = 0
            new_status[i+2][j+1] = 0
        else:
            return
    else:
        return

    # 生成节点，并入队列
    node = Node()
    node.data = new_status
    node.hash_str = ''.join([''.join(map(str, row)) for row in new_status])
    node.parent = parent_node
    node.dir_str = 'up ('+str(i)+','+str(j)+')'
    if node.hash_str in visit_list:
        return
    status_queue.put(node)
    visit_list.append(node.hash_str)

# 向左移动 #
def move_left(parent_node, i, j):
    current_status = parent_node.data
    new_status = copy.deepcopy(current_status)
    # 先判断是否可移动
    if current_status[i][j+1] == 0:
        return
    elif current_status[i][j+1] == 1 and current_status[i-1][j] == 0:
        if current_status[i-1][j+1] == 3:
            new_status[i-1][j] = 3
            new_status[i][j] = 1
            new_status[i-1][j+1] = 0
            new_status[i][j+1] = 0
        elif current_status[i][j+1] == 5:
            new_status[i-1][j] = 5
            new_status[i][j] = 1
            new_status[i-1][j+1] = 1
            new_status[i][j+1] = 1
            new_status[i-1][j+2] = 0
            new_status[i][j+2] = 0
        else:
            return
    elif current_status[i][j+1] == 2:
        new_status[i][j] = 2
        new_status[i][j+1] = 0
    elif current_status[i][j+1] == 3 and current_status[i+1][j] == 0:
        new_status[i][j] = 3
        new_status[i+1][j] = 1
        new_status[i][j+1] = 0
        new_status[i+1][j+1] = 0
    elif current_status[i][j+1] == 4:
        new_status[i][j] = 4
        new_status[i][j+1] = 1
        new_status[i][j+2] = 0
    elif current_status[i][j+1] == 5:
        if current_status[i+1][j] == 0:
            new_status[i][j] = 5
            new_status[i+1][j] = 1
            new_status[i][j+1] = 1
            new_status[i+1][j+1] = 1
            new_status[i][j+2] = 0
            new_status[i+1][j+2] = 0
        else:
            return
    else:
        return

    # 入队列
    node = Node()
    node.data = new_status
    node.hash_str = ''.join([''.join(map(str, row)) for row in new_status])
    node.parent = parent_node
    node.dir_str = 'left ('+str(i)+','+str(j)+')'
    if node.hash_str in visit_list:
        return
    status_queue.put(node)
    visit_list.append(node.hash_str)

# 向右移动 #
def move_right(parent_node, i, j):
    current_status = parent_node.data
    new_status = copy.deepcopy(current_status)

    if current_status[i][j-1] == 0:
        return
    elif current_status[i][j-1] == 1:
        if i-1 >= 0 and current_status[i-1][j-1] == 3 and current_status[i-1][j] == 0:
            new_status[i-1][j-1] = 0
            new_status[i][j-1] = 0
            new_status[i-1][j] = 3
            new_status[i][j] = 1
        elif j-2 >= 0 and current_status[i][j-2] == 4:
            new_status[i][j-2] = 0
            new_status[i][j-1] = 4
            new_status[i][j] = 1
        elif i-1 >= 0 and j-2 >= 0 and current_status[i-1][j-2] == 5 and current_status[i-1][j] == 0:
            new_status[i-1][j-2] = 0
            new_status[i][j-2] = 0
            new_status[i-1][j-1] = 5
            new_status[i][j-1] = 1
            new_status[i-1][j] = 1
            new_status[i][j] = 1
        else:
            return
    elif current_status[i][j-1] == 2:
        new_status[i][j-1] = 0
        new_status[i][j] = 2
    elif current_status[i][j-1] ==3 and current_status[i+1][j] == 0:
        new_status[i][j-1] = 0
        new_status[i+1][j-1] = 0
        new_status[i][j] = 3
        new_status[i+1][j] = 1
    else:
        return

    #
    node = Node()
    node.data = new_status
    node.hash_str = ''.join([''.join(map(str, row)) for row in new_status])
    node.parent = parent_node
    node.dir_str = 'right ('+str(i)+','+str(j)+')'
    if node.hash_str in visit_list:
        return
    status_queue.put(node)
    visit_list.append(node.hash_str)

# 向下移动 #
def move_down(parent_node, i, j):
    current_status = parent_node.data
    new_status = copy.deepcopy(current_status)
    #
    if current_status[i-1][j] == 0:
        return
    elif current_status[i-1][j] == 1:
        if i-2 >= 0 and current_status[i-2][j] == 3:
            new_status[i-2][j] = 0
            new_status[i-1][j] = 3
            new_status[i][j] = 1
        elif j-1 >= 0 and current_status[i-1][j-1] == 4 and current_status[i][j-1] == 0:
            new_status[i-1][j-1] = 0
            new_status[i-1][j] = 0
            new_status[i][j-1] = 4
            new_status[i][j] = 1
        elif i-2 >= 0 and j-1 >= 0 and current_status[i-2][j-1] == 5 and current_status[i][j-1] == 0:
            new_status[i-2][j-1] = 0
            new_status[i-2][j] = 0
            new_status[i-1][j-1] = 5
            new_status[i-1][j] = 1
            new_status[i][j-1] = 1
            new_status[i][j] = 1
        else:
            return
    elif current_status[i-1][j] == 2:
        new_status[i-1][j] = 0
        new_status[i][j] = 2
    elif current_status[i-1][j] == 4 and current_status[i][j+1] == 0:
        new_status[i-1][j] = 0
        new_status[i-1][j+1] = 0
        new_status[i][j] = 4
        new_status[i][j+1] = 1
    else:
        return
    #
    node = Node()
    node.data = new_status
    node.hash_str = ''.join([''.join(map(str, row)) for row in new_status])
    node.parent = parent_node
    node.dir_str = 'down ('+str(i)+','+str(j)+')'
    if node.hash_str in visit_list:
        return
    status_queue.put(node)
    visit_list.append(node.hash_str)

# 寻找下一步的状态空间 #
def find_next_status(current_node):
    for i in range(len(current_node.data)):
        if 0 in current_node.data[i]:
            for j in range(len(current_node.data[i])):
                if current_node.data[i][j] == 0:
                    if i-1 >= 0:
                        move_down(current_node, i, j)
                    if i+1 < len(current_node.data):
                        move_up(current_node, i, j)
                    if j-1 >= 0:
                        move_right(current_node, i, j)
                    if j+1 < len(current_node.data[i]):
                        move_left(current_node, i, j)

#广度优先搜索算法#
def BFS(current_node):
    while not status_queue.empty():
        current_node = status_queue.get()
        cr_state = ''.join([''.join(map(str, row)) for row in current_node.data])
        pa_state = ''
        if current_node.parent is not None:
            pa_state = ''.join([''.join(map(str, row)) for row in current_node.parent.data])
        print('parent state = ' +pa_state+', move '+current_node.dir_str+' to current state = '+cr_state)
        # print('visit node num=', len(visit_list))
        # 判断是否成功
        if current_node.data[3][1] == 5:
            print('success! find the final state')
            return current_node
        find_next_status(current_node)

# 打印状态图 #
def print_pic(status_list):
    pic_matrix = [
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
            ]
    for i in range(5):
        for j in range(4):
            if status_list[i][j] == 0:
                pic_matrix[i*2][j*2] = '  '
                pic_matrix[i*2+1][j*2] = '  '
                pic_matrix[i*2][j*2+1] = '  '
                pic_matrix[i*2+1][j*2+1] = '  '
            elif status_list[i][j] == 2:
                pic_matrix[i*2][j*2] = '|¯'
                pic_matrix[i*2+1][j*2] = '|_'
                pic_matrix[i*2][j*2+1] = '¯|'
                pic_matrix[i*2+1][j*2+1] = '_|'
            elif status_list[i][j] == 3:
                #
                pic_matrix[i*2][j*2] = '|¯'
                pic_matrix[i*2][j*2+1] = '¯|'
                #
                pic_matrix[i*2+1][j*2] = '| '
                pic_matrix[i*2+1][j*2+1] = ' |'
                #
                pic_matrix[i*2+2][j*2] = '| '
                pic_matrix[i*2+2][j*2+1] = ' |'
                #
                pic_matrix[i*2+3][j*2] = '|_'
                pic_matrix[i*2+3][j*2+1] = '_|'
            elif status_list[i][j] == 4:
                #
                pic_matrix[i*2][j*2] = '|¯'
                pic_matrix[i*2][j*2+1] = '¯¯'
                pic_matrix[i*2][j*2+2] = '¯¯'
                pic_matrix[i*2][j*2+3] = '¯|'
                #
                pic_matrix[i*2+1][j*2] = '|_'
                pic_matrix[i*2+1][j*2+1] = '__'
                pic_matrix[i*2+1][j*2+2] = '__'
                pic_matrix[i*2+1][j*2+3] = '_|'
            elif status_list[i][j] == 5:
                #第一行
                pic_matrix[i*2][j*2] = '|¯'
                pic_matrix[i*2][j*2+1] = '¯¯'
                pic_matrix[i*2][j*2+2] = '¯¯'
                pic_matrix[i*2][j*2+3] = '¯|'
                #第二行
                pic_matrix[i*2+1][j*2] = '| '
                pic_matrix[i*2+1][j*2+1] = '  '
                pic_matrix[i*2+1][j*2+2] = '  '
                pic_matrix[i*2+1][j*2+3] = ' |'
                #第三行
                pic_matrix[i*2+2][j*2] = '| '
                pic_matrix[i*2+2][j*2+1] = '  '
                pic_matrix[i*2+2][j*2+2] = '  '
                pic_matrix[i*2+2][j*2+3] = ' |'
                #第四行
                pic_matrix[i*2+3][j*2] = '|_'
                pic_matrix[i*2+3][j*2+1] = '__'
                pic_matrix[i*2+3][j*2+2] = '__'
                pic_matrix[i*2+3][j*2+3] = '_|'
    pic_str = ''
    for i in range(len(pic_matrix)):
        for j in range(len(pic_matrix[i])):
            pic_str += pic_matrix[i][j]
        pic_str += '\n'

    print(pic_str)

# 打印状态图，字母代替 #
def print_pic_1(status_list):
    pic_str = ''
    for i in range(len(status_list)):
        for j in range(len(status_list[i])):
            if status_list[i][j] == 0:
                pic_str += '  '
            elif status_list[i][j] == 1:
                if i == 0 and status_list[i][j-1] == 3:
                    pic_str += 'C '
                elif i == 0 and status_list[i][j-1] == 5:
                    pic_str += 'T '
                elif j == 0 and status_list[i-1][j] == 4:
                    pic_str += 'B '
                elif j == 0 and status_list[i-1][j] == 5:
                    pic_str += 'T '
                elif status_list[i-1][j] == 3:
                    pic_str += 'B '
                elif status_list[i][j-1] == 4:
                    pic_str += 'C '
                elif (i+1 <= 4 and status_list[i+1][j] == 1) or\
                        (i-1 >= 0 and status_list[i-1][j] == 1) or\
                        (i-1 >= 0 and status_list[i-1][j] == 5):
                    pic_str += 'T '
            elif status_list[i][j] == 2:
                pic_str += 'A '
            elif status_list[i][j] == 3:
                pic_str += 'B '
            elif status_list[i][j] == 4:
                pic_str += 'C '
            elif status_list[i][j] == 5:
                pic_str += 'T '
        pic_str += '\n'
    print(pic_str)


#----------------主函数------------------------
# init_str = '35131111341312212002'
# 空格 = 0
# 占位 = 1
# 1 X 1 = 2
# 2 X 1 = 3
# 1 X 2 = 4
# 2 X 2 = 5
init_str = '35131111341312212002'
init_status = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]]
# split status
for i in range(5):
    for j in range(4):
        init_status[i][j] = int(init_str[i*4+j])
print_pic(init_status)

# 根节点初始化
node = Node()
node.data = init_status
node.hash_str = ''.join([''.join(map(str, row)) for row in init_status])

#根节点入队列
status_queue.put(node)
visit_list.append(node)

#BFS搜索最终状态
final_node = BFS(node)

#----恢复路径-------
show_node = final_node
show_queue = queue.LifoQueue()
while show_node is not None:
    show_queue.put(show_node)
    show_node = show_node.parent

while not show_queue.empty():
    show_node = show_queue.get()
    print('Move '+show_node.dir_str+' to current state = ')
    print_pic(show_node.data)

