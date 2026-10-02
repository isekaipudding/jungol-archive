# 링크 : https://jungol.co.kr/problem/1880
import sys

input = sys.stdin.readline

small_decryption:str = input().rstrip()
large_decryption:str = small_decryption.upper()

D:dict = dict()

for i in range(26) :
    D[chr(97 + i)] = small_decryption[i]
    D[chr(65 + i)] = large_decryption[i]

D[" "] = " "

sentence:str = input().rstrip()

result:str = ""
for i in range(len(sentence)) :
    result += D[sentence[i]]

print(result)