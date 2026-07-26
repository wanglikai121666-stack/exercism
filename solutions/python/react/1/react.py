class InputCell:
    def __init__(self, initial_value):
        # _value 是真正存放数值的内部属性。
        self._value = initial_value

        # 哪些 ComputeCell 依赖当前 InputCell。
        # 例如 total = a + b，则 a 和 b 的 _dependents 都会包含 total。
        self._dependents = []

    @property
    def value(self):
        # 读取 input_cell.value 时，返回当前值。
        return self._value

    @value.setter
    def value(self, new_value):
        # InputCell 允许外部直接修改值。
        self._value = new_value

        # 输入改变后，让所有直接或间接受影响的计算格重新计算。
        self._propagate_changes()

    def _propagate_changes(self):
        # 先找出所有会被当前 InputCell 影响的 ComputeCell。
        # 用 set 是为了避免同一个计算格被重复收集。
        affected_cells = set()

        def collect_dependents(cell):
            # 从一个格子出发，找到所有直接依赖它的 ComputeCell。
            for dependent in cell._dependents:
                if dependent not in affected_cells:
                    affected_cells.add(dependent)

                    # dependent 也可能被更后面的 ComputeCell 依赖。
                    # 例如：a -> first_total -> final_total
                    collect_dependents(dependent)

        collect_dependents(self)

        # 保存每个计算格更新前的值。
        # 最后只有“新旧值不同”的格子才应触发 callback。
        old_values = {
            cell: cell._value
            for cell in affected_cells
        }

        # 记录已经重新计算过的格子，避免重复计算。
        updated_cells = set()

        def update_cell(cell):
            if cell in updated_cells:
                return

            # 如果当前 ComputeCell 的输入里还有 ComputeCell，
            # 必须先更新上游计算格，保证读取到的是最新值。
            for input_cell in cell.inputs:
                if isinstance(input_cell, ComputeCell):
                    update_cell(input_cell)

            # 收集所有输入格子的最新 value。
            values = []

            for input_cell in cell.inputs:
                values.append(input_cell.value)

            # 调用创建 ComputeCell 时传入的计算规则。
            # 例如 lambda values: values[0] + values[1]。
            cell._value = cell.compute_function(values)

            updated_cells.add(cell)

        # 将所有受影响的 ComputeCell 更新到新的稳定状态。
        for cell in affected_cells:
            update_cell(cell)

        # 所有计算完成后，再通知 callback。
        # 这样 callback 观察到的是稳定后的最终结果。
        for cell in affected_cells:
            if cell._value != old_values[cell]:
                # list(...) 是副本，避免 callback 执行时修改列表影响循环。
                for callback in list(cell._callbacks):
                    callback(cell._value)


class ComputeCell:
    def __init__(self, inputs, compute_function):
        # inputs 是当前格子依赖的格子列表。
        # 其中元素可以是 InputCell，也可以是另一个 ComputeCell。
        self.inputs = inputs

        # compute_function 是具体计算规则。
        self.compute_function = compute_function

        # 当前 ComputeCell 的下游依赖者。
        # 它也可以作为另一个 ComputeCell 的输入。
        self._dependents = []

        # 当前 ComputeCell 登记的回调函数。
        self._callbacks = []

        # 创建时，先用输入格子的当前值算出初始结果。
        values = []

        for input_cell in self.inputs:
            values.append(input_cell.value)

            # 建立反向关系：
            # “当前 ComputeCell 依赖 input_cell”。
            input_cell._dependents.append(self)

        self._value = self.compute_function(values)

    @property
    def value(self):
        # ComputeCell 对外只能读取，不能直接赋值。
        # 它的值只能由 inputs 自动重新计算。
        return self._value

    def add_callback(self, callback):
        # 登记一个 callback。
        # 当这个 ComputeCell 的值真的变化时，会调用 callback(新值)。
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        # 移除已登记的 callback。
        if callback in self._callbacks:
            self._callbacks.remove(callback)