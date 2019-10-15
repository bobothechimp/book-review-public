DROP TABLE IF EXISTS "reviews";
CREATE TABLE "public"."reviews" (
    "poster" VARCHAR NOT NULL, --author of review
    "review_text" VARCHAR NOT NULL,
    "isbn" VARCHAR PRIMARY KEY
) WITH (oids = false);
