# 링크 : https://jungol.co.kr/problem/8009
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

# 세그먼트 트리 비츠 참고 자료 : https://justicehui.github.io/hard-algorithm/2019/10/10/segment-tree-beats/
# 추가로 원래 이 문제는 단조 스택 + PST 문제이긴 한데 굳이 Beats로 바꾸는 이유는 다음과 같습니다.
# 1. 이 문제는 1차원 순방향 DP 리스트이고
# 2. 그 다음 부분 구간에 대하여 max(L[i], a_i)를 적용해야 하며
# 3. 과거의 기록까지 다 보는 것이 아닌 최적해만 구하는 것이므로
# 4. 2차원이면 PST가 더 유용하나 1차원인 경우 PST가 오히려 메모리 부분에서 효율성이 떨어지므로
# 5. 1차원 최적해만 구하는 경우 메모리 부분에서 Beats가 더 효율적입니다.

INF = 10 ** 18

"""
동적 배열 A(dynamic_value)와 정적 배열 B(base_value)에 대해
1. 구간 chmax 갱신: A[k] = max(A[k], update_value)
2. 단일 원소 갱신 및 조회
3. 구간 최솟값 쿼리: min(A[k] + B[k])
를 수행하는 범용 세그먼트 트리 비츠 클래스
"""
class SegmentTreeBeats:
    def __init__(self, element_count:int) -> None:
        self.element_count:int = element_count
        self.tree_height:int = (element_count - 1).bit_length()
        self.leaf_offset:int = 1 << self.tree_height
        self.tree_capacity:int = self.leaf_offset << 1

        # 비츠 관리를 위한 노드 상태 배열
        self.first_min_value:list = [INF] * self.tree_capacity
        self.second_min_value:list = [INF] * self.tree_capacity
        self.first_min_base:list = [INF] * self.tree_capacity
        self.other_min_sum:list = [INF] * self.tree_capacity
        self.total_min_sum:list = [INF] * self.tree_capacity

    # 바텀 업(Bottom-Up) 방식으로 전체 세그먼트 트리를 초기화합니다.
    def build(self, initial_dynamic_values:list, initial_base_values:list) -> None:
        limit:int = min(self.element_count, len(initial_dynamic_values))
        for index in range(limit):
            leaf_node:int = index + self.leaf_offset
            dynamic_value:int = initial_dynamic_values[index]
            base_value:int = initial_base_values[index]

            self.first_min_value[leaf_node] = dynamic_value
            self.second_min_value[leaf_node] = INF
            self.first_min_base[leaf_node] = base_value
            self.other_min_sum[leaf_node] = INF
            self.total_min_sum[leaf_node] = dynamic_value + base_value

        for parent_node in range(self.leaf_offset - 1, 0, -1):
            self.pull_up(parent_node)

    # 두 자식 노드(parent << 1, (parent << 1) | 1)의 정보를 부모 노드로 병합합니다.
    def pull_up(self, parent_node:int) -> None:
        left_child:int = parent_node << 1
        right_child:int = (parent_node << 1) | 1

        left_min1:int = self.first_min_value[left_child]
        right_min1:int = self.first_min_value[right_child]

        if left_min1 == right_min1:
            self.first_min_value[parent_node] = left_min1
            left_min2:int = self.second_min_value[left_child]
            right_min2:int = self.second_min_value[right_child]
            self.second_min_value[parent_node] = left_min2 if left_min2 < right_min2 else right_min2

            left_base:int = self.first_min_base[left_child]
            right_base:int = self.first_min_base[right_child]
            self.first_min_base[parent_node] = left_base if left_base < right_base else right_base

            left_other:int = self.other_min_sum[left_child]
            right_other:int = self.other_min_sum[right_child]
            self.other_min_sum[parent_node] = left_other if left_other < right_other else right_other

        elif left_min1 < right_min1:
            self.first_min_value[parent_node] = left_min1
            left_min2:int = self.second_min_value[left_child]
            self.second_min_value[parent_node] = left_min2 if left_min2 < right_min1 else right_min1

            self.first_min_base[parent_node] = self.first_min_base[left_child]

            left_other:int = self.other_min_sum[left_child]
            right_total:int = self.total_min_sum[right_child]
            self.other_min_sum[parent_node] = left_other if left_other < right_total else right_total

        else:
            self.first_min_value[parent_node] = right_min1
            right_min2:int = self.second_min_value[right_child]
            self.second_min_value[parent_node] = left_min1 if left_min1 < right_min2 else right_min2

            self.first_min_base[parent_node] = self.first_min_base[right_child]

            left_total:int = self.total_min_sum[left_child]
            right_other:int = self.other_min_sum[right_child]
            self.other_min_sum[parent_node] = left_total if left_total < right_other else right_other

        candidate_sum:int = self.first_min_value[parent_node] + self.first_min_base[parent_node]
        other_sum:int = self.other_min_sum[parent_node]
        self.total_min_sum[parent_node] = candidate_sum if candidate_sum < other_sum else other_sum

    # 단일 노드에 chmax 태그를 반영하고 구간의 최소 합을 O(1)에 갱신합니다.
    def apply_node_chmax(self, node_index:int, update_value:int) -> None:
        if update_value <= self.first_min_value[node_index]:
            return
        self.first_min_value[node_index] = update_value
        candidate_sum:int = update_value + self.first_min_base[node_index]
        other_sum:int = self.other_min_sum[node_index]
        self.total_min_sum[node_index] = candidate_sum if candidate_sum < other_sum else other_sum

    # 부모 노드의 최솟값(지연 태그)을 두 자식 노드로 전파합니다.
    def push_down(self, parent_node:int) -> None:
        parent_min1:int = self.first_min_value[parent_node]
        if parent_min1 >= INF:
            return

        left_child:int = parent_node << 1
        right_child:int = (parent_node << 1) | 1

        if self.first_min_value[left_child] < parent_min1:
            self.apply_node_chmax(left_child, parent_min1)
        if self.first_min_value[right_child] < parent_min1:
            self.apply_node_chmax(right_child, parent_min1)

    # 루트부터 특정 리프 노드까지의 경로에 쌓인 지연 태그를 위에서 아래로 전파합니다.
    def push_path_from_root(self, leaf_node:int) -> None:
        for bit_shift in range(self.tree_height, 0, -1):
            self.push_down(leaf_node >> bit_shift)

    # 특정 리프 노드부터 루트까지 바텀 업(child >> 1) 방식으로 갱신합니다.
    def pull_path_to_root(self, leaf_node:int) -> None:
        parent_node:int = leaf_node >> 1
        while parent_node >= 1:
            self.pull_up(parent_node)
            parent_node >>= 1

    # 바텀 업 방식으로 단일 인덱스의 (A[target_index], B[target_index]) 값을 설정합니다.
    def point_update(self, target_index:int, dynamic_value:int, base_value:int) -> None:
        leaf_node:int = target_index + self.leaf_offset
        self.push_path_from_root(leaf_node)

        self.first_min_value[leaf_node] = dynamic_value
        self.second_min_value[leaf_node] = INF
        self.first_min_base[leaf_node] = base_value
        self.other_min_sum[leaf_node] = INF
        self.total_min_sum[leaf_node] = dynamic_value + base_value

        self.pull_path_to_root(leaf_node)

    # 바텀 업 경로 추적을 통해 A[target_index]의 현재 값을 비재귀로 조회합니다.
    def point_get_dynamic(self, target_index:int) -> int:
        current_node:int = target_index + self.leaf_offset
        maximum_dynamic_value:int = self.first_min_value[current_node]
        current_node >>= 1
        while current_node >= 1:
            if self.first_min_value[current_node] < INF:
                if self.first_min_value[current_node] > maximum_dynamic_value:
                    maximum_dynamic_value = self.first_min_value[current_node]
            current_node >>= 1
        return maximum_dynamic_value

    # 구간 [query_left, query_right]에 대해 A[k] = max(A[k], update_value)를 수행합니다.
    def range_chmax(self, query_left:int, query_right:int, update_value:int) -> None:
        if query_left > query_right:
            return
        self._range_chmax_top_down(1, 0, self.leaf_offset - 1, query_left, query_right, update_value)

    # 세그먼트 트리 비츠의 Break / Tag 조건에 따라 탑 다운으로 구간을 갱신합니다.
    def _range_chmax_top_down(
        self,
        node_index:int,
        node_left:int,
        node_right:int,
        query_left:int,
        query_right:int,
        update_value:int
    ) -> None:
        # 1. Break Condition: 구간을 벗어나거나 갱신할 값이 현재 구간의 최솟값 이하인 경우
        if query_right < node_left or node_right < query_left or update_value <= self.first_min_value[node_index]:
            return

        # 2. Tag Condition: 구간에 완전히 포함되며 두 번째 최솟값보다 작은 경우 노드에서 즉시 처리
        if query_left <= node_left and node_right <= query_right and update_value < self.second_min_value[node_index]:
            self.apply_node_chmax(node_index, update_value)
            return

        # 3. 자식 노드로 분할 탐색 후 병합
        self.push_down(node_index)
        middle:int = (node_left + node_right) >> 1
        self._range_chmax_top_down(node_index << 1, node_left, middle, query_left, query_right, update_value)
        self._range_chmax_top_down((node_index << 1) | 1, middle + 1, node_right, query_left, query_right, update_value)
        self.pull_up(node_index)

    # 바텀 업 방식으로 구간 [query_left, query_right] 내의 min(A[k] + B[k])를 반환합니다.
    def range_query_min_sum(self, query_left:int, query_right:int) -> int:
        if query_left > query_right:
            return INF

        left_node:int = query_left + self.leaf_offset
        right_node:int = query_right + self.leaf_offset

        self.push_path_from_root(left_node)
        self.push_path_from_root(right_node)

        minimum_sum_result:int = INF
        while left_node <= right_node:
            if (left_node & 1) == 1:
                if self.total_min_sum[left_node] < minimum_sum_result:
                    minimum_sum_result = self.total_min_sum[left_node]
                left_node += 1
            if (right_node & 1) == 0:
                if self.total_min_sum[right_node] < minimum_sum_result:
                    minimum_sum_result = self.total_min_sum[right_node]
                right_node -= 1
            left_node >>= 1
            right_node >>= 1

        return minimum_sum_result

N, P = map(int, input().split())
A:list = list(map(int, input().split()))

tree:SegmentTreeBeats = SegmentTreeBeats(N)
dp:list = [0] * (N + 1)
left:int = 0

# 점화식: dp[i] = min{ dp[j] - j + max(a_k) } + i - 1  (단, j < k <= i)
# 여기서 max(a_k)는 분할 시작점 j부터 현재 i까지의 요구 편의성 최댓값을 의미합니다.
# 일반적인 지연 전파는 구간 전체에 일괄 덧셈(+x)이나 덮어쓰기(=x)만 가능할 뿐,
# 원소의 크기에 따라 갱신 여부가 달라지는 조건부 연산을 처리할 수 없습니다.
# 여기서 조건부 연산은 chmax(A[j], a_i)
# 따라서 Beats를 동원하여 트리 내부에서 상태(최솟값, 두번째 최솟값)를 추적하고,
# 조건에 맞는 원소들만 O(log N)에 한꺼번에 chmax 갱신을 수행합니다.
for current in range(1, N + 1):
    requirement:int = A[current - 1]
    index:int = current - 1

    # 1. 새로운 분할 시작점 j = current - 1 등록
    # 구간 [current, current]의 초기 최댓값 A[j] = a_i, 고정 가중치 B[j] = DP[j] - j
    tree.point_update(
        index,
        requirement,
        dp[index] - index
    )

    # 2. 이전 분할 시작점들 [left, current - 2]에 대해 A[j] = max(A[j], a_i) 갱신
    if left <= index - 1:
        tree.range_chmax(left, index - 1, requirement)

    # 3. 도로 하나의 비용 한계(P)를 초과하는 좌측 인덱스 배제
    # 조건: A[j] + current - j - 1 <= P  <=>  A[j] - j <= P - current + 1
    cost:int = P - current + 1
    while left < index:
        if tree.point_get_dynamic(left) - left > cost:
            left += 1
        else:
            break

    # 4. 유효한 구간 [left, current - 1]에서 최적의 DP 값 도출
    best:int = tree.range_query_min_sum(left, index)
    dp[current] = index + best

print(dp[N])