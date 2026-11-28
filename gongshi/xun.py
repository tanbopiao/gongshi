"""巡（XUN）· 巡检官：注册表巡检，输出巡检单。

巡＝按册查役。三查：重名多版并存是否合预期、句柄是否失效、停用未销是否积压。
"""


class Xun:
    """巡检官：注册表巡检。"""

    def patrol(self, ledger, board):
        """三查并出巡检单：findings 逐条带 kind 与证据。"""
        findings = []
        # 一查：重名插件（多版本并存属设计内，但须点名可见）
        by_name = {}
        for e in ledger.values():
            by_name.setdefault(e["name"], []).append(e["plugin_id"])
        for name, pids in sorted(by_name.items()):
            if len(pids) > 1:
                findings.append({"kind": "multi_version", "name": name, "plugin_ids": pids})
        # 二查：失效句柄（handler 不可调用）
        for pid, e in sorted(ledger.items()):
            if not callable(e.get("handler")):
                findings.append({"kind": "broken_handler", "plugin_id": pid, "name": e["name"]})
        # 三查：停用未销（停用后仍在册）
        for pid, state in sorted(board.items()):
            if not state.get("active") and pid in ledger:
                findings.append({"kind": "idle_registered", "plugin_id": pid, "name": ledger[pid]["name"]})
        return {"findings": findings, "checked": len(ledger)}
