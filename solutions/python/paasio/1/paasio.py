import io


class MeteredFile(io.BufferedRandom):
    """Implement using a subclassing model.

    继承 io.BufferedRandom，在其基础上增加 IO 统计功能。
    统计指标：读/写的字节数、读/写操作次数。
    """

    def __init__(self, *args, **kwargs):
        """
        构造函数，直接透传给父类 io.BufferedRandom。

        父类的初始化需要传入一个 RawIOBase（如 FileIO）作为参数：
            MeteredFile(open("test.txt", "rb"))
        或者直接传路径给 FileIO：
            MeteredFile(io.FileIO("test.txt", "rb"))
        """
        # 先初始化父类（io.BufferedRandom 负责真正的读写）
        super().__init__(*args, **kwargs)

        # --- 统计计数器 ---
        # 读操作相关
        self._read_bytes = 0      # 累计读了多少字节
        self._read_ops = 0        # 累计读了多少次
        # 写操作相关
        self._write_bytes = 0     # 累计写了多少字节
        self._write_ops = 0       # 累计写了多少次

    def __enter__(self):
        """进入上下文管理器（with 语句），返回自身。"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器。

        调用 super().__exit__(...) 让父类（io.BufferedRandom）处理退出逻辑。
        在真实场景下，父类的 __exit__ 会调用 self.close() 来关闭文件。
        在测试场景下，如果父类被 mock 替换，这个调用会触发 mock 的 __exit__。

        返回值：父类 __exit__ 的返回值（通常为 None 或 False）。
        """
        return super().__exit__(exc_type, exc_val, exc_tb)

    def __iter__(self):
        """
        返回迭代器自身，支持 for line in file: 语法。

        Python 的文件迭代每次读一行，直到文件末尾。
        """
        return self

    def __next__(self):
        """
        迭代器的下一行。

        每次调用通过 self.readline() 读一行（计数已在 readline 中做），
        到文件末尾时抛出 StopIteration 终止循环。

        注意：这里不再单独计数，避免和 readline() 重复计数。
        """
        # 用父类的 readline 读一行（计数已在 readline 重写中完成）
        line = self.readline()
        if not line:
            # 空行表示已到文件末尾 → 终止迭代
            raise StopIteration
        return line

    def read(self, size=-1):
        """
        读文件，统计读的字节数和操作次数。

        参数：
            size: 要读的字节数。默认为 -1 表示读全部。

        返回值：
            读到的字节串 bytes
        """
        # 调用父类的 read 方法（真正干活）
        data = super().read(size)
        # 统计：读了多少字节、1 次操作
        self._read_bytes += len(data)
        self._read_ops += 1
        return data

    @property
    def read_bytes(self):
        """已读字节数（只读属性）。"""
        return self._read_bytes

    @property
    def read_ops(self):
        """已读操作次数（只读属性）。"""
        return self._read_ops

    def write(self, b):
        """
        写文件，统计写的字节数和操作次数。

        参数：
            b: 要写入的字节串 bytes

        返回值：
            实际写入的字节数 int
        """
        # 调用父类的 write 方法（真正干活）
        bytes_written = super().write(b)
        # 统计：写了多少字节、1 次操作
        self._write_bytes += bytes_written
        self._write_ops += 1
        return bytes_written

    def readline(self, size=-1):
        """
        读一行，统计读的字节数和操作次数。

        这个方法特别重要，因为文件迭代 (for line in mf) 内部就是
        反复调用 readline()，所以也需要计入统计。

        参数：
            size: 限制最大读多少字节。默认 -1 表示读到行尾。

        返回值：
            一行字节串 bytes (到换行符或 EOF 为止)
        """
        # 调用父类的 readline 方法（真正干活）
        line = super().readline(size)
        # 统计：读了多少字节、1 次操作
        self._read_bytes += len(line)
        self._read_ops += 1
        return line

    @property
    def write_bytes(self):
        """已写字节数（只读属性）。"""
        return self._write_bytes

    @property
    def write_ops(self):
        """已写操作次数（只读属性）。"""
        return self._write_ops


class MeteredSocket:
    """Implement using a delegation model.

    委托模式：内部持有真实的 socket 对象，把 send/recv 委托给它，
    在委托前后添加统计逻辑。
    """

    def __init__(self, socket):
        """
        构造函数，传入一个真实的 socket 对象。

        参数：
            socket: 一个 socket.socket 实例，我们要给它加"仪表盘"
        """
        # 持有真实 socket 的引用（委托给它的方法）
        self._socket = socket

        # --- 统计计数器 ---
        # 接收相关
        self._recv_bytes = 0      # 累计接收了多少字节
        self._recv_ops = 0        # 累计接收了多少次
        # 发送相关
        self._send_bytes = 0      # 累计发送了多少字节
        self._send_ops = 0        # 累计发送了多少次

    def __enter__(self):
        """进入上下文管理器（with 语句），返回自身。"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出上下文管理器。

        委托给底层 socket 的 __exit__，由它决定如何处理异常。
        返回值就是底层 socket.__exit__ 的返回值：
          - True  → 抑制异常（不往外抛）
          - False → 异常继续往外传
          - None  → 异常继续往外传

        这种"委托 + 返回底层结果"的模式让包装对象保留自己的异常处理逻辑。
        例如底层 socket.__exit__ 返回 True 时会吞掉异常，
        我作为包装类只是透传它这个决定。
        """
        # 委托给底层 socket 的 __exit__，返回它的返回值
        return self._socket.__exit__(exc_type, exc_val, exc_tb)

    def recv(self, bufsize, flags=0):
        """
        接收数据，统计接收的字节数和操作次数。

        参数：
            bufsize: 最多接收多少字节
            flags:   套接字标志（透传给底层 recv）

        返回值：
            接收到的字节串 bytes
        """
        # 委托给真实的 socket 接收数据
        data = self._socket.recv(bufsize, flags)
        # 统计：收了多少字节、1 次操作
        self._recv_bytes += len(data)
        self._recv_ops += 1
        return data

    @property
    def recv_bytes(self):
        """已接收字节数（只读属性）。"""
        return self._recv_bytes

    @property
    def recv_ops(self):
        """已接收操作次数（只读属性）。"""
        return self._recv_ops

    def send(self, data, flags=0):
        """
        发送数据，统计发送的字节数和操作次数。

        参数：
            data:  要发送的字节串 bytes
            flags: 套接字标志（透传给底层 send）

        返回值：
            实际发送的字节数 int
        """
        # 委托给真实的 socket 发送数据
        bytes_sent = self._socket.send(data, flags)
        # 统计：发了多少字节、1 次操作
        self._send_bytes += bytes_sent
        self._send_ops += 1
        return bytes_sent

    @property
    def send_bytes(self):
        """已发送字节数（只读属性）。"""
        return self._send_bytes

    @property
    def send_ops(self):
        """已发送操作次数（只读属性）。"""
        return self._send_ops
