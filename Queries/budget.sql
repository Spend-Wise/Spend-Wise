CREATE TABLE "budget" (
	"budget_id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"budget_name"	TEXT NOT NULL,
	"budget_amount"	INTEGER NOT NULL,
	"budget_category"	TEXT,
	"budget_status"	INTEGER NOT NULL DEFAULT 0,
	"date"	TEXT,
	"time"	TEXT,
	PRIMARY KEY("budget_id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "registration"("user_id")
);