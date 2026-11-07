# 来源和范围

这些名单是已审核的目标集合，不是对第三方整个仓库的镜像，也不是官方完整依赖保证。首次公开迁入日期：2026-11-07。

- [Anthropic 官方 IP 范围](https://platform.claude.com/docs/en/api/ip-addresses)：入站范围用于客户端目标；云端出站来源不能混入。
- [Claude Code 网络配置](https://code.claude.com/docs/en/network-config)：用于核对网络目标。
- [Claude Code 数据使用](https://code.claude.com/docs/en/data-usage)：遥测政策参考。
- [kenzok8 Claude.list](https://github.com/kenzok8/ruleset/blob/main/rule/Claude.list)：社区目标发现参考。
- [v2fly anthropic 数据](https://github.com/v2fly/domain-list-community/blob/master/data/anthropic)：域名参考。
- [Statsig 域名说明](https://docs.statsig.com/infrastructure/statsig_domains)：共享主机与专用域名边界。
- OpenAI/Cursor 名单取自此前审核的显式规则，并非全部依赖。共享第三方主机不自动归为某产品独占。

Claude Auxiliary 和 LegacyCompatibility 有意保留共享服务后缀、关键词、较宽网段及ASN，可能影响非Claude流量；不将其解释为官方必需范围。初始校验会约束现有核心基线；修改边界时需同步审核测试，不能只绕过检查。

来源链接可能变化。这里不提供第三方许可证重新授权；使用、补充或复制其他来源内容时，应遵守相应项目许可并保留归属。没有节点／私有配置从原私有仓库公开，也没有复制其Git历史。
