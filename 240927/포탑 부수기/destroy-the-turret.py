from collections import deque

N, M, K = map(int, input().split(" "))

grid = []

for i in range(N):
    temp = list(map(int, input().split(" ")))
    grid.append(temp)

# 최근에 공격한 포탑, 최근에 공격받은 포탑에 대한  global 정보를 저장해야 한다.
attacker_list = []
attacked_list = []

time = [[0]*M for _ in range(N)]

# 우/하/좌/상 우선순위
way_order = {"right":1, "down":2, "left":3, "up":4}

# 부서지지 않은 포탑들의 리스트 가져오기 
def find_alive_rook(grid_map):
    alive_rook_list = []
    for i in range(N):
        for j in range(M):
            if grid_map[i][j]>0:
                alive_rook_list.append([i,j])
    return alive_rook_list

# 모든 포탑들은 시점 0에 공격한 경험과 공격받은 경험이 있다고 가정한다.
first_alive_rook = find_alive_rook(grid)
# attacker_list.append(first_alive_rook)



# 1. 공격자 선정 함수
def decide_attacker():
    # 반환 : weakest_rook, 즉 가장 약한 포탑의 좌표 
    weakest_rook = [0,0]
    # 공격력이 가장 낮은 포탑 찾기
    smallest_power = 5001 # (0<=공격력<=5,000이므로)
    smallest_power_rook_list = []
    for i in range(N):
        for j in range(M):
            if grid[i][j]<smallest_power and grid[i][j]>0:
                smallest_power = grid[i][j]
                smallest_power_rook_list = [[i,j]]
            elif grid[i][j]==smallest_power and grid[i][j]>0:
                smallest_power_rook_list.append([i,j])
    # 공격력이 가장 낮은 포탑이 하나라면, 결정완
    num_smallest_power_rook = len(smallest_power_rook_list)
    if num_smallest_power_rook==1:
        weakest_rook = smallest_power_rook_list[0]
    else:
        # if iter!=0:
        #     # 가장 최근에 공격한 포탑 찾기
        #     earliest_attack_rook_list = []
        #     for i in reversed(range(len(attacker_list))):
        #         check = False
        #         for j in smallest_power_rook_list:
        #             if j == attacker_list[i]:
        #                 check = True
        #                 earliest_attack_rook_list.append(j)
        #                 break
        #         if check==True:
        #             break
        #     num_earliest_attack_rook = len(earliest_attack_rook_list)
        # else:
        #     earliest_attack_rook_list = smallest_power_rook_list
        #     num_earliest_attack_rook = num_smallest_power_rook

        earliest_attack_rook_list = []

        earliest_time = 0
        for temp in smallest_power_rook_list:
            i, j = temp
            if time[i][j]>earliest_time:
                earliest_time = time[i][j]
                earliest_attack_rook_list = [[i,j]]
            elif time[i][j]==earliest_time:
                earliest_attack_rook_list.append([i,j])
        num_earliest_attack_rook = len(earliest_attack_rook_list)

        if num_earliest_attack_rook==1:
            weakest_rook = earliest_attack_rook_list[0]
        else:
            # 각 포탑 위치의 행과 열의 합이 가장 큰 포탑 찾기
            largest_list = []
            largest_value = 0
            for i in range(num_earliest_attack_rook):
                temp = earliest_attack_rook_list[i][0] + earliest_attack_rook_list[i][1]
                if temp > largest_value:
                    largest_list = [earliest_attack_rook_list[i]]
                    largest_value = temp
                elif temp == largest_value:
                    largest_list.append(earliest_attack_rook_list[i])
            num_n_plus_m = len(largest_list)
            if num_n_plus_m==1:
                weakest_rook = largest_list[0]
            else:
                # 각 포탑 위치의 열 값이 가장 큰 포탑 찾기
                largest_value = -1
                largest_look = []
                for i in range(num_n_plus_m):
                    if largest_list[i][1]>largest_value:
                        largest_look = [largest_list[i]]
                        largest_value = largest_list[i][1]
                weakest_rook = largest_look[0]
    return weakest_rook


# 2-1. 공격되는 포탑 선정 함수
def decide_attacked_rook(attacker_rk):
    # 반환 : strongest_rook, 즉 가장 강한 포탑의 좌표 
    strongest_rook = [0,0]
    # 공격력이 가장 높은 포탑 찾기
    biggest_power = 0 # (0<=공격력<=5,000이므로)
    biggest_power_rook_list = []
    for i in range(N):
        for j in range(M):
            if [i,j] != attacker_rk:
                if grid[i][j] > biggest_power and grid[i][j]>0:
                    biggest_power = grid[i][j]
                    biggest_power_rook_list = [[i,j]]
                elif grid[i][j]==biggest_power and grid[i][j]>0:
                    biggest_power_rook_list.append([i,j])
    # 공격력이 가장 높은 포탑이 하나라면, 결정완
    num_biggest_power_rook = len(biggest_power_rook_list)
    if num_biggest_power_rook==1:
        strongest_rook = biggest_power_rook_list[0]
    else:
        # if iter!=0:
        #     # 공격한지 가장 오래된 포탑 찾기
        #     old_attack_rook_list = []
        #     for i in range(len(attacker_list)):
        #         check = False
        #         for j in biggest_power_rook_list:
        #             if j == attacker_list[i]:
        #                 check = True
        #                 old_attack_rook_list.append(j)
        #                 break
        #         if check==True:
        #             break
        #     num_old_attack_rook = len(old_attack_rook_list)
        # else:
        #     old_attack_rook_list = biggest_power_rook_list
        #     num_old_attack_rook = num_biggest_power_rook
        old_attack_rook_list = []

        oldest_time = 1001
        for temp in biggest_power_rook_list:
            i, j = temp
            if time[i][j]<oldest_time:
                oldest_time = time[i][j]
                old_attack_rook_list = [[i,j]]
            elif time[i][j]==oldest_time:
                old_attack_rook_list.append([i,j])
        num_old_attack_rook = len(old_attack_rook_list)

        if num_old_attack_rook==1:
            strongest_rook = old_attack_rook_list[0]
        else:
            # 각 포탑 위치의 행과 열의 합이 가장 작은 포탑 찾기
            smallest_list = []
            smallest_value = 50
            for i in range(num_old_attack_rook):
                temp = old_attack_rook_list[i][0] + old_attack_rook_list[i][1]
                if temp < smallest_value:
                    smallest_list = [old_attack_rook_list[i]]
                    smallest_value = temp
                elif temp == smallest_value:
                    smallest_list.append(old_attack_rook_list[i])
            num_n_plus_m = len(smallest_list)
            if num_n_plus_m==1:
                strongest_rook = smallest_list[0]
            else:
                # 각 포탑 위치의 열 값이 가장 큰 포탑 찾기
                largest_value = -1
                largest_look = []
                for i in range(num_n_plus_m):
                    if smallest_list[i][1]>largest_value:
                        largest_look = [smallest_list[i]]
                        largest_value = smallest_list[i][1]
                strongest_rook = largest_look[0]
    return strongest_rook

# 2-2. 레이저 공격
def attack_raser(attacker_rk, attacked_rk):
    check_raser = False
    closest_way = [] # 영향을 받은 포탑들 (경로에 존재하던) 이때 공격자와 공격받은 포탑은 제외

    q = deque()
    start_r, start_c = attacker_rk
    q.append([start_r, start_c, 0, [], []])
    min_len = 10000
    # 우하좌상
    change_list = [[0,1], [1,0], [0,-1], [-1,0]]
    visited = [[0]*M for _ in range(N)]
    visited[start_r][start_c] = 1
    route_list = []
    way_list = []

    while q:
        cur_r, cur_c, cur_len, cur_route, cur_way = q.popleft()
        if cur_r==attacked_rk[0] and cur_c==attacked_rk[1]:
            break
        for c in change_list:
            next_r, next_c = cur_r+c[0], cur_c+c[1]
            # 가장자리에서 막힌 방향으로 진행하고자 하면 반대편으로 나온다
            if next_r < 0:
                next_r = N-1
            elif next_r >= N:
                next_r = 0
            if next_c < 0:
                next_c = M-1
            elif next_c >= M:
                next_c = 0
            
            if visited[next_r][next_c]==0:
                if next_r==attacked_rk[0] and next_c==attacked_rk[1]:
                    route_list.append(cur_route)
                    way_list.append(cur_way)
                    min_len = min(min_len, cur_len)
                    if cur_len>min_len:
                        route_list.pop()
                        way_list.pop()
                elif grid[next_r][next_c]>0 :
                    visited[next_r][next_c] +=1
                    temp = cur_route[:]
                    temp.append([next_r, next_c])
                    temp_way = cur_way[:]
                    if c==[1,0]:
                        temp_way.append("down")
                    elif c==[-1,0]:
                        temp_way.append("up")
                    elif c==[0,1]:
                        temp_way.append("right")
                    elif c==[0,-1]:
                        temp_way.append("left")
                    q.append([next_r, next_c, cur_len+1, temp, temp_way])



    num_route = len(route_list)
    if num_route==1:
        check_raser=True
        closest_way = route_list[0]
    # 경로의 길이가 똑같은 최단 경로가 2개 이상이라면, 우/하/좌/상 순위대로 먼저 움직인 경로
    elif num_route>=2:
        closest_way = route_list[0]
        check_raser = True
        closest = len(route_list[0])
        for i in range(closest):
            best_way = way_list[0][i]
            for j in range(1, num_route):
                if way_order[way_list[j][i]] < way_order[best_way]:
                    closest_way = route_list[j]
                    break

    return check_raser, closest_way

def bomb_attack(attacked_rk):
    ans_list = []
    # 공격받은 포탑 주변의 8개의 포탑들 뽑기
    cur_r, cur_c, = attacked_rk
    change_list = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
    for c in change_list:
        next_r, next_c = cur_r+c[0], cur_c+c[1]
        if next_r < 0:
            next_r = N-1
        elif next_r >= N:
            next_r = 0
        if next_c < 0:
            next_c = M-1
        elif next_c >= M:
            next_c = 0
        if grid[next_r][next_c]>0:
            ans_list.append([next_r, next_c])
    return ans_list


for x in range(K):
    # 부서지지 않은 포탑이 1개가 된다면, 중지
    now_alive_rook = find_alive_rook(grid)
    if len(now_alive_rook)==1:
        break

    # 1. 공격자 선정
    attacker = decide_attacker()

    # 2. 공격자의 공격

    # 2-1. 공격되는 포탑 선정
    attacked_rook = decide_attacked_rook(attacker)

    grid[attacker[0]][attacker[1]]+=(N+M)
    time[attacker[0]][attacker[1]] = x+1

    # 2-2. 레이저 공격
    can_raser, influenced_rook_list = attack_raser(attacker, attacked_rook)

    if can_raser==False:
        # 2-3. 포탄 공격 
        influenced_rook_list = bomb_attack(attacked_rook)

    for t in range(0, len(influenced_rook_list)-1):
        i, j = influenced_rook_list[t]
        if [i,j]==attacker:
            influenced_rook_list.pop(t)


    # 3. 공격을 받아 공격력이 0 이하가 된 포탑은 부서진다.
    damage_1 = grid[attacker[0]][attacker[1]]
    damage_2 = int(grid[attacker[0]][attacker[1]]//2)

    temp = grid[attacked_rook[0]][attacked_rook[1]] - damage_1
    if temp>=0:
        grid[attacked_rook[0]][attacked_rook[1]]  = temp
    elif temp<0:
        grid[attacked_rook[0]][attacked_rook[1]] = 0

    for i in influenced_rook_list:
        temp = grid[i[0]][i[1]] - damage_2
        if temp>=0:
            grid[i[0]][i[1]] = temp
        else:
            grid[i[0]][i[1]] = 0

    influenced_rook_list.append([attacker[0], attacker[1]])
    influenced_rook_list.append([attacked_rook[0], attacked_rook[1]])

    # 4. 포탑 정비 
    for i in range(N):
        for j in range(M):
            if [i,j] not in influenced_rook_list and grid[i][j]>0:
                grid[i][j]+=1

answer = 0

for i in grid:
    for j in i:
        answer = max(answer, j)

print(answer)