class Scale:
    def __init__(self, tonic):
        # 保留原始大小写：
        # "C" 和 "c" 在本题中代表不同的调性规则
        self.tonic = tonic

    def chromatic(self):
        sharp_scale = [
            "A", "A#", "B", "C", "C#", "D",
            "D#", "E", "F", "F#", "G", "G#"
        ]

        flat_scale = [
            "A", "Bb", "B", "C", "Db", "D",
            "Eb", "E", "F", "Gb", "G", "Ab"
        ]

        # 只有这些“完全一致”的 tonic 使用降号表
        flat_tonics = {
            "F", "Bb", "Eb", "Ab", "Db", "Gb",
            "d", "g", "c", "f", "bb", "eb"
        }

        # 依据 tonic 原始大小写决定选哪一张表
        if self.tonic in flat_tonics:
            scale = flat_scale
        else:
            scale = sharp_scale

        # 输出音名要大写首字母；
        # 例如输入 "c" 时，要在音阶中查找 "C"
        tonic_for_lookup = self.tonic[0].upper() + self.tonic[1:]

        # 找主音位置，并循环拼接
        start_index = scale.index(tonic_for_lookup)
        return scale[start_index:] + scale[:start_index]
    def interval(self, intervals):
        # 先取得从主音开始的完整 12 音循环
        scale = self.chromatic()

        # 每种 interval 对应走几格
        steps = {
            "m": 1,  # 半步
            "M": 2,  # 全步
            "A": 3,  # 增二度
        }

        # 起点永远是第一个音
        position = 0
        result = [scale[position]]

        # 依次按照 interval 的步长向前走
        for interval in intervals:
            # % 12：超过最后一个音时，绕回第一个音
            position = (position + steps[interval]) % 12

            # 保存这一步走到的音
            result.append(scale[position])

        return result