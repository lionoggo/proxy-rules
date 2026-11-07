#!/usr/bin/env python3
"""只读共享名单格式/已审核范围检查；无部署或网络操作。"""
import ipaddress
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    "Claude.Core.list", "Claude.Auxiliary.list", "Claude.Inbound.list",
    "Claude.LegacyCompatibility.list", "OpenAI.Core.list", "Cursor.Core.list",
)
IP_TYPES = {"IP-CIDR", "IP-CIDR6", "IP-ASN"}
DOMAIN = re.compile(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+")


def parse(text):
    rows = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith(("#", "//", ";")):
            continue
        parts = line.split(",")
        if len(parts) not in (2, 3):
            raise ValueError(f"line {number}: 只允许匹配条件及no-resolve")
        kind, value = parts[:2]
        if kind in IP_TYPES:
            if parts[2:] != ["no-resolve"]:
                raise ValueError(f"line {number}: IP/ASN须保留no-resolve")
        elif len(parts) != 2:
            raise ValueError(f"line {number}: 不允许策略或域名参数")
        if kind in {"DOMAIN", "DOMAIN-SUFFIX"}:
            if not DOMAIN.fullmatch(value):
                raise ValueError(f"line {number}: 非法域名")
        elif kind == "DOMAIN-KEYWORD":
            if not re.fullmatch(r"[a-z0-9-]+", value) or value in {"claude", "anthropic"}:
                raise ValueError(f"line {number}: 未批准关键词")
        elif kind in {"IP-CIDR", "IP-CIDR6"}:
            network = ipaddress.ip_network(value, strict=True)
            if network.version != (4 if kind == "IP-CIDR" else 6):
                raise ValueError(f"line {number}: IP类型错误")
            if network.is_private or network.is_loopback or network.is_link_local:
                raise ValueError(f"line {number}: 不应公开本地网段")
        elif kind == "IP-ASN":
            if not value.isdecimal() or not 0 < int(value) < 2**32:
                raise ValueError(f"line {number}: 非法ASN")
        else:
            raise ValueError(f"line {number}: 未支持类型")
        if tuple(parts) in rows:
            raise ValueError(f"line {number}: 重复规则")
        rows.append(tuple(parts))
    if not rows:
        raise ValueError("不允许空列表")
    return rows


def validate(root=ROOT):
    files = {path.name for path in (root / "rules").iterdir() if path.is_file()}
    if files != set(NAMES):
        raise ValueError("文件白名单改变，先审核发布范围")
    data = {name: parse((root / "rules" / name).read_text()) for name in NAMES}
    expected_domains = {
        "anthropic.com", "anthropic.team", "claude.ai", "claude.com", "claude.app",
        "claude.dev", "claude.new", "claude.site", "clau.de", "claudeacademy.com",
        "claudemcpclient.com", "claudemcpcontent.com", "claudepages.dev",
        "claudestudio.com", "claudeusercontent.com", "chatbotclaude.com",
        "ant.dev", "antspace.dev", "statsig.anthropic.com",
    }
    if not {("DOMAIN-SUFFIX", domain) for domain in expected_domains} <= set(data["Claude.Core.list"]):
        raise ValueError("Claude核心基线缺失；删除需要单独审核客户端兜底")
    if set(data["Claude.Inbound.list"]) != {
        ("IP-CIDR", "160.79.104.0/23", "no-resolve"),
        ("IP-CIDR", "153.61.224.0/22", "no-resolve"),
        ("IP-CIDR6", "2607:6bc0::/48", "no-resolve"),
    }:
        raise ValueError("官方目标IP基线改变，需同步审核")
    if any(row[1] == "153.61.208.0/20" for rows in data.values() for row in rows):
        raise ValueError("不能混入云端出站来源段")
    return data


if __name__ == "__main__":
    for name, rows in validate().items():
        print(f"通过：{name}，{len(rows)} 条")
