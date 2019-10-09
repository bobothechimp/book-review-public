
DROP TABLE IF EXISTS "accounts";
CREATE TABLE "public"."accounts" (
    "username" VARCHAR NOT NULL,
    "password" VARCHAR NOT NULL,
    "user_id" SERIAL PRIMARY KEY
) WITH (oids = false);
