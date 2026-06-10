# DummyJSON 接口参数总表（全量清单）

站点文档：`https://dummyjson.com/docs`

> 说明：DummyJSON 的“新增/更新/删除”类接口为 **模拟写入**（不会真正改服务端数据），适合用于接口自动化框架演示与报告展示。

## 通用 Query 参数（几乎所有资源通用）

- **limit**: int，分页大小；`0` 表示不限制（返回全部）
- **skip**: int，跳过数量（分页偏移）
- **select**: string 或重复 select 参数，字段筛选  
  - 形式1：`select=key1,key2,key3`  
  - 形式2：`select=key1&select=key2&select=key3`
- **delay**: int，模拟延迟（0-5000ms）
- **sortBy**: string，排序字段名（Products/Users/Posts/Recipes 等列表接口支持）
- **order**: string，`asc` / `desc`

## System/辅助接口

### GET `/test`
- **参数**：无

### GET `/ip`
- **参数**：无

### GET `/http/{code}/{message?}`
- **Path 参数**
  - **code**: int，HTTP 状态码（如 200/404/500）
  - **message**: string，可选，自定义 message（如 `Hello_Peter`）

### GET `/image/{size}` 或 `/image/{width}x{height}/{background?}/{color?}`
- **Path 参数**
  - **size**: `150` 或 `200x100`
  - **background**: hex（如 `008080`/`282828`），可选
  - **color**: hex（如 `ffffff`），可选
- **Query 参数**
  - **text**: string，自定义文本（空格用 `+`）
  - **type**: `png` / `jpg` / `webp`
  - **fontFamily**: 字体名（如 `poppins`/`pacifico` 等）
  - **fontSize**: int

### GET `/icon/{hash}/{size}?type=png|svg`
- **Path 参数**
  - **hash**: string（任意字符串）
  - **size**: int
- **Query 参数**
  - **type**: `png` / `svg`

## Auth（认证）

### POST `/auth/login`
- **Body 参数（JSON）**
  - **username**: string
  - **password**: string
  - **expiresInMins**: int，可选（默认 60）

### GET `/auth/me`
- **Header**
  - **Authorization**: `Bearer <accessToken>`

### POST `/auth/refresh`
- **Body 参数（JSON）**
  - **refreshToken**: string，可选（不传时服务端可尝试用 cookie）
  - **expiresInMins**: int，可选（accessToken 有效期，默认 60）

### 兼容接口（Users 文档里出现）

#### POST `/user/login`
- **Body**：同 `/auth/login`

#### GET `/user/me`
- **Header**：同 `/auth/me`

## Products（商品）

### GET `/products`
- **Query**：通用（limit/skip/select/delay/sortBy/order）

### GET `/products/{id}`
- **Path**：`id` int
- **Query**：`select`、`delay`

### GET `/products/search`
- **Query**
  - **q**: string（关键字）
  - + 通用（limit/skip/select/delay）

### GET `/products/categories`
- **Query**：`delay`

### GET `/products/category-list`
- **Query**：`delay`

### GET `/products/category/{slug}`
- **Path**：`slug` string（如 `smartphones`）
- **Query**：通用（limit/skip/select/delay）

### POST `/products/add`
- **Body（JSON）**：商品字段（文档示例只展示 `title`，可附加更多字段）
  - 常用：`title`,`description`,`category`,`price`,`stock`,`brand`,`tags`,`sku`,`weight`…

### PUT/PATCH `/products/{id}`
- **Path**：`id` int
- **Body（JSON）**：更新字段（可只传部分字段）

### DELETE `/products/{id}`
- **Path**：`id` int

## Carts（购物车）

### GET `/carts`
- **Query**：通用（limit/skip/select/delay）

### GET `/carts/{id}`
- **Path**：`id` int
- **Query**：`select`,`delay`

### GET `/carts/user/{userId}`
- **Path**：`userId` int
- **Query**：通用（limit/skip/select/delay）

### POST `/carts/add`
- **Body（JSON）**
  - **userId**: int
  - **products**: array
    - item: `{ id: int, quantity: int }`

### PUT/PATCH `/carts/{id}`
- **Path**：`id` int
- **Body（JSON）**
  - **merge**: bool（可选，true 表示保留旧商品再合并）
  - **products**: array（同 add）

### DELETE `/carts/{id}`
- **Path**：`id` int

## Users（用户）

### GET `/users`
- **Query**：通用（limit/skip/select/delay/sortBy/order）

### GET `/users/{id}`
- **Path**：`id` int
- **Query**：`select`,`delay`

### GET `/users/search`
- **Query**：`q` + 通用（limit/skip/select/delay）

### GET `/users/filter`
- **Query**
  - **key**: string（支持嵌套 key，如 `hair.color`）
  - **value**: string（大小写敏感）
  - + 通用（limit/skip/select/delay）

### GET `/users/{id}/carts`、`/users/{id}/posts`、`/users/{id}/todos`
- **Path**：`id` int
- **Query**：`delay`

### POST `/users/add`
- **Body（JSON）**：用户字段（文档示例为 `firstName/lastName/age`，可附加更多字段）

### PUT/PATCH `/users/{id}`
- **Path**：`id` int
- **Body（JSON）**：更新字段

### DELETE `/users/{id}`
- **Path**：`id` int

## Posts（帖子）

### GET `/posts`
- **Query**：通用（limit/skip/select/delay/sortBy/order）

### GET `/posts/{id}`
- **Path**：`id` int
- **Query**：`select`,`delay`

### GET `/posts/search`
- **Query**：`q` + 通用（limit/skip/select/delay）

### GET `/posts/tags`、`/posts/tag-list`
- **Query**：`delay`

### GET `/posts/tag/{slug}`
- **Path**：`slug` string（如 `life`）
- **Query**：通用（limit/skip/select/delay）

### GET `/posts/user/{userId}`
- **Path**：`userId` int
- **Query**：通用（limit/skip/select/delay）

### GET `/posts/{id}/comments`
- **Path**：`id` int
- **Query**：通用（limit/skip/select/delay）

### POST `/posts/add`
- **Body（JSON）**
  - **title**: string
  - **userId**: int
  - 其它字段可选：`body`,`tags`…

### PUT/PATCH `/posts/{id}`
- **Path**：`id` int
- **Body（JSON）**：更新字段

### DELETE `/posts/{id}`
- **Path**：`id` int

## Comments（评论）

### GET `/comments`
- **Query**：通用（limit/skip/select/delay）

### GET `/comments/{id}`
- **Path**：`id` int
- **Query**：`select`,`delay`

### GET `/comments/post/{postId}`
- **Path**：`postId` int
- **Query**：通用（limit/skip/select/delay）

### POST `/comments/add`
- **Body（JSON）**
  - **body**: string
  - **postId**: int
  - **userId**: int

### PUT/PATCH `/comments/{id}`
- **Path**：`id` int
- **Body（JSON）**：更新字段

### DELETE `/comments/{id}`
- **Path**：`id` int

## Todos（待办）

### GET `/todos`
- **Query**：通用（limit/skip/delay）

### GET `/todos/{id}`
- **Path**：`id` int
- **Query**：`delay`

### GET `/todos/random` 或 `/todos/random/{length}`
- **Path**：`length` int（可选，最大 10）
- **Query**：`delay`

### GET `/todos/user/{userId}`
- **Path**：`userId` int
- **Query**：通用（limit/skip/delay）

### POST `/todos/add`
- **Body（JSON）**
  - **todo**: string
  - **completed**: bool
  - **userId**: int

### PUT/PATCH `/todos/{id}`
- **Path**：`id` int
- **Body（JSON）**：更新字段

### DELETE `/todos/{id}`
- **Path**：`id` int

## Quotes（名言）

### GET `/quotes`
- **Query**：通用（limit/skip/delay）

### GET `/quotes/{id}`
- **Path**：`id` int
- **Query**：`delay`

### GET `/quotes/random` 或 `/quotes/random/{length}`
- **Path**：`length` int（可选，最大 10）
- **Query**：`delay`

## Recipes（菜谱）

### GET `/recipes`
- **Query**：通用（limit/skip/select/delay/sortBy/order）

### GET `/recipes/{id}`
- **Path**：`id` int
- **Query**：`select`,`delay`

### GET `/recipes/search`
- **Query**：`q` + 通用（limit/skip/select/delay）

### GET `/recipes/tags`
- **Query**：`delay`

### GET `/recipes/tag/{tag}`
- **Path**：`tag` string（如 `Pakistani`）
- **Query**：通用（limit/skip/select/delay）

### GET `/recipes/meal-type/{mealType}`
- **Path**：`mealType` string（如 `snack`）
- **Query**：通用（limit/skip/select/delay）

### POST `/recipes/add`
- **Body（JSON）**
  - **name**: string
  - 其他字段可选：`ingredients`,`instructions`,`difficulty`,`cuisine`,`tags`,`mealType`,`servings`…

### PUT/PATCH `/recipes/{id}`
- **Path**：`id` int
- **Body（JSON）**：更新字段

### DELETE `/recipes/{id}`
- **Path**：`id` int

