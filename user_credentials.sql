CREATE TABLE user_credentials(
	username		varchar(40) PRIMARY KEY,
	password_hash	bytea NOT NULL,
	password_salt	bytea NOT NULL,
	grants			jsonb NOT NULL
);
