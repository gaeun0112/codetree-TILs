from collections import deque
from copy import deepcopy

answer = 0

n, m = map(int, input().split(" "))

basecamp_map = []
for i in range(n):
    temp = list(map(int, input().split(" ")))
    basecamp_map.append(temp)

shop_map = [[0]*n for _ in range(n)]
for i in range(m):
    r, c = map(int, input().split(" "))
    shop_map[r-1][c-1] = i+1

human_dic = {}
cango_map = [[True]*n for _ in range(n)]

# 격자에 있는 사람들 리스트
human_list = []
check_moving_human = {}
for i in range(m):
    check_moving_human[i+1]=True

# 0:위, 1:왼, 2:오, 3:아 
change_list = [[-1,0], [0,-1], [0,1], [1,0]]

# 격자에서 해당 숫자 어디 있는지 알려주는 함수
def get_grid(num, grid):
    r, c = 0, 0
    for i in range(n):
        for j in range(n):
            if num==grid[i][j]:
                r, c = i, j
    return r, c

def go_shop(alive_human):
    for h in alive_human:
        if check_moving_human[h]==True:
            way_list = [] # 최단경로들 저장하는 리스트 
            best_way = []

            # 편의점을 향한 최단거리 구하기 : bfs
            visited = [[False]*n for _ in range(n)]
            q = deque()
            min_len = 500

            start_r, start_c  = human_dic[h]
            visited[start_r][start_c] = True
            q.append([start_r, start_c, 0, []])

            while q:
                cur_r, cur_c, cur_len, cur_way = q.popleft()
                if shop_map[cur_r][cur_c] == h:
                    if cur_len==min_len:
                        way_list.append(cur_way)
                    elif cur_len<min_len:
                        min_len = cur_len
                        way_list = [cur_way]
                for idx,c in enumerate(change_list):
                    next_r, next_c = cur_r+c[0], cur_c+c[1]
                    if 0<=next_r<n and 0<=next_c<n:
                        if visited[next_r][next_c]==False:
                            if cango_map[next_r][next_c]==True:
                                visited[next_r][next_c] = True
                                temp_way = deepcopy(cur_way)
                                temp_way.append(idx)
                                q.append([next_r, next_c, cur_len+1, temp_way])
            if len(way_list)==1:
                best_way = way_list[0] 
            else:
                look_way_list = [x for x in range(len(way_list))]
                for i in range(len(way_list[0])):
                    if len(look_way_list)==1:
                        break
                    temp_best = 10
                    best_idx = 0
                    for j in range(len(way_list)):  
                        if j in look_way_list:   
                            if way_list[j][i]<temp_best:
                                best_idx = j
                                temp_best = way_list[j][i]
                            elif way_list[j][i]>temp_best:
                                look_way_list.remove(j)
                best_way = way_list[best_idx]
            final_next_r, final_next_c = start_r+change_list[best_way[0]][0], start_c+change_list[best_way[0]][1]
            human_dic[h] = [final_next_r, final_next_c]

def go_basecamp(human_num):

    # 편의점과 가장 가까운 베이스캠프 리스트 찾기 : bfs
    close_basecamp_list = []
    q = deque()
    visited = [[False]*n for _ in range(n)]
    min_len = 10000

    start_r, start_c = get_grid(human_num, shop_map)
    visited[start_r][start_c] = True
    q.append([start_r, start_c, 0])

    while q:
        cur_r, cur_c, cur_len = q.popleft()
        if basecamp_map[cur_r][cur_c]==1:
            if cur_len==min_len:
                close_basecamp_list.append([cur_r, cur_c])
            elif cur_len<min_len:
                close_basecamp_list = [[cur_r, cur_c]]
                min_len = cur_len
        for c in change_list:
            next_r, next_c = cur_r+c[0], cur_c+c[1]
            if 0<=next_r<n and 0<=next_c<n:
                if visited[next_r][next_c]==False:
                    if cango_map[next_r][next_c]==True:
                        visited[next_r][next_c]=True
                        q.append([next_r, next_c, cur_len+1])

    if len(close_basecamp_list)==1:
        base_r, base_c = close_basecamp_list[0][0], close_basecamp_list[0][1]
    # 가장 가까운 베이스캠프가 여러 개일 경우 행이 작은 애, 행이 같다면 열이 작은 애
    else:
        min_row = 100
        min_col = 100
        min_row_list = []
        min_col_list = []
        for basecamp in close_basecamp_list:
            if min_row==basecamp[0]:
                min_row_list.append(basecamp)
            elif min_row > basecamp[0]:
                min_row = basecamp[0]
                min_row_list = [basecamp]
        if len(min_row_list)==1:
            base_r, base_c = min_row_list[0][0], min_row_list[0][1]
        else:
            for basecamp in min_row_list:
                if min_col == basecamp[1]:
                    min_col_list.append(basecamp)
                elif min_col > basecamp[1]:
                    min_col = basecamp[1]
                    min_col_list = [basecamp]
            base_r, base_c = min_col_list[0][0], min_col_list[0][1]

    return base_r, base_c


for t in range(1, 61):

    cango_list = []

    if t!=1:
        # 1번 행동, 2번 행동

        # 1번 행동
        go_shop(human_list)

        after_action1 = 0

        # 2번 행동
        for h in human_list:
            if check_moving_human[h]==True:
                x, y = get_grid(h, shop_map)
                if human_dic[h] == [x,y]:
                    cango_map[x][y] = False
                    # 추가로, 편의점에 도착한 사람은 더이상 움직이면 안됨 
                    check_moving_human[h] = False

        after_action2 = 0

    # 3번 행동 
    if t <= m:
        human_list.append(t)
        base_r, base_c = go_basecamp(t)
        # human_dic에 t번째 사람의 좌표(베이스캠프 좌표) 추가해주기 
        human_dic[t] = [base_r, base_c]
        # 해당 베이스캠프 cango_list에 추가해주기 
        cango_list.append([base_r, base_c])

    after_action3 = 0

    for temp in cango_list:
        r,c = temp
        cango_map[r][c] = False

    after_all_action = 0

    check_ans = True
    for temp in check_moving_human:
        if check_moving_human[temp]==True:
            check_ans=False
            break
    if check_ans:
        answer = t
        break


print(answer)