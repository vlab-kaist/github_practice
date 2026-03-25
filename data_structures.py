class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("스택이 비어있습니다")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("스택이 비어있습니다")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


class Queue:
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("큐가 비어있습니다")
        return self._items.pop(0)

    def front(self):
        if self.is_empty():
            raise IndexError("큐가 비어있습니다")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Queue({self._items})"


class LinkedList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, data):
        new_node = self.Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, data):
        new_node = self.Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def delete(self, data):
        if not self.head:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def find(self, data):
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def size(self):
        return self._size

    def __repr__(self):
        return f"LinkedList({self.to_list()})"


class BinarySearchTree:
    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = self.Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = self.Node(value)
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = self.Node(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def height(self):
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if not node:
            return 0
        return 1 + max(
            self._height_recursive(node.left), self._height_recursive(node.right)
        )


class HashMap:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _hash(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        index = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[index]):
            if k == key:
                self.buckets[index][i] = (key, value)
                return
        self.buckets[index].append((key, value))
        self.size += 1

    def get(self, key, default=None):
        index = self._hash(key)
        for k, v in self.buckets[index]:
            if k == key:
                return v
        return default

    def remove(self, key):
        index = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[index]):
            if k == key:
                del self.buckets[index][i]
                self.size -= 1
                return True
        return False

    def keys(self):
        all_keys = []
        for bucket in self.buckets:
            for k, v in bucket:
                all_keys.append(k)
        return all_keys

    def values(self):
        all_values = []
        for bucket in self.buckets:
            for k, v in bucket:
                all_values.append(v)
        return all_values

    def __repr__(self):
        items = []
        for bucket in self.buckets:
            for k, v in bucket:
                items.append(f"{k}: {v}")
        return "HashMap({" + ", ".join(items) + "})"


if __name__ == "__main__":
    print("=== Stack ===")
    s = Stack()
    for x in [1, 2, 3, 4, 5]:
        s.push(x)
    print(f"  {s}")
    print(f"  pop: {s.pop()}, peek: {s.peek()}")

    print("\n=== Queue ===")
    q = Queue()
    for x in ["a", "b", "c", "d"]:
        q.enqueue(x)
    print(f"  {q}")
    print(f"  dequeue: {q.dequeue()}, front: {q.front()}")

    print("\n=== LinkedList ===")
    ll = LinkedList()
    for x in [10, 20, 30, 40, 50]:
        ll.append(x)
    ll.prepend(0)
    print(f"  {ll}")
    ll.delete(30)
    print(f"  30 삭제 후: {ll}")

    print("\n=== BST ===")
    bst = BinarySearchTree()
    for x in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(x)
    print(f"  중위순회: {bst.inorder()}")
    print(f"  전위순회: {bst.preorder()}")
    print(f"  높이: {bst.height()}")
    print(f"  40 검색: {bst.search(40)}")
    print(f"  99 검색: {bst.search(99)}")

    print("\n=== HashMap ===")
    hm = HashMap()
    hm.put("name", "철수")
    hm.put("age", 25)
    hm.put("city", "서울")
    print(f"  {hm}")
    print(f"  name: {hm.get('name')}")
