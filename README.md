# Proxy Rules

供 Surge 与 Nikki/Mihomo 共用的公开目标名单。这里只回答“哪些目标属于哪个服务”，不包含节点、策略组、DNS、监听或完整客户端配置。

| 列表 | 用途 | 初始条数 |
| --- | --- | --- |
| `rules/Claude.list` | Claude 核心、共享辅助服务、入站网段及历史兼容范围 | 41 |
| `rules/OpenAI.Core.list` | OpenAI/ChatGPT 目标 | 15 |
| `rules/Cursor.Core.list` | Cursor 目标 | 4 |

初始内容于 2026-11-07 从已审核、已部署列表迁入。Claude 四份名单已按原顺序合成 `Claude.list`，41 条匹配条件完全等价，文件内用注释区分范围。本仓库直接维护 `rules/`，不再生成重复的 `dist/`。来源与适用边界见 [SOURCES.md](SOURCES.md)。

旧 `Claude.Core.list`、`Claude.Auxiliary.list`、`Claude.Inbound.list`、`Claude.LegacyCompatibility.list` 保留原字节，供旧客户端和回滚使用，**冻结且不再同步新修改**。日常只维护 `Claude.list`，不要继续订阅四份旧名单，也不要同时订阅新旧名单。旧文件的历史“生成产物”注释描述原来源。

## 订阅

每份文件的稳定地址为：

```text
https://raw.githubusercontent.com/lionoggo/proxy-rules/main/rules/<文件名>
```

Surge 示例：

```ini
RULE-SET,https://raw.githubusercontent.com/lionoggo/proxy-rules/main/rules/Claude.list,Claude,no-resolve,update-interval=3600
```

Nikki/Mihomo 示例：

```yaml
rule-providers:
  ManagedClaude:
    type: http
    behavior: classical
    format: text
    url: https://raw.githubusercontent.com/lionoggo/proxy-rules/main/rules/Claude.list
    path: ./providers/rule/shared/Claude.list
    interval: 3600
    proxy: 自建代理

rules:
  - RULE-SET,ManagedClaude,Claude,no-resolve
```

例子不是完整配置。OpenAI 和 Cursor 使用各自独立的 URL／缓存路径。名单没有策略字段，IP/ASN 行保留 `no-resolve`；不能当作 domain/ipcidr/mrs 格式加载。合并时只替换四个连续的 Claude 引用，原有精确例外、策略组和静态拒绝兜底保持位置不变。

## 本地策略不随订阅同步

- Claude 组仅自建或拒绝；OpenAI 当前固定节点或拒绝；Cursor 各端自行选择。
- `events.statsigapi.net` 精确例外、Statsig 后缀拒绝、Fathom 拒绝及其顺序保留在客户端。
- 现有静态内联拒绝兜底保留：新增目标不自动获得兜底，删去目标可能仍被旧兜底拒绝。删除、跨列表迁移或改变策略前，必须审核客户端基线。
- 代理组、节点、DNS、透明代理、防火墙、局域网规则及运行时选择均在各端维护。

## 更新

1. 只修改三个正式名单，不修改冻结的四份兼容文件，不添加凭据、订阅URL或设备信息。
2. 运行 `python3 tools/validate.py` 和 `python3 tools/test_validate.py`。
3. 通过 PR，校验成功后合入 `main`；不自动合并第三方内容。
4. 两端原生每小时检查，无需另行部署完整配置。文档／工具改动不改变规则内容。

原生刷新不执行每次连接终结或全量验收；已有连接可能继续使用旧规则，断网／休眠／缓存会延迟更新，多份文件不保证原子加载。首次接入及后续配置重载仍需受控维护。重大范围变化要单独验收。

有效缓存和静态兜底不等于全系统 kill switch；不保证未知工具目标、所有接口或全部节点故障时绝对无旁路。代理路由成功也不等于登录、支付或模型业务成功。
