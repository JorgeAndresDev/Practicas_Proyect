-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS app_empresa_bd
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

-- Usar la base de datos
USE app_empresa_bd;

-- Eliminar la tabla 'users' si existe
DROP TABLE IF EXISTS `users`;

-- Crear la tabla 'users'
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name_surname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email_user` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL UNIQUE,
  `pass_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_user` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Eliminar la tabla 'tbl_empleados' si existe
DROP TABLE IF EXISTS `tbl_empleados`;

-- Crear la tabla 'tbl_empleados'
CREATE TABLE `tbl_empleados` (
  `CC` int NOT NULL,
  `NOM` varchar(100),
  `CAR` varchar(100),
  `CENTRO` varchar(100),
  `CASH` varchar(100),
  `SAC` varchar(100),
  `CHECK` varchar(100),
  `MOD` varchar(100),
  `ER` varchar(100),
  `PARADAS` varchar(100),
  `PERFORMANCE` varchar(100),
  PRIMARY KEY (`CC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
