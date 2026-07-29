import json


class RestAPI:
    def __init__(self, database=None):
        # 测试传入的格式是：{"users": []}
        self.database = database if database is not None else {"users": []}

    def _find_user(self, name):
        """在 users 列表中，根据名字找到对应用户字典。"""
        for user in self.database["users"]:
            if user["name"] == name:
                return user

    def _update_balance(self, user):
        """更新用户余额：别人欠我的钱 - 我欠别人的钱。"""
        user["balance"] = (
            sum(user["owed_by"].values()) - sum(user["owes"].values())
        )

    def get(self, url, payload=None):
        # 获取用户信息
        if url == "/users":
            users = self.database["users"]

            # 如果 payload 存在，只返回指定用户
            if payload is not None:
                payload_data = json.loads(payload)
                requested_names = payload_data["users"]

                users = [
                    user for user in users
                    if user["name"] in requested_names
                ]

            # 按用户姓名排序
            users = sorted(users, key=lambda user: user["name"])

            # 必须返回 JSON 字符串
            return json.dumps({"users": users})

    def post(self, url, payload=None):
        # 测试传入的是 JSON 字符串，先转成 Python 字典
        payload_data = json.loads(payload)

        # 添加用户
        if url == "/add":
            name = payload_data["user"]

            new_user = {
                "name": name,
                "owes": {},
                "owed_by": {},
                "balance": 0.0
            }

            self.database["users"].append(new_user)

            # 返回 JSON 字符串
            return json.dumps(new_user)

        # 添加一笔借款记录
        if url == "/iou":
            lender_name = payload_data["lender"]
            borrower_name = payload_data["borrower"]
            amount = payload_data["amount"]

            lender = self._find_user(lender_name)
            borrower = self._find_user(borrower_name)

            # borrower 原本欠 lender 的钱
            old_debt = borrower["owes"].get(lender_name, 0)

            # lender 原本欠 borrower 的钱
            reverse_debt = lender["owes"].get(borrower_name, 0)

            # 这次借款与反方向债务抵消
            if reverse_debt >= amount:
                # 例如 Adam 欠 Bob 10，Adam 借给 Bob 4
                # 最后 Adam 仍欠 Bob 6
                remaining = reverse_debt - amount

                if remaining == 0:
                    lender["owes"].pop(borrower_name)
                    borrower["owed_by"].pop(lender_name)
                else:
                    lender["owes"][borrower_name] = remaining
                    borrower["owed_by"][lender_name] = remaining
            else:
                # 先消除反方向债务
                if reverse_debt > 0:
                    lender["owes"].pop(borrower_name)
                    borrower["owed_by"].pop(lender_name)

                # 剩余部分变成 borrower 欠 lender
                new_debt = old_debt + amount - reverse_debt
                borrower["owes"][lender_name] = new_debt
                lender["owed_by"][borrower_name] = new_debt

            # 更新双方余额
            self._update_balance(lender)
            self._update_balance(borrower)

            # 返回两人资料，按姓名排序
            result = sorted([lender, borrower], key=lambda user: user["name"])
            return json.dumps({"users": result})