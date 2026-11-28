# gongshi · 工师

**插件注册中心：百工准入，核验乃收。**

> 命名即种子：工师＝《周礼·考工记》百工之长，「审曲面势，以饬五材」。名字所对应的逻辑与架构，是从种子长出来的。

## 命名映射（道统 → 架构）

| 道 | 义 | 算子 |
|----|----|------|
| 工师 | 百工之长，审曲面势 | `Gongshi` 门面（原 v1 骨架收编） |
| 版 | 版籍在官，一业数承 | `Ban` 版籍官：同插件多版本并存登记，version 核验 |
| 巡 | 按册查役，纠偏补漏 | `Xun` 巡检官：重名多版、失效句柄、停用未销三查出巡检单 |
| 点 | 卯时点名，到者应卯 | `Dian` 点卯官：启用/停用状态板，停用后调用核验即拒 |

逻辑本体：**插件入册必有名帖与可调用入口；版本并存可查，巡检纠偏可见，启停状态可控。**

## 安装

零第三方依赖，仅 Python 3.10+ 标准库。

```bash
git clone https://github.com/tanbopiao/gongshi.git
cd gongshi
python -m unittest discover -s tests -v   # 自测
python examples/demo_registry.py          # 端到端演示
```

## 用法

```python
from gongshi import Gongshi

gate = Gongshi()

# 骨架原 API：登记与准入（行为不变）
pid = gate.register({"name": "算盘", "handler": lambda x: x * 2})

# 版：同插件多版本并存
v1 = gate.register_version({"name": "良工", "handler": fn1}, "1.0")
v2 = gate.register_version({"name": "良工", "handler": fn2}, "2.0")
gate.versions("良工")   # -> [{version: "1.0", ...}, {version: "2.0", ...}]

# 点：停用后调用核验即拒
gate.toggle(v2["plugin_id"], active=False)
gate.admit_for(v2["plugin_id"])   # -> False

# 巡：三查巡检单
gate.inspect()   # -> {findings: [{kind: multi_version|broken_handler|idle_registered, ...}], checked: N}
```

原单文件骨架 API（`describe()` / `register()` / `admit()`）收编保留，行为不变。

## 自测

```bash
python -m unittest discover -s tests -v
```

## 许可

MIT
