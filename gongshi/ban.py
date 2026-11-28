"""版（BAN）· 版籍官：同插件多版本并存登记，version 字段核验。

版籍＝官府登记人户与产业的簿册。一插件多版本，各立一页，互不覆盖。
"""


class Ban:
    """版籍官：版本并存登记。"""

    def __init__(self):
        self.ledger = {}  # plugin_id -> {name, version, handler, created_seq}
        self._seq = 0

    def enroll(self, plugin, version):
        """版籍登记：插件须有名与可调用入口，version 必填非空。"""
        if not isinstance(plugin, dict) or not plugin.get("name") or not callable(plugin.get("handler")):
            raise ValueError("插件不合准入：缺名或缺可调用入口")
        if not version or not isinstance(version, str):
            raise ValueError("版籍登记须带非空 version")
        self._seq += 1
        pid = "GS-%04d" % self._seq
        self.ledger[pid] = {
            "plugin_id": pid,
            "name": plugin["name"],
            "version": version,
            "handler": plugin["handler"],
        }
        return dict(self.ledger[pid])

    def versions_of(self, name):
        """查某插件全部并存版本，按登记序返回。"""
        return [dict(e) for e in self.ledger.values() if e["name"] == name]
