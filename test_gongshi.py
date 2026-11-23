"""工师（GONGSHI）算子单测：名帖完整、行为达标、只增不覆盖。"""
import unittest

from gongshi import Gongshi


class TestGongshi(unittest.TestCase):
    def setUp(self):
        self.op = Gongshi()

    def test_describe(self):
        d = self.op.describe()
        self.assertEqual(d["repo"], "gongshi")
        self.assertEqual(d["code"], "GONGSHI")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))
        self.assertTrue(d["mingwen"])

    def test_register(self):
        pid = self.op.register({"name": "良工", "handler": lambda x: x})
        self.assertTrue(pid.startswith("GS-"))
        with self.assertRaises(ValueError):
            self.op.register({"name": "无名之工"})


if __name__ == "__main__":
    unittest.main()
