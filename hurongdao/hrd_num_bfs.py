#使用BFS算法来解决数字华容道，但是这个空间巨大，需要运行非常久

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

# 移动 #
def move_step(parent_node, i, j, move_type):
    current_status = parent_node.data
    new_status = copy.deepcopy(current_status)
    if move_type == 'up': #up
        new_status[i][j] = current_status[i+1][j]
        new_status[i+1][j] = '0'
    elif move_type == 'down': #down
        new_status[i][j] = current_status[i-1][j]
        new_status[i-1][j] = '0'
    elif move_type == 'left': #left
        new_status[i][j] = current_status[i][j+1]
        new_status[i][j+1] = '0'
    elif move_type == 'right': #right
        new_status[i][j] = current_status[i][j-1]
        new_status[i][j-1] = '0'

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

# 寻找下一步的状态空间 #
def find_next_status(current_node):
    for i in range(len(current_node.data)):
        if '0' in current_node.data[i]:
            for j in range(len(current_node.data[i])):
                if current_node.data[i][j] == '0':
                    if i-1 >= 0:
                        move_step(current_node, i, j, 'down')
                    if i+1 < len(current_node.data):
                        move_step(current_node, i, j, 'up')
                    if j-1 >= 0:
                        move_step(current_node, i, j, 'right')
                    if j+1 < len(current_node.data[i]):
                        move_step(current_node, i, j, 'left')

#广度优先搜索算法#
def BFS(current_node):
    while not status_queue.empty():
        print('visit num = '+str(len(visit_list)))
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

