"""工师（GONGSHI）算子骨架单测：名帖完整、桩位齐整、只增不覆盖。"""
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

    def test_register_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.register(None)

    def test_admit_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.admit(None)


if __name__ == "__main__":
    unittest.main()
