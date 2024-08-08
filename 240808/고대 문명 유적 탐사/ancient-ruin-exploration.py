from collections import deque

k, m = map(int, input().split()) 
grid = []
for i in range(5):
    grid.append(list(map(int, input().split()) ))

additional_list = list(map(int, input().split()))

angle_list = [270, 180, 90] 
center_list = [(3,3), (2,3), (1,3), (3,2), (2,2), (1,2), (3,1), (2,1), (1,1)]

change_list = [(0,1), (0,-1), (1,0), (-1,0)]

def rotate(grid_map, angle, center_pos):
    output_grid_map = []
    r, c = center_pos[0], center_pos[1]
    for x in grid_map:
        temp = []
        for y in x:
            temp.append(y)
        output_grid_map.append(temp)

    if angle == 90:
        output_grid_map[r-1][c+1] = grid_map[r-1][c-1]
        output_grid_map[r][c+1] = grid_map[r-1][c]
        output_grid_map[r+1][c+1] = grid_map[r-1][c+1]
        output_grid_map[r+1][c] = grid_map[r][c+1]
        output_grid_map[r+1][c-1] = grid_map[r+1][c+1]
        output_grid_map[r][c-1] = grid_map[r+1][c]
        output_grid_map[r-1][c-1] = grid_map[r+1][c-1]
        output_grid_map[r-1][c] = grid_map[r][c-1]

    elif angle == 180:
        for change in [-1,0,1]:
            output_grid_map[r+1][c+change] = grid_map[r-1][c+change]
            output_grid_map[r-1][c+change] = grid_map[r+1][c+change]
    
    elif angle == 270:
        output_grid_map[r-1][c-1] = grid_map[r-1][c+1]
        output_grid_map[r-1][c] = grid_map[r][c+1]
        output_grid_map[r-1][c+1] = grid_map[r+1][c+1]
        output_grid_map[r][c+1] = grid_map[r+1][c]
        output_grid_map[r+1][c+1] = grid_map[r+1][c-1]
        output_grid_map[r+1][c] = grid_map[r][c-1]
        output_grid_map[r+1][c-1] = grid_map[r-1][c-1]
        output_grid_map[r][c-1] = grid_map[r-1][c]

    return output_grid_map # 회전 후 그리드 맵

def search_value(grid_map):
    pos_list = []
    output_value = 0

    for i in range(5):
        for j in range(5):
            if [i,j] not in pos_list:
                queue = deque()
                queue.append((i,j))
                temp_value = 1
                temp_pos = [[i, j]]
                visited = [[False]*5 for i in range(5)]
                visited[i][j] = True
                while queue:
                    cur_r, cur_c = queue.popleft()
                    for change in change_list:
                        next_r, next_c = cur_r+change[0], cur_c+change[1]
                        # 조건1 : 좌표 범위를 벗어나지 않고, 조건2 : 다음 칸이 기존 숫자와 같은 경우, 조건3 : visited=False인 경우
                        if ((0<=next_r<5) and (0<=next_c<5)):
                            if (grid_map[next_r][next_c]==grid_map[cur_r][cur_c]) and visited[next_r][next_c]==False:
                                visited[next_r][next_c] = True
                                queue.append((next_r, next_c))
                                temp_pos.append([next_r,next_c])
                                temp_value += 1
                if temp_value >= 3:
                    pos_list.extend(temp_pos)
                    output_value += temp_value

    return output_value, pos_list


answer_list = []
for i in range(k):
    value_sum = 0
    # 1차 탐색 진행
    max_first_value = 0
    max_angle = angle_list[0]
    max_center = center_list[0]
    for ang in angle_list:
        for center in center_list:
            rotated_grid = rotate(grid, ang, center)
            first_value, value_pos_list = search_value(rotated_grid)
            if first_value>max_first_value:
                max_first_value = first_value
                max_angle = ang
                max_center = center
            elif first_value == max_first_value:
                # 우선순위1 : 회전한 각도가 최소화되는 경우 인정해줌.
                if ang < max_angle:
                    max_first_value = first_value
                    max_angle = ang
                    max_center = center
                # 우선순위2 : 중심 좌표 열이 작은 방향으로
                elif ang == max_angle:
                    if center[1] < max_center[1]:
                        max_first_value = first_value
                        max_angle = ang
                        max_center = center
                    # 우선순위3 : 중심 좌표 행이 작은 방향으로
                    elif center[1] == max_center[1]:
                        if center[0] < max_center[0]:
                            max_first_value = first_value
                            max_angle = ang
                            max_center = center          
            
    # 초기에 주어지는 유적지에서는 탐사 진행 이전에 유물이 발견되지 않으며, 첫 번째 턴에서 탐사를 진행한 이후에는 항상 유물이 발견됨을 가정해도 좋습니다.
    grid = rotate(grid, max_angle, max_center)
    # 유물 찾고 없애기
    # 연쇄적 탐사
    while True:
        value, prod_list = search_value(grid)
        # 제거 가능한 유물 있으면 제거
        if value >0:
            value_sum += value
            # 유적의 벽면에 적혀있는 순서대로 새로운 조각 만들기
            # 열 번호가 작은 순으로, 열 번호가 같다면 큰 순으로
            # [0] 요소 내림차순, [1] 요소 오름차순
            prod_list.sort(key=lambda x:(x[1], -x[0]))
            for prod in prod_list:
                new_prod = additional_list.pop(0)
                grid[prod[0]][prod[1]] = new_prod

        # 제거할 수 있는 유물 없으면, 중단
        else:
            break
    answer_list.append(value_sum)

answer = ""
for a in answer_list:
    if a!=0:
        answer += " " + str(a)

print(answer.strip())