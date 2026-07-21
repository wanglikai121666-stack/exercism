class Node:
    def __init__(self, value, succeeding=None, previous=None):
        # 当前节点保存的值
        self.value = value

        # 当前节点的后一个节点
        self.succeeding = succeeding

        # 当前节点的前一个节点
        self.previous = previous


class LinkedList:
    def __init__(self):
        # 链表的第一个节点
        self.head = None

        # 链表的最后一个节点
        self.tail = None

        # 链表中节点的数量
        self.length = 0

    def push(self, value):
        """在链表末尾添加一个节点。"""

        # 新节点的前一个节点是当前尾节点
        new_node = Node(value, previous=self.tail)

        # 如果链表为空，新节点同时是头节点和尾节点
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            # 原尾节点的 succeeding 指向新节点
            self.tail.succeeding = new_node

            # 新节点成为新的尾节点
            self.tail = new_node

        self.length += 1

    def pop(self):
        """删除并返回链表末尾节点的值。"""

        if self.length == 0:
            raise IndexError("List is empty")

        # 先保存尾节点的值，删除后需要返回
        value = self.tail.value

        # 如果链表中只有一个节点
        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            # 尾节点向前移动一位
            self.tail = self.tail.previous

            # 新尾节点后面不再有节点
            self.tail.succeeding = None

        self.length -= 1
        return value

    def unshift(self, value):
        """在链表开头添加一个节点。"""

        # 新节点的后一个节点是当前头节点
        new_node = Node(value, succeeding=self.head)

        # 如果链表为空，新节点同时是头节点和尾节点
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            # 原头节点的 previous 指向新节点
            self.head.previous = new_node

            # 新节点成为新的头节点
            self.head = new_node

        self.length += 1

    def shift(self):
        """删除并返回链表开头节点的值。"""

        if self.length == 0:
            raise IndexError("List is empty")

        # 先保存头节点的值
        value = self.head.value

        # 如果只有一个节点
        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            # 头节点向后移动一位
            self.head = self.head.succeeding

            # 新头节点前面不再有节点
            self.head.previous = None

        self.length -= 1
        return value

    def delete(self, value):
        """删除链表中第一个值等于 value 的节点。"""

        current_node = self.head

        # 从头节点开始向后寻找
        while current_node is not None:
            if current_node.value == value:
                # 删除的是头节点
                if current_node is self.head:
                    self.shift()
                    return

                # 删除的是尾节点
                if current_node is self.tail:
                    self.pop()
                    return

                # 删除的是中间节点
                previous_node = current_node.previous
                next_node = current_node.succeeding

                # 前一个节点跳过当前节点，指向后一个节点
                previous_node.succeeding = next_node

                # 后一个节点跳过当前节点，指向前一个节点
                next_node.previous = previous_node

                self.length -= 1
                return

            # 移动到下一个节点
            current_node = current_node.succeeding

        # 遍历结束仍然没找到
        raise ValueError("Value not found")

    def __len__(self):
        """让 len(linked_list) 返回节点数量。"""
        return self.length

    def __iter__(self):
        """让链表可以从头到尾进行遍历。"""

        current_node = self.head

        while current_node is not None:
            yield current_node.value
            current_node = current_node.succeeding