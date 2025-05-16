CREATE DATABASE IF NOT EXISTS banca;
USE banca;

DROP TABLE IF EXISTS conturi;  -- opțional, pentru a recrea tabela curat

CREATE TABLE conturi (
    id_cont INT AUTO_INCREMENT PRIMARY KEY,
    nume VARCHAR(255) NOT NULL,
    parola VARCHAR(255) NOT NULL,
    tip ENUM('curent', 'depozit') NOT NULL,
    sold DECIMAL(10, 2) DEFAULT 0,
    rol ENUM('client', 'admin') NOT NULL DEFAULT 'client'
);

INSERT INTO conturi (nume, parola, tip, sold, rol) VALUES
('ana', '1234', 'curent', 500.00, 'admin'),
('bogdan', 'abcd', 'depozit', 1200.00, 'client'),
('maria', 'qwerty', 'curent', 1000.00, 'client'),
('ion', 'password', 'depozit', 2000.00, 'client'),
('ionel', 'alex12942', 'depozit', 2000.00, 'client');

-- Exemplu de interogări
SELECT * FROM conturi WHERE nume = 'ionel' AND parola = 'alex12942';
SELECT * FROM conturi;
SELECT * FROM conturi WHERE id_cont = 3;
