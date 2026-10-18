# 링크 : https://jungol.co.kr/problem/13754
import sys

# 입출력이 너무 많아서 어쩔 수 없이 read, write로 했습니다.
read = sys.stdin.read
write = sys.stdout.write

# 도미네이터 트리 자료구조는 훗날 쓸 일이 있어서 참고 자료로서 남깁니다.

# =========================================================================================
# [학습 가이드 및 복습용 핵심 노트]
# 1. 도미네이터 트리 (Dominator Tree) 기본 개념:
#    - 위키백과: https://en.wikipedia.org/wiki/Dominator_(graph_theory)
#    - 방향 그래프에서 루트(1번)로부터 특정 노드 v로 가는 모든 경로가 "반드시 거쳐야만 하는" 
#      정점(지배자, Dominator)들의 포함 관계를 트리 형태로 압축한 구조입니다.
#    - 핵심 성질: 모든 정점 v에 대해 DFN[idom[v]] < DFN[v]가 성립합니다. (지배자는 항상 DFS 조상)
#
# 2. 렌가우어-타잔(Lengauer-Tarjan) 알고리즘:
#    - 원 논문: "A fast algorithm for finding dominators in a flowgraph" (1979)
#    - 이론적 복잡도: 단순 경로 압축(Path Compression) 적용 시 O((V+E) log V)에 동작하며 상수가 매우 작음.
#    - 복습 추천 자료 1 (Tanuj Khattar 튜토리얼): https://tanujkhattar.wordpress.com/2016/01/11/dominator-tree-of-a-directed-graph/
#    - 복습 추천 자료 2 (USACO Guide Advanced): https://usaco.guide/adv/critical
#    - 복습 포인트: 준지배자(Semi-dominator)의 정의와 Disjoint Set 경로 압축(find_best_candidate) 과정 이해하기.
#
# 3. Heavy-Light Decomposition (HLD)를 이용한 최저 공통 조상 (LCA):
#    - 여러 노드 w_1, ..., w_k의 '공통 지배자(Common Dominator)'는 
#      도미네이터 트리 상에서 이들의 공통 조상들과 같으며, 그중 가장 깊은 노드가 바로 LCA(w_1, ..., w_k)입니다.
# =========================================================================================

class DominatorTree:
    def __init__(self, node_count:int, inspection_cost:list):
        self.node_count:int = node_count
        self.inspection_cost:list = inspection_cost

        # 원본 방향 그래프와 역방향 그래프 (준지배자 계산 시 역방향 진입 간선 탐색이 필수적임)
        self.forward_graph:list = [[] for _ in range(node_count + 1)]
        self.backward_graph:list = [[] for _ in range(node_count + 1)]

        # --- Lengauer-Tarjan 알고리즘을 위한 변수들 ---
        # discovery_order: DFS 방문 번호(DFN). DFN[idom[v]] < DFN[v] 성질 덕분에 도미네이터 트리의 위상 정렬 순서를 겸함.
        self.discovery_order:list = [0] * (node_count + 1)
        self.node_at_order:list = [0] * (node_count + 1)
        self.tree_parent:list = [0] * (node_count + 1)
        self.total_visited:int = 0

        # semi_dominator (sdom): 정점 u에서 v로 가는 우회 경로(내부 경유지들의 DFN이 모두 DFN[v]보다 큰 경로) 중,
        # 시작점 u의 DFN이 가장 작은(가장 상단에 있는) DFS 조상 노드. 초기값은 자기 자신.
        self.semi_dominator:list = list(range(node_count + 1))
        # immediate_dominator (idom): 도미네이터 트리에서 v의 직속 부모(유일한 직속 지배자).
        self.immediate_dominator:list = [0] * (node_count + 1)
        
        # 가중치/경로 압축 Disjoint Set (논문의 EVAL 및 LINK 연산 수행)
        # best_candidate[v]: 현재까지 압축된 Disjoint Set 트리 경로 상에서 sdom의 DFN이 가장 작은 정점 기록
        self.best_candidate:list = list(range(node_count + 1))
        self.disjoint_set_parent:list = list(range(node_count + 1))

        # --- HLD 및 LCA, 최소 비용 쿼리를 위한 변수들 ---
        self.tree_depth:list = [0] * (node_count + 1)
        self.subtree_size:list = [0] * (node_count + 1)
        self.heavy_child:list = [0] * (node_count + 1)
        self.chain_head:list = [0] * (node_count + 1)
        # 루트(1번)부터 해당 노드까지 도미네이터 트리 경로 상에 존재하는 정점들의 '최소 조사 비용' 누적 배열
        self.minimum_ancestor_cost:list = [0] * (node_count + 1)

    def add_edge(self, source_node:int, target_node:int) -> None:
        self.forward_graph[source_node].append(target_node)
        self.backward_graph[target_node].append(source_node)

    # 1단계 : 비재귀 DFS를 통한 탐색 번호(DFN) 및 DFS 스패닝 트리 구축
    # 파이썬의 재귀 깊이 제한(RecursionError)과 함수 호출 오버헤드를 피하기 위해 명시적 스택 사용
    def build_depth_first_tree(self, root_node:int) -> None:
        traversal_stack:list = [(root_node, 0)]
        discovery_order:list = self.discovery_order
        node_at_order:list = self.node_at_order
        tree_parent:list = self.tree_parent
        forward_graph:list = self.forward_graph
        current_order:int = 0

        while traversal_stack:
            current_node, parent_node = traversal_stack.pop()
            if discovery_order[current_node] != 0:
                continue

            current_order += 1
            discovery_order[current_node] = current_order
            node_at_order[current_order] = current_node
            tree_parent[current_node] = parent_node

            for next_node in forward_graph[current_node]:
                if discovery_order[next_node] == 0:
                    traversal_stack.append((next_node, current_node))

        self.total_visited = current_order

    # Disjoint Set의 경로 압축(Path Compression) + 구간 최솟값 갱신 (논문의 EVAL 함수)
    # target_node에서 현재 Disjoint Set의 루트까지 올라가는 경로 중 sdom의 DFN이 최소인 정점을 반환함
    def find_best_candidate(self, target_node:int) -> int:
        disjoint_set_parent:list = self.disjoint_set_parent
        best_candidate:list = self.best_candidate
        semi_dominator:list = self.semi_dominator
        discovery_order:list = self.discovery_order

        path_nodes:list = []
        current_node:int = target_node
        while disjoint_set_parent[current_node] != current_node:
            path_nodes.append(current_node)
            current_node = disjoint_set_parent[current_node]

        root_node:int = current_node
        # 루트 바로 아래부터 역순으로 내려오며 조상의 최적 후보(best_candidate)를 자식에게 전파 및 경로 압축
        for index in range(len(path_nodes) - 2, -1, -1):
            child_node:int = path_nodes[index]
            parent_node:int = disjoint_set_parent[child_node]
            if discovery_order[semi_dominator[best_candidate[parent_node]]] < discovery_order[semi_dominator[best_candidate[child_node]]]:
                best_candidate[child_node] = best_candidate[parent_node]
            disjoint_set_parent[child_node] = root_node

        return best_candidate[target_node]

    # 2단계 : Lengauer-Tarjan 핵심 로직 (sdom 계산 -> 상대적 idom 후보 지정 -> 최종 idom 확정)
    def compute_dominators(self, root_node:int) -> None:
        self.build_depth_first_tree(root_node)

        discovery_order:list = self.discovery_order
        node_at_order:list = self.node_at_order
        tree_parent:list = self.tree_parent
        semi_dominator:list = self.semi_dominator
        immediate_dominator:list = self.immediate_dominator
        disjoint_set_parent:list = self.disjoint_set_parent
        backward_graph:list = self.backward_graph

        bucket:list = [[] for _ in range(self.node_count + 1)]

        # DFN 역순(Bottom-up)으로 탐색: 현재 노드보다 DFN이 큰 노드들은 이미 Disjoint Set에 병합된 상태임이 보장됨
        for order_index in range(self.total_visited, 1, -1):
            current_node:int = node_at_order[order_index]

            # 2-1. 모든 역방향 진입 간선 (predecessor_node -> current_node)을 검사하여 sdom 갱신
            # - predecessor의 DFN이 더 작으면: 트리 조상/전방향 간선이므로 predecessor 자체가 후보
            # - predecessor의 DFN이 더 크면: 이미 처리된 서브트리/교차 간선이므로 Disjoint Set 경로 상 최소 sdom이 후보
            # (아직 처리되지 않은 노드는 자기 자신이 루트이므로 find_best_candidate가 두 경우를 단일 호출로 통합 처리함)
            for predecessor_node in backward_graph[current_node]:
                if discovery_order[predecessor_node] == 0:
                    continue
                candidate_node:int = self.find_best_candidate(predecessor_node)
                if discovery_order[semi_dominator[candidate_node]] < discovery_order[semi_dominator[current_node]]:
                    semi_dominator[current_node] = semi_dominator[candidate_node]

            # 계산된 sdom의 버킷에 현재 노드를 등록하고, 현재 노드를 DFS 부모와 LINK(병합)
            bucket[semi_dominator[current_node]].append(current_node)
            parent_node:int = tree_parent[current_node]
            disjoint_set_parent[current_node] = parent_node

            # 2-2. Lengauer-Tarjan 정리에 따른 idom(직속 지배자) 1차 판정
            # bucket_node(w)의 준지배자가 parent_node(sdom[w])와 같아진 시점에,
            # sdom[w]에서 w로 가는 트리 경로 상에서 sdom이 최소인 정점 best_node(u)를 조회함
            for bucket_node in bucket[parent_node]:
                best_node:int = self.find_best_candidate(bucket_node)
                # 따름정리 1: sdom[u] == sdom[w] 이면, idom[w] = sdom[w] (즉, parent_node)
                if semi_dominator[best_node] == semi_dominator[bucket_node]:
                    immediate_dominator[bucket_node] = parent_node
                # 따름정리 2: sdom[u] < sdom[w] 이면, idom[w] = idom[u] (일단 u를 저장해 두고 2-3에서 최종 갱신)
                else:
                    immediate_dominator[bucket_node] = best_node
            bucket[parent_node].clear()

        # 2-3. 최종 Immediate Dominator 확정 (DFN 정방향 Top-down 순회)
        # 따름정리 2에 해당했던 노드들에 대해 idom[w] = idom[u]를 순차적으로 대입하여 완성
        for order_index in range(2, self.total_visited + 1):
            current_node = node_at_order[order_index]
            if immediate_dominator[current_node] != semi_dominator[current_node]:
                immediate_dominator[current_node] = immediate_dominator[immediate_dominator[current_node]]

    # 3단계 : O(N) Heavy-Light Decomposition (HLD) 및 경로 최소 비용 DP 전처리
    # DFN[idom[v]] < DFN[v]가 항상 성립하므로, node_at_order 배열 자체가 도미네이터 트리의 완벽한 위상 정렬 순서임.
    # 따라서 별도의 트리 인접 리스트 생성이나 추가 DFS 없이 1차원 배열 정/역방향 순회만으로 모든 트리 DP를 끝냄.
    def build_heavy_light_decomposition(self, root_node:int) -> None:
        node_at_order:list = self.node_at_order
        immediate_dominator:list = self.immediate_dominator
        tree_depth:list = self.tree_depth
        subtree_size:list = self.subtree_size
        heavy_child:list = self.heavy_child
        chain_head:list = self.chain_head
        minimum_ancestor_cost:list = self.minimum_ancestor_cost
        inspection_cost:list = self.inspection_cost

        for order_index in range(1, self.total_visited + 1):
            subtree_size[node_at_order[order_index]] = 1

        # 역방향 순회(Bottom-up): 서브트리 크기 누적 및 무거운 자식(Heavy Child) 결정
        for order_index in range(self.total_visited, 1, -1):
            current_node:int = node_at_order[order_index]
            parent_node:int = immediate_dominator[current_node]
            subtree_size[parent_node] += subtree_size[current_node]
            if subtree_size[current_node] > subtree_size[heavy_child[parent_node]]:
                heavy_child[parent_node] = current_node

        minimum_ancestor_cost[root_node] = inspection_cost[root_node]
        chain_head[root_node] = root_node

        # 정방향 순회(Top-down): 트리 깊이, HLD 체인 헤드(chain_head), 루트부터의 최소 비용 누적 DP 계산
        for order_index in range(2, self.total_visited + 1):
            current_node = node_at_order[order_index]
            parent_node = immediate_dominator[current_node]
            tree_depth[current_node] = tree_depth[parent_node] + 1

            # 루트(1번) ~ 현재 정점까지의 도미네이터 경로 중 최소 조사 비용 갱신
            parent_minimum_cost:int = minimum_ancestor_cost[parent_node]
            current_cost:int = inspection_cost[current_node]
            minimum_ancestor_cost[current_node] = current_cost if current_cost < parent_minimum_cost else parent_minimum_cost

            # 부모의 무거운 자식이면 체인을 이어받고, 가벼운 자식이면 자신이 새 체인의 시작점이 됨
            if heavy_child[parent_node] == current_node:
                chain_head[current_node] = chain_head[parent_node]
            else:
                chain_head[current_node] = current_node

    # 4단계 : HLD 기반 O(log N) 최저 공통 조상(LCA) 탐색
    def get_lowest_common_ancestor(self, first_node:int, second_node:int) -> int:
        chain_head:list = self.chain_head
        tree_depth:list = self.tree_depth
        immediate_dominator:list = self.immediate_dominator

        # 두 노드가 속한 체인이 다르면, 체인 헤드의 깊이가 더 깊은 쪽을 부모 체인으로 점프시킴 (최대 O(log N)회)
        while chain_head[first_node] != chain_head[second_node]:
            if tree_depth[chain_head[first_node]] < tree_depth[chain_head[second_node]]:
                first_node, second_node = second_node, first_node
            first_node = immediate_dominator[chain_head[first_node]]

        # 동일한 체인 위에 놓이면 깊이가 더 얕은 노드가 LCA임
        return first_node if tree_depth[first_node] < tree_depth[second_node] else second_node

    # 5단계 : 질의로 주어진 불만 접수 우체국들의 공통 지배자 중 최소 비용 반환
    def query_minimum_candidate_cost(self, complaint_offices:list) -> int:
        common_dominator:int = complaint_offices[0]
        for office_node in complaint_offices[1:]:
            # 누적 LCA를 통해 모든 목표 우체국을 지배하는 가장 낮은(깊은) 공통 지배자를 찾음
            common_dominator = self.get_lowest_common_ancestor(common_dominator, office_node)
            # 공통 지배자가 루트(1번)에 도달하면 더 이상 조상이 없으므로 조기 종료 (가지치기)
            if common_dominator == 1:
                break
        
        # 1번부터 common_dominator까지의 모든 조상이 유효한 후보이므로, 전처리된 경로 최솟값을 O(1)에 반환
        return self.minimum_ancestor_cost[common_dominator]


# I/O 오버헤드를 최소화하기 위해 전체 입력을 단일 리스트로 토큰화하여 인덱스 포인터로 파싱
def process_all_queries(raw_tokens:list) -> list:
    token_index:int = 0
    node_count:int = int(raw_tokens[token_index])
    edge_count:int = int(raw_tokens[token_index + 1])
    token_index += 2

    edge_end_index:int = token_index + 2 * edge_count
    cost_start_index:int = edge_end_index

    inspection_cost:list = [0] * (node_count + 1)
    for office_number in range(1, node_count + 1):
        inspection_cost[office_number] = int(raw_tokens[cost_start_index + office_number - 1])

    dominator_tree:DominatorTree = DominatorTree(node_count, inspection_cost)

    while token_index < edge_end_index:
        source_node:int = int(raw_tokens[token_index])
        target_node:int = int(raw_tokens[token_index + 1])
        dominator_tree.add_edge(source_node, target_node)
        token_index += 2

    token_index = cost_start_index + node_count
    query_count:int = int(raw_tokens[token_index])
    token_index += 1

    dominator_tree.compute_dominators(1)
    dominator_tree.build_heavy_light_decomposition(1)

    query_answers:list = []
    for _ in range(query_count):
        complaint_count:int = int(raw_tokens[token_index])
        token_index += 1
        # 리스트 컴프리헨션을 통한 빠른 질의 배열 생성
        complaint_offices:list = [
            int(raw_tokens[token_index + offset]) for offset in range(complaint_count)
        ]
        token_index += complaint_count

        minimum_cost:int = dominator_tree.query_minimum_candidate_cost(complaint_offices)
        query_answers.append(str(minimum_cost))

    return query_answers

write("\n".join(process_all_queries(read().split())))

"""
=========================================================================================
[전력계통(스마트 그리드)에서 도미네이터 트리의 실전 적용 노트]

이 알고리즘의 '우체국 물류망' 모델은 특정 운전 상태(Operating Point)에서 유효전력 조류 방향이 결정된
'송전망(Transmission Network) 및 배전망 전력 조류(Power Flow)' 시스템과 위상수학적(Topological) 동형을 이룹니다.
전력망 해석 및 감시 모델을 구축할 때 다음과 같이 직접 응용할 수 있습니다.

0. 다중 발전원(Multi-Source) 계통으로의 모델링 확장 기법
   - 실제 전력망은 발전기(Source)가 여러 대 존재하므로, 가상의 '통합 전원 모선(Virtual Super-Source, 1번 노드)'을 
     생성하고 이 가상 노드에서 모든 발전기 모선(Generator Bus)으로 단방향 간선을 연결합니다.
   - 이렇게 변환하면 단일 루트 기반의 도미네이터 트리 코드를 다중 발전기 전력망에 수정 없이 그대로 적용할 수 있습니다.
   - 만약 특정 부하 모선의 직속 지배자(idom)가 가상 루트(1번)로 나온다면, 해당 모선은 단일 발전기나 단일 변전소에 
     종속되지 않고 복수의 독립 경로로부터 전력을 안정적으로 공급받고 있음을 의미합니다.

1. 단일 장애점(SPOF) 기반의 연쇄 고장(Cascading Outage) 진원지 역추적
   - 우체국(Node) : 발전기, 변전소 모선(Bus) 및 수용가 부하(Load)
   - 우편 전달 경로(Edge) : 조류 계산(Power Flow) 결과로 방향이 결정된 송전선로 및 변압기 가지(Branch)
   - 고객 불만(Query) : 복수의 하위 변전소에서 동시에 감지된 전력 공급 단절(Loss of Load) 또는 계통 이상 경보
   - 공통 지배자(Dominator) : 해당 하위 모선들로 향하는 모든 전력 조류가 반드시 통과해야 하는 상위 계통의 '병목 모선(Critical Bus)'
   - 도미네이터 트리를 HLD로 압축해 두면, 광역 감시 제어 시스템(WAMS)에서 다수의 PMU(위상측정장치)나 SCADA 알람이 
     동시에 발생했을 때 O(log N)의 시간 안에 연쇄 고장의 공통 분기점(LCA)을 실시간으로 특정할 수 있습니다.

2. 감시 센서(PMU) 최적 배치 및 유지보수 비용 최소화 (Optimal Sensor Placement)
   - 조사 비용(inspection_cost)은 각 변전소의 정밀 점검 비용, 계측 설비 설치 비용, 또는 차단기 동작 비용에 대응됩니다.
   - 고장 파급 경로 상의 지배자 노드들 중 비용이 가장 낮은 노드를 O(1)에 조회할 수 있으므로, 
     최소 예산으로 핵심 병목 지점의 가시성(Observability)을 확보하거나 우선 점검 대상을 선정하는 알고리즘으로 활용됩니다.

3. 계통 신뢰도 및 N-1 상정고장(Contingency) 스크리닝의 고속화
   - 도미네이터 트리에서 특정 모선 u가 탈락(Outage)하면, 트리 상에서 u의 서브트리에 속한 모든 하위 모선들은 
     전원으로부터의 모든 공급 경로를 상실하여 위상학적으로 완전히 고립(Topological Islanding / Blackout)됩니다.
   - 대규모 전력망에서 무거운 비선형 조류 계산(Newton-Raphson)이나 과도 안정도 미분방정식을 풀기 위한 룽게-쿠타 기법(Runge-Kutta)을 
     모든 선로/모선 탈락 케이스마다 일일이 시뮬레이션하기 전에, O((V+E) log V)의 도미네이터 트리 전처리만으로 
     치명적인 계통 분리(Islanding)를 유발하는 위상학적 취약 모선을 1차 스크리닝(Filtering)하여 전체 해석 속도를 비약적으로 높일 수 있습니다.
=========================================================================================
"""