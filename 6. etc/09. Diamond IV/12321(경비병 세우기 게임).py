# 링크 : https://jungol.co.kr/problem/12321
import sys

input = sys.stdin.readline

T:int = int(input().rstrip())

for _ in range(T) :
    N, M, K = map(int, input().split())
    if N // 2 < K and M // 2 < K :
        print("Yuto")
        continue
    if (N * M - 2 * K ** 2) % 2 == 1 :
        print("Yuto")
    else : 
        print("Platina")
    
"""
N, M, K = 1, 2, 1인 경우
1x2 보드판에서 경비병 한 명 설치하면 사정거리가 1x1입니다.
o
o
Yuto가 1, Platina 2라고 가정합니다.
N, M, K = 1, 2, 1인 경우는 Yuto가 무슨 수를 쓰더라도 반드시 다음에 Platina가 마무리하므로 항상 Platina가 승리합니다.
그러면 이번엔 N, M, K = 1, 3, 1으로 합니다.
그러면 어떻게 될까요?
Yuto -> Platina -> Yuto 순으로 진행되어 항상 Yuto가 승리합니다.
그 뒤 N = 1로 고정할 때 M이 홀수이면 Yuto 승리, 짝수이면 Platina 승리입니다.

그러면 이번엔 N = 2로 시작할까요?
N <= M이므로 M = 2로 시작해야 합니다.
N, M, K = 2, 2, 1로 합니다.
그러면 Yuto -> Platina -> Yuto -> Platina 순으로 진행되어 Platina가 승리합니다.
그 뒤 N = 2, K = 1인 경우 M이 얼마이든 무조건 Platina가 승리합니다.
이것으로 알 수 있는 것은 N*M과 K 사이에 어떤 관계가 있는 것을 알 수 있습니다.

그러면 이번엔 N = 2, M = 2, K = 2로 합니다.
그러면 Yuto가 사거리 2x2인 경비병 하나 배치하면 바로 Yuto 승리로 게임이 끝납니다.

잘 생각해보니 만약
ooooo
ooooo
ooooo
ooooo
ooooo
이렇게 되어 있을 때 처음부터
111oo
111oo
111oo
ooooo
ooooo
이렇게 N // 2 < K 그리고 M // 2 < K이면 어떻게 될까요?
Platina가 둘 수 있는 자리가 없어 무조건 Yuto가 승리합니다.
여기서 <=가 아닌 <인 이유는 N = 4, M = 4, K = 2인 상황에서는 Platina가 이기기 때문입니다.

그러면 나머지 경우는 어떻게 해야 할까요?
N * M 그리고 K와 관련이 있다고 했죠?
그러면 N // 2 >= K일 때는 Platina는 반드시 자리 하나를 차지할 수 있습니다.
N = 4, M = 4, K = 2이라고 가정합니다.
oooo
oooo
oooo
oooo
각각 자리를 하나 배치합니다.
11oo
11oo
oo22
oo22
이런 경우 Platina가 승리합니다.

그 다음으로 N = 5, M = 5, K = 2입니다.
각각 자리를 하나 배치합니다.
11ooo
11ooo
ooooo
ooo22
ooo22
이런 경우는 언듯 보면 Platina가 이길 것처럼 보입니다.
그런데 과연 그럴까요?
문제를 자세히 보면 
"이 게임에서 '안전상태'라는 것은 격자판 안에 완벽히 포함되는 
어떤 K × K 크기의 정사각형에도 1명 이상의 경비병이 있는 상태를 의미한다."
라는 조건에 의해
111oo
111oo
ooooo
ooo22
ooo22
이렇게 상대한테 우겨도(?) 규칙을 어기지 않았으니 문제 없습니다.
이런 경우 끝까지 가면 Yuto가 이깁니다.

그 뒤 노가다를 좀 더 해서 N, M, K = 6, 6, 2 그리고 N, M, K = 7, 7, 2를 확인해보면
각각 Platina 승리, Yuto 승리라는 것을 확인할 수 있습니다.

이것으로 알 수 있는 것은 처음 2턴 동안을 제외한 나머지 빈칸의 개수에 따라 결과가 달라지는 것을 확인할 수 있습니다.
빈칸들을 각각 계산해봅니다.
N = 4, M = 4, K = 2 -> N * M - 2 * K ** 2 = 4 * 4 - 2 * 2 ** 2 = 8(Platina 승리)
N = 5, M = 5, K = 2 -> 5 * 5 - 2 * 2 ** 2 = 17(Yuto 승리)
N = 6, M = 6, K = 2 -> 6 * 6 - 2 * 2 ** 2 = 28(Platina 승리)
N = 7, M = 7, K = 2 -> 7 * 7 - 2 * 2 ** 2 = 41(Yuto 승리)

오잉? 이거 빈칸의 개수를 확인해보니 홀수이면 Yuto 승리, 짝수이면 Platina 승리이군요!?
그러면 if (N * M - 2 * K ** 2) % 2 == 1로 해서 구하면 되겠군요!
"""