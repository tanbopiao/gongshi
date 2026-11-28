"""工师（GONGSHI）· 插件注册中心：百工准入，核验乃收。

命名即种子：工师＝《周礼·考工记》百工之长，「审曲面势，以饬五材」。
逻辑本体：插件入册必有名帖与可调用入口，版本并存、巡检纠偏、点卯控启停。

三算子：
- 版（ban.Ban）    版籍官：同插件多版本并存登记，version 字段核验。
- 巡（xun.Xun）    巡检官：注册表巡检，发现重名插件与失效句柄，输出巡检单。
- 点（dian.Dian）  点卯官：插件启用/停用状态跟踪，停用后调用核验即拒。

三算子合枢于 Gongshi 门面（register_version / inspect / toggle）。
原单文件骨架 API（describe / register / admit）收编保留，行为不变。
"""

from .legacy import Gongshi as _LegacyGongshi
from .ban import Ban
from .xun import Xun
from .dian import Dian

__all__ = ["Gongshi", "Ban", "Xun", "Dian"]


class Gongshi(_LegacyGongshi):
    """工师门面：原 v1 API 之上长出版/巡/点三算子。"""

    def __init__(self, config=None):
        super().__init__(config)
        self._ban = Ban()
        self._xun = Xun()
        self._dian = Dian()

    # ---- 版：多版本并存登记 ----
    def register_version(self, plugin, version):
        """版籍登记：同插件多版本并存，version 必填。"""
        entry = self._ban.enroll(plugin, version)
        pid = entry["plugin_id"]
        self._dian.mark(pid, active=True)
        self.events.append({"event": "register_version", "plugin_id": pid, "version": version})
        return entry

    def versions(self, name):
        """查某插件全部并存版本。"""
        return self._ban.versions_of(name)

    # ---- 巡：注册表巡检 ----
    def inspect(self):
        """巡检单：重名插件、失效句柄、停用未销三查。"""
        report = self._xun.patrol(self._ban.ledger, self._dian.board)
        self.events.append({"event": "inspect", "findings": len(report["findings"])})
        return report

    # ---- 点：启用/停用 ----
    def toggle(self, plugin_id, active):
        """点卯：启用或停用插件。停用后 admit_for 调用核验即拒。"""
        ok = self._dian.mark(plugin_id, active=active)
        if ok:
            self.events.append({"event": "toggle", "plugin_id": plugin_id, "active": active})
        return ok

    def admit_for(self, plugin_id):
        """调用前核验：未注册或已停用即拒。"""
        return self._dian.check(plugin_id)
