## v0.2.0 2022-02-11

`liuli` v0.2.0 👏 成功发布，看板计划见[这里](https://github.com/howie6879/liuli/projects/1)，相关特性和功能提升见下方描述。

**提升**:
- 部分代码重构，重命名为 [liuli](https://github.com/liuli-io/liuli/issues/29)
- 提升部署效率，支持`docker-compose` [#17](https://github.com/howie6879/liuli/issues/17)
- 项目容量从100m缩小到3m（移除模型）

**修复**:
- 分发器：企业微信分发部门ID参数不定 [#16](https://github.com/howie6879/liuli/issues/16) @zyd16888
- 修复含有特殊字符密码链接失败 [#35](https://github.com/liuli-io/liuli/pull/35) @gclm

**特性**:
- [官网](https://github.com/liuli-io/liuli/issues/19) @123seven
- [LOGO](https://github.com/liuli-io/liuli/issues/23) @我妹妹
- [采集器]书籍小说大类订阅支持
- [分发器]支持 TG、Bark [#8](https://github.com/howie6879/liuli/issues/8)
  - [TG](https://github.com/liuli-io/liuli/projects/1#card-75295457) @123seven
  - [Bark](https://github.com/liuli-io/liuli/projects/1#card-75295458) @LeslieLeung
- [RSS 支持](https://github.com/liuli-io/liuli/projects/1#card-75295442)
- 备份器支持：
  - [MongoDB](https://github.com/liuli-io/liuli/issues/33)
  - [GitHub](https://github.com/liuli-io/liuli/issues/20)

## v0.1.2 2021-12-23

`liuli` 正式发布第一个可用版本 v0.1.2 👏 ，终于迈出了第一步，相关特性和功能提升见下方描述。

**特性**:
- 完成相似度模型，等训练集增加后再提升 [#5](https://github.com/howie6879/liuli/issues/5)
- 完成分发器，支持微信和钉钉 [#8](https://github.com/howie6879/liuli/issues/8)
- 完成基于`playwright`的公众号采集器（以前是依赖第三方项目，不稳定）[#15](https://github.com/howie6879/liuli/issues/15)

**提升**:
- 完成[使用文档](https://github.com/howie6879/liuli/blob/main/docs/01.%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B.md) [#10](https://github.com/howie6879/liuli/issues/10)
- 支持Docker部署 [liuliio/schedule:v0.1.2](https://hub.docker.com/repository/docker/howie6879/liuli/tags?page=1&ordering=last_updated)