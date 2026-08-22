# Private Clash Rules

Personal Clash / Surge rule lists used with a customized ACL4SSR `main.ini` (subconverter). Rules are **first-match-wins**: earlier `ruleset=` lines take priority.

Raw prefix: `https://raw.githubusercontent.com/Banezzz/private_clash_rules/main/`

## Files

| File | Policy group | Notes |
|------|----------------|-------|
| `main.ini` | — | Subconverter config: ruleset order + strategy groups |
| `ai.list` | 🤖 AI Suite | OpenAI, Anthropic, Gemini, Cursor, and related AI hosts |
| `trading.list` | 📈 交易相关 | Exchanges and market-data hosts (curated, not a wholesale dump) |
| `Netflix.list` | 🎥 奈飞视频 | Netflix hosts / keywords (no broad AWS CIDR) |
| `steam.list` | 🎮 游戏平台 | Steam and Valve-related hosts |
| `selfbuilt.list` | 🫡 自建节点 | Overlay hook only — see below |
| `discord.list` | 💬 Discord | Discord hosts |
| `github.list` | 🛠️ GitHub | GitHub / git-related hosts |
| `spotify.list` | 🎵 Spotify | Spotify hosts |

There is **no** `ai_suite.list`, **no** `ACL4SSR_Online_Full_MultiMode.ini`, and **no** local `ChinaDomain.list`. China domains come from upstream ACL4SSR.

Local lists are referenced as:

`https://raw.githubusercontent.com/Banezzz/private_clash_rules/main/<file>`

## Load order

`main.ini` `ruleset=` lines are applied top to bottom.

1. 🎯 LocalAreaNetwork
2. 🎯 UnBan
3. 🛑 BanAD
4. 🫡 `selfbuilt.list` (local overlay)
5. 📈 `trading.list` (local)
6. 🍃 BanProgramAD
7. 📢 GoogleFCM
8. 🎯 GoogleCN
9. ~~SteamCN~~ **commented out** — Steam downloads must stay on 🎮 游戏平台 (proxy), not DIRECT
10. Ⓜ️ Bing / OneDrive / Microsoft
11. 🍎 Apple
12. 📲 Telegram
13. 💬 `discord.list` (local)
14. 🤖 `ai.list` (local)
15. 🛠️ `github.list` (local)
16. 🎶 NetEaseMusic
17. 🎮 Epic / Origin / Sony / `steam.list` / Nintendo
18. 📹 YouTube
19. 🎥 `Netflix.list` (local)
20. 🎵 `spotify.list` (local)
21. 📺 Bahamut / BilibiliHMT / Bilibili
22. 🌏 ChinaMedia
23. 🌍 ProxyMedia
24. 🚀 ProxyGFWlist
25. 🎯 ChinaIp (enabled)
26. 🎯 ACL4SSR `ChinaDomain.list` (upstream URL, not a repo file)
27. 🎯 ChinaCompanyIp / Download
28. 🎯 `[]GEOIP,LAN`
29. 🎯 `[]GEOIP,CN`
30. 🐟 `[]FINAL`

Local lists sit above ACL4SSR `ProxyMedia` / `ProxyGFWlist`, so a domain listed here wins over the generic media/GFW sets.

## Default exits

The **first** item of each `select` group is the Clash default.

| Group | Default (first item) |
|-------|----------------------|
| 🚀 节点选择 | 🚀 手动切换 |
| 📈 交易相关 | 💸 交易节点 |
| 🎥 奈飞视频 | 🎥 奈飞节点 |
| 🤖 AI Suite | 🫡 自建节点 |
| 📹 油管视频 | 🫡 自建节点 |
| 🌍 国外媒体 | 🫡 自建节点 |
| 🛠️ GitHub | 🫡 自建节点 |
| 🎵 Spotify | 🫡 自建节点 |
| 📲 电报消息 | 🚀 节点选择 |
| 💬 Discord | 🚀 节点选择 |
| Ⓜ️ 微软云盘 / 微软服务 / 微软Bing | 🚀 节点选择 |
| 📢 谷歌FCM | 🚀 节点选择 |
| 🎮 游戏平台 | 🚀 节点选择 |
| 🐟 漏网之鱼 | 🚀 节点选择 |
| 🫡 自建节点 | 🔀 双入口LB |
| 📺 巴哈姆特 | 🇨🇳 台湾节点 |
| 📺 哔哩哔哩 | 🎯 全球直连 |
| 🌏 国内媒体 | DIRECT |
| 🎶 网易音乐 | DIRECT (unlock-name filter kept) |
| 🍎 苹果服务 | DIRECT |
| 🎯 全球直连 | DIRECT |
| 🛑 广告拦截 / 🍃 应用净化 | REJECT |

Function groups use short menus (自建 / 节点选择 / 手动切换 / DIRECT) instead of repeating every region group.

Helper groups:

- 🤖 AI 自动 / 💸 交易自动 — `url-test` over all nodes
- 🎥 奈飞节点 — name filter `(NF|奈飞|解锁|Netflix|NETFLIX|Media)`, not `.*`
- 💸 交易节点 — `select` `.*`
- 🔀 双入口LB — `load-balance` on `腾讯云内网`, **round-robin**
- 🔮 负载均衡 — full-set `load-balance`, **consistent-hashing** (same destination sticks)

## `selfbuilt.list` is an overlay hook

🫡 自建节点 is the **exit selector** (default: 🔀 双入口LB over Tencent 内网 nodes). `selfbuilt.list` is **not** a catalog. It only pins rare domains that must use that exit. Empty / one-line is expected; add a `DOMAIN-SUFFIX` when a host truly needs that path.

## Region name tokens

| Group | Notes |
|-------|--------|
| 🇭🇰 香港节点 | Official-style `(港\|HK\|hk\|Hong Kong\|HongKong\|hongkong)`. **Do not** match `pis` / `sak`. |
| 🇺🇲 美国节点 | Existing US tokens plus `bwh` / `BDWH` / `bdwh` (Bandwagon-style names). |
| 🇲🇾 马来西亚节点 | `MY` / `my` is **intentional** (owner naming). |
| 🇯🇵 🇹🇼 🇸🇬 🇰🇷 | Unchanged. |

## Do-not list

Do **not** add these (too broad or they fight the intended exit):

- `DOMAIN-SUFFIX,googleapis.com` (and similarly `googleusercontent.com` / `goog`)
- Netflix AWS `IP-CIDR` `/12`–`/16` blocks
- Enabling ACL4SSR `SteamCN.list` (that would DIRECT Steam downloads)
- Wholesale blackmatrix7 Crypto dumps into `trading.list`

## Rule format

- `DOMAIN` — exact host
- `DOMAIN-SUFFIX` — host and all subdomains
- `DOMAIN-KEYWORD` — substring match (easy to over-capture)
- `IP-CIDR` / `IP-CIDR6` — always append `,no-resolve`
- `PROCESS-NAME` — desktop / Android package name (not DNS)

## `scripts/check_rules.py`

Python 3, no extra deps. From the repo root:

```bash
python3 scripts/check_rules.py
```

It scans every `*.list` in the repo root for duplicate rules, `IP-CIDR`/`IP-CIDR6` missing `,no-resolve`, a dangerous `DOMAIN-SUFFIX` blacklist, and whether `README.md` mentions each existing list plus `main.ini`. Exit code `1` on findings, `0` when clean.
