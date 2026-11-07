# Proxy Rules

供 Surge 与 Nikki/Mihomo 共用的公开目标名单。这里只回答“哪些目标属于哪个服务”，不包含节点、策略组、DNS、监听或完整客户端配置。

| 列表 | 用途 | 初始条数 |
| --- | --- | --- |
| `rules/Claude.Core.list` | Claude 核心域名、认证/CDN及专用 Statsig | 23 |
| `rules/Claude.Auxiliary.list` | 共享辅助服务；会影响其他应用 | 9 |
| `rules/Claude.Inbound.list` | 客户端访问的官方入站目标网段 | 3 |
| `rules/Claude.LegacyCompatibility.list` | 原有宽关键词、网段与ASN兼容范围 | 6 |
| `rules/OpenAI.Core.list` | OpenAI/ChatGPT 目标 | 15 |
| `rules/Cursor.Core.list` | Cursor 目标 | 4 |

初始内容于 2026-11-07 从已审核、已部署列表迁入，保持字节一致。文件中的历史“生成产物”注释描述原来源；本仓库直接维护 `rules/`，不再生成重复的 `dist/`。来源与适用边界见 [SOURCES.md](SOURCES.md)。

## 订阅

每份文件的稳定地址为：

```text
https://raw.githubusercontent.com/lionoggo/proxy-rules/main/rules/<文件名>
```

Surge 示例：

```ini
RULE-SET,https://raw.githubusercontent.com/lionoggo/proxy-rules/main/rules/Claude.Core.list,Claude,no-resolve,update-interval=3600
```

Nikki/Mihomo 示例：

```yaml
rule-providers:
  ManagedClaudeCore:
    type: http
    behavior: classical
    format: text
    url: https://raw.githubusercontent.com/lionoggo/proxy-rules/main/rules/Claude.Core.list
    path: ./providers/rule/shared/Claude.Core.list
    interval: 3600
    proxy: 自建代理

rules:
  - RULE-SET,ManagedClaudeCore,Claude,no-resolve
```

例子不是完整配置。其余五份列表使用各自独立的 URL／缓存路径。名单没有策略字段，IP/ASN 行保留 `no-resolve`；不能当作 domain/ipcidr/mrs 格式加载。

## 本地策略不随订阅同步

- Claude 组仅自建或拒绝；OpenAI 当前固定节点或拒绝；Cursor 各端自行选择。
- `events.statsigapi.net` 精确例外、Statsig 后缀拒绝、Fathom 拒绝及其顺序保留在客户端。
- 现有静态内联拒绝兜底保留：新增目标不自动获得兜底，删去目标可能仍被旧兜底拒绝。删除、跨列表迁移或改变策略前，必须审核客户端基线。
- 代理组、节点、DNS、透明代理、防火墙、局域网规则及运行时选择均在各端维护。

## 更新

1. 只修改 `rules/`，不添加凭据、订阅URL或设备信息。
2. 运行 `python3 tools/validate.py` 和 `python3 tools/test_validate.py`。
3. 通过 PR，校验成功后合入 `main`；不自动合并第三方内容。
4. 两端原生每小时检查，无需另行部署完整配置。文档／工具改动不改变规则内容。

原生刷新不执行每次连接终结或全量验收；已有连接可能继续使用旧规则，断网／休眠／缓存会延迟更新，多份文件不保证原子加载。首次接入及后续配置重载仍需受控维护。重大范围变化要单独验收。

有效缓存和静态兜底不等于全系统 kill switch；不保证未知工具目标、所有接口或全部节点故障时绝对无旁路。代理路由成功也不等于登录、支付或模型业务成功。
