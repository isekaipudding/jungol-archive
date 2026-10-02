# 링크 : https://jungol.co.kr/problem/3699
import sys

input = sys.stdin.readline

T:int = int(input().rstrip())

for _ in range(T) :
    N:int = int(input().rstrip())

    D:dict = dict()

    for _ in range(N) :
        clothe_name, clothe_type = map(str, input().split())
        if clothe_type not in D.keys() :
            D[clothe_type] = 1
        else :
            D[clothe_type] += 1
    
    result:int = 1
    
    for v in D.values() :
        result *= (v + 1)
    
    result -= 1
    print(result)

"""
type 1의 개수 : a
type 2의 개수 : b
type 3의 개수 : c
이렇게 있다고 가정할 때
1가지 입는 경우 : a + b + c
2가지 입는 경우 : ab + bc + ca
3가지 입는 경우 : abc

이것은 (a + 1)(b + 1)(c + 1)로 구할 수 있습니다.
(a + 1)(b + 1)(c + 1) = abc + ab + bc + ca + a + b + c + 1
따라서 정답은 (a + 1)(b + 1)(c + 1) - 1입니다.
"""