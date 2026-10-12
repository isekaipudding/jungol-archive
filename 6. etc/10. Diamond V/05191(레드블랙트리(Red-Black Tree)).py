# 링크 : https://jungol.co.kr/problem/5191
import sys

input = sys.stdin.readline

# RBTree 소스 코드 출처 : https://lamp2357.tistory.com/46

class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1 # 1: RED, 0: BLACK

class RBTree:
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    # 탐색 및 최소값 찾기
    def search(self, k):
        node = self.root
        while node != self.TNULL:
            if k == node.data:
                return node
            elif k < node.data:
                node = node.left
            else:
                node = node.right
        return self.TNULL
    
    # 최소값 노드 찾기
    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    # Left Rotate
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
    
    # Right Rotate
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    
    # Insert & Fixup(더블 레드 복구)
    def insert_fix(self, k):
        while k.parent != None and k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left # 삼촌 노드
                
                # 삼촌 노드가 RED인 경우
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                # 삼촌 노드가 BLACK인 경우
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            
            if k == self.root:
                break
        self.root.color = 0
    
    # 삽입 함수
    def insert(self, key):
        if self.search(key) != self.TNULL:
            return
        
        node = Node(key)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1
        
        y = None
        x = self.root
        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right
        
        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return
        if node.parent.parent == None:
            return

        self.insert_fix(node)
    
    # 레드 블랙 트리 노드 이식 함수
    def rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    # Delete & Fixup(이중 흑색 노드 복구)
    def delete_fix(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                
                # Case 1 -> 형제 노드가 RED인 경우 -> 형재 BLACK, 부모 RED 후 회전
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right
                
                # Case 2 -> 형제의 양쪽 자식이 모두 BLACK인 경우 -> 형제 RED, 부모로 BLACK 전가
                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    # Case 3 -> 형제의 왼쪽 자식만 RED인 경우 -> 형제 RED, 왼쪽 조카 BLACK 후 회전
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right
                    
                    # Case 4 -> 형제의 오른쪽 자식이 RED인 경우 -> 최종 복구
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left
                
                if s.right.color == 0 and s.left.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left
                    
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0
    # 삭제 함수
    def delete(self, key):
        z = self.search(key)
        if z == self.TNULL:
            return
        
        y = z
        y_original_color = y.color
        
        if z.left == self.TNULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        
        if y_original_color == 0:
            self.delete_fix(x)
    
    # 중위 순회
    def inorder(self):
        result = []
        def _traverse(node):
            if node != self.TNULL:
                _traverse(node.left)
                color_str = "R" # node.color == 1
                if node.color == 0:
                    color_str = "B"
                result.append(f"{node.data}{color_str}")
                _traverse(node.right)
        # 여기서 증위 순회(dfs) 탐색 시작
        _traverse(self.root)
        print(*result)

# 메인 로직
N:int = int(input().rstrip())
S = RBTree()

for _ in range(N):
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    if cmd == "i":
        S.insert(int(query[1]))
    if cmd == "d":
        S.delete(int(query[1]))
    if cmd == "o":
        S.inorder()