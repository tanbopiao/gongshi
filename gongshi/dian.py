"""点（DIAN）· 点卯官：插件启用/停用状态跟踪，停用后调用核验即拒。

点卯＝旧时官署卯时点名，到者应卯。在册应卯为启用，缺席为停用；未入册者无从应卯。
"""


class Dian:
    """点卯官：启用/停用状态板。"""

    def __init__(self):
        self.board = {}  # plugin_id -> {"active": bool}

    def mark(self, plugin_id, active):
        """点卯：登记启用/停用。未入册者拒。"""
        if not isinstance(plugin_id, str) or not plugin_id:
            return False
        self.board.setdefault(plugin_id, {"active": None})
        self.board[plugin_id]["active"] = bool(active)
        return True

    def check(self, plugin_id):
        """调用前核验：在册且启用才放行。"""
        state = self.board.get(plugin_id)
        return bool(state and state.get("active"))
