DROP TABLE IF EXISTS "books";
CREATE TABLE "public"."books" (
    "isbn" VARCHAR PRIMARY KEY,
    "title" VARCHAR NOT NULL,
    "author" VARCHAR NOT NULL,
    "year" INTEGER NOT NULL
) WITH (oids = false);
