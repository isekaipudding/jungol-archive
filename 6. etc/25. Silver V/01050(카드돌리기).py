# 링크 : https://jungol.co.kr/problem/1050
import sys

input = sys.stdin.readline

SUIT_ORDER = {'C': 0, 'D': 1, 'S': 2, 'H': 3}
RANK_ORDER = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}
PLAYERS = ['N', 'E', 'S', 'W']

def card_sort_key(card:str):
    return (SUIT_ORDER[card[0]], RANK_ORDER[card[1]])

dealer = input().rstrip()

# 카드 52장이 적힌 두 줄 입력받기
card_str = input().rstrip() + input().rstrip()

# 2글자씩 쪼개어 52장의 카드 리스트 생성
cards = [card_str[i:i + 2] for i in range(0, len(card_str), 2)]

hands = {'N': [], 'E': [], 'S': [], 'W': []}

# 딜러의 다음 사람부터 시작
start_index = (PLAYERS.index(dealer) + 1) % 4

for i, card in enumerate(cards):
    recipient = PLAYERS[(start_index + i) % 4]
    hands[recipient].append(card)
    
# 각 플레이어 패 정렬
for p in PLAYERS:
    hands[p].sort(key=card_sort_key)
    
# S -> W -> N -> E 순서로 출력
for p in ['S', 'W', 'N', 'E']:
    print(f"{p}: {" ".join(hands[p])}")