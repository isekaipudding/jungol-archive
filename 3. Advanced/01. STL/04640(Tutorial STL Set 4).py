# 링크 : https://jungol.co.kr/problem/4640
import sys

input = sys.stdin.readline

class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1  
        self.size = 1   

class RBTree:
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.TNULL.size = 0  
        self.root = self.TNULL
        self.tree_size = 0

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

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

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
        y.size = x.size
        x.size = x.left.size + x.right.size + 1

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
        y.size = x.size
        x.size = x.left.size + x.right.size + 1

    def insert_fix(self, k):
        while k.parent != None and k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left 
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
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

    def insert(self, key):
        if self.search(key) != self.TNULL:
            return  

        node = Node(key)
        node.parent = None
        node.data = key
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

        curr = node.parent
        while curr != None:
            curr.size += 1
            curr = curr.parent

        if node.parent == None:
            node.color = 0
            self.tree_size += 1
            return
        if node.parent.parent == None:
            self.tree_size += 1
            return

        self.insert_fix(node)
        self.tree_size += 1

    def rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_fix(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right
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

    def delete(self, key):
        z = self.search(key)
        if z == self.TNULL:
            return  

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            curr = z.parent
            while curr != None:
                curr.size -= 1
                curr = curr.parent
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            curr = z.parent
            while curr != None:
                curr.size -= 1
                curr = curr.parent
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            curr = y.parent
            while curr != None:
                curr.size -= 1
                curr = curr.parent

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
            y.size = y.left.size + y.right.size + 1
            
        self.tree_size -= 1
        
        if y_original_color == 0:
            self.delete_fix(x)

    def ceil(self, k):
        node = self.root
        result = self.TNULL
        
        while node != self.TNULL:
            if node.data == k:
                return node
            elif node.data > k:
                result = node
                node = node.left
            else:
                node = node.right
                
        return result

    def floor(self, k):
        node = self.root
        result = self.TNULL
        
        while node != self.TNULL:
            if node.data == k:
                return node
            elif node.data < k:
                result = node
                node = node.right
            else:
                node = node.left
                
        return result

Q:int = int(input().rstrip())
s = RBTree()

for _ in range(Q):
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "i":
        N:int = int(query[1])
        s.insert(N)
    if cmd == "r":
        N:int = int(query[1])
        s.delete(N)
    if cmd == "b":
        N:int = int(query[1])
        result = s.ceil(N)
        if result != s.TNULL:
            print(result.data)
    if cmd == "s":
        N:int = int(query[1])
        result = s.floor(N)
        if result != s.TNULL:
            print(result.data)