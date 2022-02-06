CREATE DATABASE IF NOT EXISTS hospital;
USE hospital;

DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS diagnosis;
DROP TABLE IF EXISTS test;
DROP TABLE IF EXISTS record;
DROP TABLE IF EXISTS nursealloc;
DROP TABLE IF EXISTS nurse;
DROP TABLE IF EXISTS specialization;
DROP TABLE IF EXISTS dosage;
DROP TABLE IF EXISTS medicine;
DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS doctor;
DROP TABLE IF EXISTS patient;

CREATE TABLE patient(
mailId varchar(20),
passwd varchar(20) NOT NULL,
Pname varchar(30) NOT NULL,
dob date NOT NULL,
bloodGroup varchar(3) NOT NULL,
sex char(1) NOT NULL,
PRIMARY KEY (mailId)
);

CREATE TABLE doctor(
docMailId varchar(20),
passwd varchar(20) NOT NULL,
docName varchar(30) NOT NULL,
sex char(1) NOT NULL,
availableDate date ,
PRIMARY KEY (docMailId)
);

CREATE TABLE appointment(
mailId varchar(20) NOT NULL,
appointmentDate date NOT NULL,
docMailId varchar(20) NOT NULL,
PRIMARY KEY(mailId, appointmentDate, docMailid),
FOREIGN KEY (mailId) REFERENCES patient(mailId) ON DELETE CASCADE,
FOREIGN KEY (docMailId) REFERENCES doctor(docMailId) ON DELETE CASCADE
);

CREATE TABLE medicine(
medicineId varchar(6) PRIMARY KEY,
medicineName varchar(30) NOT NULL
);

CREATE TABLE dosage(
mailId varchar(20) NOT NULL,
medicineId varchar(6) NOT NULL,
quantity numeric(3) NOT NULL,
doseDate date NOT NULL,
PRIMARY KEY(mailId, medicineId, doseDate),
FOREIGN KEY (medicineId) REFERENCES medicine(medicineId) ON DELETE CASCADE,
FOREIGN KEY (mailId) REFERENCES patient(mailId) ON DELETE CASCADE
);

CREATE TABLE specialization(
docMailId varchar(20) NOT NULL,
specialization varchar(6) NOT NULL,
PRIMARY KEY(docMailId, specialization),
FOREIGN KEY(docMailId) REFERENCES doctor(docMailId) ON DELETE CASCADE
);

CREATE TABLE nurse(
nurseId varchar(20) PRIMARY KEY,
nurseName varchar(20) NOT NULL,
phoneNumber numeric(10) NOT NULL,
availableDate date
);

CREATE TABLE nursealloc(
nurseId varchar(20) NOT NULL,
mailId varchar(20) NOT NULL,
dateIn date NOT NULL,
dateOut date,
PRIMARY KEY(mailId, dateIn),
FOREIGN KEY (mailId) REFERENCES patient(mailId) ON DELETE CASCADE,
FOREIGN KEY (nurseId) REFERENCES nurse(nurseId) ON DELETE CASCADE
);

CREATE TABLE record(
mailId varchar(20) NOT NULL,
recordId int auto_increment PRIMARY KEY,
Analysis text,
FOREIGN KEY (mailId) REFERENCES patient(mailId) ON DELETE CASCADE
);

CREATE TABLE test(
testId int auto_increment PRIMARY KEY,
testName varchar(20) NOT NULL,
testCategory varchar(20)
);

CREATE TABLE diagnosis(
mailId varchar(20) NOT NULL,
testId int NOT NULL,
testDate date NOT NULL,
analysis text,
PRIMARY KEY(mailId, testId, testDate),
FOREIGN KEY (testId) REFERENCES test(testId) ON DELETE CASCADE,
FOREIGN KEY (mailId) REFERENCES patient(mailId) ON DELETE CASCADE
);

CREATE TABLE admin(
mailId varchar(20) PRIMARY KEY,
passwd varchar(20),
adminName varchar(20)
);

INSERT INTO admin(mailId, passwd, adminName)
VALUES
  ('a1@gmail.com','0000','Pushpa'),
  ('a2@gmail.com','0000','Rocky'),
  ('a3@gmail.com','0000','Ram');

INSERT INTO patient(mailId, passwd, PName, dob, bloodGroup, sex)
VALUES
  ('0@gmail.com','0000','Abhay','1988-09-05','O+','M'),
  ('a@gmail.com','0000','Shaan','1988-12-10','O+','F'),
  ('1@gmail.com','0000','John','1995-11-14','O+','M'),
  ('2@gmail.com','0000','Dubravka','1998-06-26','B+','M'),
  ('3@gmail.com','0000','Fabio','2007-05-22','O+','F'),
  ('4@gmail.com','0000','Freddy','2007-05-22','O+','M'),
  ('5@gmail.com','0000','Roxy','1972-11-04','AB+','F'),
  ('6@gmail.com','0000','Rohan','1977-10-18','B+','M'),
  ('7@gmail.com','0000','Arjun','1975-10-15','A+','M'),
  ('8@gmail.com','0000','Ajay','1976-11-27','O+','M'),
  ('9@gmail.com','0000','Sankalp','1983-11-08','O+','F');
  
INSERT INTO medicine(medicineId, medicineName)
VALUES
  (1,'Phenolphatline'),
  (2,'Paracetomal'),
  (3,'Lysonamic'),
  (4,'Aquathacin'),
  (5,'Amioramine'),
  (6,'Caffeicor'),
  (7,'Fragnuma'),
  (8,'Vitrarabine');
  
INSERT INTO doctor(docMailid, passwd, docName, sex) 
VALUES
  ('dr1@gmail.com','0000','Preethi','F'),
  ('dr2@gmail.com','0000','Shreesha','M'),
  ('dr3@gmail.com','0000','Varun','M'),
  ('dr4@gmail.com','0000','Suhas','M'),
  ('dr5@gmail.com','0000','Jessie','F'),
  ('dr6@gmail.com','0000','James','M'),
  ('dr7@gmail.com','0000','Toby','M'),
  ('dr8@gmail.com','0000','Norn','F'),
  ('dr9@gmail.com','0000','Naveen','M');

INSERT INTO nurse(nurseId, nurseName, phoneNumber) 
VALUES
  ('n0@hp.com','Manasa',9247775899),
  ('n1@hp.com','Anagha',9246665899),
  ('n2@hp.com','Jothi',9245555899),
  ('n3@hp.com','Emily',9244445899),
  ('n4@hp.com','Shivani',9241115899),
  ('n5@hp.com','Dia',9274775899),
  ('n6@hp.com','Demetria',9249975899),
  ('n7@hp.com','Sabina',9247775999);

INSERT INTO appointment(mailId, appointmentDate, docMailId) 
VALUES
  ('0@gmail.com','2020-11-12','dr1@gmail.com'),
  ('a@gmail.com','2020-10-12','dr2@gmail.com');

INSERT INTO test(testId, testName, testCategory) 
VALUES
  (1, 'Haemoglobin', 'Blood'),
  (2, 'Cranium', 'CT'),
  (3, 'Femur', 'X-Ray'),
  (4, 'Brain Scan','MRI'),
  (5, 'Sugar', 'Blood');

INSERT INTO record VALUES
  ('1@gmail.com', 1, 'The Patient is fine'),
  ('1@gmail.com', 2, 'The Patient Physically fine, but requires psychological therapy');
