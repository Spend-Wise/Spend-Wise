CREATE TABLE "registration" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"first_name"	TEXT NOT NULL,
	"last_name"	TEXT,
	"email"	TEXT NOT NULL,
	"username"	TEXT,
	"password"	TEXT NOT NULL,
	"sec_que"	TEXT,
	"sec_que_ans"	TEXT,
	"sqa_tog"	TEXT NOT NULL DEFAULT 'off',
	"tfa_tog"	TEXT NOT NULL DEFAULT 'off',
	"valid_email"	INTEGER NOT NULL DEFAULT 0,
	"user_type"	TEXT NOT NULL DEFAULT 'user',
	"valid_user"	INTEGER NOT NULL DEFAULT 0,
	"secret_key"	TEXT,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);
