# LiuLi API 接口说明文档

> 一站式构建多源、干净、个性化的阅读环境

## 注意事项

- 发起HTTP-POST请求请在Header头加上如下字段： 
   - `Content-Type: application/json`
- 当前服务版本为：v1
- 接口完整 URL 为：接入地址/版本号/接口地址

## 状态码

| 状态码 | 名称                  | 说明                     |
| ------ | --------------------- | ------------------------ |
| 200    | SUCCESS               | OK                       |
| 400    | BAD_REQUEST           | 错误请求                 |
| 401    | NOT_AUTHORIZED        | 验证未通过               |
| 500    | SERVER_ERR            | 服务异常                 |
| 901    | USER_LOGIN_ERROR      | 用户登录失败             |
| 902    | USER_CHANGE_PWD_ERROR | 用户修改密码失败         |
| 903    | GEN_RSS_FAILED        | RSS 生成失败             |
| 904    | GEN_BACKUP_FAILED     | BACKUP 生成失败          |
| 905    | GET_DC_EMPTY          | 获取不到 doc_source 配置 |


## 通用参数

### 请求Header头

| 参数名        | 参数类型 | 描述               | 是否必填 |
| ------------- | -------- | ------------------ | -------- |
| Content-Type  | string   | application/json   | T        |
| Authorization | string   | 需要校验的接口必填 | F        |

### 通用返回参数

| 字段名 | 类型   | 描述                                               | 示例               |
| ------ | ------ | -------------------------------------------------- | ------------------ |
| status | int    | 业务状态码，200 为正常，否则为异常                 | 200                |
| info   | string | 业务状态描述，正常为 `ok` ，异常为业务异常具体描述 | "ok"               |
| data   | json   | 业务数据，异常为 {}                                | {"hello": "world"} |

### 通用响应

#### 请求成功

```json
{
	"status": 200,
	"info": "OK",
	"data": {}
}
```

#### 参数错误

```json
{
  "data": {},
  "info": "参数错误!",
  "status": 400
}
```

#### 验证失败

```json
{
  "data": {},
  "info": "验证未通过",
  "status": 401
}
```

#### 未知错误

```json
{
  "data": {},
  "info": "未知错误",
  "status": 500
}
```

## [User] 修改密码

### 描述

修改用户密码

### URL路径

/user/change_pwd

### 请求方式

POST

### 请求参数

`Header` 头必须带上 `Authorization`：

| 参数名     | 类型   | 必选 | 描述   |
| ---------- | ------ | ---- | ------ |
| username   | string | 是   | 用户名 |
| o_password | string | 是   | 老密码 |
| n_password | string | 是   | 新密码 |

### 返回参数

响应返回的是接口标准的通用响应

### 请求示例

```json
{
    "username": "liuli",
    "o_password": "liuli",
    "n_password": "liuli"
}
```

### 返回示例

#### 成功示例

```json
{
    "data": {
        "username": "liuli"
    },
    "info": "OK",
    "status": 0
}
```

#### 失败示例

```json
{
    "data": {},
    "info": "用户修改密码失败",
    "status": 902
}
```


## [User] 登录

### 描述

用户登录

### URL路径

/user/login

### 请求方式

POST

### 请求参数

| 参数名   | 类型   | 必选 | 描述   |
| -------- | ------ | ---- | ------ |
| username | string | 是   | 用户名 |
| password | string | 是   | 密码   |

### 返回参数

响应返回的是接口标准的通用响应

### 请求示例

```json
{
    "username": "liuli",
    "password": "liuli"
}
```

### 返回示例

#### 成功示例

```json
{
  "data": {
    "token": "",
    "username": "liuli"
  },
  "info": "ok",
  "status": 200
}
```

#### 失败示例

```json
{
    "data": {},
    "info": "用户登录失败",
    "status": 901
}
```

## [User] Token 校验

### 描述

用户 token 校验接口

### URL路径

/user/token_valid

### 请求方式

POST

### 请求参数

`Header` 头必须带上 `Authorization`：

| 参数名   | 类型   | 必选 | 描述   |
| -------- | ------ | ---- | ------ |
| username | string | 是   | 用户名 |

### 返回参数

响应返回的是接口标准的通用响应

### 请求示例

```json
{
    "username": "liuli"
}
```

### 返回示例

#### 成功示例

```json
{
  "data": {},
  "info": "ok",
  "status": 200
}
```

#### 失败示例

注意这里 `HTTP` 状态码是 `401`

```json
{
  "msg": "Token has expired"
}
```

## [Stats] 获取所有文档源统计信息

### 描述

获取所有文档源统计信息

### URL路径

/stats/source_list

### 请求方式

POST

### 请求参数

| 参数名   | 类型   | 必选 | 描述   |
| -------- | ------ | ---- | ------ |
| username | string | 是   | 用户名 |

### 返回参数

响应返回的是接口标准的通用响应

### 请求示例

```json
{
    "username": "liuli"
}
```

### 返回示例

#### 成功示例

```json
{
    "data": {
        "doc_counts": 3,
        "doc_source_counts": 3,
        "doc_source_stats_dict": {
            "liuli_book": {
                "counts": 0,
                "doc_source_alias_name": "小说源",
                "rows": [],
                "rows_info": []
            },
            "liuli_wechat_feeddd": {
                "counts": 0,
                "doc_source_alias_name": "微信源(feeddd)",
                "rows": [],
                "rows_info": []
            },
            "liuli_wechat_sg": {
                "counts": 0,
                "doc_source_alias_name": "微信源(搜狗)",
                "rows": [],
                "rows_info": []
            }
        }
    },
    "info": "ok",
    "status": 200
}
```

#### 失败示例

```json
{
    "data": {},
    "info": "用户修改密码失败",
    "status": 902
}
```

## [Action] 查询历史文章

### 描述

查询历史文章

### URL路径

/action/articles

### 请求方式

POST

### 请求参数

| 参数名          | 类型   | 必选 | 描述                  |
| --------------- | ------ | ---- | --------------------- |
| username        | string | 是   | 用户名                |
| doc_source      | string | 否   | 订阅源                |
| doc_source_name | string | 否   | 订阅源目标名          |
| size            | int    | 否   | 每页数量              |
| page            | int    | 否   | 第几页                |
| sorted_order    | int    | 否   | 1(正序) 或者 -1(倒序) |

### 返回参数

参考数据库 `liuli_articles` 表设计[TODO]

### 请求示例

```json
{
  "username": "liuli",
  "doc_source": "liuli_wechat",
  "doc_source_name": "老胡的储物柜",
  "size": 100,
  "page": 1,
  "sorted_order": -1
}
```

### 返回示例

#### 成功示例

```json
{
    "data": {
        "total": 14,
        "rows": [
            {}
        ],
        "size": 1,
        "page": 1
    },
    "info": "ok",
    "status": 200
}
```

#### 失败示例

```json
{
    "data": {},
    "info": "数据库操作错误",
    "status": 500
}
```

## [Action] 数据源备份

### 描述

对数据源进行备份

### URL路径

/action/backup_generate

### 请求方式

POST

### 请求参数

会自动读取表 `liuli_doc_source` 对应的 `backup` 字段进行备份：

| 参数名          | 类型   | 必选 | 描述         |
| --------------- | ------ | ---- | ------------ |
| username        | string | 是   | 用户名       |
| doc_source      | string | 否   | 订阅源       |
| doc_source_name | string | 否   | 订阅源目标名 |

### 返回参数

响应返回的是接口标准的通用响应.

### 请求示例

```json
{
    "username": "liuli",
    "doc_source": "liuli_wechat_sg",
    "doc_source_name": "老胡的储物柜"
}
```

### 返回示例

#### 成功示例

```json
{
  "data": {},
  "info": "ok",
  "status": 200
}
```

#### 失败示例

```json
{
    "data": {},
    "info": "BACKUP 生成失败",
    "status": 904
}
```

## [Action] 生成目标 RSS 源

### 描述

生成目标 RSS 源

### URL路径

/user/rss_generate

### 请求方式

POST

### 请求参数

| 参数名          | 类型   | 必选 | 描述             |
| --------------- | ------ | ---- | ---------------- |
| username        | string | 是   | 用户名           |
| doc_source_list | list   | 是   | 订阅源列表       |
| link_source     | string | 是   | 链接返回规则类型 |

关于 `link_source`:

- self: 不替换，用本身的 `doc_link`
- mongodb: 用 liuli api 服务的连接 `{LL_DOMAIN}/backup/{doc_source}/{doc_source_name}/{doc_name}`
-  github: 用 github 仓库地址 `{LL_GITHUB_DOMAIN}/{doc_source}/{doc_source_name}/{doc_name}.html`

### 返回参数

响应返回的是接口标准的通用响应.

### 请求示例

```json
{
    "username": "liuli",
    "doc_source_list": [
        "liuli_wechat"
    ],
    "link_source": "mongodb",
    "rss_count": 20
}
```

### 返回示例

#### 成功示例

```json
{
  "data": {},
  "info": "ok",
  "status": 200
}
```

#### 失败示例

```json
{
    "data": {},
    "info": "RSS 生成失败",
    "status": 903
}
```

## [Action] 获取用户下所有 RSS 链接地址

### 描述

获取用户下所有 RSS 链接地址

### URL路径

/action/rss_list

### 请求方式

POST

### 请求参数

| 参数名     | 类型   | 必选 | 描述   |
| ---------- | ------ | ---- | ------ |
| username   | string | 是   | 用户名 |
| doc_source | string | 否   | 订阅源 |

### 返回参数

响应返回的是接口标准的通用响应.

### 请求示例

```json
{
  "username": "liuli",
  "doc_source": "liuli_wechat"
}
```

### 返回示例

#### 成功示例

```json
{
  "data": [
    {
      "doc_source": "liuli_wechat",
      "doc_source_name": "老胡的储物柜",
      "rss_url": "http://0.0.0.0:8765/rss/liuli_wechat/老胡的储物柜",
      "updated_at": "2023-01-25 14:47:16"
    }
  ],
  "info": "ok",
  "status": 200
}
```

#### 失败示例

```json
{
    "data": {},
    "info": "数据库操作错误",
    "status": 500
}
```

## [doc_source] 删除

### 描述

删除 doc_source

### URL路径

/doc_source/delete

### 请求方式

POST

### 请求参数

| 参数名     | 类型   | 必选 | 描述   |
| ---------- | ------ | ---- | ------ |
| username   | string | 是   | 用户名 |
| doc_source | string | 否   | 订阅源 |

### 返回参数

响应返回的是接口标准的通用响应.

### 请求示例

```json
{
  "username": "liuli",
  "doc_source": "liuli_wechat"
}
```

### 返回示例

#### 成功示例

```json
{
    "data": {},
    "info": "ok",
    "status": 200
}
```

#### 失败示例

```json
{
    "data": {},
    "info": "数据库操作错误",
    "status": 500
}
```

## [doc_source] 获取

### 描述

获取 doc_source

### URL路径

/doc_source/get

### 请求方式

POST

### 请求参数

| 参数名     | 类型   | 必选 | 描述   |
| ---------- | ------ | ---- | ------ |
| username   | string | 是   | 用户名 |
| doc_source | string | 否   | 订阅源 |

### 返回参数

响应返回的是接口标准的通用响应.

### 请求示例

```json
{
  "username": "liuli",
  "doc_source": "liuli_wechat_sg"
}
```

### 返回示例

#### 成功示例

见 [liuli](https://github.com/howie6879/liuli) 项目配置示例：[wechat.json](https://github.com/howie6879/liuli/blob/main/liuli_config/wechat.json)

#### 失败示例

```json
{
  "data": "",
  "info": "获取不到 doc_source 配置",
  "status": 905
}
```

## [doc_source] 更新

### 描述

更新 doc_source

### URL路径

/doc_source/update

### 请求方式

POST

### 请求参数

见 [liuli](https://github.com/howie6879/liuli) 项目配置示例：[wechat.json](https://github.com/howie6879/liuli/blob/main/liuli_config/wechat.json)

### 返回参数

响应返回的是接口标准的通用响应.

### 请求示例

见 [liuli](https://github.com/howie6879/liuli) 项目配置示例：[wechat.json](https://github.com/howie6879/liuli/blob/main/liuli_config/wechat.json)

### 返回示例

#### 成功示例

```json
{
  "data": {},
  "info": "ok",
  "status": 200
}
```

#### 失败示例

```json
{
    "data": {},
    "info": "数据库操作错误",
    "status": 500
}
```