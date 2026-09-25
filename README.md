# Private Clash Rules

Personal Clash / Surge rule lists used with a customized ACL4SSR `main.ini` (subconverter). Rules are **first-match-wins**: earlier `ruleset=` lines take priority.

Raw prefix: `https://raw.githubusercontent.com/Banezzz/private_clash_rules/main/`

## Files

| File | Policy group | Notes |
|------|----------------|-------|
| `main.ini` | — | Subconverter config: ruleset order + strategy groups |
| `apple.list` | 🍎 苹果服务 | Local replacement for ACL4SSR `Apple.list`. System, iCloud, App Store, Shazam, Private Cloud Compute. Drops `akadns.net`, `crashlytics.com`, and the glued `apple.comscoreresearch.com` token |
| `apple-media.list` | 🍎 苹果媒体 | Music / TV / Podcasts / News. Loads before `apple.list` so those hosts beat `DOMAIN-SUFFIX,apple.com`. Default stays DIRECT |
| `ai.list` | 🤖 AI Suite | OpenAI, Anthropic, Gemini, Cursor, Meta AI / Llama / Muse, and related international AI hosts (aligned with geosite `category-ai-chat-!cn`, minus CN brands and over-broad SaaS) |
| `trading.list` | 📈 交易相关 | Exchanges and market-data hosts (curated). Android Play Store packages + Binance/OKX mobile-only hosts. Loads before BanAD |
| `Netflix.list` | 🎥 奈飞视频 | Netflix hosts / keywords (no broad AWS CIDR) |
| `steam.list` | 🎮 游戏平台 | Steam and Valve-related hosts |
| `riot.list` | 🎮 游戏平台 | Riot Client plus first-party web (LoL / TFT / Valorant / Wild Rift / 2XKO). Tencent CN LoL omitted |
| `selfbuilt.list` | 🫡 自建节点 | Overlay hook only — see below |
| `discord.list` | 💬 Discord | Discord hosts |
| `github.list` | 🛠️ GitHub | GitHub / git-related hosts |
| `spotify.list` | 🎵 Spotify | Spotify hosts |
| `tiktok.list` | 📱 TikTok | International TikTok + Android packages. `snssdk.com` is shared with Douyin and is included on purpose. Other ByteDance CN suffixes stay out |

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
11. 🍎 `apple-media.list` then `apple.list` (local; upstream `Apple.list` is not used)
12. 📲 Telegram
13. 💬 `discord.list` (local)
14. 🤖 `ai.list` (local)
15. 🛠️ `github.list` (local)
16. 🎶 NetEaseMusic
17. 🎮 Epic / Origin / Sony / `steam.list` / `riot.list` / Nintendo
18. 📹 YouTube
19. 🎥 `Netflix.list` (local)
20. 🎵 `spotify.list` (local)
21. 📱 `tiktok.list` (local) — before ChinaMedia / ChinaDomain so `snssdk.com` is not DIRECT
22. 📺 Bahamut / BilibiliHMT / Bilibili
23. 🌏 ChinaMedia
24. 🌍 ProxyMedia
25. 🚀 ProxyGFWlist
26. 🎯 ChinaIp (enabled)
27. 🎯 ACL4SSR `ChinaDomain.list` (upstream URL, not a repo file)
28. 🎯 ChinaCompanyIp / Download
29. 🎯 `[]GEOIP,LAN`
30. 🎯 `[]GEOIP,CN`
31. 🐟 `[]FINAL`

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
| 🍎 苹果媒体 | DIRECT |
| 🍎 苹果服务 | DIRECT |
| 🎯 全球直连 | DIRECT |
| 🛑 广告拦截 / 🍃 应用净化 | REJECT |

Function groups use short menus (自建 / 节点选择 / 手动切换 / DIRECT) instead of repeating every region group.

Helper groups:

- 🎥 奈飞节点 — `select` `.*` (same as 手动切换: every available node)
- 💸 交易节点 — `select` `.*` (manual pick; 📈 交易相关 defaults here)
- 🔀 双入口LB — `load-balance` on `腾讯云内网`. The INI asks for **round-robin**, but official subconverter's INI parser drops the strategy field and emits **consistent-hashing**. A TOML/YAML `custom_groups` entry with `strategy = "round-robin"` is what actually round-robins.
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
- ByteDance CN suffixes (`bytedance.com`, `pstatp.com`, `byteimg.com`, `douyin.com`) into `tiktok.list`
- `DOMAIN-SUFFIX,akadns.net`, `DOMAIN-SUFFIX,crashlytics.com`, or `DOMAIN-SUFFIX,edgesuite.net` (Akamai / Firebase zones, not Apple)
- Mac `PROCESS-NAME` for generic names (`Music`, `TV`, `App Store`, `Finder`)

## Rule format

- `DOMAIN` — exact host
- `DOMAIN-SUFFIX` — host and all subdomains
- `DOMAIN-KEYWORD` — substring match (easy to over-capture)
- `IP-CIDR` / `IP-CIDR6` — always append `,no-resolve`
- `PROCESS-NAME` — desktop binary or Android package name (not DNS). Mihomo matches the executable basename exactly (case-insensitive). On Mac, Electron helpers are different names (`Discord Helper (Renderer)`, `Spotify Helper`), so a bare `Discord` / `Spotify` line misses them. On Android this matches the package (or `package:push`). TUN / VPN and `find-process-mode` other than `off` are required. iOS cannot match another app's process.
- `PROCESS-NAME-WILDCARD` — Mihomo wildcard (e.g. `com.okinc.okex*`) for Android `:push` / `:remote` subprocesses when exact `PROCESS-NAME` misses. OKX and TikTok Android HTTPDNS then dial a raw CN IP; without a process hit the flow falls through to `GEOIP,CN` DIRECT.
- `PROCESS-PATH-REGEX` — Mihomo-only. Used for Mac `.app` bundles so every helper inside the bundle hits the same group. Surge, Stash, Shadowrocket, and Clash Premium do not accept this rule type.

## Clients

One subscription URL with `target=clash` is the shared profile for Android, Mac, and Windows **when the GUI is Mihomo**: Clash Meta for Android, FlClash, Clash Verge Rev, ClashX Meta.

It is not a Surge, Stash, Shadowrocket, sing-box, or Clash Premium config. `PROCESS-NAME-WILDCARD` and `PROCESS-PATH-REGEX` are Mihomo rule types. Importing the generated file into Surge iOS, Stash, or Shadowrocket can fail on those lines before any Apple rule is applied.

iOS Apple coverage is the domain and `IP-CIDR` lines in `apple.list` / `apple-media.list`, not process rules. Under fake-ip, `IP-CIDR,...,no-resolve` does not see `17.0.0.0/8` until the connection already uses a real Apple address, so a missing Apple hostname will not be saved by the `/8`.

Android must use the VPN/TUN stack. A system-proxy-only mode does not supply package names, and an airport base that sets `find-process-mode: off` disables every `PROCESS-NAME` line.

## Apple on Mac, Windows, Android, and iOS

| Platform | What this repo covers | What it does not |
|----------|----------------------|------------------|
| Mac | `apple.com` / `icloud.com` / `mzstatic.com` / `cdn-apple.com`, China iCloud `apzones.com`, Live Photos, Safari `.apple` hosts, Private Cloud Compute relays, Apple IPv6 ranges | Process match for Music / TV / App Store (those names are too generic). Domain rules cover the apps |
| Windows | Same domains, plus `AppleMusic.exe`, `AppleTV.exe`, iCloud executables, `APSDaemon.exe`, `AppleDevices.exe` | iTunes device sync stays on 🍎 苹果服务 (`iTunes.exe` is not in the media list) |
| Android | Same domains, plus `com.apple.android.music`, `com.apple.atve.androidtv.appletv`, `com.shazam.android`. Crashlytics is no longer pulled into the Apple group | No other Apple apps ship on Play |
| iOS | Same domains and Apple IPv4/IPv6 ranges. APNs, updates, captive portal, and iCloud stay DIRECT with the services group | `PROCESS-NAME` cannot see other apps. Private Relay still conflicts with a full-tunnel VPN at the OS layer; that is not a ruleset fix |

🍎 苹果媒体 and 🍎 苹果服务 both default to DIRECT, so current traffic does not move. Point only 苹果媒体 at a node when Apple Music or TV+ should follow a chosen region. Leaving 苹果服务 on DIRECT keeps push, software update, and iCloud off the proxy.

`snssdk.com` in `tiktok.list` is shared with Douyin. It is listed so international TikTok wins over ChinaDomain DIRECT. Douyin / Toutiao hosts on that suffix follow 📱 TikTok (default 🫡 自建节点). Other ByteDance CN suffixes (`douyin.com`, `bytedance.com`, `pstatp.com`, `byteimg.com`) stay out of `tiktok.list`.

## `scripts/check_rules.py`

Python 3, no extra deps. From the repo root:

```bash
python3 scripts/check_rules.py
```

It scans every `*.list` in the repo root for duplicate rules, `IP-CIDR`/`IP-CIDR6` missing `,no-resolve`, a dangerous `DOMAIN-SUFFIX` blacklist, and whether `README.md` mentions each existing list plus `main.ini`. Exit code `1` on findings, `0` when clean.
