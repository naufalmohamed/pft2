CREATE TABLE IF NOT EXISTS therapist_cred (
    id SERIAL PRIMARY KEY NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(18) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL
);

INSERT INTO therapist_cred (email,password,first_name,last_name) VALUES ('ramu@dubakoor.com','Ramu@123','Ramu','Lal');

