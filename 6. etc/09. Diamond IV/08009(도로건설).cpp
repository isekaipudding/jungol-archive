// 링크 : https://jungol.co.kr/problem/8009
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const long long INF = 1e18; // 10 ** 18

/*
동적 배열 A(dynamic_value)와 정적 배열 B(base_value)에 대해
1. 구간 chmax 갱신: A[k] = max(A[k], update_value)
2. 단일 원소 갱신 및 조회
3. 구간 최솟값 쿼리: min(A[k] + B[k])
를 수행하는 범용 세그먼트 트리 비츠 클래스
*/
class SegmentTreeBeats {
public:
    int element_count;
    int tree_height;
    int leaf_offset;
    int tree_capacity;

    // 비츠 관리를 위한 노드 상태 배열
    vector<long long> first_min_value;
    vector<long long> second_min_value;
    vector<long long> first_min_base;
    vector<long long> other_min_sum;
    vector<long long> total_min_sum;

    // 파이썬의 (n).bit_length() 와 동일하게 동작하는 함수
    int get_bit_length(int n) {
        if (n == 0) return 0;
        return 32 - __builtin_clz(n);
    }

    SegmentTreeBeats(int element_count) {
        this->element_count = element_count;
        this->tree_height = get_bit_length(element_count - 1);
        this->leaf_offset = 1 << tree_height;
        this->tree_capacity = leaf_offset << 1;

        first_min_value.assign(tree_capacity, INF);
        second_min_value.assign(tree_capacity, INF);
        first_min_base.assign(tree_capacity, INF);
        other_min_sum.assign(tree_capacity, INF);
        total_min_sum.assign(tree_capacity, INF);
    }

    // 두 자식 노드(parent << 1, (parent << 1) | 1)의 정보를 부모 노드로 병합합니다.
    void pull_up(int parent_node) {
        int left_child = parent_node << 1;
        int right_child = (parent_node << 1) | 1;

        long long left_min1 = first_min_value[left_child];
        long long right_min1 = first_min_value[right_child];

        if (left_min1 == right_min1) {
            first_min_value[parent_node] = left_min1;
            long long left_min2 = second_min_value[left_child];
            long long right_min2 = second_min_value[right_child];
            second_min_value[parent_node] = min(left_min2, right_min2);

            long long left_base = first_min_base[left_child];
            long long right_base = first_min_base[right_child];
            first_min_base[parent_node] = min(left_base, right_base);

            long long left_other = other_min_sum[left_child];
            long long right_other = other_min_sum[right_child];
            other_min_sum[parent_node] = min(left_other, right_other);

        } else if (left_min1 < right_min1) {
            first_min_value[parent_node] = left_min1;
            long long left_min2 = second_min_value[left_child];
            second_min_value[parent_node] = min(left_min2, right_min1);

            first_min_base[parent_node] = first_min_base[left_child];

            long long left_other = other_min_sum[left_child];
            long long right_total = total_min_sum[right_child];
            other_min_sum[parent_node] = min(left_other, right_total);

        } else {
            first_min_value[parent_node] = right_min1;
            long long right_min2 = second_min_value[right_child];
            second_min_value[parent_node] = min(left_min1, right_min2);

            first_min_base[parent_node] = first_min_base[right_child];

            long long left_total = total_min_sum[left_child];
            long long right_other = other_min_sum[right_child];
            other_min_sum[parent_node] = min(left_total, right_other);
        }

        long long candidate_sum = first_min_value[parent_node] + first_min_base[parent_node];
        long long other_sum = other_min_sum[parent_node];
        total_min_sum[parent_node] = min(candidate_sum, other_sum);
    }

    // 단일 노드에 chmax 태그를 반영하고 구간의 최소 합을 O(1)에 갱신합니다.
    void apply_node_chmax(int node_index, long long update_value) {
        if (update_value <= first_min_value[node_index]) {
            return;
        }
        first_min_value[node_index] = update_value;
        long long candidate_sum = update_value + first_min_base[node_index];
        long long other_sum = other_min_sum[node_index];
        total_min_sum[node_index] = min(candidate_sum, other_sum);
    }

    // 부모 노드의 최솟값(지연 태그)을 두 자식 노드로 전파합니다.
    void push_down(int parent_node) {
        long long parent_min1 = first_min_value[parent_node];
        if (parent_min1 >= INF) return;

        int left_child = parent_node << 1;
        int right_child = (parent_node << 1) | 1;

        if (first_min_value[left_child] < parent_min1) {
            apply_node_chmax(left_child, parent_min1);
        }
        if (first_min_value[right_child] < parent_min1) {
            apply_node_chmax(right_child, parent_min1);
        }
    }

    // 루트부터 특정 리프 노드까지의 경로에 쌓인 지연 태그를 위에서 아래로 전파합니다.
    void push_path_from_root(int leaf_node) {
        for (int bit_shift = tree_height; bit_shift > 0; --bit_shift) {
            push_down(leaf_node >> bit_shift);
        }
    }

    // 특정 리프 노드부터 루트까지 바텀 업(child >> 1) 방식으로 갱신합니다.
    void pull_path_to_root(int leaf_node) {
        int parent_node = leaf_node >> 1;
        while (parent_node >= 1) {
            pull_up(parent_node);
            parent_node >>= 1;
        }
    }

    // 바텀 업 방식으로 단일 인덱스의 (A[target_index], B[target_index]) 값을 설정합니다.
    void point_update(int target_index, long long dynamic_value, long long base_value) {
        int leaf_node = target_index + leaf_offset;
        push_path_from_root(leaf_node);

        first_min_value[leaf_node] = dynamic_value;
        second_min_value[leaf_node] = INF;
        first_min_base[leaf_node] = base_value;
        other_min_sum[leaf_node] = INF;
        total_min_sum[leaf_node] = dynamic_value + base_value;

        pull_path_to_root(leaf_node);
    }

    // 바텀 업 경로 추적을 통해 A[target_index]의 현재 값을 비재귀로 조회합니다.
    long long point_get_dynamic(int target_index) {
        int current_node = target_index + leaf_offset;
        long long maximum_dynamic_value = first_min_value[current_node];
        current_node >>= 1;
        while (current_node >= 1) {
            if (first_min_value[current_node] < INF) {
                if (first_min_value[current_node] > maximum_dynamic_value) {
                    maximum_dynamic_value = first_min_value[current_node];
                }
            }
            current_node >>= 1;
        }
        return maximum_dynamic_value;
    }

    // 세그먼트 트리 비츠의 Break / Tag 조건에 따라 탑 다운으로 구간을 갱신합니다.
    void _range_chmax_top_down(int node_index, int node_left, int node_right, int query_left, int query_right, long long update_value) {
        // 1. Break Condition
        if (query_right < node_left || node_right < query_left || update_value <= first_min_value[node_index]) {
            return;
        }

        // 2. Tag Condition
        if (query_left <= node_left && node_right <= query_right && update_value < second_min_value[node_index]) {
            apply_node_chmax(node_index, update_value);
            return;
        }

        // 3. 자식 노드로 분할 탐색 후 병합
        push_down(node_index);
        int middle = (node_left + node_right) >> 1;
        _range_chmax_top_down(node_index << 1, node_left, middle, query_left, query_right, update_value);
        _range_chmax_top_down((node_index << 1) | 1, middle + 1, node_right, query_left, query_right, update_value);
        pull_up(node_index);
    }

    // 구간 [query_left, query_right]에 대해 A[k] = max(A[k], update_value)를 수행합니다.
    void range_chmax(int query_left, int query_right, long long update_value) {
        if (query_left > query_right) return;
        _range_chmax_top_down(1, 0, leaf_offset - 1, query_left, query_right, update_value);
    }

    // 바텀 업 방식으로 구간 [query_left, query_right] 내의 min(A[k] + B[k])를 반환합니다.
    long long range_query_min_sum(int query_left, int query_right) {
        if (query_left > query_right) return INF;

        int left_node = query_left + leaf_offset;
        int right_node = query_right + leaf_offset;

        push_path_from_root(left_node);
        push_path_from_root(right_node);

        long long minimum_sum_result = INF;
        while (left_node <= right_node) {
            if ((left_node & 1) == 1) {
                if (total_min_sum[left_node] < minimum_sum_result) {
                    minimum_sum_result = total_min_sum[left_node];
                }
                left_node += 1;
            }
            if ((right_node & 1) == 0) {
                if (total_min_sum[right_node] < minimum_sum_result) {
                    minimum_sum_result = total_min_sum[right_node];
                }
                right_node -= 1;
            }
            left_node >>= 1;
            right_node >>= 1;
        }

        return minimum_sum_result;
    }
};


// 세그먼트 트리 비츠 참고 자료 : https://justicehui.github.io/hard-algorithm/2019/10/10/segment-tree-beats/
// 추가로 원래 이 문제는 단조 스택 + PST 문제이긴 한데 굳이 Beats로 바꾸는 이유는 다음과 같습니다.
// 1. 이 문제는 1차원 순방향 DP 리스트이고
// 2. 그 다음 부분 구간에 대하여 max(L[i], a_i)를 적용해야 하며
// 3. 과거의 기록까지 다 보는 것이 아닌 최적해만 구하는 것이므로
// 4. 2차원이면 PST가 더 유용하나 1차원인 경우 PST가 오히려 메모리 부분에서 효율성이 떨어지므로
// 5. 1차원 최적해만 구하는 경우 메모리 부분에서 Beats가 더 효율적입니다.
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    long long P;
    cin >> N >> P;

    vector<long long> A(N);
    for (int i = 0; i < N; i++) {
        cin >> A[i];
    }

    SegmentTreeBeats tree(N);
    vector<long long> dp(N + 1, 0);
    int left = 0;
    
    // 점화식: dp[i] = min{ dp[j] - j + max(a_k) } + i - 1  (단, j < k <= i)
    // 여기서 max(a_k)는 분할 시작점 j부터 현재 i까지의 요구 편의성 최댓값을 의미합니다.
    // 일반적인 지연 전파는 구간 전체에 일괄 덧셈(+x)이나 덮어쓰기(=x)만 가능할 뿐,
    // 원소의 크기에 따라 갱신 여부가 달라지는 조건부 연산을 처리할 수 없습니다.
    // 여기서 조건부 연산은 chmax(A[j], a_i)
    // 따라서 Beats를 동원하여 트리 내부에서 상태(최솟값, 두번째 최솟값)를 추적하고,
    // 조건에 맞는 원소들만 O(log N)에 한꺼번에 chmax 갱신을 수행합니다.
    for (int current = 1; current <= N; current++) {
        long long requirement = A[current - 1];
        int index = current - 1;

        // 1. 새로운 분할 시작점 j = current - 1 등록
        tree.point_update(index, requirement, dp[index] - index);

        // 2. 이전 분할 시작점들 [left, current - 2]에 대해 A[j] = max(A[j], a_i) 갱신
        if (left <= index - 1) {
            tree.range_chmax(left, index - 1, requirement);
        }

        // 3. 도로 하나의 비용 한계(P)를 초과하는 좌측 인덱스 배제
        long long cost = P - current + 1;
        while (left < index) {
            if (tree.point_get_dynamic(left) - left > cost) {
                left += 1;
            } else {
                break;
            }
        }

        // 4. 유효한 구간 [left, current - 1]에서 최적의 DP 값 도출
        long long best = tree.range_query_min_sum(left, index);
        dp[current] = index + best;
    }

    cout << dp[N] << "\n";

    return 0;
}