# 如何高效评审代码：一位 GitHub 资深工程师的理念 - GitHub 博客

> 来源: https://github.blog/developer-skills/github/how-to-review-code-effectively-a-github-staff-engineers-philosophy/

[Sarah Vessels](https://github.blog/author/cheshire137/)·[@cheshire137](https://github.com/cheshire137)

2024 年 7 月 23 日|16 分钟

- 分享：

作为 GitHub 的一名资深工程师（staff engineer），[代码评审](https://github.com/features/code-review)是我日常工作中最主要的关注领域之一。在过去的八年里，我评审了 7000 多个拉取请求（PR）。为什么这么多？因为代码评审对于打造优质软件至关重要，而多一双眼睛往往能发现你原本会忽略的问题。

我把代码评审视为工作中最重要的环节之一。事实上，每当我看到队友有一个拉取请求（PR）准备好接受代码评审时，我都宁愿放下手头正在处理的分支，转而去评审他们提出的改动。毕竟，他们的拉取请求已经通过了持续集成（CI）的重重考验，并达到了他们自己判定为"完成"的标准，所以它可能比我自己尚未完成的工作更接近可发布状态。我更愿意把他们的代码推过终点线，而不是再花上一段未知的时间去完成我自己的代码。

我越早给出反馈——"这里可能为 nil 并导致错误"、"这看起来像是一个 n+1 查询"、"这里要是有个方法签名就好了"——这些反馈就能越早得到处理，漏洞也能更快被修复，或功能更快被发布。

我想分享一下我是如何进行代码评审的，希望我们都能交付更好的代码。

## 什么是代码评审？

严格来说，代码评审——通过 GitHub 上的[拉取请求评审](https://docs.github.com/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)——让协作者能够对拉取请求中提议的改动发表评论，表明他们是否批准这些改动，或在拉取请求合并之前要求进一步修改。

我把拉取请求看作对话的开端。我把它理解为作者在说："我认为这比我们现有的方案有所改进。"代码评审是塑造产品实现方式的大好机会。作为一名代码评审者，我的职责是与作者反复讨论，通过提问、质疑假设，以及总体上充当第二双眼睛，来改进他们的代码。

## 优化你的代码评审流程

### 如何找到需要评审的拉取请求

我常驻在 [GitHub 通知收件箱](https://github.com/notifications?query=is:unread)里。这是我在浏览器中固定的少数几个标签页之一，所以它随时可用。每当我等待 CI、在两个任务之间切换、开始新的一天，或者只是有空的时候，我都喜欢查看收件箱。我评审的大多数拉取请求都是在那里找到的。GitHub 的各个团队往往会有一个特定的 Slack 频道作为大本营，那是分享"准备好接受评审"的拉取请求的好地方——这也是我发现拉取请求的另一个主要途径。

我还很幸运地使用了 [GitHub Slack 集成](https://slack.github.com/)，让某个 Slack 频道订阅与我团队相关的新拉取请求。为了筛选哪些拉取请求会出现在 Slack 中，我使用了团队专属的标签，然后在 Slack 中使用 'subscribe' 命令，例如 `/github subscribe your/repo pulls +label:"your-team-label"`。

我喜欢用类似 `is:open archived:false is:pr org:github -is:draft team-review-requested:github/relevant-codeowner-team` 这样的查询来搜索可能需要评审的待处理拉取请求。通过这个查询，我能找到 GitHub 组织内处于[开放](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-open-or-closed-state)、未[归档](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-based-on-whether-a-repository-is-archived)状态的[拉取请求](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-only-issues-or-pull-requests)，它们位于 [GitHub 组织内部](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-within-a-users-or-organizations-repositories)，不是[草稿](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-for-draft-pull-requests)，并且已将[相关的代码所有者团队列为请求的评审人](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-pull-request-review-status-and-reviewer)。我通常会省略 [review:required](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-pull-request-review-status-and-reviewer) 这个搜索限定符，因为即使队友已经评审过某个拉取请求，我也有兴趣去评审它。毕竟，评审代码不仅对作者有帮助，也能让我及时了解影响我所负责代码的改动。

### 使用评审者团队来管理通知

你不希望代码改动通知到规模如此庞大的团队，以至于团队里的每个人都觉得评审这项改动不是自己的[责任](https://en.wikipedia.org/wiki/Diffusion_of_responsibility)。这可能导致拉取请求要么长期无人评审而搁置，要么在本不该合并时被合并，因为关键评审者在海量通知中错过了它们。这两种情况都会影响产品质量。

我建议，如果可以的话，精简你所加入的[代码所有者](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)（code owner）团队的数量，让通知量保持在可控范围内。这样一来，进入你收件箱的拉取请求就不再是噪音，而是你确实觉得自己应该评审的内容。虽然庞大、包罗万象的代码所有者团队作为备选方案也许可以接受，但它们并不适合作为自动评审请求的一线默认选择。保持代码仓库的 CODEOWNERS 文件井然有序，并配上清晰界定的代码边界，以限制通知数量，帮助评审者避免通知疲劳。

限制基于团队的通知的另一种方法，是创建一个"第一响应者"团队，然后使用自动化手段按排班表增减团队成员。这能让你的团队专注于日常的代码库工作，而按排班表轮值的第一响应者则会收到团队负责领域内拉取请求的通知。例如，使用 [PagerDuty API](https://developer.pagerduty.com/api-reference/3f03afb2c84a4-get-a-schedule)，你可以确定某一天谁是第一响应者。然后你可以使用 [Octokit 库](https://docs.github.com/rest/using-the-rest-api/libraries-for-the-rest-api?apiVersion=2022-11-28#official-github-libraries) 来增减团队成员。

### 通过自动化在各团队间标准化代码评审

仓库级别的配置与自动化，例如使用 [CODEOWNERS 文件](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners#codeowners-file-location)和[分支保护规则](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)，有助于在各团队间强制执行评审流程标准。而其他标准，比如拉取请求中哪些内容值得评论，则必须由我们人类来维护。把团队内部的代码评审运作方式记录下来，确保无论是提供代码评审的人还是提交拉取请求的人，都知道如何让自己的拉取请求得到评审、评审的预期周转时间，以及使用了哪些自动化手段来辅助评审。

有些团队使用项目看板来跟踪哪些拉取请求进入评审；我见过这对管理共享 API 的团队很有效——这类领域经常被团队外部人员修改。另一些团队则完全依赖 GitHub 通知；我见过当代码所有权范围界定清晰、且团队能自律地在拉取请求进来时及时评审时，这种方式也很有效。

如果你遵循的是某个特定团队独有的流程，自动化可以帮助向团队外部的人传达预期。例如，如果许多其他团队都依赖你们团队的评审，你可以用一个机器人自动在请求你们团队评审的拉取请求上留言，告诉作者他们什么时候可以收到你们的回复。

## 什么样的代码评审是好评审，什么样的又是差评审？

好的代码评审能增加清晰度，并把代码推向比一开始更好的状态。

作为评审者，沟通的清晰度是关键。你要明确区分哪些评论只是个人偏好，哪些是阻止批准的阻碍项。提供一个你所建议方法的示例，能提升代码评审的质量，并让你的意思更加清晰。如果你能从该拉取请求所在的同一代码仓库中给出示例，那就更好了——这能通过鼓励一致的实现方式，进一步支撑你的建议。

相比之下，糟糕的代码评审缺乏清晰度。例如，不加任何评论就一概批准或否决，会让拉取请求作者怀疑这次评审是否认真彻底。哪怕只是在批准时重申你对作者意图的理解，也能显示出你和作者是否达成了一致的理解。

如果代码评审没有说清楚其建议应该在什么时候落实，对作者来说也可能是一次糟糕的体验。指出已有的、未改动的代码应该被重构，或者应该处理某个额外的场景，这都没有问题；但重要的是要明确这些是否是批准的前置条件。如果即使不采纳你的建议，这个拉取请求也可以合并，那就一定要说明这一点。保持较小的改动范围，把这些改动作为独立的拉取请求单独发布，可能更为稳妥。

下面是一条体现出具体性、并清楚传达了建议实现方式的代码评审评论：

"我看到你的新方法沿用了这个文件中现有的风格，接收 [X] 个参数。这么多参数会损害可读性，也意味着这个函数承担了过多的职责。你觉得在之后的拉取请求中重构这个方法和现有的那些方法，以减少它们接收的参数数量，怎么样？"

这条评论做得好的地方：

- 提供了具体的细节。
- 引用了具体的代码或问题。
- 提出了解决问题的方案。
- 引用了证据或给出了说明

在另一个极端，以下是一些本可以写得更好的评审评论示例：

"我不喜欢这个。"——评审者到底不喜欢什么？他们心里是否有一个可以明确说出来的替代方案？

可能的改进：

- "这一行做了太多事情，我们能不能简化一下以提高可读性？"
- "我认为这会因为 n+1 查询而产生性能问题。"
- "我们能不能用 [首选框架] 的解决方案来处理这个，而不是自己写一个自定义实现？"

"这行不通。"——为什么这些改动行不通？

可能的改进：

- "这行不通，因为 [X]，参见这个相关的问题：[问题链接]。"
- "这在 [拉取请求链接] 中曾经尝试过，但因为 [X] 而没有成功。"
- "如果你在 [X] 上遇到问题，可以试试 [替代方案]。"

"我认为这修复了一个漏洞。"——我很喜欢这种指出问题的方式，但是否有一些额外的上下文，比如问题链接，能让这一点更清楚呢？

可能的改进：

- "我认为这修复了 [问题链接]。"
- "这是不是修复了 [问题链接] 中的漏洞？"
- "这看起来像是我们在 [失败的构建链接] 中遇到的那个漏洞。感谢修复！"

## 如何给出好的代码评审

### 提出问题

我把拉取请求作者看作是对其拉取请求所做改动拥有最多上下文的人。我可以根据自己的经历——在 Ruby on Rails 单体应用中工作的经验、使用 TypeScript 的经验，或使用高流量数据库的经验——指出我看到的问题，但我相信作者对我所提问题的回答。我认为他们对细节的理解胜过我的理解。

我也喜欢提出涉及代码中所做假设的问题。他们正在处理的数据是什么样的结构？是否存在不符合该结构的数据？代码对这种情况的响应是否良好？代码是否消耗大量资源？它的性能表现会好吗？作为评审者，我最喜欢的回应是作者提供一个自动化测试，验证在这些场景下的行为。我第二喜欢的回应是经验数据，比如来自数据仓库的一次查询，或者一张 Datadog 图表，说明为什么这些场景不成问题。

作为拉取请求作者，我很乐意收到问题。当有人提出问题时，这为我腾出了空间，让我可以解释为什么我对自己的改动有信心，并在必要时引用问题、查询或图表。这也让我能与他人分享我的知识和经验。我的回复不仅作者能看到，其他评审者以及未来可能追溯某个历史决策上下文的读者也能看到。

### 给予肯定

除了提出问题，对你认同的拉取请求部分发表评论也是一种良好做法。这些评论可以表明你阅读并理解了正在改动的内容，或者你验证了代码中的某个假设。以下是一些例子：

- "看起来这与本模块中其他类使用的模式一致。"
- "谢谢你为此添加了测试！"
- "这比以前可读性强多了。"

根据我的经验，收到这样的评论感觉也很棒。收到代码评审有时会让人感到精力被消耗。当我正在应对来自好几方的问题和建议时，能收到几条不对我提出任何要求、而是支持和认可我已经付出的工作的评论，会是一种很好的提振。

### 留意偏见与假设

很容易让你对评审对象、或对他们所改动代码领域的偏见影响你的评审。你习惯了某人在某个领域工作、或具备一定资历，就假定他们知道自己在做什么——但**每个人**都会犯错。你亲自审视他们的改动、通过提问检验他们的假设或验证你自己的假设，都能在问题被部署之前发现它。

我非常推崇编写测试，因为它们能消除一部分偏见。当你写一个测试来检验代码是否正常工作时，你不必只听作者的一面之词([你不必听作者怎么说](https://www.youtube.com/watch?v=NIKAsGC1Iy8))，只需看测试是否通过——当然，前提是你把测试写对了。😅

我也非常支持初级开发者在代码评审中向资深开发者提问，即使他们认为自己的问题很傻、或者答案显而易见。如果你觉得不明显，那就是合理的。对别人来说它也未必显而易见！把问题提出来，给作者腾出空间写下答案，并把这份知识留存下来，供后来者受益。

### 批准还是不批准

我把自己的评审看作一道可能阻挡他人改进产品的门禁，所以我会审慎地暂缓批准。我经常会有个人偏好，并提出一些希望作者做出的可选改动，但我不会仅仅因为那些就暂缓批准。如果我对某人的拉取请求有建议，但该拉取请求按现状不会破坏生产环境、不会对用户造成负面影响，也不会引发其他问题，我就会连同这些评论一起批准。作者可以选择在合并拉取请求之前处理我的反馈，也可以在另一个分支中跟进。

在评审代码时，要牢记你的建议的重要性。为了让你的建议得到落实而推迟发布，值得吗？让作者看到你的反馈、做出建议的改动、等待 CI、再次评审、部署、最后合并——这整个循环值得吗？如果缺少某条建议不会让任何人的日子变得更糟，那就让作者自己决定是否以及何时做出这项改动。

[「请求修改」（Request changes）选项](https://docs.github.com/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request#submitting-your-review)会阻止拉取请求被合并，直到评审者回来批准它为止。我很少使用它，因为它通常显得过于强硬。我相信我的团队知道什么时候该批准拉取请求，所以队友的批准可以替代我的批准。同样，我也相信拉取请求作者会尊重并考虑我的反馈，而不是因为别人批准了、我没批准就盲目合并。我唯一会选择"请求修改"选项的情况，大致是当我认为存在迫在眉睫的安全问题，并担心他们在合并前看不到我的顾虑时。

## 如何充分利用代码评审

### 评审你自己的代码

GitHub 高级软件工程师 [Paul Smith](https://github.com/paulcsmith) 教会了我，在请别人评审之前先评审自己的拉取请求，我也建议你这样做。先过一遍，对不明显的改动、或那些如果出现在别人的拉取请求中你会想要询问的改动，留下行内评论。自我评审还有助于判断某个拉取请求是否过大、是否最好[拆分](https://github.blog/2020-05-21-github-protips-tips-tricks-hacks-and-secrets-from-sarah-vessels/)开来。

特别致谢：如果你在意保持拉取请求小巧，可以使用 [lerebear/sizeup-action](https://github.com/lerebear/sizeup-action) 自动为拉取请求打上标签，标明其复杂度和大小。

### 欢迎合并后的评审

如果我碰巧在别人有机会评审之前就合并了拉取请求，我仍然欢迎他们的评审。如果我的拉取请求破坏了某些东西或产生了意料之外的后果，在拉取请求上尽量多留言，就能留下线索（breadcrumb trail），帮助未来的读者追溯到底发生了什么！

如果我在一个已合并的拉取请求上收到评审，我会像在该拉取请求合并之前那样处理反馈。也许是写一条评论解释我的观点，也许是追加一些拉取请求来迭代我最初交付的代码，也许是为需要完成的额外工作创建新的问题。

### 使用草稿拉取请求

当你创建一个新的拉取请求时，可以选择将其设为草稿。我非常依赖[草稿阶段](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request)来表明我是否希望获得评审。例如，如果必需的 CI 构建失败，或者我还没完成，我就会把它保持为草稿。我也倾向于对他人的拉取请求抱有同样的预期：如果是草稿，我就认为作者还没准备好接受评审。如果它被标记为"准备好接受评审"，我就认为他们部署这个拉取请求只差获得足够的批准了。

草稿状态意味着拉取请求尚未完成，所以在解决合并冲突或处理评审者反馈时，我会把拉取请求改回草稿。如果我必须修改代码，我会先把我的拉取请求标记为草稿，以免让已经评审过它的人不堪其扰。当我把它改回"准备好"状态时，会向那些评审者发送 GitHub 通知，让他们再来看一遍。

### 保持友善得体

我想到一句俗语："用蜂蜜比用醋能捉到更多苍蝇。"（好言胜于恶语。）我希望自己的拉取请求能得到评审，所以我喜欢回复拉取请求上的评论——尤其是当我不同意评审者的时候。即使我没有对评审评论写回复，我也经常会点个 👍 表示同意，或者点个 ❤ 表示感谢。

我希望评审者相信他们的建议不会被遗忘，所以我会通过评论让他们保持知情。如果我同意他们的建议——比如进一步重构现有代码——我可能会明说，同时也反对在当前拉取请求中做这项改动。当我在之后的拉取请求中处理他们的反馈时，我会回来提供链接，让评审者知道他们的反馈没有被忽视。

我还会在之后那些落实了建议改动的拉取请求中@他们，并附上一句说明："这处理了 @某某 在 <之前的拉取请求 URL> 中提出的反馈。"这既为其他读者提供了上下文，也向最初的评审者致意，肯定这个想法来自他们。

当你兑现承诺、在之后的分支中处理反馈时，这有助于与评审者建立信任，使他们能放心地批准你未来的拉取请求，因为他们知道你不会把事情半途而废。

## 结语

代码评审对产品质量的重要性再怎么强调也不为过，尤其是在 AI 生成代码的时代。在我的职业生涯中，有很多次，仅仅因为多了一双眼睛，就发现了一个漏洞或避免了一次故障事件。代码评审非常值得投入时间，无论是花在日常评审上、理顺流程上，还是构建支持它的自动化上。对开发者来说，现在彻底地评审拉取请求，要比等到问题已经进入生产环境后再去处理来得更快、更省心。

感谢你对代码质量的关心，愿意阅读我的代码评审理念。你最近查看过[你的评审队列](https://github.com/search?q=review-requested:@me+is:open+archived:false&type=pullrequests)吗？也许现在正是把这些想法付诸行动的好时机。

如果你想了解更多关于如何在 GitHub 上使用拉取请求评审的知识，可以看看 GitHub 社区上由 DevOps 架构师 [Mickey Gousset](https://github.com/mickeygousset) 和 DevOps 架构师 [Joshua Johanning](https://github.com/joshjohanning) 撰写的帖子，其中讨论了[评审拉取请求的 5 个技巧](https://github.com/orgs/community/discussions/130771)。

## 标签：

- 代码评审

## 作者

GitHub 高级软件工程师（Staff Software Engineer）

## 相关文章

[开发者技能](https://github.blog/developer-skills/)

### GitHub 新手入门：开始使用 GitHub 安全功能

了解如何使用 GitHub Advanced Security 保护你的项目并保持其安全。

[AI 与机器学习](https://github.blog/ai-and-ml/)

### 使用 Copilot SDK 构建 AI 驱动的 GitHub 问题分类

了解如何将 Copilot SDK 集成到 React Native 应用中，以生成 AI 驱动的问题摘要，并采用优雅降级和缓存的生产级模式。

[开发者技能](https://github.blog/developer-skills/)

### GitHub 新手入门：开始使用 GitHub Actions

在这份操作指南中搭建你的第一个 GitHub Actions 工作流。
