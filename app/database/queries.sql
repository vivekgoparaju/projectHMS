CREATE TABLE "admin" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"password"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)

CREATE TABLE "doctors" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"specialization"	TEXT,
	"other"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"mail"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);