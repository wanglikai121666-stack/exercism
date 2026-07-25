class CustomSet:
    def __init__(self, elements=None):
        # None 表示调用时没有传元素，例如 CustomSet()
        if elements is None:
            elements = []

        # 用 Python 内置 set 保存数据：
        # 自动去重，例如 [1, 2, 2, 3] 会变成 {1, 2, 3}
        self.elements = set(elements)

    def isempty(self):
        # 空集合的长度是 0
        return len(self.elements) == 0

    def __contains__(self, element):
        # 让 Python 支持：
        # element in my_set
        return element in self.elements

    def issubset(self, other):
        # 当前集合是否完全包含在 other 中
        # 例如 {1, 2} 是 {1, 2, 3} 的子集
        return self.elements.issubset(other.elements)

    def isdisjoint(self, other):
        # 两个集合是否没有任何相同元素
        # 例如 {1, 2} 与 {3, 4} 没有交集
        return self.elements.isdisjoint(other.elements)

    def __eq__(self, other):
        # 让两个 CustomSet 可以用 == 比较。
        # set 比较时不看元素顺序。
        return self.elements == other.elements

    def add(self, element):
        # set.add() 会自动忽略已存在的元素，不会重复添加
        self.elements.add(element)

    def intersection(self, other):
        # & 是集合交集：只保留两边都有的元素
        common_elements = self.elements & other.elements

        # 结果也必须包装成 CustomSet，而不是直接返回内置 set
        return CustomSet(common_elements)

    def __sub__(self, other):
        # 让 Python 支持：
        # set_a - set_b
        #
        # - 是差集：保留只在当前集合中的元素
        remaining_elements = self.elements - other.elements
        return CustomSet(remaining_elements)

    def __add__(self, other):
        # 让 Python 支持：
        # set_a + set_b
        #
        # | 是并集：合并两边全部元素，并自动去重
        all_elements = self.elements | other.elements
        return CustomSet(all_elements)