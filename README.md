# Private Clash Rules

Personal Clash / Surge rule lists used with a customized ACL4SSR `main.ini` (subconverter). Rules are **first-match-wins**: earlier `ruleset=` lines take priority.

Raw prefix: `https://raw.githubusercontent.com/Banezzz/private_clash_rules/main/`

## Files

| File | Policy group | Notes |
|------|----------------|-------|
| `main.ini` | — | Subconverter config: ruleset order + strategy groups |
| `apple-proxy.list` | 🍏 苹果代理 | TV+, News, Private Cloud Compute, TestFlight. Default is 🚀 节点选择. Loaded before Microsoft so Akamai names are not stolen |
| `apple-media.list` | 🍎 苹果媒体 | Apple Music and Podcasts only. Default stays DIRECT |
| `apple.list` | 🍎 苹果服务 | Local replacement for ACL4SSR `Apple.list`. System, iCloud, App Store, Shazam. Drops `akadns.net`, `crashlytics.com`, and the glued `apple.comscoreresearch.com` token |
| `android.list` | 🤖 Android 服务 | Play Store package and Play API hosts only. Not Play Services, not `android.com` |
| `telegram.list` | 📲 电报消息 | Process names and official CIDRs missing from ACL4SSR Telegram |
| `youtube.list` | 📹 油管视频 | Android YouTube package names, loaded before the upstream YouTube list |
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
3. 📈 `trading.list`, 📱 `tiktok.list`, 🤖 `android.list` — **before BanAD**
4. 🛑 BanAD
5. 🫡 `selfbuilt.list` (local overlay)
6. 🍃 BanProgramAD
7. 📢 GoogleFCM
8. 🎯 GoogleCN
9. ~~SteamCN~~ **commented out** — Steam downloads must stay on 🎮 游戏平台 (proxy), not DIRECT
10. 🍏 `apple-proxy.list` then upstream `AppleTV.list`, 🍎 `apple-media.list`, 🍎 `apple.list`, 🎥 `Netflix.list` then upstream `Netflix.list`, 🎵 `spotify.list` then upstream `Spotify.list` — **before Microsoft**, because `Microsoft.list` claims all of `akadns.net` and `edgesuite.net`
11. Ⓜ️ Bing / OneDrive / Microsoft
12. 📲 `telegram.list` then upstream Telegram
13. 💬 `discord.list` (local)
14. 🤖 `ai.list` (local)
15. 🛠️ `github.list` (local)
16. 🎶 NetEaseMusic
17. 🎮 Epic / EA launcher processes, then Epic / Origin / Sony / `steam.list` / `riot.list` / Nintendo
18. 📹 `youtube.list` then upstream YouTube
19. 📺 Bahamut / BilibiliHMT / Bilibili
20. 🌏 ChinaMedia
21. 🌍 ProxyMedia
22. 🚀 ProxyGFWlist
23. 🎯 ChinaIp (enabled)
24. 🎯 ACL4SSR `ChinaDomain.list` (upstream URL, not a repo file)
25. 🎯 ChinaCompanyIp / Download
26. 🎯 `[]GEOIP,LAN,no-resolve`
27. 🎯 `[]GEOIP,CN`
28. 🐟 `[]FINAL`

Local lists sit above ACL4SSR `ProxyMedia` / `ProxyGFWlist`, so a domain listed here wins over the generic media/GFW sets. `trading.list` and `tiktok.list` also sit above `BanAD`: otherwise Android init (AppsFlyer tenant, vendor push) is REJECT and the app never wakes those services. `tiktok.list` is also above ChinaDomain, so `snssdk.com` is not DIRECT. That suffix is shared with Douyin, so Douyin hosts on it follow 📱 TikTok.

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
| 🤖 Android 服务 | 🚀 节点选择 |
| 🍏 苹果代理 | 🚀 节点选择 |
| 🍎 苹果媒体 | DIRECT |
| 🍎 苹果服务 | DIRECT |
| 🎯 全球直连 | DIRECT |
| 🛑 广告拦截 / 🍃 应用净化 | REJECT |

Function groups use short menus (自建 / 节点选择 / 手动切换 / DIRECT) instead of repeating every region group.

Helper groups:

- 🎥 奈飞节点 — `select` `.*` (same as 手动切换: every available node)
- 💸 交易节点 — `select` `.*` (manual pick; 📈 交易相关 defaults here)
- 🔀 双入口LB — `load-balance` on `腾讯云内网`. The group uses `!!strategy=round-robin`, which the asdlokj1qpi233 subconverter fork honors. tindy2013 ignores that filter and emits **consistent-hashing**. A trailing `,round-robin` field is dropped by both.
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
- `PROCESS-NAME-WILDCARD` and `PROCESS-*-REGEX` (Mihomo older than v1.19.19 rejects wildcard rules and fails the whole profile)
- `DOMAIN-SUFFIX,android.com` or `PROCESS-NAME,com.google.android.gms` (that is all of Play Services)

## Rule format

- `DOMAIN` — exact host
- `DOMAIN-SUFFIX` — host and all subdomains
- `DOMAIN-KEYWORD` — substring match (easy to over-capture)
- `IP-CIDR` / `IP-CIDR6` — always append `,no-resolve`
- `PROCESS-NAME` — desktop binary or Android package name (not DNS). Mihomo matches the executable basename exactly (case-insensitive). On Mac, Electron helpers are separate names (`Discord Helper`, `Spotify Helper`), so those lines are listed next to the main binary. On Android the name is the package of the app UID, which already covers `:push` subprocesses. TUN / VPN and `find-process-mode` other than `off` are required. iOS cannot match another app's process.

## Clients

One subscription URL with `target=clash` is the shared profile for Android, Mac, and Windows on Mihomo: Clash Meta for Android, FlClash, Clash Verge Rev, ClashX Meta.

Rules stay on `PROCESS-NAME` so a core older than Mihomo v1.19.19 can still load the file. Surge, Stash, Shadowrocket, and sing-box are not targets. iOS only uses the domain and IP rules.

Under fake-ip, `IP-CIDR,...,no-resolve` does not see `17.0.0.0/8` until the connection already uses a real Apple address.

Android must use the VPN/TUN stack. An airport base that sets `find-process-mode: off` disables every `PROCESS-NAME` line. If no node name contains `腾讯云内网`, 🫡 自建节点 falls through to DIRECT.

## Apple on Mac, Windows, Android, and iOS

| Group | Default | What it is for |
|-------|---------|----------------|
| 🍏 苹果代理 | 🚀 节点选择 | TV+, News, Private Cloud Compute, TestFlight. These are checked by exit region and do not work on a mainland direct path |
| 🍎 苹果媒体 | DIRECT | Apple Music and Podcasts. Switch this group alone for another storefront |
| 🍎 苹果服务 | DIRECT | APNs, iCloud, App Store, updates, Shazam, China iCloud (`apzones.com`), Apple IPv6 |

Mac Music / TV process names are not listed. Windows uses `AppleMusic.exe` / `AppleTV.exe` / iCloud executables. Android uses the Play packages for Music, TV, and Shazam. iOS is domain and IP only. Private Relay hosts stay on 🍎 苹果服务 so they are not forced through a proxy.

`snssdk.com` in `tiktok.list` is shared with Douyin. It is listed so international TikTok wins over ChinaDomain DIRECT. Douyin / Toutiao hosts on that suffix follow 📱 TikTok (default 🫡 自建节点). Other ByteDance CN suffixes (`douyin.com`, `bytedance.com`, `pstatp.com`, `byteimg.com`) stay out of `tiktok.list`.

## `scripts/check_rules.py`

Python 3, no extra deps. From the repo root:

```bash
python3 scripts/check_rules.py
```

It scans every `*.list` in the repo root for duplicate rules, `IP-CIDR`/`IP-CIDR6` missing `,no-resolve`, a dangerous `DOMAIN-SUFFIX` blacklist, and whether `README.md` mentions each existing list plus `main.ini`. Exit code `1` on findings, `0` when clean.
