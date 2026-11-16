# MCP 注册表简介 | 模型上下文协议（MCP）博客

> 来源: https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/

今天，我们正式推出模型上下文协议（Model Context Protocol，MCP）注册表——这是一个面向公开可用 MCP 服务器的开放目录与 API，旨在提升可发现性和使用便利性。通过标准化服务器的分发与发现方式，我们扩大了它们的覆盖面，同时让客户端更容易连接。

MCP 注册表现已开放预览。开始使用：

- 按照《向 MCP 注册表添加服务器》指南添加你的服务器（面向服务器维护者）
- 按照《访问 MCP 注册表数据》指南访问服务器数据（面向客户端维护者）

# MCP 服务器的单一事实来源

2025 年 3 月，我们曾表示希望为 MCP 生态构建一个中央注册表。今天，我们宣布已推出 [https://registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) 作为官方 MCP 注册表。作为 MCP 项目的一部分，MCP 注册表及其上层 [OpenAPI 规格说明](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/api/official-registry-api.md)均为开源，允许任何人构建兼容的子注册表。

我们的目标是标准化服务器的分发与发现方式，提供一个可供子注册表依托的主要事实来源。这反过来将扩大服务器的覆盖面，并帮助客户端在整个 MCP 生态中更轻松地找到服务器。

## 公共与私有子注册表

在构建中央注册表时，我们很重视不削弱社区和公司已有的注册表。MCP 注册表充当公开可用 MCP 服务器的主要事实来源，各组织可以选择基于自定义标准[创建子注册表](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/registry-aggregators.mdx)。例如：

**公共子注册表**，例如与每个 MCP 客户端相关联、带有鲜明倾向性的「MCP 市场」，可以自由地扩充和增强它们从上游 MCP 注册表摄取的数据。每一类 MCP 终端用户画像都有不同需求，如何以有倾向性的方式妥善服务其终端用户，取决于 MCP 客户端市场。

**私有子注册表**将存在于对隐私和安全有严格要求的企业内部，但 MCP 注册表为这些企业提供了一个可依托的单一上游数据源。至少，我们计划与这些私有实现共享 API 模式（schema），以便相关的 SDK 和工具能够在整个生态中共享。

在这两种情况下，MCP 注册表都是起点——它是 MCP 服务器维护者发布和维护其自报信息的集中位置，供这些下游消费者加工后交付给各自的终端用户。

## 社区驱动的内容治理机制

MCP 注册表是由注册表工作组维护的官方 MCP 项目，采用宽松许可。社区成员可以提交 issue，标记违反 MCP[内容治理指南](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/moderation-policy.mdx)的服务器——例如包含垃圾内容、恶意代码或冒充合法服务的服务器。随后，注册表维护者可以将这些条目列入拒绝名单，并追溯性地将其从公开访问中移除。

# 开始使用

开始使用：

- 按照《向 MCP 注册表添加服务器》指南添加你的服务器（面向服务器维护者）
- 按照《访问 MCP 注册表数据》指南访问服务器数据（面向客户端维护者）

MCP 注册表的这一预览版旨在帮助我们在正式发布前改进用户体验，不提供数据持久性保证或其他保证。我们建议 MCP 采用者密切关注开发进展，因为在注册表正式发布之前可能会出现破坏性变更。

在我们持续开发注册表的同时，欢迎大家在 [modelcontextprotocol/registry GitHub 仓库](https://github.com/modelcontextprotocol/registry)中提供反馈和贡献：讨论（Discussion）、议题（Issues）和拉取请求（PR）都欢迎。

# 感谢 MCP 社区

MCP 注册表从一开始就是一项协作成果，我们由衷感谢更广泛开发者社区的热情与支持。

2025 年 2 月，它最初是一个草根项目：MCP 的创造者 [David Soria Parra](https://github.com/dsp-ant) 和 [Justin Spahr-Summers](https://github.com/jspahrsummers) 邀请 [PulseMCP](https://www.pulsemcp.com/) 和 [Goose](https://block.github.io/goose/) 团队协助构建一个中央社区注册表。来自 [PulseMCP](https://www.pulsemcp.com/) 的注册表维护者 [Tadas Antanavicius](https://github.com/tadasant) 与来自 [Block](https://block.xyz/) 的 [Alex Hancock](https://github.com/alexhancock) 合作，牵头推动了最初的工作。不久后，[GitHub](https://github.com/) 的 MCP 负责人、注册表维护者 [Toby Padilla](https://github.com/toby) 加入进来；最近，来自 [Anthropic](https://www.anthropic.com/) 的 [Adam Jones](https://github.com/domdomegg) 也作为注册表维护者加入，推动项目走向今天的发布。关于 MCP 注册表开发的[最初公告](https://github.com/modelcontextprotocol/registry/discussions/11)列出了来自至少 9 家不同公司的 16 位贡献者。

还有许多人为这个项目的落地做出了关键贡献：来自 [Stacklok](https://stacklok.com/) 的 [Radoslav Dimitrov](https://github.com/rdimitrov)、来自 [GitHub](https://github.com/) 的 [Avinash Sridhar](https://github.com/sridharavinash)、来自 [VS Code](https://code.visualstudio.com/) 的 [Connor Peet](https://github.com/connor4312)、来自 [NuGet](https://www.nuget.org/) 的 [Joel Verhagen](https://github.com/joelverhagen)、来自 [Last9](https://last9.io/) 的 [Preeti Dewani](https://github.com/pree-dew)、来自 [Microsoft](https://www.microsoft.com/) 的 [Avish Porwal](https://github.com/Avish34)、[Jonathan Hefner](https://github.com/jonathanhefner)，以及许多提供代码评审和开发支持的 Anthropic 与 GitHub 员工。我们还感谢[注册表贡献者日志](https://github.com/modelcontextprotocol/registry/graphs/contributors)中的每一位，以及参与[讨论与议题](https://github.com/modelcontextprotocol/registry)的所有人。

我们深深感谢所有为这一基础性开源基础设施投入努力的人。携手之下，我们正在帮助全球的开发者和组织构建更可靠、具备上下文感知能力的 AI 应用。谨代表 MCP 社区，谢谢大家。
