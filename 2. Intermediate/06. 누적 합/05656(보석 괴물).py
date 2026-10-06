# 링크 : https://jungol.co.kr/problem/5656
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().rstrip())) # split()이 아니라 rstrip()으로!