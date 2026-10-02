# 링크 : https://jungol.co.kr/problem/3106
import sys

input = sys.stdin.readline

# 입력 캐시
D_in:dict = dict()
for i in range(0, 10, 1) :
    D_in[str(i)] = i
for i in range(65, 65 + 26, 1) :
    D_in[chr(i)] = i - 55

# 출력 캐시
D_out:dict = dict()
for i in range(0, 10, 1) :
    D_out[i] = str(i)
for i in range(65, 65 + 26, 1) :
    D_out[i - 55] = chr(i)

while True :
    L:list = list(map(str, input().split()))
    if L == ["0"] :
        break
    
    A, S, B = int(L[0]), L[1], int(L[2])
    
    # A진법 -> 10진법
    N:int = 0
    
    shift:int = 1
    for i in range(len(S)-1, -1, -1) :
        N += shift * D_in[S[i]]
        shift *= A
    
    # 10진법 -> B진법
    result:str = ""
    
    while N :
        result = D_out[N % B] + result
        N //= B
        
    if N == 0 and result == "" :
        result = "0"
    
    print(result)