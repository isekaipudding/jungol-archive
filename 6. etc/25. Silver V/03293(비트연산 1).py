# 링크 : https://jungol.co.kr/problem/3293
op = ["?", "~", "&", "|", "^", "<<", ">>"]

print(op[2])                          # (1)
print(op[1], op[2], sep="")           # (2)
print(op[5])                          # (3)
print(op[6], op[2], op[5], sep="")    # (4)
print(op[4], op[4], op[4], sep="")    # (5)
print(op[6], op[2], sep="")           # (6)
print(op[2], op[1], op[5], sep="")    # (7)
print(op[4], op[5], sep="")           # (8)
print(op[2])                          # (9)
print(op[4], op[2], sep="")           # (10)