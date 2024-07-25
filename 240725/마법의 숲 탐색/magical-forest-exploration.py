R, C, K = map(int, input().split())
robot_list = []
for i in range(K):
    c_i, d_i = map(int, input().split())
    robot_list.append([c_i, d_i])

grid_r = R+3
forest = [[0]*C for _ in range(grid_r)]
change_list = [[0,0], [0,1], [0,-1], [1,0],[-1,0]]

def check_exit(r, c, way, grid):
    if way==0:
        grid[r-1][c] = 2
    elif way==1:
        grid[r][c+1] = 2
    elif way==2:
        grid[r+1][c] = 2
    elif way==3:
        grid[r][c-1] = 2
    return grid

def erase(r, c, grid):
    for change in change_list:
        grid[r+change[0]][c+change[1]] = 0
    return grid

def draw(r, c, grid):
    for change in change_list:
        grid[r+change[0]][c+change[1]] = 1
    return grid

for robot in robot_list:
    cur_r, cur_c, cur_way = 0, robot[0], robot[1]
    while (cur_r<(R+1)):
        down_r, down_c = cur_r+1, cur_c
        if down_r < (R+1): 
            if forest[down_r][down_c+1]==0 and forest[down_r][down_c-1]==0 and forest[down_r+1][down_c]==0:
                # 현재 위치 우선 지우고
                forest = erase(cur_r, cur_c, forest)
                cur_r, cur_c = down_r, down_c
                forest = draw(cur_r, cur_c, forest)
                forest = check_exit(cur_r, cur_c, cur_way, forest)
            else:
                right_r, right_c = cur_r+1, cur_c-1
                if right_r<(R+1) and (0<right_c<(C-1)):
                    if forest[right_r][right_c-1]==0 and forest[right_r+1][right_c]==0:
                        forest = erase(cur_r, cur_c, forest)
                        cur_r, cur_c = right_r, right_c
                        if cur_way==0:
                            cur_way = 3
                        else:
                            cur_way-=1
                        forest = draw(cur_r, cur_c, forest)
                        forest = check_exit(cur_r, cur_c, cur_way, forest)
                    else:
                        left_r, left_c = cur_r+1, cur_c+1
                        if left_r<(R+1) and (0<left_c<(C-1)):
                            if forest[left_r+1][left_c]==0 and forest[left_r][left_c+1]==0:
                                forest = erase(cur_r, cur_c, forest)
                                cur_r, cur_c = left_r, left_c
                                if cur_way == 2:
                                    cur_way=0
                                else:
                                    cur_way+=1
                                forest = draw(cur_r, cur_c, forest)
                                forest = check_exit(cur_r, cur_c, cur_way, forest)
                            else:
                                # 어디로도 갈 수 없으면 이동 종료
                                break
    
    # 이동을 모두 종료했는데, 삐져나온 부분이 있으면 초기화
    if cur_r<4:
        forest = [[0]*C for _ in range(grid_r)]

print(forest)