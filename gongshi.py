"""工师（GONGSHI）· 插件注册中心

道统出处：元极恒一·道统构件定名册 V2 ｜ 第五批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：插件注册中心。

边界：本件为算子骨架 v0——接口先立、实现随进化轮补齐；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。
"""

class Gongshi:
    """工师（GONGSHI）算子骨架 v0。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "GONGSHI"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：会话内事件留痕

    def describe(self):
        """构件名帖：名、代号、职责、铭文、体系锚。"""
        return {
            "repo": "gongshi",
            "cn": "工师",
            "code": self.CODE,
            "duty": "插件注册中心",
            "mingwen": "百工准入，核验乃收",
            "anchor": self.ANCHOR,
        }

    def register(self, plugin):
        """百工准入：插件登记（骨架桩：实现随进化轮补齐）。"""
        raise NotImplementedError("GONGSHI.register 骨架桩，候进化轮补齐")

    def admit(self, plugin):
        """核验乃收：准入核验（骨架桩：实现随进化轮补齐）。"""
        raise NotImplementedError("GONGSHI.admit 骨架桩，候进化轮补齐")
