-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 17-03-2025 a las 07:07:09
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `qlocuri`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('94006b7186b4');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE `pedido` (
  `id` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  `producto_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `ubicacion` varchar(255) NOT NULL,
  `metodo_pago` enum('EFECTIVO','NEQUI','DAVIPLATA') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedido`
--

INSERT INTO `pedido` (`id`, `fecha`, `producto_id`, `usuario_id`, `ubicacion`, `metodo_pago`) VALUES
(5, '2025-03-17 04:29:30', 1, 1, 'usme', 'EFECTIVO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `precio` float NOT NULL,
  `categoria` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `precio`, `categoria`) VALUES
(1, 'Doriloco', 10000, 'Dela casa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reporte_pedido`
--

CREATE TABLE `reporte_pedido` (
  `id` int(11) NOT NULL,
  `hora_salida` time NOT NULL,
  `hora_llegada` time NOT NULL,
  `precio_total` float NOT NULL,
  `pedido_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `nombre` enum('CLIENTE','DOMICILIARIO','ADMINISTRADOR') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `nombre`) VALUES
(1, 'CLIENTE'),
(3, 'DOMICILIARIO'),
(4, 'ADMINISTRADOR');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contrasena_hash` varchar(255) NOT NULL,
  `rol_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `contrasena_hash`, `rol_id`) VALUES
(1, 'Adrian David', 'adrian@gmail.com', 'scrypt:32768:8:1$MqBnsVobvJIvMRYC$6e885ea3be08d21d4bf0f971b7081c15cd138c1b347851d4dac2c3cdb0cfaf0d53e109cb1c2b93bd1a773044637dffc1b8b8d01f831444dac5854fa607e2ce48', 1),
(2, 'Brayan ', 'brayan@gmail.com', 'scrypt:32768:8:1$U0ygaNpjUvI0xZRb$614eb250bbbc9c231bd98ea55837d1cbcaa7420bfbfbf2b770fa06c73f023750aeb5076cdb6bbe44b8454deee8c187284198549d77bd5dae1d4549afd051c20e', 3),
(3, 'Dillan', 'dillan@gmail.com', 'scrypt:32768:8:1$Fw7PbJn73PyD0ZYH$71db855fdee5e5928e37c8283d686351bc9b776ac88d56908553a409e2aa3925bf36fbf9ecd48243a8da710b727b31b5ff454d755e5b8e66264af2e7512a97d6', 4),
(4, 'johan ', 'johan@gmail.com', 'scrypt:32768:8:1$HxXwDSJC1O8oyFe2$16b7be98ae93bb57f89e9e57bf9bb243eb2fa9a314cca95c6afff1f3cebbfb185b85a0f2633931f799fad8da176865848dfb0bf0ca4942921f50ce4d2d292110', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indices de la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `reporte_pedido`
--
ALTER TABLE `reporte_pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pedido_id` (`pedido_id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `rol_id` (`rol_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `reporte_pedido`
--
ALTER TABLE `reporte_pedido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `reporte_pedido`
--
ALTER TABLE `reporte_pedido`
  ADD CONSTRAINT `reporte_pedido_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
