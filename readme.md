## 表结构
session.query(Comics.comic_url).filter(Comics.comic_url=="shiyish").count()
### Comic
id: int
status: int
comic_url: varchar(80)
name: varchar(80)
author: varchar(80)
comic_cover: varchar(80)
last_update_date: date
topic: varchar(20)
former: varchar(80)
category: list
area: varchar(20)
popularity: varchar(20)
summary: text
chapter_urls: list
device: int


### Chapter
id: int
comic_id: int
chapter_order: int
url: varchar(20)
name: varchar(20)
images: list