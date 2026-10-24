# Web3 入门手册

> 从核心原理出发，一步步走进区块链与 Web3 的世界。**八章，一章一个「为什么」。**

区块链资料浩如烟海，却散乱、碎片化，对第一次接触的人极不友好。这份手册尝试给出一条**按原理组织**的路径：先讲清「为什么需要区块链」和必要的前置知识，再落到具体的链，最后扩展到智能合约、DApp 与整个 Web3 生态。

[![CI](https://github.com/yuyu2929/web3-primer/actions/workflows/ci.yml/badge.svg)](https://github.com/yuyu2929/web3-primer/actions/workflows/ci.yml)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE)
[![docs](https://img.shields.io/badge/docs-8%20chapters%20%2B%20glossary-6c8cff)](docs/)
[![lang](https://img.shields.io/badge/lang-中文-9d6cff)](#)

## 三十秒速览

如果只想知道这份手册讲什么：

| 章 | 一句话 |
| --- | --- |
| [01](docs/01-why-blockchain.md) | 区块链不是为了「更快」，而是为了在**互不信任**时也能对同一本账达成一致 |
| [02](docs/02-cryptography-basics.md) | 哈希负责防篡改，签名负责所有权——**私钥即资产** |
| [03](docs/03-consensus.md) | PoW 用算力、PoS 用质押，共同点是**让作恶比诚实更贵** |
| [04](docs/04-bitcoin.md) | UTXO + PoW + 减半，一条只做转账的链如何做到极致可靠 |
| [05](docs/05-ethereum.md) | 账户模型 + EVM，把账本变成一台**可编程的状态机** |
| [06](docs/06-smart-contracts.md) | 合约是自动售货机；DApp = 前端 + 合约，后端是链而非服务器 |
| [07](docs/07-web3-stack.md) | 钱包、存储、索引、跨链、DAO——一个 DApp 的全景零件表 |
| [08](docs/08-risks-future.md) | 扩容、安全、监管、体验：热潮之下的真实难题 |

## 为什么有这份手册

大多数教程的问题是「只见树不见林」：要么直接教你怎么发一笔交易，却不说交易为什么可信；要么堆砌名词，把「哈希」「共识」「Gas」当作已知概念。本手册坚持三个原则：

1. **原理优先**——先回答「为什么」，再回答「是什么」，最后才是「怎么用」。
2. **链在后，原理在前**——前三章不出现任何具体链，先建立能检验任何链的心智模型。
3. **可独立阅读**——每章自成一体，也按顺序构成完整路径，术语表随时可查。

## 阅读路径

| 章节 | 主题 | 解决的问题 |
| --- | --- | --- |
| [01 为什么需要区块链](docs/01-why-blockchain.md) | 信任、双花、分布式账本 | 区块链解决的是什么问题？ |
| [02 密码学前置知识](docs/02-cryptography-basics.md) | 哈希、数字签名、地址、助记词 | 链上「所有权」与「不可篡改」靠什么保证？ |
| [03 共识机制](docs/03-consensus.md) | PoW、PoS、分叉、最终性 | 没有中心机构，大家如何达成一致？ |
| [04 比特币](docs/04-bitcoin.md) | UTXO、挖矿、发行曲线 | 第一条真正落地的链如何运转？ |
| [05 以太坊](docs/05-ethereum.md) | 账户模型、Gas、代币标准 | 可编程的链与比特币有何不同？ |
| [06 智能合约与 DApp](docs/06-smart-contracts.md) | Solidity、DeFi、预言机 | 「链上程序」如何改变应用形态？ |
| [07 Web3 技术栈与身份](docs/07-web3-stack.md) | 钱包、存储、索引、跨链 | Web3 应用由哪些模块组成？ |
| [08 风险、局限与展望](docs/08-risks-future.md) | 扩容、安全、监管 | 热潮之下，真实世界还有哪些问题？ |
| [术语表](docs/glossary.md) | 中英对照 | 忘了某个词？来这里查。 |

建议顺序读一遍（约 2 小时），之后把它当查询手册用。

## 开始阅读

```bash
git clone https://github.com/yuyu2929/web3-primer.git
cd web3-primer

open docs/01-why-blockchain.md      # macOS
xdg-open docs/01-why-blockchain.md  # Linux
start docs\01-why-blockchain.md     # Windows
```

不需要任何工具链：纯 Markdown，用任何编辑器、浏览器或 GitHub 网页都能读。

## 适合谁

- 刚接触区块链、想建立系统认知的**开发者**
- 需要给团队或学生讲区块链基础的**讲师**
- 想动手做 Web3 项目、但缺一块「原理拼图」的**学习者**

阅读前不需要区块链知识；有编程经验会更顺畅（尤其第 6 章）。

## 目录结构

```text
web3-primer/
├── README.md          # 本文件：总览、速览与导航
├── LICENSE            # CC BY-NC-SA 4.0
├── CONTRIBUTING.md    # 纠错与投稿约定
├── COMMERCIAL.md      # 商业使用授权
├── docs/              # 手册正文
│   ├── 01-why-blockchain.md
│   ├── 02-cryptography-basics.md
│   ├── 03-consensus.md
│   ├── 04-bitcoin.md
│   ├── 05-ethereum.md
│   ├── 06-smart-contracts.md
│   ├── 07-web3-stack.md
│   ├── 08-risks-future.md
│   └── glossary.md
├── scripts/check_docs.py  # 链接/锚点/结构检查（CI 用）
├── LOG.md             # 写作过程记录
└── IDEAS.md           # 设计思路与取舍
```

## 本地校验

仓库自带一个零依赖的文档检查器，CI 跑的就是它：

```bash
python3 scripts/check_docs.py             # 相对链接、锚点、结构、占位符
python3 scripts/check_docs.py --external  # 额外检查外链（需要网络）
```

## 如何参与

欢迎纠错、补充、翻译。具体约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。

核心要求只有两条：**内容原创**，**引用必须注明出处**。

## 许可

本手册采用 [CC BY-NC-SA 4.0](LICENSE)：

- **个人学习、教学、非商业转载**：自由使用，保留署名并以相同方式共享即可；
- **商业用途**（付费课程、企业内部培训产品、客户交付物、出版）需要授权，
  见 [COMMERCIAL.md](COMMERCIAL.md)。

---

*本手册按「原理 → 链 → 生态」的顺序写作，力求每个结论都有推导过程，而不是结论先行。*
