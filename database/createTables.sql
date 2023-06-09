CREATE TABLE "games" (
	"id" serial NOT NULL,
	"home_player" varchar NOT NULL,
	"away_player" varchar NOT NULL,
	"home_score" integer NOT NULL,
	"away_score" integer NOT NULL,
	CONSTRAINT "games_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "players" (
	"name" varchar NOT NULL,
	CONSTRAINT "players_pk" PRIMARY KEY ("name")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "games" ADD CONSTRAINT "games_fk0" FOREIGN KEY ("home_player") REFERENCES "players"("name");
ALTER TABLE "games" ADD CONSTRAINT "games_fk1" FOREIGN KEY ("away_player") REFERENCES "players"("name");