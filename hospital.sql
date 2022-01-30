CREATE DATABASE IF NOT EXISTS hospital;
USE hospital;

DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS testDesc;
DROP TABLE IF EXISTS tests;
DROP TABLE IF EXISTS record;
DROP TABLE IF EXISTS nursealloc;
DROP TABLE IF EXISTS nurse;
DROP TABLE IF EXISTS specialization;
DROP TABLE IF EXISTS dose;
DROP TABLE IF EXISTS medicines;
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
availableDate date ,
PRIMARY KEY (docMailId)
);

CREATE TABLE appointment(
mailId varchar(20) NOT NULL,
appointmentDate date NOT NULL,
docMailId varchar(20) NOT NULL,
PRIMARY KEY(mailId, appointmentDate, docMailid),
FOREIGN KEY (mailId) REFERENCES patient(mailId),
FOREIGN KEY (docMailId) REFERENCES doctor(docMailId)
);

CREATE TABLE medicines(
medicineId varchar(6) PRIMARY KEY,
medicineName varchar(30) NOT NULL
);

CREATE TABLE dose(
mailId varchar(20) NOT NULL,
medicineId varchar(6) NOT NULL,
quantity numeric(3) NOT NULL,
doseDate date NOT NULL,
PRIMARY KEY(mailId, medicineId, doseDate),
FOREIGN KEY (medicineId) REFERENCES medicines(medicineId),
FOREIGN KEY (mailId) REFERENCES patient(mailId)
);

CREATE TABLE specialization(
docMailId varchar(20) NOT NULL,
specialization varchar(6) NOT NULL,
PRIMARY KEY(docMailId, specialization),
FOREIGN KEY(docMailId) REFERENCES doctor(docMailId)
);

CREATE TABLE nurse(
nurseId int NOT NULL,
nurseName varchar(20) NOT NULL,
phoneNumber numeric(10) NOT NULL,
availableDate date,
PRIMARY KEY (nurseId)
);

CREATE TABLE nursealloc(
docMailId varchar(20) NOT NULL,
nurseId int NOT NULL,
mailId varchar(20) NOT NULL,
dateIn date NOT NULL,
dateOut date,
PRIMARY KEY(mailId,dateIn),
FOREIGN KEY (mailId) REFERENCES patient(mailId),
FOREIGN KEY (nurseId) REFERENCES nurse(nurseId),
FOREIGN KEY (docMailId) REFERENCES doctor(docMailId)
);

CREATE TABLE record(
mailId varchar(20) NOT NULL,
recordId int PRIMARY KEY,
Analysis text,
FOREIGN KEY(mailId) REFERENCES patient(mailId)
);

CREATE TABLE tests(
testId int PRIMARY KEY,
testName varchar(20) NOT NULL
);

CREATE TABLE testDesc(
mailId varchar(20) NOT NULL,
testId int NOT NULL,
testDate date,
Analysis text,
PRIMARY KEY(mailId, testId, testDate),
FOREIGN KEY (testId) REFERENCES tests(testId),
FOREIGN KEY (mailId) REFERENCES patient(mailId)
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
  ('5@gmail.com','0000','Roxy','1972-11-04','AB+','M'),
  ('6@gmail.com','0000','Rohan','1977-10-18','B+','M'),
  ('7@gmail.com','0000','Arjun','1975-10-15','A+','M'),
  ('8@gmail.com','0000','Ajay','1976-11-27','O+','M'),
  ('9@gmail.com','0000','Sankalp','1983-11-08','O+','F');
  
INSERT INTO medicines(medicineId, medicineName)
VALUES
  (1,'Phenolphatline'),
  (2,'Paracetomal'),
  (3,'Lysonamic'),
  (4,'Aquathacin'),
  (5,'Amioramine'),
  (6,'Caffeicor'),
  (7,'Fragnuma'),
  (8,'Vitrarabine');
  
INSERT INTO doctor(docMailid, passwd, docName, availableDate) 
VALUES
  ('dr1@gmail.com','0000','Preethi','2021-11-12'),
  ('dr2@gmail.com','0000','Shreesha','2021-11-12'),
  ('dr3@gmail.com','0000','Varun','2020-11-14'),
  ('dr4@gmail.com','0000','Suhas','2020-10-12'),
  ('dr5@gmail.com','0000','Jessie','2020-11-08'),
  ('dr6@gmail.com','0000','James','2020-10-12'),
  ('dr7@gmail.com','0000','Toby','2020-11-21'),
  ('dr8@gmail.com','0000','Rahul','2020-12-12'),
  ('dr9@gmail.com','0000','Naveen','2020-08-12');

INSERT INTO nurse(nurseId, nurseName, phoneNumber) 
VALUES
  (400000,'Manasa',9247775899),
  (400001,'Anagha',9246665899),
  (400002,'Jothi',9245555899),
  (400003,'Emily',9244445899),
  (400004,'Shivani',9241115899),
  (400005,'Dia',9274775899),
  (400006,'Demetria',9249975899),
  (400007,'Sabina',9247775999);

INSERT INTO appointment(mailId, appointmentDate, docMailId) 
VALUES
  ('0@gmail.com','2020-11-12','dr1@gmail.com'),
  ('a@gmail.com','2020-10-12','dr2@gmail.com');

INSERT INTO tests(testId, testName) 
VALUES
  (600000,'blood test'),
  (600001,'urine test'),
  (600002,'X ray'),
  (600003,'MRI scan'),
  (600004,'diabetic test'),
  (600005,'HIV test'),
  (600006,'covid19 test'),
  (600007,'wbc test');

INSERT INTO record VALUES
  ('1@gmail.com', 1, 'The Patient is fine'),
  ('1@gmail.com', 2, 'The Patient Physically fine, but requires psychological therapy');
