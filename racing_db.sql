-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 15, 2025 at 04:46 PM
-- Server version: 8.0.41-0ubuntu0.20.04.1
-- PHP Version: 7.4.3-4ubuntu2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `racing_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `circuit`
--

CREATE TABLE `circuit` (
  `circuit_id` int NOT NULL,
  `circuit_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `country_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `sorting_order` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `circuit`
--

INSERT INTO `circuit` (`circuit_id`, `circuit_name`, `country_name`, `image_url`, `sorting_order`) VALUES
(0, 'Melbourne', 'Australia', 'Australia', 2),
(1, 'Paul Ricard', 'France', 'France', 24),
(2, 'Shanghai', 'China', 'China', 4),
(3, 'Sakhir', 'Bahrain', 'Bahrain', 0),
(4, 'Barcelona', 'Spain', 'Spain', 9),
(5, 'Monaco', 'Monaco', 'Monaco', 7),
(6, 'Montreal', 'Canada', 'Canada', 8),
(7, 'Silverstone', 'Great Britain', 'UnitedKingdom', 11),
(8, 'Hockenheim', 'Germany', 'Germany', 25),
(9, 'Hungaroring', 'Hungary', 'Hungary', 12),
(10, 'Spa Francorchamps', 'Belgium', 'Belgium', 13),
(11, 'Monza', 'Italy', 'Italy', 15),
(12, 'Singapore', 'Singapore', 'Singapore', 17),
(13, 'Suzuka', 'Japan', 'Japan', 3),
(14, 'Abu Dhabi', 'Abu Dhabi', 'UAE', 23),
(15, 'Austin', 'USA', 'UnitedStates', 18),
(16, 'Sao Paulo', 'Brazil', 'Brazil', 20),
(17, 'Red Bull Ring', 'Austria', 'Austria', 10),
(18, 'Sochi', 'Russia', 'Russia', 26),
(19, 'Mexico City', 'Mexico', 'Mexico', 19),
(20, 'Baku', 'Azerbaijan', 'Azerbaijan', 16),
(21, 'Sakhir Short', 'Bahrain', 'Bahrain', 27),
(22, 'Silverstone Short', 'Great Britain', 'UnitedKingdom', 28),
(23, 'COTA Short', 'Texas', 'UnitedStates', 29),
(24, 'Suzuka Short', 'Japan', 'Japan', 30),
(25, 'Hanoi', 'Vietnam', 'Vietnam', 31),
(26, 'Zandvoort', 'Netherlands', 'Netherlands', 14),
(27, 'Imola', 'Emilia Romagna', 'Italy', 6),
(28, 'Portimão', 'Portugal', 'Portugal', 32),
(29, 'Jeddah', 'Saudi Arabia', 'SaudiArabia', 1),
(30, 'Miami', 'Miami', 'UnitedStates', 5),
(31, 'Las Vegas', 'USA', 'UnitedStates', 21),
(32, 'Losail', 'Qatar', 'Qatar', 22);

-- --------------------------------------------------------

--
-- Table structure for table `news`
--

CREATE TABLE `news` (
  `news_id` int NOT NULL,
  `player_id` int NOT NULL,
  `circuit_id` int NOT NULL,
  `timest` int NOT NULL,
  `lap_time` int NOT NULL,
  `is_best_update` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `players`
--

CREATE TABLE `players` (
  `player_id` int NOT NULL,
  `display_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `times`
--

CREATE TABLE `times` (
  `player_id_fk` int NOT NULL,
  `circuit_id_fk` int NOT NULL,
  `best_time` int NOT NULL,
  `sector_one` int NOT NULL,
  `sector_two` int NOT NULL,
  `sector_three` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `circuit`
--
ALTER TABLE `circuit`
  ADD PRIMARY KEY (`circuit_id`);

--
-- Indexes for table `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`news_id`),
  ADD KEY `player_id` (`player_id`),
  ADD KEY `circuit_id` (`circuit_id`);

--
-- Indexes for table `players`
--
ALTER TABLE `players`
  ADD PRIMARY KEY (`display_name`),
  ADD UNIQUE KEY `display_name` (`display_name`),
  ADD UNIQUE KEY `player_id` (`player_id`),
  ADD KEY `player_id_2` (`player_id`),
  ADD KEY `player_id_3` (`player_id`);

--
-- Indexes for table `times`
--
ALTER TABLE `times`
  ADD PRIMARY KEY (`player_id_fk`,`circuit_id_fk`),
  ADD KEY `circuit_time` (`circuit_id_fk`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `news`
--
ALTER TABLE `news`
  MODIFY `news_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `players`
--
ALTER TABLE `players`
  MODIFY `player_id` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `times`
--
ALTER TABLE `times`
  ADD CONSTRAINT `circuit_time` FOREIGN KEY (`circuit_id_fk`) REFERENCES `circuit` (`circuit_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `player_time` FOREIGN KEY (`player_id_fk`) REFERENCES `players` (`player_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
