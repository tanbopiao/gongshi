"""工师（GONGSHI）算子单测：三算子＋门面＋legacy 兼容＋边界。"""
import unittest

from gongshi import Gongshi
from gongshi.ban import Ban
from gongshi.xun import Xun
from gongshi.dian import Dian


def good(name="良工", h=None):
    return {"name": name, "handler": h or (lambda x: x)}


class TestLegacyCompat(unittest.TestCase):
    """骨架原 API 行为不变。"""

    def setUp(self):
        self.op = Gongshi()

    def test_describe(self):
        d = self.op.describe()
        self.assertEqual(d["repo"], "gongshi")
        self.assertEqual(d["code"], "GONGSHI")
        self.assertEqual(d["cn"], "工师")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))
        self.assertEqual(d["mingwen"], "百工准入，核验乃收")

    def test_register(self):
        pid = self.op.register(good())
        self.assertTrue(pid.startswith("GS-"))
        with self.assertRaises(ValueError):
            self.op.register({"name": "无名之工"})

    def test_admit(self):
        self.assertTrue(self.op.admit(good()))
        self.assertFalse(self.op.admit({"name": "缺手"}))
        self.assertFalse(self.op.admit("不是字典"))


class TestBan(unittest.TestCase):
    def test_enroll_version_required(self):
        ban = Ban()
        e = ban.enroll(good(), "1.0")
        self.assertEqual(e["version"], "1.0")
        with self.assertRaises(ValueError):
            ban.enroll(good(), "")
        with self.assertRaises(ValueError):
            ban.enroll(good(), None)

    def test_multi_version_coexist(self):
        ban = Ban()
        ban.enroll(good(), "1.0")
        ban.enroll(good(), "2.0")
        vs = ban.versions_of("良工")
        self.assertEqual([v["version"] for v in vs], ["1.0", "2.0"])
        self.assertEqual(ban.versions_of("不存在"), [])


class TestXun(unittest.TestCase):
    def test_patrol_three_findings(self):
        ban, dian = Ban(), Dian()
        a = ban.enroll(good("甲"), "1.0")
        b = ban.enroll(good("甲"), "2.0")
        c = ban.enroll(good("乙"), "0.1")
        c["handler"] = 123  # 登记后句柄失效（模拟句柄被垃圾回收/替换）
        ban.ledger[c["plugin_id"]] = c
        dian.mark(a["plugin_id"], active=True)
        dian.mark(b["plugin_id"], active=False)   # 停用未销
        report = Xun().patrol(ban.ledger, dian.board)
        kinds = sorted(f["kind"] for f in report["findings"])
        self.assertEqual(kinds, ["broken_handler", "idle_registered", "multi_version"])
        self.assertEqual(report["checked"], 3)

    def test_patrol_clean(self):
        ban, dian = Ban(), Dian()
        a = ban.enroll(good(), "1.0")
        dian.mark(a["plugin_id"], active=True)
        report = Xun().patrol(ban.ledger, dian.board)
        self.assertEqual(report["findings"], [])


class TestDian(unittest.TestCase):
    def test_mark_and_check(self):
        d = Dian()
        d.mark("GS-0001", active=True)
        self.assertTrue(d.check("GS-0001"))
        d.mark("GS-0001", active=False)
        self.assertFalse(d.check("GS-0001"))

    def test_check_unregistered(self):
        self.assertFalse(Dian().check("GS-9999"))


class TestFacade(unittest.TestCase):
    def setUp(self):
        self.gate = Gongshi()

    def test_register_version_marks_active(self):
        e = self.gate.register_version(good(), "1.0")
        self.assertTrue(self.gate.admit_for(e["plugin_id"]))

    def test_toggle_then_admit_for_rejects(self):
        e = self.gate.register_version(good(), "1.0")
        self.gate.toggle(e["plugin_id"], active=False)
        self.assertFalse(self.gate.admit_for(e["plugin_id"]))
        self.gate.toggle(e["plugin_id"], active=True)
        self.assertTrue(self.gate.admit_for(e["plugin_id"]))

    def test_inspect_reports(self):
        self.gate.register_version(good("甲"), "1.0")
        self.gate.register_version(good("甲", h=lambda x: x), "2.0")
        report = self.gate.inspect()
        self.assertTrue(any(f["kind"] == "multi_version" for f in report["findings"]))

    def test_events_ledger_grows(self):
        n0 = len(self.gate.events)
        self.gate.register_version(good(), "1.0")
        self.gate.inspect()
        self.assertGreater(len(self.gate.events), n0)


if __name__ == "__main__":
    unittest.main()
