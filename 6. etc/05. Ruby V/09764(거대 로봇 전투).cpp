// 링크 : https://jungol.co.kr/problem/9764
#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <cstring>

using namespace std;

// 에디토리얼 : https://static.ucpc.me/files/2023/ucpc23-finals-solutions.pdf
// 학원 도시 소녀들의 우정과 사랑, 감동의 밀리터리 액션! 블루 아카이브!

const long long VIRTUAL_MINION_HEIGHT = 2000000000LL;
const long long INF = 2LL * VIRTUAL_MINION_HEIGHT;
const int LOG = 19;
const int MAXN = 250005;

struct Node {
    long long hmi;
    long long hmx;
    int force;
};

int N, Q;
long long H[MAXN];
int parent_node[MAXN];
int up_table[MAXN][LOG];
int depth_node[MAXN];

int segment_size;
vector<Node> SegmentTree;

vector<pair<int, int>> update_queue[MAXN];

int parent_dsu[MAXN];
int left_most[MAXN];
int right_most[MAXN];
bool active_dsu[MAXN];
int precalc_L[MAXN];
int precalc_R[MAXN];

int segment_ends[MAXN];
int result[MAXN];

inline int get_ancestor(int node, int k) {
    for (int j = 0; j < LOG; ++j) {
        if ((k >> j) & 1) {
            node = up_table[node][j];
        }
    }
    return node;
}

inline Node calculate_leaf(int start_index, int end_index, int current_k_value) {
    if (start_index == end_index) {
        if (depth_node[start_index] < current_k_value) {
            return {0, 0, 0};
        } else if (depth_node[start_index] == current_k_value) {
            return {0, 0, 1};
        } else {
            return {INF, 0, 1};
        }
    }

    int distance = depth_node[start_index] - depth_node[end_index];
    int s_mx = get_ancestor(start_index, distance - 1);

    if (depth_node[start_index] <= current_k_value) {
        return {0, H[s_mx], 0};
    } else {
        if (depth_node[s_mx] > current_k_value) {
            return {INF, 0, 1};
        } else {
            int jump = depth_node[start_index] - current_k_value;
            int s_mi = get_ancestor(start_index, jump);
            return {H[s_mi], H[s_mx], 0};
        }
    }
}

inline void schedule_segment(int start_index, int end_index, int current_k) {
    int next_k = 0;
    if (start_index == end_index) {
        if (current_k > depth_node[start_index]) {
            return;
        } else if (current_k == depth_node[start_index]) {
            next_k = current_k + 1;
        } else {
            next_k = depth_node[start_index];
        }
    } else {
        if (current_k >= depth_node[start_index]) {
            return;
        }
        int distance = depth_node[start_index] - depth_node[end_index];
        int s_mx = get_ancestor(start_index, distance - 1);
        if (current_k < depth_node[s_mx]) {
            next_k = depth_node[s_mx];
        } else {
            next_k = current_k + 1;
        }
    }

    if (next_k <= N + 1) {
        update_queue[next_k].push_back({start_index, end_index});
    }
}

inline Node merge_nodes(const Node& left_node, const Node& right_node) {
    long long l_hmi = left_node.hmi;
    long long l_hmx = left_node.hmx;
    int l_force = left_node.force;

    long long r_hmi = right_node.hmi;
    long long r_hmx = right_node.hmx;
    int r_force = right_node.force;

    long long new_hmi = 0;
    long long new_hmx = 0;
    int new_force = 0;

    long long required_hmi = (l_hmx < r_hmi) ? r_hmi : 0;

    if (l_force == 0 && r_force == 0) {
        new_hmi = (l_hmi > required_hmi) ? l_hmi : required_hmi;
        new_hmx = (l_hmx > r_hmx) ? l_hmx : r_hmx;
        new_force = 0;
    } else if (l_force == 0 && r_force == 1) {
        new_hmi = (l_hmi > required_hmi) ? l_hmi : required_hmi;
        new_hmx = r_hmx;
        new_force = 1;
    } else if (l_force == 1 && r_force == 0) {
        new_hmi = (l_hmx < r_hmi) ? INF : l_hmi;
        new_hmx = (l_hmx > r_hmx) ? l_hmx : r_hmx;
        new_force = 1;
    } else {
        new_hmi = (l_hmx < r_hmi) ? INF : l_hmi;
        new_hmx = r_hmx;
        new_force = 1;
    }

    return {new_hmi, new_hmx, new_force};
}

inline void update(int index, const Node& value) {
    index += segment_size;
    SegmentTree[index] = value;
    while (index > 1) {
        index >>= 1;
        SegmentTree[index] = merge_nodes(SegmentTree[index << 1], SegmentTree[index << 1 | 1]);
    }
}

int find_dsu(int x) {
    int root = x;
    while (parent_dsu[root] != root) {
        root = parent_dsu[root];
    }
    int current = x;
    while (current != root) {
        int next_node = parent_dsu[current];
        parent_dsu[current] = root;
        current = next_node;
    }
    return root;
}

void union_dsu(int x, int y) {
    int rootX = find_dsu(x);
    int rootY = find_dsu(y);
    if (rootX != rootY) {
        parent_dsu[rootY] = rootX;
        if (left_most[rootY] < left_most[rootX]) left_most[rootX] = left_most[rootY];
        if (right_most[rootY] > right_most[rootX]) right_most[rootX] = right_most[rootY];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> Q;

    for (int i = 0; i < N; i++) {
        cin >> H[i];
    }
    H[N] = VIRTUAL_MINION_HEIGHT;

    vector<pair<long long, int>> sorted_queries(Q);
    for (int i = 0; i < Q; i++) {
        cin >> sorted_queries[i].first;
        sorted_queries[i].second = i;
    }

    for (int i = 0; i <= N; i++) {
        parent_node[i] = N;
    }

    vector<int> stack_list;
    stack_list.reserve(N + 1);
    for (int i = 0; i <= N; i++) {
        while (!stack_list.empty() && H[stack_list.back()] < H[i]) {
            parent_node[stack_list.back()] = i;
            stack_list.pop_back();
        }
        stack_list.push_back(i);
    }

    for (int j = 0; j < LOG; j++) {
        up_table[N][j] = N;
    }
    depth_node[N] = 0;

    for (int i = N - 1; i >= 0; i--) {
        up_table[i][0] = parent_node[i];
        depth_node[i] = depth_node[parent_node[i]] + 1;
        for (int j = 1; j < LOG; ++j) {
            up_table[i][j] = up_table[up_table[i][j - 1]][j - 1];
        }
    }

    int bits = 0;
    while ((1 << bits) < (N + 1)) {
        bits++;
    }
    segment_size = 1 << bits;
    SegmentTree.assign(2 * segment_size, {0, 0, 0});

    int current_k_value = 1;

    memset(segment_ends, -1, sizeof(segment_ends));
    segment_ends[0] = N;

    update(0, calculate_leaf(0, N, current_k_value));
    schedule_segment(0, N, current_k_value);

    for (int i = segment_size - 1; i > 0; i--) {
        SegmentTree[i] = merge_nodes(SegmentTree[i << 1], SegmentTree[i << 1 | 1]);
    }

    sort(sorted_queries.begin(), sorted_queries.end(), greater<pair<long long, int>>());

    vector<pair<long long, int>> minions_desc(N);
    vector<pair<long long, int>> minions_asc(N);
    for (int i = 0; i < N; i++) {
        minions_desc[i] = {H[i], i};
        minions_asc[i] = {H[i], i};
    }

    sort(minions_desc.begin(), minions_desc.end(), greater<pair<long long, int>>());
    sort(minions_asc.begin(), minions_asc.end(), [](const pair<long long, int>& a, const pair<long long, int>& b) {
        if (a.first != b.first) return a.first < b.first;
        return a.second > b.second;
    });

    for (int i = 0; i < N; i++) {
        parent_dsu[i] = i;
        left_most[i] = i;
        right_most[i] = i;
        active_dsu[i] = false;
    }

    for (int i = 0; i < N; i++) {
        int index = minions_asc[i].second;
        if (index > 0 && active_dsu[index - 1]) {
            precalc_L[index] = left_most[find_dsu(index - 1)] - 1;
        } else {
            precalc_L[index] = index - 1;
        }

        if (index < N - 1 && active_dsu[index + 1]) {
            precalc_R[index] = right_most[find_dsu(index + 1)] + 1;
        } else {
            precalc_R[index] = index + 1;
        }

        active_dsu[index] = true;
        if (index > 0 && active_dsu[index - 1]) {
            union_dsu(index, index - 1);
        }
        if (index < N - 1 && active_dsu[index + 1]) {
            union_dsu(index, index + 1);
        }
    }

    int minion_pointer = 0;

    for (int q_index = 0; q_index < Q; q_index++) {
        long long robot_height = sorted_queries[q_index].first;
        int index = sorted_queries[q_index].second;

        while (minion_pointer < N && minions_desc[minion_pointer].first >= robot_height) {
            int minion_index = minions_desc[minion_pointer].second;
            minion_pointer++;

            int left_start = precalc_L[minion_index] + 1;
            int right_end = precalc_R[minion_index];

            if (left_start <= minion_index) {
                segment_ends[left_start] = minion_index;
                update(left_start, calculate_leaf(left_start, minion_index, current_k_value));
                schedule_segment(left_start, minion_index, current_k_value);
            }

            if (minion_index + 1 <= right_end) {
                segment_ends[minion_index + 1] = right_end;
                update(minion_index + 1, calculate_leaf(minion_index + 1, right_end, current_k_value));
                schedule_segment(minion_index + 1, right_end, current_k_value);
            }
        }

        while (SegmentTree[1].hmi > 0) {
            current_k_value++;

            if (current_k_value <= N + 1) {
                for (const auto& seg : update_queue[current_k_value]) {
                    int segment_start = seg.first;
                    int segment_end = seg.second;

                    if (segment_ends[segment_start] != segment_end) {
                        continue;
                    }

                    update(segment_start, calculate_leaf(segment_start, segment_end, current_k_value));
                    schedule_segment(segment_start, segment_end, current_k_value);
                }
                vector<pair<int, int>>().swap(update_queue[current_k_value]);
            }
        }

        result[index] = current_k_value;
    }

    for (int i = 0; i < Q; i++) {
        cout << result[i] << '\n';
    }

    return 0;
}