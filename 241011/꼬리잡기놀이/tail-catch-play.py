from collections import deque


def main():
    n, m, k = map(int, input().split(" "))

    grid_map = []
    for i in range(n):
        temp = list(map(int, input().split(" ")))
        grid_map.append(temp)

    team_score = [0]*m

    direction_list = [[1,0], [-1,0], [0,1], [0,-1]]

    man_list = []
    
    def bfs(start_r, start_c, team_num, visited):
        q = deque()
        q.append([start_r, start_c])
        visited[start_r][start_c] = True
        team_list = [[grid_map[start_r][start_c], [start_r, start_c], team_num]]

        while q:
            cur_r, cur_c = q.popleft()
            for d in direction_list:
                next_r, next_c = cur_r+d[0], cur_c+d[1]
                if 0<=next_r<n and 0<=next_c<n:
                    if 1<=grid_map[next_r][next_c]<=3 and visited[next_r][next_c]==False:
                        visited[next_r][next_c] = True
                        q.append([next_r, next_c])
                        team_list.append([grid_map[next_r][next_c], [next_r, next_c], team_num])
        return team_list, visited

    num_t = 0
    visited = [[False]*n for _ in range(n)] 
    for i in range(n):
        for j in range(n):
            if grid_map[i][j]==1 and visited[i][j]==False:
                t_list, visited = bfs(i,j,num_t, visited)
                if len(t_list)>0:
                    t_list.sort()
                    man_list.append(t_list)

    debugging = 0

    for turn in range(k):

        turn+=1

        debugging = 0

        # 1. 각 팀은 머리사람을 따라서 한 칸 이동
        for t_idx, team in enumerate(man_list):
            for m_idx, man in enumerate(team):
                cur_r, cur_c = man[1]
                if man[0]==1 :
                    for d in direction_list:
                        next_r, next_c = cur_r+d[0], cur_c+d[1]
                        if 0<=next_r<n and 0<=next_c<n:
                            if grid_map[next_r][next_c]==4 or grid_map[next_r][next_c]==3:
                                break
                man_list[t_idx][m_idx][1] = [next_r, next_c]
                next_r, next_c = cur_r, cur_c
                grid_map[cur_r][cur_c] = 4


        for team in man_list:
            for man in team:
                r, c = man[1][0], man[1][1]
                grid_map[r][c] = man[0]

        debugging = 0


        # 2. 각 라운드마다 공이 정해진 선을 따라 던져짐.
        def get_ball():

            temp = (turn//n)%4
            if turn%n==0:
                temp = ((turn//n) - 1)%4

            if temp==0 or temp==1:
                if temp==0:
                    row_col = "row"
                elif temp==1:
                    row_col = "col"
                min_max = "min"
                t_num = turn%n
                if t_num==0:
                    x = n-1
                else:
                    x = t_num-1
            else:
                if temp==2:
                    row_col = "row"
                elif temp==3:
                    row_col = "col"
                min_max = "max"
                t_num = turn%n
                if t_num==0:
                    x = 0
                else:
                    x = n - t_num
            return x, row_col, min_max
        
        x, row_col, min_max = get_ball()

        get_score_man = [25,25]

        if row_col=="row" and min_max=="min":
            for idx, grid in enumerate(grid_map[x]):
                if 1<=grid<=3:
                    get_score_man = [x, idx]
                    break
        elif row_col=="row" and min_max=="max":
            for idx in range(n-1,-1, -1):
                if 1<=grid_map[x][idx]<=3:
                    get_score_man = [x, idx]
                    break
        elif row_col == "col" and min_max=="min":
            for idx in range(n-1, -1, -1):
                if 1<=grid_map[idx][x]<=3:
                    get_score_man = [idx, x]
                    break
        elif row_col == "col" and min_max=="max":
            for idx in range(0, n):
                if 1<=grid_map[idx][x]<=3:
                    get_score_man = [idx, x]
                    break

        if get_score_man!=[25,25]:
            for t_idx, team in enumerate(man_list):
                for m_idx, man in enumerate(team):
                    if man[1]==get_score_man:
                        team_score[t_idx]+=(m_idx+1)**2
                        man_list[t_idx][0][0] = 3
                        man_list[t_idx][-1][0] = 1
                        grid_map[man_list[t_idx][0][1][0]][man_list[t_idx][0][1][1]] = 3
                        grid_map[man_list[t_idx][-1][1][0]][man_list[t_idx][-1][1][1]] = 1
                        # before_head = man_list[t_idx][0]
                        # before_tail = man_list[t_idx][-1]
                        new_team = []
                        for t in reversed(team):
                            new_team.append(t)
                        man_list[t_idx]=new_team
                        break


    debugging = 0

    print(sum(team_score))


main()