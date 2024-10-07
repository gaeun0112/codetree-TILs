def get_int_input():
    return map(int, input().split(" "))

n, m, k = get_int_input()

answer = 0

grid_map = []
for i in range(n):
    temp = list(get_int_input())
    grid_map.append(temp)

man_dic = {}
for i in range(m):
    r, c = get_int_input()
    man_dic[i+1] = [r-1, c-1, 0]

exit_r, exit_c = get_int_input()
exit_r -=1
exit_c -=1

direction_list = [[1,0], [-1,0], [0,1], [0,-1]]

def get_plus(num):
    if num<0:
        return -num
    else:
        return num

def get_distance(x1, y1, x2, y2):
    temp_1 = get_plus(x1-x2)
    temp_2 = get_plus(y1-y2)
    return temp_1+temp_2

for sec in range(k):

    check_escape = True

    for man in man_dic:
        _, _, escape = man_dic[man]
        if escape==0:
            check_escape = False

    if check_escape == True:
        break

    # 1. 모든 참가자들이 한 칸씩 움직임
    for man in man_dic:
        cur_r, cur_c, escape = man_dic[man]

        if escape==0:

            nearest_list = []
            nearest_distance = 10000
            initial_distance = get_distance(cur_r, cur_c, exit_r, exit_c)
            for direction in direction_list:
                temp_r, temp_c = cur_r+direction[0], cur_c+direction[1]
                if 0<=temp_r<n and 0<=temp_c<n:
                    if grid_map[temp_r][temp_c]==0:
                        temp_distance= get_distance(temp_r, temp_c, exit_r, exit_c)
                        if temp_distance<initial_distance:
                            if temp_distance<nearest_distance:
                                nearest_distance = temp_distance
                                nearest_list = [direction]
                            elif temp_distance==nearest_distance:
                                nearest_list.append(direction)
            
            if len(nearest_list)==0:
                nearest_direction = [0,0]
            else:
                nearest_direction = nearest_list[0]
                answer += 1

            next_r, next_c = cur_r+nearest_direction[0], cur_c+nearest_direction[1]

            if next_r==exit_r and next_c == exit_c:
                escape=1
                next_r, next_c = 100, 100

            man_dic[man] = [next_r, next_c, escape]


    debugging = 9


    # 2. 미로가 회전
    # 2-1. 사람과 미로를 포함하는 가장 작은 정사각형 찾기
    rec_dic = {}
    for man in man_dic:
        cur_r, cur_c, escape = man_dic[man]

        if escape==0:

            temp_1 = get_plus(cur_r-exit_r)
            temp_2 = get_plus(cur_c-exit_c)

            if temp_1>=temp_2:
                rec_len = temp_1
            else:
                rec_len = temp_2

            debugging = 0

            if cur_r<=exit_r and cur_c<=exit_c:
                point_1 = [cur_r, cur_c]
                point_3 = [exit_r, exit_c]
            elif cur_r>=exit_r and cur_c>=exit_c:
                point_1 = [exit_r, exit_c]
                point_3 = [cur_r, cur_c]
            elif cur_r<=exit_r and cur_c>=exit_c:
                point_2 = [exit_r, exit_c]
                point_4 = [cur_r, cur_c]
                point_3 = [cur_r+temp_1, cur_c]
            elif cur_r>=exit_r and cur_c<=exit_c:
                point_2 = [cur_r, cur_c]
                point_4 = [exit_r, exit_c]
                point_3 = [exit_r+temp_1, exit_c]

            point_min = [point_3[0]-rec_len, point_3[1]-rec_len]

            if point_min[0]<0:
                point_min[0] = 0
            if point_min[1]<0:
                point_min[1] = 0

            if rec_len not in rec_dic:
                rec_dic[rec_len] = [point_min]
            elif rec_len in rec_dic and point_min not in rec_dic[rec_len]:
                rec_dic[rec_len].append(point_min)

    debugging = 0

    best_len = min(rec_dic)

    if len(rec_dic[best_len])==1:
        best_r, best_c = rec_dic[best_len][0][0], rec_dic[best_len][0][1]
    else:
        # 좌상단 좌표가 작은 애로 우선하기 
        min_r_list = []
        min_r = 1000
        for temp in rec_dic[best_len]:
            if temp[0]<min_r:
                min_r = temp[0]
                min_r_list = [temp]
            elif temp[0]==min_r:
                min_r_list.append(temp)
        if len(min_r_list)==1:
            best_r, best_c = min_r_list[0][0], min_r_list[0][1]
        else:
            min_c_list = []
            min_c = 1000
            for temp in min_r_list:
                if temp[1]<min_c:
                    min_c = temp[1]
                    min_c_list = [temp]
                elif temp[1]==min_c:
                    min_c_list.append(temp)
            best_r, best_c = min_c_list[0][0], min_c_list[0][1]

    debugging = 0        

    # 2-2. 정사각형 회전시키기
    new_grid = [[0]*n for _ in range(n)]
    check_change = [[0]*n for _ in range(n)]
    new_check_change =  [[0]*n for _ in range(n)]

    num=1
    for row in range(best_r, best_r+best_len+1):
        for col in range(best_c, best_c+best_len+1):
            check_change[row][col] = num
            num+=1

    col_list = []
    col_list_change = []
    for col in range(best_c, best_c+best_len+1):
        temp_col = []
        temp_col_change = []
        for row in range(best_r+best_len, best_r-1, -1):
            temp = grid_map[row][col]
            if temp>0:
                temp -=1
            temp_col.append(temp)
            temp_col_change.append(check_change[row][col])
        col_list.append(temp_col)
        col_list_change.append(temp_col_change)
    debugging = 0

    i = 0
    for row in range(best_r, best_r+best_len+1):
        new_grid[row][best_c:best_c+best_len+1] = col_list[i]
        new_check_change[row][best_c:best_c+best_len+1] = col_list_change[i]
        i+=1

    debugging = 0

    grid_change = [[0]*n for _ in range(n)]

    def find_num(n, grid):
        for i in range(len(grid)):
            for j in range(len(grid)):
                if n==grid[i][j]:
                    return i,j
                
    for i in range(1, num):
        ori_r, ori_c = find_num(i, check_change)
        new_r, new_c = find_num(i, new_check_change)
        grid_change[ori_r][ori_c] = [new_r, new_c]

    for row in range(best_r, best_r+best_len+1):
        for col in range(best_c, best_c+best_len+1):
            grid_map[row][col] = new_grid[row][col]

    exit_r, exit_c = grid_change[exit_r][exit_c][0], grid_change[exit_r][exit_c][1]

    # 포함된 사람 처리해주기 
    for man in man_dic:
        cur_r, cur_c, escape = man_dic[man]
        if escape==0:
            if best_r<=cur_r<=best_r+best_len and best_c<=cur_c<=best_c+best_len:
                man_dic[man] = [grid_change[cur_r][cur_c][0], grid_change[cur_r][cur_c][1], escape]


    debugging = 0


debugging = 0

print(answer)
print(f"{exit_r+1} {exit_c+1}")