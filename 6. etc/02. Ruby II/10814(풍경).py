# 링크 : https://jungol.co.kr/problem/10814
import sys

input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

# 에디토리얼 출처 : https://icpc.global/worldfinals/problems/2017-ICPC-World-Finals/finals2017solutions.pdf
# 레드 블랙 트리 소스 코드 출처 : https://lamp2357.tistory.com/46

# 너무 난이도가 높은 관계로 여기서는 설명하기 힘들고
# 나중에 티스토리 블로그에서 따로 설명하도록 하겠습니다.
# 추가로 맨 아래에 이 소스 코드를 어떻게 활용하는지 그 방법을 적어놓았으니
# 한번 구경하고 가세요.
# 와 이거 게시글 작성하는 것만 며칠 걸릴 정도로 매우 악랄한 난이도이네요.

# 1. Red-Black Tree (O(log N) Set)
class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1  # 1: RED, 0: BLACK

class RBTree:
    def __init__(self):
        self.TNULL:Node = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root:Node = self.TNULL
        self.tree_size:int = 0

    def search(self, k) -> Node:
        node:Node = self.root
        while node != self.TNULL:
            if k == node.data:
                return node
            elif k < node.data:
                node = node.left
            else:
                node = node.right
        return self.TNULL

    def minimum(self, node:Node) -> Node:
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node:Node) -> Node:
        while node.right != self.TNULL:
            node = node.right
        return node

    def predecessor(self, x:Node) -> Node:
        if x.left != self.TNULL:
            return self.maximum(x.left)
        y:Node = x.parent
        while y != None and x == y.left:
            x = y
            y = y.parent
        return y if y != None else self.TNULL

    def successor(self, x:Node) -> Node:
        if x.right != self.TNULL:
            return self.minimum(x.right)
        y:Node = x.parent
        while y != None and x == y.right:
            x = y
            y = y.parent
        return y if y != None else self.TNULL

    def left_rotate(self, x:Node) -> None:
        y:Node = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x:Node) -> None:
        y:Node = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert_fix(self, k:Node) -> None:
        while k.parent != None and k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u:Node = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u:Node = k.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def insert(self, key) -> None:
        if self.search(key) != self.TNULL:
            return
        node:Node = Node(key)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y:Node = None
        x:Node = self.root
        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            self.tree_size += 1
            return
        if node.parent.parent == None:
            self.tree_size += 1
            return

        self.insert_fix(node)
        self.tree_size += 1

    def rb_transplant(self, u:Node, v:Node) -> None:
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_fix(self, x:Node) -> None:
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s:Node = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s:Node = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left
                if s.right.color == 0 and s.left.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def delete(self, key) -> None:
        z:Node = self.search(key)
        if z == self.TNULL:
            return
        y:Node = z
        y_original_color:int = y.color
        if z.left == self.TNULL:
            x:Node = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x:Node = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        self.tree_size -= 1
        if y_original_color == 0:
            self.delete_fix(x)

    def lower_bound(self, k) -> Node:
        node:Node = self.root
        result:Node = self.TNULL
        while node != self.TNULL:
            if node.data == k:
                return node
            elif node.data > k:
                result = node
                node = node.left
            else:
                node = node.right
        return result

    def upper_bound(self, k) -> Node:
        node:Node = self.root
        result:Node = self.TNULL
        while node != self.TNULL:
            if node.data > k:
                result = node
                node = node.left
            else:
                node = node.right
        return result

# 펜윅 트리(세그먼트 트리)
class FenwickTree:
    def __init__(self, size: int):
        self.tree: list = [0 for _ in range(size + 1)]
        
    def update(self, index: int, value: int):
        while index < len(self.tree):
            self.tree[index] += value
            index += index & (-index)
            
    def query(self, index: int) -> int:
        s: int = 0
        while index > 0:
            s += self.tree[index]
            index -= index & (-index)
        return s

# 분리 집합
class UnionFind:
    def __init__(self, n:int):
        self.parent:list = [i for i in range(n)]
        self.offset:list = [0 for _ in range(n)]

    def find(self, x:int) -> int:
        if self.parent[x] == x:
            return x
        p: int = self.find(self.parent[x])
        if p != self.parent[x]:
            self.offset[x] += self.offset[self.parent[x]]
        self.parent[x] = p
        return p

def lower_bound_list(array:list, target, start:int, end:int) -> int:
    left, right = start, end - 1
    result:int = end
    while left <= right:
        mid:int = (left + right) // 2
        if array[mid] >= target:
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    return result

def compute_pseudo_critical_time(tree:FenwickTree, pseudo_offset_forest:UnionFind, deadlines:list, index:int, t:int) -> int:
    root:int = pseudo_offset_forest.find(index)
    ret:int = deadlines[index]
    ret -= pseudo_offset_forest.offset[index]
    
    if index != root:
        ret -= pseudo_offset_forest.offset[root]
    
    ret -= tree.query(index) * t
    return ret

def update_q(fractional_offset_tree:RBTree, pseudo_offset_forest:UnionFind, a:int, b:int, t:int) -> None:
    a %= t
    b %= t
    
    if a < b:
        affected:list = []
        node:Node = fractional_offset_tree.upper_bound((a, float('inf')))
        
        # 반복 중 트리가 수정되는 것을 막기 위해 데이터를 먼저 수집합니다.
        while node != fractional_offset_tree.TNULL:
            if node.data[0] <= b:
                affected.append(node.data)
                node = fractional_offset_tree.successor(node)
            else:
                break
        
        for data in affected:
            fractional_offset_tree.delete(data)
            
        if affected:
            root:int = affected[0][1]
            pseudo_offset_forest.offset[root] += affected[0][0] - a
            for k in range(1, len(affected), 1):
                pseudo_offset_forest.parent[affected[k][1]] = root
                pseudo_offset_forest.offset[affected[k][1]] += affected[k][0] - a - pseudo_offset_forest.offset[root]
            fractional_offset_tree.insert((a, root))
            
    else:
        # a >= b 인 경우 (두 구간으로 나뉘어 처리)
        affected:list = []
        node:Node = fractional_offset_tree.upper_bound((a, float('inf')))
        
        while node != fractional_offset_tree.TNULL:
            affected.append(node.data)
            node = fractional_offset_tree.successor(node)
            
        for data in affected:
            fractional_offset_tree.delete(data)
            
        if affected:
            root:int = affected[0][1]
            pseudo_offset_forest.offset[root] += affected[0][0] - a
            for k in range(1, len(affected), 1):
                pseudo_offset_forest.parent[affected[k][1]] = root
                pseudo_offset_forest.offset[affected[k][1]] += affected[k][0] - a - pseudo_offset_forest.offset[root]
            fractional_offset_tree.insert((a, root))
            
        affected2:list = []
        node2:Node = fractional_offset_tree.minimum(fractional_offset_tree.root)
        
        while node2 != fractional_offset_tree.TNULL:
            if node2.data[0] <= b:
                affected2.append(node2.data)
                node2 = fractional_offset_tree.successor(node2)
            else:
                break
                
        for data in affected2:
            fractional_offset_tree.delete(data)
            
        if affected2:
            root:int = affected2[0][1]
            pseudo_offset_forest.offset[root] += affected2[0][0] - a + t
            for k in range(1, len(affected2), 1):
                pseudo_offset_forest.parent[affected2[k][1]] = root
                pseudo_offset_forest.offset[affected2[k][1]] += affected2[k][0] - a + t - pseudo_offset_forest.offset[root]
            fractional_offset_tree.insert((a, root))

def run_simulation(N:int, T:int, photographs:list, deadlines:list) -> bool:
    tree:FenwickTree = FenwickTree(N + 1)
    forbidden_regions:list = []
    fractional_offset_tree:RBTree = RBTree()  
    pseudo_offset_forest:UnionFind = UnionFind(N + 1)
    relevant_deadlines:RBTree = RBTree()      
    deadline_next:int = N + 1

    # 역방향 탐색 및 마감일(Deadline) 검증 알고리즘
    for i in range(N, 0, -1):
        a:int = photographs[i][0]
        b:int = photographs[i][1]
        
        index:int = lower_bound_list(deadlines, b, 1, N + 1)
        
        tree.update(index, 1)
        
        if deadline_next > index:
            while deadline_next > index:
                deadline_next -= 1
                q:int = deadlines[deadline_next] % T
                fractional_offset_tree.insert((q, deadline_next))
                
                if relevant_deadlines.tree_size == 0:
                    relevant_deadlines.insert(deadline_next)
                else:
                    first:int = relevant_deadlines.minimum(relevant_deadlines.root).data
                    c_prime:int = compute_pseudo_critical_time(tree, pseudo_offset_forest, deadlines, first, T)
                    
                    if deadlines[deadline_next] - T < c_prime:
                        relevant_deadlines.insert(deadline_next)
                        
        else:
            r_node:Node = relevant_deadlines.lower_bound(index)
            if r_node != relevant_deadlines.TNULL:
                index_relevant:int = r_node.data
                c_prime:int = compute_pseudo_critical_time(tree, pseudo_offset_forest, deadlines, index_relevant, T)
                
                while True:
                    current_bound:Node = relevant_deadlines.lower_bound(index)
                    if current_bound != relevant_deadlines.TNULL:
                        p_node:Node = relevant_deadlines.predecessor(current_bound)
                    else:
                        # 모든 원소가 index보다 작다면 트리 최댓값이 predecessor가 됩니다.
                        p_node:Node = relevant_deadlines.maximum(relevant_deadlines.root)
                        
                    if p_node != relevant_deadlines.TNULL:
                        p_index:int = p_node.data
                        if compute_pseudo_critical_time(tree, pseudo_offset_forest, deadlines, p_index, T) >= c_prime:
                            relevant_deadlines.delete(p_index)
                            continue
                    break
                    
        if relevant_deadlines.tree_size == 0:
            return False, []
            
        first:int = relevant_deadlines.minimum(relevant_deadlines.root).data
        c_min_prime:int = compute_pseudo_critical_time(tree, pseudo_offset_forest, deadlines, first, T)
        
        if c_min_prime < a:
            return False, []
            
        if c_min_prime < a + T:
            endpoint_left:int = c_min_prime - T
            endpoint_right:int = a - 1
            
            if forbidden_regions:
                endpoint_right = min(endpoint_right, forbidden_regions[-1][0])
                
            if endpoint_left < endpoint_right:
                update_q(fractional_offset_tree, pseudo_offset_forest, endpoint_left, endpoint_right, T)
                forbidden_regions.append((endpoint_left, endpoint_right))
                
    return True, forbidden_regions
    
N, T = map(int, input().split())

photographs:list = [(0, 0) for _ in range(N + 1)]
deadlines:list = [0 for _ in range(N + 1)]

for i in range(1, N + 1, 1):
    a, b = map(int, input().split())
    photographs[i] = (a, b, i)
    deadlines[i] = b
    
photographs[1:] = sorted(photographs[1:], key=lambda x: x[0])
deadlines[1:] = sorted(deadlines[1:])

result, forbidden_regions = run_simulation(N, T, photographs, deadlines)

if result:
    print("yes")
    """
    import heapq
    
    # 1. 금지 구역(Forbidden Regions) 병합 및 정렬
    merged_forbidden = []
    if forbidden_regions:
        forbidden_regions.sort(key=lambda x: x[0])  # 시작 시간 오름차순 정렬
        merged_forbidden.append(forbidden_regions[0])
        
        for i in range(1, len(forbidden_regions)):
            last_L, last_R = merged_forbidden[-1]
            current_L, current_R = forbidden_regions[i]
            
            # 구간이 겹치거나 바로 이어지는 경우 하나로 병합 (ex: [1, 3]과 [4, 5] -> [1, 5])
            if current_L <= last_R + 1:
                merged_forbidden[-1] = (last_L, max(last_R, current_R))
            else:
                merged_forbidden.append((current_L, current_R))
                
    # 2. 우선순위 큐(Min-Heap) 및 스윕 라인 변수 초기화
    min_heap = []
    schedule_result = []
    current_time = 0
    p_index = 1
    f_index = 0
    
    # 3. 모든 작업을 스케줄링할 때까지 타임라인 진행 (EDF 방식)
    while p_index <= N or min_heap:
        # (1) 힙이 비어있다면, 다음 작업의 시작 가능 시간으로 점프 (불필요한 공백 시간 건너뛰기)
        if not min_heap and p_index <= N:
            if current_time < photographs[p_index][0]:
                current_time = photographs[p_index][0]
        
        # (2) 현재 시간이 금지 구역에 속해 있는지 확인하고 회피
        while f_index < len(merged_forbidden):
            L, R = merged_forbidden[f_index]
            if current_time > R:
                f_index += 1
            elif L <= current_time <= R:
                current_time = R + 1  # 금지 구역을 벗어나는 즉시 시간으로 강제 점프!
                f_index += 1
            else:
                break
        
        # (3) 현재 시간 기준으로 시작할 수 있는 모든 작업을 힙에 투입
        while p_index <= N and photographs[p_index][0] <= current_time:
            a, b, original_id = photographs[p_index]
            # 마감일(b)이 가장 급한 순으로 자동 정렬되도록 힙에 추가
            heapq.heappush(min_heap, (b, a, p_index, original_id))
            p_index += 1
            
        # (4) 힙이 비어있다면 (금지 구역 점프 후 아직 시작 시간이 안 된 경우) 루프 재개
        if not min_heap:
            continue
            
        # (5) EDF(Earliest Deadline First) 로직 적용하여 최적 작업 꺼내기
        deadline, release_time, photo_id, original_id = heapq.heappop(min_heap)
        
        start_time = current_time
        end_time = current_time + T
        schedule_result.append((photo_id, original_id, start_time, end_time))
        
        # (6) 작업 시간(T)만큼 머신(카메라) 점유 후 타임라인 전진
        current_time += T

    # 4. 도출된 실제 타임라인(경로) 출력
    print("--- [최적 스케줄링 타임라인] ---")
    for photo_id, original_id, s_time, e_time in schedule_result:
        print(f"정렬된 작업 {photo_id:>2} (원본 {original_id:>2}) | 시작: {s_time:>4} ~ 종료: {e_time:>4}")
    """

else:
    print("no")
    """
    import heapq
    
    # "no" 판정 시에는 금지 구역이 무의미하므로, 순수 포워드 탐색을 진행합니다.
    min_heap = []
    schedule_result = []
    discarded_jobs = []
    
    current_time = 0
    p_index = 1
    
    # 타임라인 진행
    while p_index <= N or min_heap:
        # (1) 힙이 비어있다면 다음 작업의 시작 가능 시간으로 타임라인 점프
        if not min_heap and p_index <= N:
            if current_time < photographs[p_index][0]:
                current_time = photographs[p_index][0]
        
        # (2) 현재 시간까지 도착한 모든 작업을 힙에 투입
        while p_index <= N and photographs[p_index][0] <= current_time:
            a, b, original_id = photographs[p_index]
            # 우선순위 큐: 마감일(b)이 가장 급한 작업이 먼저 나오도록 정렬
            heapq.heappush(min_heap, (b, a, p_index, original_id))
            p_index += 1
            
        if not min_heap:
            continue
            
        # (3) 가장 급박한 작업(Earliest Deadline) 꺼내기
        deadline, release_time, photo_id, original_id = heapq.heappop(min_heap)
        
        start_time = current_time
        
        # (4) 스케줄링 가능 여부 확인 및 추출(Ejection) 로직
        if start_time + T <= deadline:
            # 4-1. 기한 내에 처리 가능하면 스케줄 확정 및 시간 전진
            end_time = start_time + T
            schedule_result.append((photo_id, original_id, start_time, end_time))
            current_time = end_time
        else:
            # 4-2. 이미 마감일을 넘겼다면 과감히 포기(Discard)하고 타임라인 유지
            discarded_jobs.append((photo_id, original_id))
            
    # 5. 최종 리포팅
    print(f"결과: 전체 {N}개 중 최대 {len(schedule_result)}개 작업 완료 가능 (포기: {len(discarded_jobs)}개)\n")
    
    for photo_id, original_id, s_time, e_time in schedule_result:
        print(f"정렬된 작업 {photo_id:>2} (원본 {original_id:>2}) | 시작: {s_time:>4} ~ 종료: {e_time:>4}")
        
    if discarded_jobs:
        print(f"\n[기각(포기)된 작업 번호 목록]")
        discarded_strings = [f"정렬 {p_id}(원본 {o_id})" for p_id, o_id in discarded_jobs]
        print(", ".join(discarded_strings))
    """

# 마무리 코멘트
"""
이 작업을 통해
1회차에서 최대한 많은 물량들을 완료시키고
만약 남은 물량들이 존재하는 경우
작업 시간 t를 -1씩 감소시키면서 브루트 포스로 시뮬레이션 돌리고
만약 남은 물량에서 "yes"로 판정되면
2회차에서 계산된 작업 시간 t로 남은 물량들을 모두 완료하면 됩니다.

예를 들어
15 10
0 10
0 12
0 14
0 16
0 20
0 30
30 40
30 50
30 60
60 70
60 80
60 90
60 100
60 110
60 120
이런 테스트 케이스가 있다고 가정합니다.

만약 위에 해둔 주석을 해제하고 시뮬레이션 돌리면 다음과 같은 결과가 나옵니다.
no
결과: 전체 15개 중 최대 12개 작업 완료 가능 (포기: 3개)

정렬된 작업  1 (원본  1) | 시작:    0 ~ 종료:   10
정렬된 작업  5 (원본  5) | 시작:   10 ~ 종료:   20
정렬된 작업  6 (원본  6) | 시작:   20 ~ 종료:   30
정렬된 작업  7 (원본  7) | 시작:   30 ~ 종료:   40
정렬된 작업  8 (원본  8) | 시작:   40 ~ 종료:   50
정렬된 작업  9 (원본  9) | 시작:   50 ~ 종료:   60
정렬된 작업 10 (원본 10) | 시작:   60 ~ 종료:   70
정렬된 작업 11 (원본 11) | 시작:   70 ~ 종료:   80
정렬된 작업 12 (원본 12) | 시작:   80 ~ 종료:   90
정렬된 작업 13 (원본 13) | 시작:   90 ~ 종료:  100
정렬된 작업 14 (원본 14) | 시작:  100 ~ 종료:  110
정렬된 작업 15 (원본 15) | 시작:  110 ~ 종료:  120

[기각(포기)된 작업 번호 목록]
정렬 2(원본 2), 정렬 3(원본 3), 정렬 4(원본 4)

여기서 (0~12), (0~14), (0~16) 작업이 기각되었습니다.
그러므로 여기서
3 T
0 12
0 14
0 16
이렇게 2회차 테스트 케이스가 만들어집니다.
만약 T = 5, T = 6으로 한다면 어떻게 될까요?
{테스트 케이스 입력 1}
3 6
0 12
0 14
0 16
{테스트 케이스 출력 1}
no
결과: 전체 3개 중 최대 2개 작업 완료 가능 (포기: 1개)

정렬된 작업  1 (원본  1) | 시작:    0 ~ 종료:    6
정렬된 작업  2 (원본  2) | 시작:    6 ~ 종료:   12

[기각(포기)된 작업 번호 목록]
정렬 3(원본 3)
{테스트 케이스 입력 2}
3 5
0 12
0 14
0 16
{테스트 케이스 출력 2}
yes
--- [최적 스케줄링 타임라인] ---
정렬된 작업  1 (원본  1) | 시작:    0 ~ 종료:    5
정렬된 작업  2 (원본  2) | 시작:    5 ~ 종료:   10
정렬된 작업  3 (원본  3) | 시작:   10 ~ 종료:   15

2회차에서는 T = 5로 남은 물량들을 모두 해치울 수 있습니다.


이렇게 작업 물량이 15개 있고 1회차 작업시간이 10이라고 가정할 때
15 10
0 10
0 12
0 14
0 16
0 20
0 30
30 40
30 50
30 60
60 70
60 80
60 90
60 100
60 110
60 120
이런 테스트 케이스가 있다면 15개 중 12개를 1회차에 작업 완료 시키고
남은 3개는 2회차 작업시간을 5로 해서 2회차 모든 작업을 완료 시킬 수 있습니다.


이렇게 PS 문제를 실전성 있게 활용할 수 있는 가능성을 만들었습니다.
"""