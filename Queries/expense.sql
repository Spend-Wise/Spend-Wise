CREATE TABLE "expense" (
	"expense_id"	INTEGER NOT NULL UNIQUE,
	"budget_id"	INTEGER NOT NULL,
	"expense_name"	TEXT NOT NULL,
	"expense_amount"	INTEGER NOT NULL,
	"expense_category"	TEXT,
	PRIMARY KEY("expense_id" AUTOINCREMENT),
	FOREIGN KEY("budget_id") REFERENCES "budget"("budget_id")
);