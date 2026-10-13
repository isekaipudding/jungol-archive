# 링크 : https://jungol.co.kr/problem/1214
import sys

input = sys.stdin.readline

# 백준 1775번(히스토그램) 문제 풀이를 참고하여 세그먼트 트리 대신 스택으로 해결합니다.
# 출처 : https://www.acmicpc.net/blog/view/12#comment-442

def largest_hist(hist) :
    """
    단조 증가 스택을 이용해 히스토그램에서 만들 수 있는
    가장 큰 직사각형 넓이를 O(N)에 계산한다.
    """
    stack:list = []  # (시작 인덱스, 높이)
    max_area:int = 0

    for i, h in enumerate(hist) :
        start:int = i
        # 지금 막대 h가 더 낮다면, 쌓여있던 더 높은 막대들을 마무리 처리
        while stack and stack[-1][1] > h :
            index, height = stack.pop()
            # index부터 i-1까지 height로 채운 직사각형
            width = i - index
            area = height * width
            if area > max_area :
                max_area = area
            # 더 낮은 h가 대신 차지하더라도, 시작점은 기존 index로 이어질 수 있음
            start = index
        # 현재 막대를 스택에 push (가능하면 왼쪽으로 최대 확장된 start 인덱스로)
        stack.append((start, h))

    # 스택에 남아 있는 막대 처리 (끝까지 내려오지 않은 애들)
    n:int = len(hist)
    for index, height in stack :
        width:int = n - index
        area:int = height * width
        if area > max_area :
            max_area = area

    return max_area

data:list = list(map(int, input().split()))
print(largest_hist(data[1:]))