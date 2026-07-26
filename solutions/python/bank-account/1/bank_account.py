class BankAccount:
    def __init__(self):
        # 刚创建账户对象时，还没有开户。
        self.is_open = False

        # 余额是账户内部状态。
        # 即使尚未开户，也先给它一个明确的初始值。
        self.balance = 0

    def get_balance(self):
        # 关闭/未开户的账户不允许查看余额。
        if not self.is_open:
            raise ValueError("account not open")

        # 账户正常开启时，返回当前余额。
        return self.balance

    def open(self):
        # 已开户不能重复开户。
        if self.is_open:
            raise ValueError("account already open")

        # 开户后，账户进入可操作状态。
        self.is_open = True

        # 每次开户都是一个新的账户周期，余额从 0 开始。
        # 因此关户后重新开户，不会保留以前的钱。
        self.balance = 0

    def deposit(self, amount):
        # 先确认账户状态，再处理金额。
        if not self.is_open:
            raise ValueError("account not open")

        # 0 或负数不是合法存款。
        if amount <= 0:
            raise ValueError("amount must be greater than 0")

        # 通过校验后，才真正修改余额。
        self.balance += amount

    def withdraw(self, amount):
        # 关闭/未开户的账户不能取款。
        if not self.is_open:
            raise ValueError("account not open")

        # 取款金额必须是正数。
        if amount <= 0:
            raise ValueError("amount must be greater than 0")

        # 不能取出超过现有余额的钱。
        if amount > self.balance:
            raise ValueError("amount must be less than balance")

        # 所有规则都满足，才扣减余额。
        self.balance -= amount

    def close(self):
        # 未开户或已经关闭的账户不能再次关闭。
        if not self.is_open:
            raise ValueError("account not open")

        # 只改变账户状态。
        # balance 可以暂时保留，但下次 open() 会把它重置为 0。
        self.is_open = False