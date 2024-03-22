BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "budget" (
	"budget_id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"budget_name"	TEXT NOT NULL,
	"budget_amount"	INTEGER NOT NULL,
	"budget_category"	TEXT,
	"budget_status"	INTEGER NOT NULL DEFAULT 0,
	"date"	TEXT,
	"time"	TEXT,
	"expense_limit"	INTEGER NOT NULL,
	"archived"	TEXT NOT NULL DEFAULT 'no',
	PRIMARY KEY("budget_id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "registration"("user_id")
);
INSERT INTO "budget" ("budget_id","user_id","budget_name","budget_amount","budget_category","budget_status","date","time","expense_limit","archived") VALUES (1,1,'bud 1',770000,NULL,700000,'19/3/2024','10:32:8',700000,'no'),
 (2,1,'sd',50000,'Grocery',5780,'19/3/2024','11:27:50',7500,'no');
COMMIT;
