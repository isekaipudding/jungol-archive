// 링크 : https://jungol.co.kr/problem/4243

// GCC 컴파일러 극한 최적화 (SIMD, 루프 언롤링, 메모리 사전 인출)
#pragma GCC optimize("O3")
#pragma GCC optimize("Ofast")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("avx,avx2,fma")

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

// 제가 할 수 있는 온몸 비틀기란 비틀기는 다 했습니다...
// vector, pair, set 등 C++ STL 컨테이너를 완전히 멸망시키고 순수 1차원 C 배열로 평탄화했습니다!
// 이제 C++ 객체지향마저 버리고 완벽한 절차지향 C언어 하드웨어 컨트롤 모드로 진입합니다.

#define INF 1000000000
#define MAXN 131072      // 1 << 17
#define MAXT 262154      // 세그먼트 트리 최대 노드 수 1 << 18 + 패딩 10
#define MAX_MEM 2097152  // 2D 세그먼트 트리를 1D로 평탄화하기 위한 최대 원소 수 (1 << 21)
#define MAX_PLAYERS 10   // 최대 플레이어 수(여유 공간)

// C언어 최적화를 위한 인라인 매크로
static inline int max_int(int a, int b) { return a > b ? a : b; }
static inline int min_int(int a, int b) { return a < b ? a : b; }
static inline void swap_int(int* a, int* b) { int t = *a; *a = *b; *b = t; }

// [0] 1차원 배열 기반(Array-based) Set 트리(C++ std::set 완벽 대체)
typedef struct {
    int tree[MAXT];
    int size;
    int count;
} ArraySet;

void ArraySet_init(ArraySet* self, int max_value) {
    self->size = 1;
    while (self->size <= max_value + 5) self->size <<= 1;
    memset(self->tree, 0, sizeof(int) * 2 * self->size);
    self->count = 0;
}

void ArraySet_insert(ArraySet* self, int k) {
    int index = k + self->size;
    if (self->tree[index] == 0) {
        self->tree[index] = 1;
        self->count++;
        index >>= 1;
        while (index > 0) {
            self->tree[index] = self->tree[index << 1] + self->tree[(index << 1) | 1];
            index >>= 1;
        }
    }
}

void ArraySet_erase(ArraySet* self, int k) {
    int index = k + self->size;
    if (self->tree[index] == 1) {
        self->tree[index] = 0;
        self->count--;
        index >>= 1;
        while (index > 0) {
            self->tree[index] = self->tree[index << 1] + self->tree[(index << 1) | 1];
            index >>= 1;
        }
    }
}

bool ArraySet_contains(ArraySet* self, int k) {
    return self->tree[k + self->size] > 0;
}

int ArraySet_upper_bound(ArraySet* self, int k) {
    int index = k + self->size;
    while (true) {
        if (index == 1) return -1;
        if ((index & 1) == 0 && self->tree[index ^ 1] > 0) {
            index ^= 1;
            break;
        }
        index >>= 1;
    }
    while (index < self->size) {
        index <<= 1;
        if (self->tree[index] == 0) index |= 1;
    }
    return index - self->size;
}

int ArraySet_get_max(ArraySet* self) {
    if (self->tree[1] == 0) return -1;
    int index = 1;
    while (index < self->size) {
        index <<= 1;
        if (self->tree[index | 1] > 0) index |= 1;
    }
    return index - self->size;
}

int ArraySet_get_count(ArraySet* self) {
    return self->tree[1];
}

ArraySet target_set;
ArraySet order_set;

// [1] 1D Max Fenwick Tree (BIT)
int fenwick_1d[MAXN];

void fenwick_1d_build(int n) {
    for (int i = 0; i < MAXN; i++) {
        fenwick_1d[i] = -INF;
    }
}

void fenwick_1d_update(int x, int v) {
    for (int i = x; i < MAXN; i += i & -i) {
        if (v > fenwick_1d[i]) fenwick_1d[i] = v;
    }
}

int fenwick_1d_query(int x) {
    int return_value = -INF;
    for (int i = x; i > 0; i -= i & -i) {
        if (fenwick_1d[i] > return_value) return_value = fenwick_1d[i];
    }
    return return_value;
}

// [2] 1D Pair Max Segment Tree(std::pair 멸망 -> 병렬 배열 사용)
int segment_pair_first[MAXT];
int segment_pair_second[MAXT];
int segment_pair_limit = 1;

void segment_pair_build(int n) {
    segment_pair_limit = 1;
    while (segment_pair_limit <= n) segment_pair_limit <<= 1;
    for (int i = 0; i < 2 * segment_pair_limit; i++) {
        segment_pair_first[i] = -INF;
        segment_pair_second[i] = -INF;
    }
}

void segment_pair_update(int x, int first_value, int second_value) {
    x += segment_pair_limit;
    segment_pair_first[x] = first_value;
    segment_pair_second[x] = second_value;
    while (x > 1) {
        x >>= 1;
        int left = x << 1;
        int right = (x << 1) | 1;
        if (segment_pair_first[left] > segment_pair_first[right] || 
           (segment_pair_first[left] == segment_pair_first[right] && segment_pair_second[left] > segment_pair_second[right])) {
            segment_pair_first[x] = segment_pair_first[left];
            segment_pair_second[x] = segment_pair_second[left];
        } else {
            segment_pair_first[x] = segment_pair_first[right];
            segment_pair_second[x] = segment_pair_second[right];
        }
    }
}

// 포인터 참조를 사용하여 C언어에서 튜플 반환을 대체
void segment_pair_query(int s, int e, int* out_first, int* out_second) {
    s += segment_pair_limit;
    e += segment_pair_limit;
    *out_first = -INF;
    *out_second = -INF;

    while (s < e) {
        if (s % 2 == 1) {
            if (segment_pair_first[s] > *out_first || 
               (segment_pair_first[s] == *out_first && segment_pair_second[s] > *out_second)) {
                *out_first = segment_pair_first[s];
                *out_second = segment_pair_second[s];
            }
            s++;
        }
        if (e % 2 == 0) {
            if (segment_pair_first[e] > *out_first || 
               (segment_pair_first[e] == *out_first && segment_pair_second[e] > *out_second)) {
                *out_first = segment_pair_first[e];
                *out_second = segment_pair_second[e];
            }
            e--;
        }
        s >>= 1;
        e >>= 1;
    }
    if (s == e) {
        if (segment_pair_first[s] > *out_first || 
           (segment_pair_first[s] == *out_first && segment_pair_second[s] > *out_second)) {
            *out_first = segment_pair_first[s];
            *out_second = segment_pair_second[s];
        }
    }
}

// [3] C언어 최적화 이진 탐색(lower_bound, upper_bound 직접 구현)
int custom_lower_bound(int* array, int start, int end, int target) {
    int length = end - start;
    int first = start;
    while (length > 0) {
        int half = length >> 1;
        int middle = first + half;
        if (array[middle] < target) {
            first = middle + 1;
            length = length - half - 1;
        } else {
            length = half;
        }
    }
    return first - start;
}

int custom_upper_bound(int* array, int start, int end, int target) {
    int length = end - start;
    int first = start;
    while (length > 0) {
        int half = length >> 1;
        int middle = first + half;
        if (target < array[middle]) {
            length = half;
        } else {
            first = middle + 1;
            length = length - half - 1;
        }
    }
    return first - start;
}

// [4] 2D Fenwick inside Segment Tree(1D Array Flattening 적용)
int segment2d_X[2][MAXN];
int segment2d_Y_input[2][MAXN];

int segment2d_Y[2][MAX_MEM];
int segment2d_value[2][MAX_MEM];
int segment2d_head[2][MAXT];
int segment2d_length[2][MAXT];
int segment2d_limit[2];

int sorted_index[MAXN];
int current_index[MAXT];

// qsort를 위한 비교 함수(전역 변수로 tree_id 통제)
int current_tree_id_for_sort = 0;
int compare_y_input(const void* a, const void* b) {
    int ia = *(const int*)a;
    int ib = *(const int*)b;
    return segment2d_Y_input[current_tree_id_for_sort][ia] - segment2d_Y_input[current_tree_id_for_sort][ib];
}

void segment2d_build(int tree_id, int n) {
    int limit = 1;
    while (limit <= n) limit <<= 1;
    segment2d_limit[tree_id] = limit;

    memset(segment2d_length[tree_id], 0, sizeof(int) * 2 * limit);
    for (int i = 0; i < n; i++) {
        int x = segment2d_X[tree_id][i];
        for (int j = x + limit; j > 0; j >>= 1) {
            segment2d_length[tree_id][j]++;
        }
    }

    segment2d_head[tree_id][0] = 0;
    int offset = 0;
    for (int i = 1; i < 2 * limit; i++) {
        segment2d_head[tree_id][i] = offset;
        offset += segment2d_length[tree_id][i] + 1; 
    }

    for (int i = 0; i < n; i++) sorted_index[i] = i;
    current_tree_id_for_sort = tree_id;
    qsort(sorted_index, n, sizeof(int), compare_y_input);

    for (int i = 0; i < 2 * limit; i++) current_index[i] = 1;
    
    for (int i = 0; i < n; i++) {
        int index = sorted_index[i];
        int x = segment2d_X[tree_id][index];
        int y = segment2d_Y_input[tree_id][index];
        for (int j = x + limit; j > 0; j >>= 1) {
            int p_index = segment2d_head[tree_id][j] + current_index[j]++;
            segment2d_Y[tree_id][p_index] = y;
            segment2d_value[tree_id][p_index] = 0;
        }
    }
}

void segment2d_add(int tree_id, int x, int y, int value) {
    int index = x + segment2d_limit[tree_id];
    while (index > 0) {
        int head = segment2d_head[tree_id][index];
        int length = segment2d_length[tree_id][index];
        
        // 펜윅 트리를 위한 1-based 인덱스를 맞추기 위해 +1을 더합니다.(무한 루프 방지)
        int position = custom_lower_bound(segment2d_Y[tree_id], head + 1, head + length + 1, y) + 1;
                  
        while (position <= length) {
            if (value > segment2d_value[tree_id][head + position]) {
                segment2d_value[tree_id][head + position] = value;
            }
            position += position & -position;
        }
        index >>= 1;
    }
}

int qnode(int tree_id, int node, int target_y) {
    int head = segment2d_head[tree_id][node];
    int length = segment2d_length[tree_id][node];
    
    int position = custom_upper_bound(segment2d_Y[tree_id], head + 1, head + length + 1, target_y);
              
    int return_value = 0;
    while (position > 0) {
        if (segment2d_value[tree_id][head + position] > return_value) {
            return_value = segment2d_value[tree_id][head + position];
        }
        position -= position & -position;
    }
    return return_value;
}

int segment2d_query(int tree_id, int s, int e, int max_y) {
    int limit = segment2d_limit[tree_id];
    s += limit;
    e += limit;
    int max_result = 0;

    while (s < e) {
        if (s % 2 == 1) max_result = max_int(max_result, qnode(tree_id, s++, max_y));
        if (e % 2 == 0) max_result = max_int(max_result, qnode(tree_id, e--, max_y));
        s >>= 1;
        e >>= 1;
    }
    if (s == e) max_result = max_int(max_result, qnode(tree_id, s, max_y));
    return max_result;
}

// [5] 메인 로직(전역 배열 컨트롤)
int buildings_L[MAXN];
int DP[MAXN];

int dp_head[MAXN + 2];
int dp_count[MAXN + 1];
int dp_flat[MAXN];
int dp_current[MAXN + 1];

int order_array[MAXN];
int reverse_array[MAXN + 1];

int result_array[MAXN][MAX_PLAYERS];
int result_count = 0;

int N_global = 0;

// C언어 qsort를 위한 DP 배열 정렬 로직
int compare_dp(const void* ptr_a, const void* ptr_b) {
    int original_x = *(const int*)ptr_a;
    int original_y = *(const int*)ptr_b;
    if (original_x == original_y) return 0;

    int x = original_x;
    int y = original_y;
    bool status = false;
    if (x > y) {
        swap_int(&x, &y);
        status = true;
    }

    int x_only = segment2d_query(0, x + 1, y, buildings_L[x] - 1);
    int y_only = segment2d_query(1, buildings_L[x], buildings_L[y] - 1, N_global - y);

    if (x_only < y_only) status ^= 1;

    // status가 true면 x가 우선순위(앞쪽)로 가야 하므로 qsort 규약에 따라 -1 반환
    return status ? -1 : 1;
}

void erase_node(int x, int N) {
    int next_node = ArraySet_upper_bound(&target_set, x);
    int y = (next_node == -1) ? N : next_node;

    ArraySet_erase(&target_set, x);
    ArraySet_erase(&order_set, order_array[x]);
    segment_pair_update(x, -INF, x);

    while (y > 0) {
        int value_first, value_second;
        segment_pair_query(0, y - 1, &value_first, &value_second);
        if (ArraySet_contains(&target_set, value_second)) break;
        if (value_first < 0) break;

        ArraySet_insert(&target_set, value_second);
        ArraySet_insert(&order_set, order_array[value_second]);
        y = value_second;
    }
}

void min_shooting_buildings(int N, int players) {
    if (N > 130000) return;
    N_global = N;

    fenwick_1d_build(N);
    memset(dp_count, 0, sizeof(int) * (N + 1));

    for (int i = N - 1; i >= 0; i--) {
        int dp_value = max_int(0, fenwick_1d_query(buildings_L[i] - 1) + 1);
        DP[i] = dp_value;
        fenwick_1d_update(buildings_L[i], dp_value);
        dp_count[dp_value]++;
    }

    dp_head[0] = 0;
    for (int i = 1; i <= N + 1; i++) {
        dp_head[i] = dp_head[i - 1] + dp_count[i - 1];
    }
    
    memset(dp_current, 0, sizeof(int) * (N + 1));
    for (int i = N - 1; i >= 0; i--) {
        int value = DP[i];
        dp_flat[dp_head[value] + dp_current[value]++] = i;
    }

    for (int i = 0; i < N; i++) {
        segment2d_X[0][i] = i + 1;
        segment2d_Y_input[0][i] = buildings_L[i];
        
        segment2d_X[1][i] = buildings_L[i];
        segment2d_Y_input[1][i] = N + 1 - i;
    }

    segment2d_build(0, N);
    segment2d_build(1, N);

    reverse_array[0] = -1;
    int current_determined = 0;
    int reverse_index = 1;

    for (int value = 0; value <= N; value++) {
        if (dp_count[value] == 0) continue;

        int start_index = dp_head[value];
        int end_index = dp_head[value] + dp_count[value];

        // qsort C 표준 정렬을 통해 람다(Lambda) 객체 오버헤드 0% 달성
        qsort(dp_flat + start_index, end_index - start_index, sizeof(int), compare_dp);

        for (int i = start_index; i < end_index; i++) {
            reverse_array[reverse_index++] = dp_flat[i];
        }
        for (int i = start_index; i < end_index; i++) {
            int index = dp_flat[i];
            current_determined++;
            order_array[index] = current_determined;
            segment2d_add(0, index + 1, buildings_L[index], order_array[index]);
            segment2d_add(1, buildings_L[index], N + 1 - index, order_array[index]);
        }
    }

    ArraySet_init(&target_set, N);
    ArraySet_init(&order_set, N);
    segment_pair_build(N);

    int current_max = 0;
    for (int j = 0; j < N; j++) {
        segment_pair_update(j, buildings_L[j], j);
        if (current_max < buildings_L[j]) {
            ArraySet_insert(&target_set, j);
            ArraySet_insert(&order_set, order_array[j]);
            current_max = buildings_L[j];
        }
    }

    int turn_count = 0;
    while (turn_count < N) {
        int available_targets = ArraySet_get_count(&target_set);
        int shooters_used = min_int(available_targets, players);

        int extracted_priorities[MAX_PLAYERS];
        for (int i = 0; i < shooters_used; i++) {
            int m = ArraySet_get_max(&order_set);
            extracted_priorities[i] = m;
            ArraySet_erase(&order_set, m);
        }

        // 역순(마지막 타겟 제외) 복구를 통해 erase_node 위임
        for (int i = 0; i < shooters_used - 1; i++) {
            ArraySet_insert(&order_set, extracted_priorities[i]);
        }

        turn_count += shooters_used;

        int turn_heights[MAX_PLAYERS];
        int h_index = 0;
        
        for (int i = 0; i < shooters_used; i++) {
            int m = extracted_priorities[i];
            int nd = reverse_array[m];
            erase_node(nd, N);
            turn_heights[h_index++] = buildings_L[nd];
        }

        while (h_index < players) {
            turn_heights[h_index++] = N + 1;
        }

        for (int i = 0; i < players; i++) {
            result_array[result_count][i] = turn_heights[i];
        }
        result_count++;
    }
}

// 출력을 위한 단순 오름차순 비교 함수
int compare_asc(const void* a, const void* b) {
    return (*(const int*)a - *(const int*)b);
}

// [6] 입출력 로직(printf/scanf 최적화)
int main() {
    int buildings_count;
    if (scanf("%d", &buildings_count) != 1) return 0;

    for (int i = 0; i < buildings_count; i++) {
        scanf("%d", &buildings_L[i]);
    }

    // 플레이어 수 동적 할당 지원
    int PLAYERS = 2;
    min_shooting_buildings(buildings_count, PLAYERS);

    printf("%d\n", result_count);

    for (int i = 0; i < result_count; i++) {
        // C표준 라이브러리 오름차순 qsort로 깔끔하게 정렬!
        qsort(result_array[i], PLAYERS, sizeof(int), compare_asc);
        for (int j = 0; j < PLAYERS; j++) {
            printf("%d", result_array[i][j]);
            if (j + 1 < PLAYERS) printf(" ");
        }
        printf("\n");
    }

    return 0;
}


/*
[7] 실전에 써먹을 수 있는 가능성

여기서 만약 단순한 사격 게임이 아닌 실전성 있는 형태로 바꿀려면 어떻게 해야 할까요?
예시로 높이가
4.5 3.6 2.4 1.2 1.2
이렇게 되어 있으면 어떻게 해결해야 할까요?

이런 경우 1-based index로 좌표 압축을 합니다.
4 3 2 1 1
그런데 문제점은 이 소스 코드는 모든 좌표가 다 다른 경우인데 1이 2개라서 성립할 수 없거든요.
그래서 저는 ε(0+)을 대입해서 반강제로 모두 다 다른 좌표로 만듭니다.
4.5 3.6 2.4 1.2 - ε, 1.2 - 2ε
이렇게 말이죠.
그러면
5 4 3 2 1
이렇게 바뀌게 되고 자연스럽게
5 6
4 6
3 6
2 6
1 6
이런 결과를 얻게 됩니다.

그 뒤 N + 1 -> -1로 변환한 뒤 후처리 해주면
4.5 -1
3.6 -1
2.4 -1
1.2 -1
1.2 -1
이렇게 바뀝니다.

이 때 플레이어가 2명, A와 B가 있다고 가정할게요. 
처음에는 A가 1발 쏩니다. 그런데 -1이라서 B는 허공에 안 쏘고 그냥 쉽니다.
이렇게 해서 count = [1, 0]가 되겠죠.
2번째 턴은 A가 안 쏘고 B가 1발 쏩니다. 이 때 A는 허공에 안 쏘고 그냥 쉽니다.
이렇게 해서 count = [1, 1]가 되겠죠.

그 뒤 count에서 가장 적게 쏜 플레이어가 우선권을 가지게 되고,
만약 쐈던 총알 수가 같으면 플레이어 번호가 작은 플레이어가 우선권을 가지는 형식으로 하면
총알을 (플레이어 수) * N발 -> N발로 최적화되면서 모든 플레이어가 평균 N / (플레이어 수)발로 골고루 격발할 수 있습니다.


여기서 플레이어 대신 레이저 빔이라고 생각하면 훨씬 효율적인 설계가 가능합니다.
반도체 웨이퍼 제작 혹은 3D 프린트 등에서 훨씬 더 적은 전력이 들어서 경제적인 효과를 얻을 수 있을 것으로 예상합니다.
*/