class EmptyListException(Exception):
    pass


class Node:
    def __init__(self, value):
        self._value = value
        self._next = None

    def value(self):
        return self._value

    def next(self):
        return self._next


class LinkedList:
    def __init__(self, values=None):
        # _head 永远指向链表的第一个节点
        # 刚创建链表时，没有任何节点，所以是 None
        self._head = None

        # values 是可选参数
        # 例如：LinkedList([1, 2, 3])
        if values is not None:
            # 依次把 values 中的值压入链表头部
            for value in values:
                self.push(value)
                
    def __iter__(self):
        # current 从头节点开始
        current = self._head

        # 只要 current 不是 None，
        # 就说明当前位置还有节点
        while current is not None:
            # yield 每次交出一个节点中的值
            # 这样链表就可以被 for 循环和 list() 使用
            yield current.value()

            # current 移动到下一个节点
            current = current.next()

    def __len__(self):
        # count 用于记录节点数量
        count = 0

        # 从头节点开始遍历
        current = self._head
        while current is not None:
            # 每遇到一个节点，数量加一
            count += 1

            # 继续移动到下一个节点
            current = current.next()

        # 返回链表节点总数
        return count

    def head(self):
        # 如果头节点是 None，说明链表为空
        if self._head is None:
            raise EmptyListException("The list is empty.")

        # 返回头节点对象
        # 注意：这里返回的是 Node，不是节点里的值
        return self._head


    def push(self, value):
         # 用传入的 value 创建一个新节点
        new_node = Node(value)

        # 新节点的下一个节点，
        # 应该指向当前的头节点
        new_node._next = self._head

        # 再让新节点成为新的头节点
        self._head = new_node

        # 例如原来：
        #
        # head → 2 → 1 → None
        #
        # push(3) 以后：
        #
        # head → 3 → 2 → 1 → None


    def pop(self):
        if self._head is None:
            raise EmptyListException("The list is empty.")

        # 先保存当前头节点中的值
        # 因为修改 _head 后，原来的头节点就会脱离链表
        value = self._head.value()

        # 让头指针移动到下一个节点
        # 原来的第二个节点成为新的头节点
        self._head = self._head.next()

        # 返回刚刚删除的节点中的值
        return value


        
    def reversed(self):
        # 创建一个新的空链表
        # 不直接修改原链表
        reversed_list = LinkedList()

        # 遍历原链表中的每一个值
        for value in self:
            # 每次都把值放到新链表的头部
            reversed_list.push(value)

        # 返回反转后的新链表
        return reversed_list

        # 例如原链表遍历顺序：
        #
        # 3 → 2 → 1
        #
        # 依次 push 到新链表：
        #
        # push(3)：3
        # push(2)：2 → 3
        # push(1)：1 → 2 → 3
        #
        # 因此顺序被反转
