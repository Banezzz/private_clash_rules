# Private Clash Rules

Personal Clash / Surge rule lists used with a customized ACL4SSR `main.ini` (subconverter). Rules are **first-match-wins**: earlier `ruleset=` lines take priority.

Raw prefix: `https://raw.githubusercontent.com/Banezzz/private_clash_rules/main/`

## Files

| File | Policy group | Notes |
|------|----------------|-------|
| `main.ini` | — | Subconverter config: ruleset order + strategy groups |
| `apple_proxy.list` | 🍏 苹果代理 | Region-gated Apple services: TV+, News, Apple Intelligence relay, TestFlight, iCloud Private Relay. Loads before every `apple.com` rule |
| `apple.list` | 🍎 苹果服务 | DIRECT supplement to ACL4SSR `Apple.list`: CN-only hosts, Apple IPv6, Apple apps on Android / Windows / macOS daemons |
| `telegram.list` | 📲 电报消息 | Telegram clients (Android / desktop) + official ranges missing from ACL4SSR `Telegram.list` |
| `youtube.list` | 📹 油管视频 | YouTube Android apps (ACL4SSR `YouTube.list` is domain-only) |
| `ai.list` | 🤖 AI Suite | OpenAI, Anthropic, Gemini, Cursor, Meta AI / Llama / Muse, and related international AI hosts (aligned with geosite `category-ai-chat-!cn`, minus CN brands and over-broad SaaS) |
| `trading.list` | 📈 交易相关 | Exchanges and market-data hosts (curated). Android Play Store packages + Binance/OKX mobile-only hosts. Loads before BanAD |
| `Netflix.list` | 🎥 奈飞视频 | Netflix hosts / keywords (no broad AWS CIDR) |
| `steam.list` | 🎮 游戏平台 | Steam and Valve-related hosts |
| `riot.list` | 🎮 游戏平台 | Riot Client plus first-party web (LoL / TFT / Valorant / Wild Rift / 2XKO). Tencent CN LoL omitted |
| `selfbuilt.list` | 🫡 自建节点 | Overlay hook only — see below |
| `discord.list` | 💬 Discord | Discord hosts |
| `github.list` | 🛠️ GitHub | GitHub / git-related hosts |
| `spotify.list` | 🎵 Spotify | Spotify hosts |
| `tiktok.list` | 📱 TikTok | International TikTok + Android packages. ByteDance CN (Douyin / Toutiao) omitted |

There is **no** `ai_suite.list`, **no** `ACL4SSR_Online_Full_MultiMode.ini`, and **no** local `ChinaDomain.list`. China domains come from upstream ACL4SSR.

Local lists are referenced as:

`https://raw.githubusercontent.com/Banezzz/private_clash_rules/main/<file>`

## Load order

`main.ini` `ruleset=` lines are applied top to bottom.

1. 🎯 LocalAreaNetwork
2. 🎯 UnBan
3. 📈 `trading.list` (local) — **before BanAD** so exchange Android `PROCESS-NAME` and first-party hosts win over AppsFlyer / push REJECT
4. 🛑 BanAD
5. 🫡 `selfbuilt.list` (local overlay)
6. 🍃 BanProgramAD
7. 📢 GoogleFCM
8. 🎯 GoogleCN
9. ~~SteamCN~~ **commented out** — Steam downloads must stay on 🎮 游戏平台 (proxy), not DIRECT
10. Ⓜ️ Bing / OneDrive / Microsoft
11. 🍏 `apple_proxy.list` (local) — **before** any `apple.com` / `icloud.com` rule
12. 🍎 `apple.list` (local) → ACL4SSR Apple
13. 📲 `telegram.list` (local) → ACL4SSR Telegram
14. 💬 `discord.list` (local)
15. 🤖 `ai.list` (local)
16. 🛠️ `github.list` (local)
17. 🎶 NetEaseMusic
18. 🎮 inline Epic / EA launcher `PROCESS-NAME` → Epic / Origin / Sony / `steam.list` / `riot.list` / Nintendo
19. 📹 `youtube.list` (local) → ACL4SSR YouTube
20. 🎥 `Netflix.list` (local)
21. 🎵 `spotify.list` (local)
22. 📱 `tiktok.list` (local) — before ChinaMedia / ChinaDomain so `snssdk.com` is not DIRECT
23. 📺 Bahamut / BilibiliHMT / Bilibili
24. 🌏 ChinaMedia
25. 🌍 ProxyMedia
26. 🚀 ProxyGFWlist
27. 🎯 ChinaIp (enabled)
28. 🎯 ACL4SSR `ChinaDomain.list` (upstream URL, not a repo file)
29. 🎯 ChinaCompanyIp / Download
30. 🎯 `[]GEOIP,LAN,no-resolve` (no DNS lookup; LocalAreaNetwork already covers private hosts)
31. 🎯 `[]GEOIP,CN`
32. 🐟 `[]FINAL`

ACL4SSR `ProxyMedia` also lists `tv.apple.com`, but ACL4SSR `Apple.list` (DIRECT) loads first and matches `apple.com`, so without `apple_proxy.list` Apple TV+ / News / TestFlight would all go DIRECT.

Local lists sit above ACL4SSR `ProxyMedia` / `ProxyGFWlist`, so a domain listed here wins over the generic media/GFW sets. `trading.list` also sits above `BanAD`: otherwise Binance / OKX Android init (AppsFlyer tenant, vendor push) is REJECT and the app never wakes those services.

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
| 📱 TikTok | 🫡 自建节点 |
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
| 🍏 苹果代理 | 🚀 节点选择 (🇺🇲 美国节点 offered 2nd for TV+) |
| 🎯 全球直连 | DIRECT |
| 🛑 广告拦截 / 🍃 应用净化 | REJECT |

Function groups use short menus (自建 / 节点选择 / 手动切换 / DIRECT) instead of repeating every region group.

Helper groups:

- 🎥 奈飞节点 — `select` `.*` (same as 手动切换: every available node)
- 💸 交易节点 — `select` `.*` (manual pick; 📈 交易相关 defaults here)
- 🔀 双入口LB — `load-balance` on `腾讯云内网`. Round-robin is requested via `!!strategy=round-robin`, which only the asdlokj1qpi233 subconverter fork honors; tindy2013 ignores it (no-match filter) and emits the default consistent-hashing. A 4th `,round-robin` field after the times is **silently dropped** by both, so do not use it
- 🔮 负载均衡 — full-set `load-balance`, **consistent-hashing** (same destination sticks)

## Node naming requirement

`🔀 双入口LB` / `🫡 自建节点` only match node names containing `腾讯云内网`. subconverter fills a group that matches nothing with `DIRECT`, so with a subscription lacking such nodes, every group defaulting to 🫡 自建节点 (AI Suite, YouTube, GitHub, Spotify, TikTok, 国外媒体) **silently goes DIRECT**. Same for empty region url-test groups. Pick 🚀 节点选择 in those groups, or rename nodes.

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
- ByteDance CN suffixes (`bytedance.com`, `pstatp.com`, `byteimg.com`, `douyin.com`) into `tiktok.list`

## Rule format

- `DOMAIN` — exact host
- `DOMAIN-SUFFIX` — host and all subdomains
- `DOMAIN-KEYWORD` — substring match (easy to over-capture)
- `IP-CIDR` / `IP-CIDR6` — always append `,no-resolve`
- `PROCESS-NAME` — process file name or Android package name (not DNS); matched case-insensitively. See the platform notes below.
- Only the types above are allowed (enforced by `scripts/check_rules.py`). In particular:
  - **No `PROCESS-NAME-WILDCARD`**: Mihomo only added it in v1.19.19; older cores (OpenClash pinned cores, old CMFA / Verge) reject the **whole profile**. It also adds nothing on Android, where the package is resolved from the app UID (`:push` / `:remote` subprocesses are already covered).
  - No `PROCESS-PATH*` / `GEOSITE` / `IP-ASN`: tindy2013 subconverter drops them.
  - No `AND` / `OR` / `NOT` in lists or `[]` inline rules: subconverter keeps only 3 comma fields and mangles them into an invalid rule that breaks the profile.

## Platform notes (Android / Windows / macOS / iOS)

| Platform | `PROCESS-NAME` value | Notes |
|----------|----------------------|-------|
| Android (CMFA / FlClash) | package name, e.g. `com.okinc.okex.gp` | Resolved from the app UID, so all subprocesses match. Cloned apps / work profiles run as another Android user and may bypass the VPN |
| Windows (Clash Verge Rev / Mihomo Party) | `App.exe` | Needs TUN or service mode for apps that ignore the system proxy (Riot, Steam, Discord voice / UDP). Store PWAs (TikTok) and UWP hosts (Netflix `WWAHost.exe`) cannot be matched |
| macOS (Verge / Mihomo Party / ClashX Meta) | binary in `App.app/Contents/MacOS/` | Electron apps talk through `App Helper` / `App Helper (Renderer)`, so lists pin those exact names too |
| iOS (Stash / Shadowrocket / Surge / Clash Mi) | — | Process rules are ignored; only domain / IP rules apply. OKX / Binance / TikTok raw-CN-IP flows fall to `GEOIP,CN` DIRECT there |

Client checklist:

- Keep Mihomo `find-process-mode` at `strict` (default) or `always`; `off` silently disables every `PROCESS-NAME` rule.
- Android: set Private DNS to **Off** (strict DoT on port 853 bypasses Mihomo DNS hijack, so domain rules miss and CN IPs hit `GEOIP,CN`). Enable the sniffer (TLS / HTTP / QUIC) to recover hostnames from HTTPDNS apps.
- `target=singbox` is **not supported**: subconverter merges each list into one sing-box rule where `process_name` is AND-ed with the domain fields, so domain rules only match inside that process.
- Surge / Loon get remote `RULE-SET` URLs and parse the lists themselves; unsupported lines may invalidate a whole ruleset on some versions, hence the strict type allowlist.

## `scripts/check_rules.py`

Python 3, no extra deps. From the repo root:

```bash
python3 scripts/check_rules.py
```

It scans every `*.list` in the repo root for case-insensitive duplicate rules, rule types outside the portable allowlist, `IP-CIDR`/`IP-CIDR6` missing `,no-resolve` or with an invalid / wrong-family network, a dangerous `DOMAIN-SUFFIX` blacklist, and wildcards in `PROCESS-NAME`. It also checks `main.ini` (every `ruleset=` / `[]` reference names a defined group, no `[]AND/OR/NOT`, local ruleset URLs exist and every local list is loaded, no ignored 4th field after `interval,timeout,tolerance`) and that `README.md` mentions each list plus `main.ini`. Exit code `1` on findings, `0` when clean.
