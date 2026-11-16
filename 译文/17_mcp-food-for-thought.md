# API 做不出好的 MCP 工具

> 来源: https://www.reillywood.com/blog/apis-dont-make-good-mcp-tools/

如今，[模型上下文协议](https://modelcontextprotocol.io/overview)（MCP）可谓炙手可热。它已成为让大语言模型（LLM）使用他人所编写工具的事实标准——而这当然会把它们变成[智能体](https://simonwillison.net/2025/May/22/tools-in-a-loop/)。但为一个新的 MCP 服务器编写工具并非易事，因此人们常常提议[将现有 API 自动转换为 MCP 工具](https://blog.christianposta.com/semantics-matter-exposing-openapi-as-mcp-tools/)；典型做法是借助 OpenAPI 元数据（[1](https://jedisct1.github.io/openapi-mcp/)、[2](https://www.gravitee.io/blog/turn-any-rest-api-into-mcp-server-inside-gravitee)）。

根据我的经验，这行得通，但效果并不好。原因如下：

## 智能体不擅长应对大量工具

众所周知，[VS Code 对工具数量设有 128 个的硬上限](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)——但[许多模型早在远未达到这个数字时，就已在准确调用工具方面显得吃力](https://arxiv.org/abs/2411.15399)。此外，每个工具及其描述都会占用宝贵的上下文窗口空间。

大多数 Web API 在设计时并未把上述限制考虑在内！当这些 API 由代码调用时，同一个产品领域拥有几十个 API 并无大碍；但如果把其中每一个 API 都映射成一个 MCP 工具，结果可能就不尽如人意了。

从零开始设计的 MCP 工具通常[比单个 Web API 灵活得多](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)，每个工具都能完成好几个单独 API 才能完成的工作。

## API 会迅速耗尽上下文窗口

试想有一个 API 每次返回 100 条记录，而每条记录都非常宽（比如 50 个字段）。把这些结果原样发送给智能体将消耗大量词元（token）；即使某个查询只需其中几个字段就能满足，每个字段最终也都会进入上下文窗口。

API 通常按记录条数分页，但记录在体积上可能差异很大。一条记录可能含有一个占用 10 万个[词元](https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens)的大文本字段，而另一条可能只有 10 个。把这些 API 结果直接放进智能体的上下文窗口是一场赌博：有时没事，有时会直接撑爆。

数据格式也可能成为问题。如今大多数 Web API 返回 JSON，但 JSON 是一种词元利用效率很低的格式。看这个例子：

```json
[
  {
    "firstName": "Alice",
    "lastName": "Johnson",
    "age": 28
  },
  {
    "firstName": "Bob",
    "lastName": "Smith",
    "age": 35
  }
]
```

再看看 CSV 格式下的同一份数据：

```csv
firstName,lastName,age
Alice,Johnson,28
Bob,Smith,35
```

CSV 数据要简洁得多——每条记录消耗的词元只有一半。[通常，CSV、TSV 或 YAML（用于嵌套数据）都是比 JSON 更好的选择](https://david-gilbertson.medium.com/llm-output-formats-why-json-costs-more-than-tsv-ebaf590bd541)。

这些问题并非无法克服。可以设想：自动添加工具参数，让智能体能够[投影](https://en.wikipedia.org/wiki/Projection_(relational_algebra))字段；自动截断或汇总庞大的结果；自动把 JSON 结果转换为 CSV（嵌套数据则转为 YAML）。但我见过的大多数服务器这些事情一件都没做。

## API 未能充分利用智能体的独特能力

API 返回的是供程序消费的结构化数据。这通常也正是智能体从工具调用中所需要的……但智能体同样能处理其他更自由的指令形式。

例如，`ask_question` 工具可以对一批文档执行检索增强生成（RAG）查询，然后以纯文本形式返回信息，用于指导下一次工具调用——完全跳过结构化数据。

又或者，调用 `search_cities` 工具可以返回一个结构化的城市列表，外加一条关于下一步该调用什么的建议：

```csv
city_name,population,country,region
Tokyo,37194000,Japan,Asia
Delhi,32941000,India,Asia
Shanghai,28517000,China,Asia

Suggestion: To get more specific information (weather, attractions, demographics), try calling get_city_details with the city_name parameter.
```

这种分层与工具链[在 MCP 服务器中可以非常有效](https://engineering.block.xyz/blog/build-mcp-tools-like-ogres-with-layers)，而如果只是把 API 自动转换成工具，你就会完全错失这一点。

## 如果智能体需要调用 API，它完全可以直接调用

如今，像 Claude Code 这样的智能体在编写并执行代码方面能力惊人，其中包括调用 Web API 的脚本。有些人甚至走得更远，[主张根本不需要 MCP](https://lucumr.pocoo.org/2025/7/3/tools/)！

我不同意这个结论，但我确实认为我们应当顺势而为——滑向冰球将要到达的地方。[智能体的沙箱隔离正在迅速改进](https://github.com/openai/codex)，如果让智能体直接调用 API 变得既容易又安全，那我们不妨就这么做，把中间人砍掉。

## 结论

智能体与 API 的典型使用者有着根本区别。从现有 API 自动创建 MCP 工具是可行的，但这样做不太可能取得好效果。只有当所提供的工具是专为智能体独特的能力与局限而设计时，智能体才能发挥最佳表现。
