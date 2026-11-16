# 代码评审：Just Do It

> 来源: https://blog.codinghorror.com/code-reviews-just-do-it/

在[让同行评审更有人情味](https://web.archive.org/web/20060315135514/http://www.processimpact.com/articles/humanizing_reviews.html)一文中，Karl Wiegers 开宗明义地提出了一个有力的论断：

> 同行评审——由软件交付物作者以外的人员对其进行检查，以发现缺陷和改进机会的活动——是现有最强大的软件质量工具之一。同行评审的方法包括检查、走查、同行桌面检查以及其他类似活动。在亲历同行评审的益处近十五年之后，我绝不会在一个不做同行评审的团队里工作。

在 Vertigo 这里参与代码评审一段时间后，我相信同行代码评审是你能为改进代码所做的头等大事。如果你此刻没有和另一位开发者一起做代码评审，那你的代码里就漏掉了大量缺陷，也让自己错失了一些关键的职业发展机会。就我而言，我的代码在与另一位开发者一起过一遍之前，都不算完成。

不过别只听我一家之言。McConnell 在[《代码大全》](http://www.amazon.com/exec/obidos/ASIN/0735619670)中提供了大量证据，证明代码评审卓有成效：

kg-card-begin: html

> ……单靠软件测试的效果有限——单元测试的平均缺陷检出率只有 25%，功能测试为 35%，集成测试为 45%。相比之下，设计检查和代码检查的平均有效性分别为 55% 和 60%。评审结果的案例研究令人印象深刻：在一家软件维护机构中，引入代码评审之前，55% 的单行维护变更都是错误的。引入评审之后，只有 2% 的变更出错。从所有变更来看，引入评审后 95% 的变更一次就正确。引入评审之前，一次就正确的还不到 20%。在同一批人开发的 11 个程序中，前 5 个没有经过评审，其余 6 个经过了评审。在所有程序发布到生产环境后，前 5 个平均每 100 行代码有 4.5 个错误，而经过检查的 6 个平均每 100 行只有 0.82 个错误。评审把错误减少了 80% 以上。Aetna 保险公司通过检查发现了一个程序中 82% 的错误，并得以将开发资源减少 20%。IBM 的 50 万行 Orbit 项目采用了 11 级检查，提前交付，且错误数仅为正常情况下预期值的约 1%。一项针对 AT&T 某 200 多人组织的研究报告称，该组织引入评审后生产率提高了 14%，缺陷减少了 90%。喷气推进实验室估计，通过在早期发现和修复缺陷，每次检查可节省约 2.5 万美元。

kg-card-end: html代码评审唯一的门槛，是找到一位你尊敬的开发者来做这件事，并腾出时间进行评审。一旦开始，我想你很快就会发现，花在代码评审上的每一分钟都会得到十倍的回报。

如果你的团队刚接触代码评审，我强烈推荐 Karl 的书[《软件同行评审》](http://www.amazon.com/exec/obidos/ASIN/0201734850)：实用指南。Karl 在其网站上提供的[样章](https://web.archive.org/web/20060315135046/http://www.processimpact.com/reviews_book/reviews_book_toc.shtml)也是很好的入门材料。

[软件开发](https://blog.codinghorror.com/tag/software-development/)[代码评审](https://blog.codinghorror.com/tag/code-reviews/)[同行评审](https://blog.codinghorror.com/tag/peer-reviews/)[代码质量](https://blog.codinghorror.com/tag/code-quality/)[职业发展](https://blog.codinghorror.com/tag/professional-development/)
