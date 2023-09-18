use mibasededatos;
describe cuentas;
describe transacciones;
select * from cuentas;
select * from transacciones;

-- *********Cuentas*****************************
INSERT INTO cuentas (nombreCliente, saldo) 
VALUES ('Adelina Rios Martell', 100.00);

INSERT INTO cuentas (nombreCliente, saldo) 
VALUES ('Alfredo Perez Quiñonez', 200.00);

INSERT INTO cuentas (nombreCliente, saldo) 
VALUES ('Carmen Dessire Gozales Bibiesca', 300.00);

INSERT INTO cuentas (nombreCliente, saldo) 
VALUES ('Daniela Heredia Tolumes ', 400.00);

INSERT INTO cuentas (nombreCliente, saldo) 
VALUES ('Heidi Fernanda Figueroa de la Torre', 500.00);

INSERT INTO cuentas (nombreCliente, saldo) 
VALUES ('Jose Adrian Paredes Villanueva', 600.00);

INSERT INTO cuentas (nombreCliente, saldo) 
VALUES ('Jose Manuel Pedro Mendez', 700.00);

INSERT INTO cuentas (nombreCliente, saldo) 
VALUES ('karina Ramirez Galindo', 800.00);

INSERT INTO cuentas (nombreCliente, saldo) 
VALUES ('Yexalen Cruz Hernandez', 900.00);

INSERT INTO cuentas (nombreCliente, saldo) 
VALUES ('Juan Perez Avila', 1000.00);

-- *********** Transacciones ***********************
INSERT INTO transacciones (IDCuenta, Tipo, Monto, Fecha)
VALUES (1,'deposito',250.50,(str_to_date("2023-09-18","%Y-%m-%d")));

INSERT INTO transacciones (IDCuenta, Tipo, Monto, Fecha)
VALUES (2,'transferencia',350.50,(str_to_date("2023-09-17","%Y-%m-%d")));

INSERT INTO transacciones (IDCuenta, Tipo, Monto, Fecha)
VALUES (3,'deposito',450.50,(str_to_date("2023-09-16","%Y-%m-%d")));

INSERT INTO transacciones (IDCuenta, Tipo, Monto, Fecha)
VALUES (4,'transferencia',550.50,(str_to_date("2023-09-16","%Y-%m-%d")));

INSERT INTO transacciones (IDCuenta, Tipo, Monto, Fecha)
VALUES (5,'deposito',650.50,(str_to_date("2023-09-15","%Y-%m-%d")));

INSERT INTO transacciones (IDCuenta, Tipo, Monto, Fecha)
VALUES (6,'transferencia',750.50,(str_to_date("2023-09-14","%Y-%m-%d")));

INSERT INTO transacciones (IDCuenta, Tipo, Monto, Fecha)
VALUES (7,'deposito',250.50,(str_to_date("2023-09-18","%Y-%m-%d")));

INSERT INTO transacciones (IDCuenta, Tipo, Monto, Fecha)
VALUES (8,'deposito',250.50,(str_to_date("2023-09-18","%Y-%m-%d")));

INSERT INTO transacciones (IDCuenta, Tipo, Monto, Fecha)
VALUES (9,'deposito',250.50,(str_to_date("2023-09-18","%Y-%m-%d")));

INSERT INTO transacciones (IDCuenta, Tipo, Monto, Fecha)
VALUES (10,'transferencia',950.50,(str_to_date("2023-09-13","%Y-%m-%d")));
