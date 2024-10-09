from collections import deque

def get_int_input():
    return map(int, input().split(" "))

n, m, k = get_int_input()

grid_map = []
rook_dic = {}
rook_idx = 1

for i in range(n):
    temp = list(get_int_input())
    grid_map.append(temp)

    for j, t in enumerate(temp):
        if t!=0:
            rook_dic[rook_idx] = [i, j, t, 0]
            rook_idx+=1

direction_list = [[0,1], [1,0], [0,-1], [-1,0]]
eight_direction_list = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]

debugging = 0

def get_inverse(r,c):
    if r < 0:
        r = n-1
    elif c < 0:
        c = m-1
    elif r >= n:
        r = 0
    elif c >= m:
        c = 0
    return r,c


for time in range(k):

    time +=1

    # 공격자 선정 
    low_power_list = []
    lowest_power = 10000000
    for rook in rook_dic:
        if rook_dic[rook][2]>0:
            if rook_dic[rook][2]<lowest_power:
                lowest_power = rook_dic[rook][2]
                low_power_list = [rook]
            elif rook_dic[rook][2] == lowest_power:
                low_power_list.append(rook)
    if len(low_power_list) == 1 :
        attacker = low_power_list[0]
    else:
        new_list = []
        new_rook = 0
        for rook in low_power_list:
            temp = rook_dic[rook][3]
            if temp > new_rook:
                new_rook = temp
                new_list = [rook]
            elif temp == new_rook:
                new_list.append(rook)
        if len(new_list)==1:
            attacker = new_list[0]
        else:
            max_sum_list = []
            max_sum = 0
            for rook in new_list:
                temp = rook_dic[rook][0]+rook_dic[rook][1]
                if temp > max_sum:
                    max_sum = temp
                    max_sum_list = [rook]
                elif temp == max_sum:
                    max_sum_list.append(rook)
            if len(max_sum_list)==1:
                attacker = max_sum_list[0]
            else:
                max_col_list = []
                max_col = 0
                for rook in max_sum_list:
                    if rook_dic[rook][1]>max_col:
                        max_col = rook_dic[rook][1]
                        max_col_list=[rook]
                    elif rook_dic[rook][1]==max_col:
                        max_col_list.append(rook)
                attacker = max_col_list[0]

    # 공격 받는 가장 강한 포탑 선정
    big_power_list = []
    big_power = 0
    for rook in rook_dic:
        if rook!=attacker:
            if rook_dic[rook][2]>big_power:
                big_power = rook_dic[rook][2]
                big_power_list = [rook]
            elif rook_dic[rook][2] == big_power:
                big_power_list.append(rook)
    if len(big_power_list)==1:
        strongest = big_power_list[0]
    else:
        old_list = []
        old_rook = 10000000000
        for rook in big_power_list:
            temp = rook_dic[rook][3]
            if temp < old_rook:
                old_rook = temp
                old_list = [rook]
            elif temp == old_rook:
                old_list.append(rook)
        if len(old_list):
            strongest = old_list[0]
        else:
            min_sum_list = []
            min_sum = 100000000
            for rook in old_list:
                temp = rook_dic[rook][0] + rook_dic[rook][1]
                if temp < min_sum:
                    min_sum = temp
                    min_sum_list = [rook]
                elif temp == min_sum:
                    min_sum_list.append(rook)
            if len(min_sum_list)==1:
                strongest = min_sum_list[0]
            else:
                min_col_list = []
                min_col = 10000000
                for rook in min_sum_list:
                    temp = rook_dic[rook][1]
                    if temp < min_col:
                        min_col = temp
                        min_col_list = [rook]
                    elif temp == min_col:
                        min_col_list.appned(rook)
                strongest = min_col_list[0]

    # 공격자 업데이트
    rook_dic[attacker][2]+=(n+m)
    rook_dic[attacker][3] = time
    grid_map[rook_dic[attacker][0]][rook_dic[attacker][1]]+=(n+m)


    # 레이저 공격
    start_r, start_c = rook_dic[attacker][0], rook_dic[attacker][1]
    end_r, end_c = rook_dic[strongest][0], rook_dic[strongest][1]

    q = deque()
    visited = [[False]*m for _ in range(n)]

    q.append([start_r, start_c, 0, []])
    visited[start_r][start_c] = True
    min_distance = 10000000
    min_route_list = []

    while q:
        cur_r, cur_c, cur_len, cur_route = q.popleft()
        for d in direction_list:
            next_r, next_c = cur_r+d[0], cur_c+d[1]

            # next_r, next_c 보정
            next_r, next_c = get_inverse(next_r, next_c)

            if next_r==end_r and next_c==end_c:
                if cur_len < min_distance:
                    min_distance = cur_len
                    output_route = cur_route[:]
                    output_route.append(d)
                    min_route_list = [output_route]
                    debugging = 0
                elif cur_len == min_distance:
                    output_route = cur_route[:]
                    output_route.append(d)
                    min_route_list.append(output_route)
                    debugging = 0

            if grid_map[next_r][next_c]!=0:
                if visited[next_r][next_c]==False:
                    visited[next_r][next_c] = True
                    temp_route = cur_route[:]
                    temp_route.append(d)
                    q.append([next_r, next_c, cur_len+1, temp_route])
      
    if len(min_route_list)==1:
        best_route = min_route_list[0]
        # 레이저 공격 처리
        influenced_list = []
        cur_r, cur_c = start_r, start_c
        for d in best_route:
            next_r, next_c = cur_r+d[0], cur_c+d[1]
            next_r, next_c = get_inverse(next_r, next_c)
            if [next_r, next_c]!=[end_r, end_c]:
                influenced_list.append([next_r, next_c])
                cur_r, cur_c = next_r, next_c
    elif len(min_route_list)>1:
        # 우하좌상 우선순위대로 찾기
        route_len = len(min_route_list[0])
        route_num = len(min_route_list)
        route_idx_list = [i for i in range(route_num)]
        for direction in range(route_len):
            best_way = 10
            best_way_list = []
            for num in range(route_num):
                if num in route_idx_list:
                    temp = direction_list.index(min_route_list[num][direction])
                    debugging = 0
                    if temp < best_way:
                        best_way = temp
                        best_way_list.append(num)
                    elif temp == best_way:
                        best_way_list.append(num)
            route_idx_list = best_way_list[:]
            if len(best_way_list)==1:
                best_route = min_route_list[best_way_list[0]]
                break
        # 레이저 공격 처리
        influenced_list = []
        cur_r, cur_c = start_r, start_c
        for d in best_route:
            next_r, next_c = cur_r+d[0], cur_c+d[1]
            next_r, next_c = get_inverse(next_r, next_c)
            if [next_r, next_c]!=[end_r, end_c]:
                influenced_list.append([next_r, next_c])
                cur_r, cur_c = next_r, next_c
    elif len(min_route_list)==0:
        influenced_list = []
        # 포탄 공격
        for d in eight_direction_list:
            next_r, next_c = end_r+d[0], end_c+d[1]
            next_r, next_c = get_inverse(next_r, next_c)
            debugging =  0
            if grid_map[next_r][next_c]!=0 and [next_r, next_c]!=[start_r, start_c]:
                influenced_list.append([next_r, next_c])

    # 공격받은 포탑 처리
    after_power = rook_dic[strongest][2] - rook_dic[attacker][2]
    if after_power<0:
        after_power = 0
    rook_dic[strongest][2] = after_power
    grid_map[rook_dic[strongest][0]][rook_dic[strongest][1]] = after_power

    turn_list = []
    turn_list.append(attacker)
    turn_list.append(strongest)

    # 영향 받은 포탑들 처리
    for temp in influenced_list:
        temp_r, temp_c = temp
        rook_idx = 0 
        for rook in rook_dic:
            if rook_dic[rook][0]==temp_r and rook_dic[rook][1] == temp_c:
                rook_idx = rook
        turn_list.append(rook_idx)
        after_power = rook_dic[rook_idx][2] - int(rook_dic[attacker][2]//2)
        if after_power<0:
            after_power = 0
        rook_dic[rook_idx][2] = after_power
        grid_map[rook_dic[rook_idx][0]][rook_dic[rook_idx][1]] = after_power

    # 공격과 무관했던 포탑들 처리
    for rook in rook_dic:
        if rook not in turn_list and rook_dic[rook][2]>0:
            rook_dic[rook][2]+=1
            grid_map[rook_dic[rook][0]][rook_dic[rook][1]]+=1

    debugging = 0


debugging = 0

# 가장 공격력이 큰 포탑 반환하기
answer = 0
for rook in rook_dic:
    if rook_dic[rook][2]>answer:
        answer = rook_dic[rook][2]

print(answer)