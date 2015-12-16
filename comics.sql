DROP TABLE IF EXISTS PUBLIC.comics;
CREATE TABLE public.comics(
  comic_url VARCHAR(128) PRIMARY KEY,
  pub_status INT,
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


DROP TABLE IF EXISTS PUBLIC.chapters;
CREATE TABLE public.chapters(
  id SERIAL PRIMARY KEY,
  comic_url VARCHAR(128) REFERENCES comics (comic_url),
  chapter_order INT,
  chapter_url VARCHAR(80),
  name VARCHAR(80),
  images text[]
);