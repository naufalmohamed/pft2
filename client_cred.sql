CREATE TABLE IF NOT EXISTS client_cred (
    id SERIAL PRIMARY KEY NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(18) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    age VARCHAR(3),
    city VARCHAR(50),
    occupation VARCHAR(20),
    concerns VARCHAR,
    phonenumber VARCHAR(20),
    emergency_contact VARCHAR(20),
    relationship_status VARCHAR(15),
    status VARCHAR(15),
    therapist VARCHAR,
    timeperiod VARCHAR(50)
);


