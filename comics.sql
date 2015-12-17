DROP TABLE IF EXISTS public.comics;
CREATE TABLE public.comics(
  comic_id INT UNIQUE,
  comic_url VARCHAR(128) PRIMARY KEY,
  pub_status INT,
  download_url VARCHAR(128),
  name VARCHAR(80),
  author VARCHAR(80),
  title_image text,
  last_update_date DATE,
  tags text[],
  origin_name VARCHAR(80),
  category VARCHAR(80),
  area_location VARCHAR(20),
  popularity VARCHAR(20),
  summary text,
  chapter_num INT
);


DROP TABLE IF EXISTS public.chapters;
CREATE TABLE public.chapters(
  id SERIAL PRIMARY KEY,
  comic_url VARCHAR(128),
  chapter_order INT,
  chapter_url VARCHAR(80),
  name VARCHAR(80),
  images text[]
);


DROP TABLE IF EXISTS public.comments;
CREATE TABLE public.comments(
  id SERIAL PRIMARY KEY ,
  comic_url VARCHAR(128),
  comment_id INT,
  uid INT,
  nickname VARCHAR(128),
  avatar_url VARCHAR(128),
  pid INT,
  comic_id INT,
  author_id INT,
  author  VARCHAR(128),
  content TEXT,
  createtime INT,
  count_reply INT,
  up INT,
  source INT,
  place VARCHAR(128),
  ip VARCHAR(16),
  source_name VARCHAR(128)
)