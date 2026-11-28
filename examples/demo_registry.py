"""工师（GONGSHI）· 插件注册中心端到端演示：百工准入，核验乃收。"""
from gongshi import Gongshi

gate = Gongshi()

# 1. 骨架原 API：登记与准入（行为不变）
pid = gate.register({"name": "算盘", "handler": lambda x: x * 2})
print("register ->", pid, "| admit ->", gate.admit({"name": "算盘", "handler": lambda x: x}))

# 2. 版：同插件多版本并存
v1 = gate.register_version({"name": "良工", "handler": lambda x: x + 1}, "1.0")
v2 = gate.register_version({"name": "良工", "handler": lambda x: x + 2}, "2.0")
print("versions(良工) ->", [(e["version"], e["plugin_id"]) for e in gate.versions("良工")])

# 3. 点：停用后调用核验即拒
gate.toggle(v2["plugin_id"], active=False)
print("admit_for v1 ->", gate.admit_for(v1["plugin_id"]), "| admit_for v2(停用) ->", gate.admit_for(v2["plugin_id"]))

# 4. 巡：三查巡检单（多版本、失效句柄、停用未销）
report = gate.inspect()
print("inspect ->", [(f["kind"], f.get("name") or f.get("plugin_id")) for f in report["findings"]])
