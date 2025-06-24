##启发式搜索算法接数字华容道，代码还没有优化完

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
map_list = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
            'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15, '0':16}

def step_cost(current_status):
    cost = 0
    for i in range(len(current_status)):
        for j in range(len(current_status[i])):
            if current_status[i][j] != '0':
                x = (map_list[current_status[i][j]] - 1) // 4
                y = (map_list[current_status[i][j]] -1) % 3
                cost += abs(x -i) + abs(y - j)
    return cost

def in_queue(parent_node, new_status, move_type):
    # 生成节点，并入队列
    node = Node()
    node.data = new_status
    node.hash_str = ''.join([''.join(map(str, row)) for row in new_status])
    node.parent = parent_node
    node.dir_str = move_type+' ('+str(i)+','+str(j)+')'
    if node.hash_str in visit_list:
        return
    status_queue.put(node)
    visit_list.append(node.hash_str)

# 移动 #
def move_step(parent_node, i, j):
    current_status = parent_node.data
    distance_up = distance_down = distance_right = distance_left = 100000000000
    if i+1 < len(current_status): #up
        new_status = copy.deepcopy(current_status)
        new_status[i][j] = current_status[i+1][j]
        new_status[i+1][j] = '0'
        hash_str = ''.join([''.join(map(str, row)) for row in new_status])
        if hash_str not in visit_list:
            distance_up = step_cost(new_status)
    if i-1 >= 0: #down
        new_status = copy.deepcopy(current_status)
        new_status[i][j] = current_status[i-1][j]
        new_status[i-1][j] = '0'
        hash_str = ''.join([''.join(map(str, row)) for row in new_status])
        if hash_str not in visit_list:
            distance_down = step_cost(new_status)
    if j+1 < len(current_status[i]): #left
        new_status = copy.deepcopy(current_status)
        new_status[i][j] = current_status[i][j+1]
        new_status[i][j+1] = '0'
        hash_str = ''.join([''.join(map(str, row)) for row in new_status])
        if hash_str not in visit_list:
            distance_left = step_cost(new_status)
    if j-1 >= 0: #right
        new_status = copy.deepcopy(current_status)
        new_status[i][j] = current_status[i][j-1]
        new_status[i][j-1] = '0'
        hash_str = ''.join([''.join(map(str, row)) for row in new_status])
        if hash_str not in visit_list:
            distance_right = step_cost(new_status)

    min_num = min([distance_up, distance_down, distance_right, distance_left])
    if min_num == 100000000000:
        return
    print('min num='+str(min_num), distance_up, distance_down, distance_right, distance_left)
    if min_num == distance_up:
        new_status = copy.deepcopy(current_status)
        new_status[i][j] = current_status[i+1][j]
        new_status[i+1][j] = '0'

        in_queue(parent_node, new_status, 'up')

    if min_num == distance_down:
        new_status = copy.deepcopy(current_status)
        new_status[i][j] = current_status[i-1][j]
        new_status[i-1][j] = '0'

        in_queue(parent_node, new_status, 'down')

    if min_num == distance_right:
        new_status = copy.deepcopy(current_status)
        new_status[i][j] = current_status[i][j-1]
        new_status[i][j-1] = '0'

        in_queue(parent_node, new_status, 'right')

    if min_num == distance_left:
        new_status = copy.deepcopy(current_status)
        new_status[i][j] = current_status[i][j+1]
        new_status[i][j+1] = '0'

        in_queue(parent_node, new_status, 'left')


# 寻找下一步的状态空间 #
def find_next_status(current_node):
    for i in range(len(current_node.data)):
        if '0' in current_node.data[i]:
            for j in range(len(current_node.data[i])):
                if current_node.data[i][j] == '0':
                    move_step(current_node, i, j)

#广度优先搜索算法#
def BFS(current_node):
    while not status_queue.empty():
        print('visit num = '+str(len(visit_list)))
        print('queue size='+str(status_queue.qsize()))
        current_node = status_queue.get()
        cr_state = ''.join([''.join(map(str, row)) for row in current_node.data])
        pa_state = ''
        if current_node.parent is not None:
            pa_state = ''.join([''.join(map(str, row)) for row in current_node.parent.data])
        print('parent state = ' +pa_state+', move '+current_node.dir_str+' to current state = '+cr_state)
        # print('visit node num=', len(visit_list))
        # 判断是否成功
        if cr_state == '123456789ABCDEF0':
            print('success! find the final state')
            return current_node
        find_next_status(current_node)

def print_pic(status_list):
    pic_str = ''
    for i in range(len(status_list)):
        for j in range(len(status_list[i])):
            if status_list[i][j] == '0':
                pic_str += ' '
            else:
                pic_str += status_list[i][j]
        pic_str += '\n'
    print(pic_str)


#----------------主函数------------------------
# 123456789ABCDEF0
init_str = '1238504C6B7F9DAE'
init_status = [
        ['','','',''],
        ['','','',''],
        ['','','',''],
        ['','','','']]
# split status
for i in range(4):
    for j in range(4):
        init_status[i][j] = init_str[i*4+j]
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

