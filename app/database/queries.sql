CREATE TABLE IF NOT EXISTS "admin" (
	"id"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "doctors" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"email" TEXT,
	"password" TEXT NOT NULL,
	"specialization"	TEXT,
	"phone"	TEXT,
	"img_url" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"email"	TEXT,
	"phone" TEXT,
	"location" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "appointments" (
    "id" INTEGER NOT NULL UNIQUE,
    "patient_id" INTEGER NOT NULL,
    "doctor_id" INTEGER NOT NULL,
    "date" TEXT NOT NULL,
    "time" TEXT NOT NULL,
    "status" TEXT DEFAULT 'pending',
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("patient_id") REFERENCES "users"("id"),
    FOREIGN KEY("doctor_id") REFERENCES "doctors"("id")
);

CREATE TABLE IF NOT EXISTS "medical_history" (
    "id" INTEGER NOT NULL UNIQUE,
    "patient_id" INTEGER NOT NULL,
    "doctor_id" INTEGER NOT NULL,
    "date" TEXT NOT NULL,
    "diagnosis" TEXT NOT NULL,
    "prescription" TEXT,
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("patient_id") REFERENCES "users"("id"),
    FOREIGN KEY("doctor_id") REFERENCES "doctors"("id")
);