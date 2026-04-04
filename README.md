# Private Clash Rules

个人 Clash/Surge 分流规则集合，配合 ACL4SSR 主配置使用。

## 规则文件

| 文件 | 对应策略组 | 说明 |
|------|-----------|------|
| `trading.list` | 📈 交易相关 | 加密货币交易所及相关服务 |
| `ai_suite.list` | 🤖 AI Suite | 各类 AI 服务（OpenAI、Anthropic、Gemini、Cursor 等） |
| `Netflix.list` | 🎥 奈飞视频 | Netflix 流媒体服务 |
| `steam.list` | 🎮 游戏平台 | Steam 游戏平台 |
| `selfbuilt.list` | 🫡 自建节点 | 走自建节点的特定域名 |
| `ChinaDomain.list` | 🎯 全球直连 | 中国域名直连规则 |
| `ACL4SSR_Online_Full_MultiMode.ini` | - | 主配置，定义规则加载顺序和策略组 |

---

## 规则覆盖机制（重要）

### 加载顺序即优先级

`ACL4SSR_Online_Full_MultiMode.ini` 中的 `ruleset=` 按顺序加载，**先加载的规则优先匹配（first-match-wins）**。

当前加载顺序（简化）：

```
1.  🎯 全球直连   ← LocalAreaNetwork, UnBan
2.  🛑 广告拦截   ← BanAD
3.  🫡 自建节点   ← selfbuilt.list          [本仓库]
4.  📈 交易相关   ← trading.list             [本仓库]
5.  🍃 应用净化   ← BanProgramAD
6.  📢 谷歌FCM   ← GoogleFCM
7.  🎯 全球直连   ← GoogleCN
8.  Ⓜ️ 微软系列  ← Bing / OneDrive / Microsoft
9.  🍎 苹果服务   ← Apple
10. 📲 电报消息   ← Telegram
11. 🤖 AI Suite  ← ai_suite.list            [本仓库]  ← 关键覆盖点
12. 🎶 网易音乐   ← NetEaseMusic
13. 🎮 游戏平台   ← Epic / Origin / Sony / steam.list / Nintendo
14. 📹 油管视频   ← YouTube
15. 🎥 奈飞视频   ← Netflix.list             [本仓库]
16. 📺 哔哩哔哩   ← BilibiliHMT / Bilibili
17. 🌏 国内媒体   ← ChinaMedia
18. 🌍 国外媒体   ← ProxyMedia.list          [外部 ACL4SSR]
19. 🚀 节点选择   ← ProxyGFWlist.list        [外部 ACL4SSR]
20. 🎯 全球直连   ← ChinaIp / ChinaDomain.list / ChinaCompanyIp / Download
21. 🐟 漏网之鱼   ← FINAL
```

### 外部规则与本地覆盖

外部 ACL4SSR 规则（第 18、19 项）包含大量通用规则，其中部分与本仓库管理的服务有重叠。由于本仓库的规则加载在前，**相同域名/关键字会被本仓库规则优先命中，外部规则中的重复条目不生效**。

#### 已知覆盖项

| 服务 | 外部规则中的条目 | 本仓库覆盖位置 | 覆盖原因 |
|------|----------------|--------------|---------|
| Anthropic/Claude | `DOMAIN-KEYWORD,anthropic`（ProxyMedia → 国外媒体） | `ai_suite.list` | 归入 AI Suite，而非国外媒体 |
| Anthropic/Claude | `DOMAIN-KEYWORD,claude`（ProxyMedia → 国外媒体） | `ai_suite.list` | 同上 |
| Anthropic/Claude | `DOMAIN-SUFFIX,claude.ai/claude.com/claudeusercontent.com`（ProxyMedia + ProxyGFWlist） | `ai_suite.list` | 同上 |
| Cursor | `DOMAIN-SUFFIX,cursor.sh/cursor.com`（ProxyMedia → 国外媒体） | `ai_suite.list` | 归入 AI Suite |
| OpenAI | `DOMAIN-KEYWORD,openai`（ProxyMedia → 国外媒体） | `ai_suite.list` | 归入 AI Suite |

> **维护提示**：如果某个 AI 或交易服务被发现路由到了国外媒体/节点选择，原因通常是外部规则包含了该域名/关键字，而本仓库还没有对应的覆盖条目。解决方法：在 `ai_suite.list` 或 `trading.list` 中加入对应规则即可（加载顺序已保证优先命中）。

---

## ai_suite.list 覆盖范围

| 服务商 | 覆盖内容 |
|-------|---------|
| OpenAI | openai.com, chatgpt.com, sora.com, oaistatic.com, oaiusercontent.com + `DOMAIN-KEYWORD,openai` |
| Anthropic | anthropic.com, claude.ai, claude.com, claudeusercontent.com + `DOMAIN-KEYWORD,anthropic` + `DOMAIN-KEYWORD,claude` |
| Grok | x.ai, grok.com |
| Gemini | gemini.google.com, bard.google.com, deepmind.com, generativeai.google, aistudio.google.com 等 |
| Cursor | cursor.sh, cursor.com |
| Poe | poe.com |
| 公共依赖 | stripe.com, auth0.com, hcaptcha.com, recaptcha.net, sentry.io, intercom.io 等 |
| Google Antigravity (Claude Code) | googleapis.com, googleusercontent.com, run.app, open-vsx.org 等 |

---

## trading.list 覆盖范围

### 中心化交易所 (CEX)
- **Binance**：主域名、API、CDN、yingwangtech 系列、IP-CIDR（7条）
- **Bybit**：主域名 + bycsi/bytick/byapis 等相关域名
- **OKX / MEXC / Coinbase / Kraken / Gate.io / HTX / Bitfinex / KuCoin / Bitget** 等

### 去中心化交易所 (DEX / PERP DEX)
- Uniswap, Pendle, Hyperliquid, dYdX, GMX
- Variational, Lighter, AsterDex, EdgeX, GRVT, Paradex, Ostium 等

### 行情 & 数据分析
- TradingView, Coinglass, CoinGecko, CoinMarketCap
- Glassnode, DefiLlama, DexTools, CryptoQuant
- **RootData**（Web3 项目数据）等

### 区块链基础设施
- Etherscan, BscScan, BaseScan, Solscan
- WalletConnect, Phantom, Ankr

---

## 规则格式参考

- `DOMAIN` — 精确域名匹配
- `DOMAIN-SUFFIX` — 域名后缀匹配（含所有子域名）
- `DOMAIN-KEYWORD` — 域名关键字匹配（最宽泛，注意误杀风险）
- `IP-CIDR` — IP 地址段匹配
- `PROCESS-NAME` — 进程名匹配（仅桌面端）
