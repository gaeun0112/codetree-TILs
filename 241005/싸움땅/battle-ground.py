n, m, k = map(int, input().split(" "))

point_list = [0]*m

gun_map = []
for i in range(n):
    temp = list(map(int, input().split(" ")))
    temp_list = []
    for t in temp:
        if t==0:
            temp_list.append([])
        elif t!=0:
            temp_list.append([t])
    gun_map.append(temp_list)

man_dic = {}
man_map = [[0]*n for _ in range(n)]
for i in range(m):
    r, c, d, s = map(int, input().split(" "))
    r -=1
    c -=1
    man_dic[i+1] = [r, c, d, s, 0]
    man_map[r][c] = i+1

direction_dic = {0:[-1,0], 1:[0,1], 2:[1,0], 3:[0,-1]}
inverse_direction = {0:2, 1:3, 2:0, 3:1}

def calculate_minus(x,y):
    if x>y:
        return x-y
    elif x<y:
        return y-x
    elif x==y:
        return 0
    
def check_direction(x,y):
    check = True
    if x<0 or x>=n or y<0 or y>=n:
        check = False
    elif man_map[x][y]>0:
        check=False
    return check

def get_gun(x, y, now_g):
    next_gun = now_g
    max_gun = max(gun_map[x][y])
    # 플레이어가 총이 있으면
    if now_g>0:
        if now_g < max_gun:
            next_gun = max_gun
            gun_map[x][y].append(now_g)
            gun_map[x][y].remove(next_gun)
    # 플레이어가 총이 없으면
    elif now_g==0:
        next_gun = max_gun
        gun_map[x][y].remove(next_gun)

    return next_gun


for turn in range(k):
    for man in man_dic:

        cur_r, cur_c, cur_d, cur_s, cur_g = man_dic[man]

        next_d, next_s, next_g = cur_d, cur_s, cur_g

        # 본인이 향하고 있는 방향대로 한 칸 이동
        next_r, next_c = cur_r + direction_dic[next_d][0], cur_c + direction_dic[next_d][1]
        if next_r<0 or next_r>=n or next_c<0 or next_c>=n:
            next_d = inverse_direction[cur_d]
            next_r, next_c = cur_r + direction_dic[next_d][0], cur_c + direction_dic[next_d][1]


        # Case 1 : 이동한 방향에 플레이어가 없다면
        if man_map[next_r][next_c]==0:
            # 해당 칸에 총이 있다면
            if len(gun_map[next_r][next_c])>0:
                next_g = get_gun(next_r, next_c, next_g)
            # man_dic, man_map 업데이트
            man_dic[man] = [next_r, next_c, next_d, next_s, next_g]
            man_map[cur_r][cur_c] = 0
            man_map[next_r][next_c] = man

            deubgging = 0
        
        # Case 2 : 이동한 방향에 플레이어가 있는 경우
        elif man_map[next_r][next_c] > 0:

            man_dic[man] = [next_r, next_c, next_d, next_s, next_g]

            winner, loser = 0, 0

            # 2-1. 승패 정하기
            player_1 = man_map[next_r][next_c]
            player_2 = man_map[cur_r][cur_c]

            man_map[cur_r][cur_c] = 0

            power_1 = man_dic[player_1][3]+ man_dic[player_1][4]
            power_2 = man_dic[player_2][3] + man_dic[player_2][4]

            if power_1 != power_2:
                if power_1 > power_2 : 
                    winner, loser = player_1, player_2
                elif power_1 < power_2 : 
                    winner, loser = player_2, player_1
            elif power_1 == power_2:
                if man_dic[player_1][3] > man_dic[player_2][3]:
                    winner, loser = player_1, player_2
                elif man_dic[player_1][3] < man_dic[player_2][3]:
                    winner, loser = player_2, player_1
            
            point = calculate_minus(power_1, power_2)
            point_list[winner-1] += point

            # 2-2. 진 플레이어 처리해주기
            # 본인이 가지고 있는 총 해당 격자에 내려놓기
            if man_dic[loser][4]>0:
                gun_map[next_r][next_c].append(man_dic[loser][4])
            man_dic[loser][4] = 0
            # 해당 플레이어가 원래 가지고 있던 방향 확인
            loser_d = man_dic[loser][2]
            next_loser_r, next_loser_c = next_r + direction_dic[loser_d][0], next_c + direction_dic[loser_d][1]

            if check_direction(next_loser_r, next_loser_c)==False:
                for i in range(3):
                    temp_d = loser_d + 1
                    check_r, check_c = next_r+direction_dic[temp_d][0], next_c+direction_dic[temp_d][1]
                    if check_direction(check_r, check_c)==True:
                        loser_d = temp_d
                        next_loser_r, next_loser_c = check_r, check_c
                        break   

            next_loser_g = man_dic[loser][3]
            next_winner_g = man_dic[winner][3]            
            # 이동하려는 칸에 총이 있다면
            if len(gun_map[next_loser_r][next_loser_c])>0:
                next_loser_g = get_gun(next_loser_r, next_loser_c, man_dic[loser][4])

            # 2-3. 이긴 플레이어 처리해주기
            if len(gun_map[next_r][next_c])>0:
                next_winner_g = get_gun(next_r, next_c, man_dic[winner][4])

            man_dic[loser] = [next_loser_r, next_loser_c, loser_d, man_dic[loser][3], next_loser_g]
            man_dic[winner] = [next_r, next_c, man_dic[winner][2], man_dic[winner][3], next_winner_g]
            

            man_map[next_loser_r][next_loser_c] = loser
            man_map[next_r][next_c] = winner

            deubgging=0


answer = ""
for p in point_list:
    answer+=f"{p} "

print(answer)