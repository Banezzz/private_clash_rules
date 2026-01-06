# Private Clash Rules

个人 Clash/Surge 分流规则集合，用于网络代理分流。

## 规则文件

| 文件 | 说明 | 更新时间 |
|------|------|----------|
| `trading.list` | 加密货币交易所及相关服务 | 2025.01.27 |
| `openai.list` | OpenAI/ChatGPT 相关服务 | - |
| `Netflix.list` | Netflix 流媒体服务 | - |
| `steam.list` | Steam 游戏平台 | - |
| `ChinaDomain.list` | 中国域名直连规则 | - |

## trading.list 详细说明

包含主流加密货币交易所和相关工具的分流规则：

### 中心化交易所 (CEX)
- Binance (币安) - 包含完整域名、API、CDN、IP-CIDR 规则
- Bybit
- OKX
- MEXC
- Coinbase、Kraken、Gate.io、HTX、Bitfinex、KuCoin 等

### 去中心化交易所 (DEX)
- Uniswap、PancakeSwap、Raydium
- Pendle、Hyperliquid、dYdX 等

### 行情分析工具
- TradingView、Coinglass、CoinGecko、CoinMarketCap
- Glassnode、DefiLlama、DexTools 等

### 区块链浏览器
- Etherscan、BscScan、BaseScan、Solscan

### 钱包
- Phantom、TokenPocket、imToken、MetaMask 等

## 使用方法

### Clash
```yaml
rule-providers:
  trading:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/your-repo/trading.list"
    path: ./ruleset/trading.list
    interval: 86400

rules:
  - RULE-SET,trading,Proxy
```

### Surge
```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/your-repo/trading.list,Proxy
```

## 规则格式

- `DOMAIN` - 精确域名匹配
- `DOMAIN-SUFFIX` - 域名后缀匹配
- `DOMAIN-KEYWORD` - 域名关键字匹配
- `IP-CIDR` - IP 地址段匹配

## 更新日志

### 2025.01.27
- 更新 Binance 分流规则，新增：
  - 主域名：fapibak、dstream、fstream、nbstream、sfstream 等 stream 节点
  - 账户域名：accounts.binance.info、accounts.binance.me
  - API 端点：api.saasexch.cc/co/io/com
  - 相关域名：forter、amazontrust、cloudfront、myqcloud、AWS ELB
  - 域名后缀：binancezh.* 系列、bnbzh.ac、yingwangtech.* 系列
  - IP-CIDR：7 个 Binance 服务器 IP 段
