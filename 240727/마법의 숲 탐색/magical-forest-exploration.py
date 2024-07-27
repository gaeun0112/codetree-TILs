from collections import deque

R, C, K = map(int, input().split())
robot_list = []
for i in range(K):
    c_i, d_i = map(int, input().split())
    robot_list.append([c_i, d_i])

grid_r = R+3
forest = [[0]*C for _ in range(grid_r)]
change_list = [[0,0], [0,1], [0,-1], [1,0],[-1,0]]
change_list_2 = [[0,1], [0,-1], [1,0],[-1,0]]
answer = 0

def check_exit(r, c, way, grid, door_num):
    if way==0:
        grid[r-1][c] = door_num
    elif way==1:
        grid[r][c+1] = door_num
    elif way==2:
        grid[r+1][c] = door_num
    elif way==3:
        grid[r][c-1] = door_num
    return grid

def erase(r, c, grid):
    for change in change_list:
        grid[r+change[0]][c+change[1]] = 0
    return grid

def draw(r, c, grid, area_num):
    for change in change_list:
        grid[r+change[0]][c+change[1]] = area_num
    return grid

area = 1
door = 2
for robot in robot_list:
    cur_r, cur_c, cur_way = 1, robot[0]-1, robot[1]
    forest = draw(cur_r, cur_c, forest, area)
    while True:
        down_r, down_c = cur_r+1, cur_c
        left_r, left_c = cur_r+1, cur_c-1
        right_r, right_c = cur_r+1, cur_c+1
        if down_r < (grid_r-1) and (0<down_c<(C-1)) and forest[down_r][down_c+1]==0 and forest[down_r][down_c-1]==0 and forest[down_r+1][down_c]==0: 
            # 현재 위치 우선 지우고
            forest = erase(cur_r, cur_c, forest)
            cur_r, cur_c = down_r, down_c
            forest = draw(cur_r, cur_c, forest, area)
            forest = check_exit(cur_r, cur_c, cur_way, forest, door)
        elif (left_r<(grid_r-1)) and (0<left_c<(C-1)) and forest[left_r+1][left_c]==0 and forest[left_r][left_c-1]==0 and forest[cur_r][cur_c-2]==0 and forest[cur_r-1][cur_c-1]==0 and forest[cur_r+1][cur_c-1]==0:
            forest = erase(cur_r, cur_c, forest)
            cur_r, cur_c = left_r, left_c
            if cur_way == 0:
                cur_way=3
            else:
                cur_way-=1
            forest = draw(cur_r, cur_c, forest, area)
            forest = check_exit(cur_r, cur_c, cur_way, forest, door)
        elif (right_r<(grid_r-1)) and (0<right_c<(C-1)) and forest[right_r][right_c+1]==0 and forest[right_r+1][right_c]==0 and forest[cur_r][cur_c+2]==0 and forest[cur_r-1][cur_c+1]==0 and forest[cur_r+1][cur_c+1]==0:
            forest = erase(cur_r, cur_c, forest)
            cur_r, cur_c = right_r, right_c
            if cur_way==3:
                cur_way = 0
            else:
                cur_way+=1
            forest = draw(cur_r, cur_c, forest, area)
            forest = check_exit(cur_r, cur_c, cur_way, forest, door)
        else:
            # 어디로도 갈 수 없으면 이동 종료
            break
    
    # 이동을 모두 종료했는데, 삐져나온 부분이 있으면 초기화
    if cur_r<4:
        area, door = 1, 2
        forest = [[0]*C for _ in range(grid_r)]
    else:
        area +=2
        door +=2
        # cur_r, cur_c로부터 마지막 줄까지의 경로 계산
        start_r, start_c = cur_r, cur_c
        max_d = start_r
        q = deque()
        q.append([start_r, start_c])
        check_grid =  [[False]*C for _ in range(grid_r)]
        check_grid[start_r][start_c] = True
        while q:
            if max_d == (grid_r-1):
                break
            now_r, now_c = q.popleft()
            for cg in change_list_2:
                next_r, next_c = now_r+cg[0], now_c+cg[1]
                if( 0<=next_r<grid_r) and (0<next_c<C) and check_grid[next_r][next_c] ==False:
                    if forest[now_r][now_c]%2!=0:
                        if (forest[next_r][next_c]==forest[now_r][now_c]) or (forest[next_r][next_c]==(forest[now_r][now_c]+1)):
                            check_grid[next_r][next_c] = True
                            q.append([next_r, next_c])
                            max_d = max(max_d, next_r)
                    elif forest[now_r][now_c]%2==0:
                        if forest[next_r][next_c]>0:
                            check_grid[next_r][next_c] = True
                            q.append([next_r, next_c])
                            max_d = max(max_d, next_r)
        answer += max_d-2

 
print(answer)