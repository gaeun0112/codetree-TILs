from collections import deque
from copy import deepcopy

L, N, Q = map(int, input().split()) 

# 초기 맵 정보 받는 함수
grid = [[0]*L for _ in range(L)]
for i in range(L):
    row = list(map(int, input().split()) )
    for j in range(L):
        grid[i][j] = [row[j],0]

# 기사들의 위치를 지도에 표시해주는 함수
def knight_to_grid(r, c, h, w, input_grid, n):
    for i in range(r, r+h):
        for j in range(c, c+w):
            input_grid[i][j][1] = n
    return input_grid

# 기사를 지도에 삭제해주는 함수
def erase_knight(r, c, h, w, input_grid):
    for i in range(r, r+h):
        for j in range(c, c+w):
            input_grid[i][j][1] = 0
    return input_grid

# 기사 정보 저장하고, 그리드에 기사들의 초기 위치 표시
knight_dic = {}
for i in range(1, N+1):
    r, c, h, w, k = map(int, input().split())
    knight_dic[i]=[[r-1,c-1], [h, w], k]
    # 그리드에 기사들 초기 위치 표시해주기
    grid = knight_to_grid(r-1, c-1, h, w, grid, i)

first_knight_dic = deepcopy(knight_dic)

# 왕의 명령 리스트
q_list = []
for i in range(Q):
    i, d = map(int, input().split())
    q_list.append([i,d])

# 방향 미리 설정 : 위오아왼
direction_dic = {0: [-1,0], 1:[0,1], 2:[1,0], 3:[0,-1]}

# 다음에 비어있어야 하는 영역 알려주는 함수
def next_check(r,c,h,w,dir):
    must_empty = []
    if dir==0:
        for i in range(c, c+w):
            must_empty.append([r-1,i])
    elif dir==1:
        for i in range(r, r+h):
            must_empty.append([i,c+w])
    elif dir==2:
        for i in range(c, c+w):
            must_empty.append([r+h,i])
    elif dir==3:
        for i in range(r,r+h):
            must_empty.append([i,c-1])
    return must_empty

# 단일 이동 함수
def one_move(r,c,h,w,dir, knight_num, input_grid):
    if dir==0:
        for i in range(c, c+w):
            input_grid[r-1][i][1]=knight_num
            input_grid[r+h-1][i][1]=0
    elif dir==1:
        for i in range(r, r+h):
            input_grid[i][c+w][1] = knight_num
            input_grid[i][c][1] = 0
    elif dir==2:
        for i in range(c, c+w):
            input_grid[r+h][i][1] = knight_num
            input_grid[r][i][1] = 0
    elif dir==3:
        for i in range(r,r+h):
            input_grid[i][c-1] = knight_num
            input_grid[i][c+w-1] = 0 
    return input_grid


# 연쇄 이동 함수
def move_knights(knight_num, direction, grid, knight_dic):

    move_knights_list = [knight_num]

    check_wall = True
    first_r, first_c, first_knight = knight_dic[knight_num][0][0], knight_dic[knight_num][0][1], knight_num
    q = deque()
    q.append([first_r, first_c, first_knight])
    visited = [[False]*L for _ in range(L)]
    while q and check_wall==True:
        cur_r, cur_c, cur_knight = q.popleft()
        r, c, h, w = cur_r, cur_c, knight_dic[cur_knight][1][0], knight_dic[cur_knight][1][1]
        must_empty_list = next_check(r,c,h,w,direction)
        can_move = True
        for temp in must_empty_list:
            # 다음 이동 칸 범위에 벽이 있다면, 이동할 수 없는 것이므로 while문 break
            if temp[0]<0 or temp[0]>=L or temp[1]<0 or temp[1]>=L:
                check_wall=False
                break
            elif grid[temp[0]][temp[1]][0]==2:
                check_wall=False
                break
        if check_wall==True:
            for temp in must_empty_list:
                # 다음 칸들 중에 이미 기사가 있는 칸이 있고, 아직 탐색하지 않은 칸이라면 
                if grid[temp[0]][temp[1]][1]>0 and visited[temp[0]][temp[1]]==False:
                    if grid[temp[0]][temp[1]][1] not in move_knights_list:
                        can_move = False 
                        # 다음 연쇄이동 진행해야 한다.
                        cur_knight = grid[temp[0]][temp[1]][1]
                        cur_r, cur_c = knight_dic[cur_knight][0][0], knight_dic[cur_knight][0][1]
                        visited[temp[0]][temp[1]] = True
                        q.append([cur_r, cur_c, cur_knight])
                        move_knights_list.append(cur_knight)

    if check_wall==True:
        for idx, kn in enumerate(move_knights_list):
            r,c,h,w = knight_dic[kn][0][0], knight_dic[kn][0][1], knight_dic[kn][1][0],knight_dic[kn][1][1]
            grid = erase_knight(r,c,h,w, grid)
            new_r, new_c = r + direction_dic[direction][0], c+direction_dic[direction][1]
            knight_dic[kn][0] = [new_r, new_c]

        for idx, kn in enumerate(move_knights_list):
            r,c,h,w = knight_dic[kn][0][0], knight_dic[kn][0][1], knight_dic[kn][1][0],knight_dic[kn][1][1]
            grid = knight_to_grid(r,c,h,w,grid, kn)

        for idx, kn in enumerate(move_knights_list):
            r,c,h,w = knight_dic[kn][0][0], knight_dic[kn][0][1], knight_dic[kn][1][0],knight_dic[kn][1][1]

            # 데미지 처리
            if idx>0:
                # 밀린 기사, 즉 재설정된 기사의 움직였을 때의 데미지를 계산.
                r,c,h,w = knight_dic[kn][0][0], knight_dic[kn][0][1], knight_dic[kn][1][0],knight_dic[kn][1][1]
                trash_num = 0
                for i in range(r, r+h):
                    for j in range(c, c+w):
                        if grid[i][j][0]==1:
                            trash_num+=1
                cur_score = knight_dic[kn][2]
                next_score = cur_score - trash_num
                if next_score<0:
                    knight_dic[kn][2]=0
                    # 지도 상에서 삭제 
                    grid = erase_knight(r, c, h, w, grid)
                else:
                    knight_dic[kn][2] = next_score




# 왕의 명령 순회
for q in q_list:
    knight, d = q 
    # 명령받은 knight가 체스판에 있을 때만 실행 (체력이 0 초과면)
    if knight_dic[knight][2]>0:
        move_knights(knight, d, grid, knight_dic)

answer = 0

for idx in range(1, N+1):
    if knight_dic[idx][2]>0:
        temp = first_knight_dic[idx][2] - knight_dic[idx][2]
        answer+=temp

print(answer)