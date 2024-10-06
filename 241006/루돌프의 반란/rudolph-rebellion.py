def get_int_input():
    return map(int, input().split(" "))

n, m, p, c, d = get_int_input()

r_r, r_c = get_int_input()
r_r -=1
r_c -=1

grid_map = [[0]*n for _ in range(n)]
grid_map[r_r][r_c] = -1

first_santa_dic = {}
for i in range(p):
    s_n, s_r, s_c = get_int_input()
    s_r -=1
    s_c -=1
    grid_map[s_r][s_c] = s_n
    first_santa_dic[s_n] = [s_r, s_c, 1, -1, 0]

santa_dic = {}
for i in range(p):
    for j in first_santa_dic:
        if j == i+1:
            santa_dic[j] = first_santa_dic[j]

eight_direction = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
four_direction = [[-1,0], [0,1], [1,0], [0,-1]]

def get_distance(r1, c1, r2, c2):
    return int((r1-r2)**2 + (c1-c2)**2)

def bump(score, santa_df, direction, time, from_who, s_dic):
    s_dic[santa_df][4]+=score

    s_r, s_c = s_dic[santa_df][0], s_dic[santa_df][1]

    inverse_direction = [direction[0]*(-1), direction[1]*(-1)]

    if from_who=="rdf":
        real_direction = direction
    elif from_who=="santa":
        real_direction = inverse_direction

    next_r, next_c = s_r+(real_direction[0]*score), s_c+(real_direction[1]*score)

    if next_r<0 or next_r>=n or next_c<0 or next_c>=n:
        s_dic[santa_df][2] = 3
    else:
        if grid_map[next_r][next_c]==0:
            grid_map[next_r][next_c] = santa_df
            s_dic[santa_df] = [next_r, next_c, 2, time, s_dic[santa_df][4]]
            debugging = 0
        elif grid_map[next_r][next_c]>0:
            s_dic[santa_df][2], s_dic[santa_df][3] = 2, time
            # 상호작용
            previous_santa = grid_map[next_r][next_c]
            new_santa = santa_df
            while True:
                grid_map[s_dic[previous_santa][0]][s_dic[previous_santa][1]] = new_santa
                s_dic[new_santa][0], s_dic[new_santa][1] = s_dic[previous_santa][0], s_dic[previous_santa][1]
                next_r, next_c = s_dic[previous_santa][0] + real_direction[0], s_dic[previous_santa][1] + real_direction[1]

                if next_r<0 or next_r>=n or next_c<0 or next_c>=n:
                    s_dic[previous_santa] = [0,0,3,-1, s_dic[previous_santa][4]]
                    break
                else:
                    if grid_map[next_r][next_c]==0:
                        grid_map[next_r][next_c] = previous_santa
                        s_dic[previous_santa][0], s_dic[previous_santa][1] = next_r, next_c
                        break
                    else:
                        new_santa = previous_santa
                        previous_santa = grid_map[next_r][next_c]
    return s_dic

for turn in range(m):
    # 기절한 산타들 일어날 시점이면 처리해줘야 함
    for i in santa_dic:
        if santa_dic[i][2]==2:
            if santa_dic[i][3]+2==turn:
                santa_dic[i][2]=1
                santa_dic[i][3]=-1

    # 1. 루돌프의 움직임
    # 1-1. 가장 가까운 산타 찾기
    near_santa_list = []
    nearest_distance = 100000
    for i in santa_dic:
        if santa_dic[i][2]!=3:
            temp_distance = get_distance(r_r, r_c, santa_dic[i][0], santa_dic[i][1])
            if temp_distance < nearest_distance:
                nearest_distance = temp_distance
                near_santa_list = [i]
            elif temp_distance == nearest_distance:
                near_santa_list.append(i)
    if len(near_santa_list)==1:
        nearest_santa = near_santa_list[0]
    else:
        # r좌표 비교
        max_r_list = []
        max_r = 0
        for i in near_santa_list:
            temp_r = santa_dic[i][0]
            if temp_r > max_r:
                max_r = temp_r
                max_r_list=[i]
            elif temp_r == max_r:
                max_r_list.append(i)
        if len(max_r_list)==1:
            nearest_santa = max_r_list[0]
        else:
            # c좌표 비교
            max_c_list = []
            max_c = 0
            for i in max_r_list:
                temp_c = santa_dic[i][1]
                if temp_c > max_c:
                    max_c = temp_c
                    max_c_list = [i]
                elif temp_c == max_c:
                    max_c_list.append(i)
            nearest_santa = max_c_list[0]
    # 1-2. 산타랑 가장 가까워지는 칸 찾기
    nearest_distance = 10000000
    nearest_direction = [0,0]
    for direction in eight_direction:
        next_r, next_c = r_r+direction[0], r_c+direction[1]
        obj_r, obj_c = santa_dic[nearest_santa][0], santa_dic[nearest_santa][1]
        temp_distance = get_distance(next_r, next_c, obj_r, obj_c)
        if temp_distance <= nearest_distance:
            nearest_distance = temp_distance
            nearest_direction = direction
    # 1-3 루돌프 돌진
    nearest_grid = [r_r+nearest_direction[0], r_c+nearest_direction[1]]
    if grid_map[nearest_grid[0]][nearest_grid[1]]>0:
        grid_map[r_r][r_c] = 0
        r_r, r_c = nearest_grid[0], nearest_grid[1]
        grid_map[r_r][r_c] = -1
        # 루돌프->산타 충돌
        santa_dic = bump(c, nearest_santa, nearest_direction, turn, "rdf", santa_dic)
    else:
        grid_map[r_r][r_c] = 0
        r_r, r_c = nearest_grid[0], nearest_grid[1]
        grid_map[r_r][r_c] = -1

    debugging = 0


    # 2. 산타의 움직임
    for santa in range(p):
        santa += 1
        if santa_dic[santa][2]==1:
            # 2-1. 루돌프에게 거리가 가장 가까워지는 방향 찾기
            nearest_distance = 1000000000
            initial_distance = get_distance(r_r,r_c, santa_dic[santa][0], santa_dic[santa][1])
            near_direction_list = []
            for direction in four_direction:
                next_r, next_c = santa_dic[santa][0]+direction[0], santa_dic[santa][1]+direction[1]
                if 0<=next_r<n and 0<=next_c<n:
                    if grid_map[next_r][next_c]<=0:
                        temp_distance = get_distance(next_r, next_c, r_r, r_c)
                        if temp_distance < nearest_distance:
                            nearest_distance = temp_distance
                            near_direction_list = [direction]
                        elif temp_distance == nearest_distance:
                            near_direction_list.append(direction)
            if initial_distance <= nearest_distance or len(near_direction_list)==0:
                nearest_direction = [0,0]
            else:
                nearest_direction = near_direction_list[0]
            nearest_grid = [santa_dic[santa][0]+nearest_direction[0], santa_dic[santa][1]+nearest_direction[1]]

            # 2-2. 산타 충돌 확인
            grid_map[santa_dic[santa][0]][santa_dic[santa][1]] = 0
            santa_dic[santa][0], santa_dic[santa][1] = nearest_grid[0], nearest_grid[1]
            if grid_map[nearest_grid[0]][nearest_grid[1]]==-1:
                # 산타->루돌프 충돌 
                santa_dic = bump(d, santa, nearest_direction, turn, "santa", santa_dic)
            else:
                grid_map[santa_dic[santa][0]][santa_dic[santa][1]] = santa

    debugging = 0

    # 탈락하지 않은 산타들 확인
    alive_santa_list = []
    for i in santa_dic:
        if santa_dic[i][2]!=3:
            alive_santa_list.append(i)

    if len(alive_santa_list)==0:
        break

    else:
        for i in alive_santa_list:
            santa_dic[i][4]+=1

    debugging = 0


debugging = 0

answer = ""
for i in santa_dic:
    score = santa_dic[i][4]
    answer += f"{score} "

print(answer)