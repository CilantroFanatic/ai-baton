# ai-baton

[English](README.md)

便携、可审计、文件优先的 AI 助手交接协议。

在 Claude Code、Codex CLI、Cursor、GitHub Copilot,或者任何能读写文件的工具之间切换,同一个长期项目不用每次从头讲一遍。所有东西都存在你项目文件夹里的普通文本文件里——不需要服务器、不需要向量数据库、不用绑定哪一家的产品。

## 什么时候用得上

- **手头这个工具额度用完了,想换一个接着用。** 比如 Cursor 额度不够了,想临时切到 Codex 或者别的工具接着写——没有这东西的话,就得把这个项目从头到尾重新跟新工具唠一遍:技术选型、踩过的坑,全部重讲一次。
- **聊得太久了,想开新对话又怕丢东西。** 要么是想省 token,要么是上下文太长 AI 开始变笨,想开个新的接着聊——但又不想因为开了新对话,就把之前已经定下来的东西全忘光,还得重新解释一遍。
- **同一个项目,不同部分想交给不同工具做。** 比如后端用 Claude Code、前端用 Cursor,或者一个负责写代码、一个负责改文档——接口怎么定的、命名规范是什么,双方都得知道,不然各写各的,对不上。

## 怎么运作

- `PROTOCOL.md` —— 这个项目该遵守的规则
- `memory/` —— 沉淀下来的事实和决定,一个文件一条,标注 `confidence: verified` 或 `unverified`
- `status/CURRENT_STATUS.md` —— 现在在做什么(每次覆盖写,不是追加)
- `evidence/` —— 值得留存的原始细节,只追加
- `handover/` / `archive/` —— 交接快照 / 被取代的旧方案——不会删除任何东西

装一次 [Agent Skills](https://agentskills.io/) skill(`ai-baton skill install`),支持的 AI 工具就会自动照做:按正确顺序读文件、写之前先问、及时更新状态——不用每次提醒。

需要本地文件系统访问权限——适用于跑在你电脑上、或者被授权访问某个文件夹的工具(Claude Code、Codex CLI、Cursor、Windsurf、装了文件系统连接器的 Claude Desktop 等)。纯网页版 ChatGPT 或网页版 Claude.ai 聊天界面,没有文件访问权限,读不到 `PROTOCOL.md`,不管支不支持 Agent Skills 都没用。

## 现状

Pre-alpha。

**已经跑通的:**
- 协议规范(`SPEC.md`)和 CLI —— `pip install ai-baton-tool`(PyPI 上的发行包名跟 `ai-baton` 命令不一样,名字被一个不相关的已有包占了,但命令本身还是 `ai-baton`):`init` / `validate` / `status` / `list` / `workspace set` / `skill install`
- 一套默认工作区约定 —— `~/ai-baton-workspace/<项目名>/`,根目录只在第一次用的时候问一次、记住,换工具/换会话时靠 `ai-baton list` 就能发现已有项目
- 一个完整的示例项目(`examples/demo-project/`)
- `validate` 会检测常见凭证格式(启发式安全网,不是完整的密钥扫描工具),`memory/` 变大到会明显增加每次会话的 token 开销时也会警告(阈值可以按项目通过 `.ai-baton.json` 自定义)
- 路径不对时给出人话错误提示,不是 Python 报错栈
- 49 个测试本地全过

**还没做的:** 语义搜索(有意不做,见下面的取舍说明)、任何自动化的交接效果量化(方法论写在 `docs/metrics.md` 里,还没接进代码)。

不是第一个想做跨工具 AI 记忆的系统——Mem0、OpenMemory、Letta 解决的是类似的问题,靠的是向量库和/或 agent 运行时。这个项目走的是相反的取舍:零基础设施、Git 原生可审计,代价是没有语义搜索和自动抽取。详见 [`docs/comparison.md`](docs/comparison.md)。

## 快速上手

- [`docs/quickstart.md`](docs/quickstart.md) —— 安装和试用(英文)。
- [`SPEC.md`](SPEC.md) —— 协议本身(英文)。
- [`docs/comparison.md`](docs/comparison.md) —— 跟 Mem0 / OpenMemory / Letta / Letta Code 的对比(英文)。
- [`docs/metrics.md`](docs/metrics.md) —— 打算怎么衡量交接效果(英文)。
- [`examples/demo-project/`](examples/demo-project/) —— 完整示例。
- [`.agents/skills/ai-baton/SKILL.md`](.agents/skills/ai-baton/SKILL.md) —— 装一次,AI 工具就会自动遵守协议,不用每次提醒。

## License

MIT —— 见 [`LICENSE`](LICENSE)。
