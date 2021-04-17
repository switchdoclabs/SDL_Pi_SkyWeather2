-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 27, 2020 at 03:41 PM
-- Server version: 10.3.25-MariaDB-0+deb10u1
-- PHP Version: 7.3.19-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS SkyWeather2;

USE SkyWeather2;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `SkyWeather2`
--

-- --------------------------------------------------------

--
-- Table structure for table `IndoorTHSensors`
--

CREATE TABLE `IndoorTHSensors` (
  `id` int(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(), 
  `DeviceID` int(11) NOT NULL,
  `ChannelID` int(11) NOT NULL,
  `Temperature` float NOT NULL,
  `Humidity` int(11) NOT NULL,
  `BatteryOK` text NOT NULL,
  `TimeRead` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `PowerSystem`
--

CREATE TABLE `PowerSystem` (
  `ID` int(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `batteryVoltage` float NOT NULL,
  `batteryCurrent` float NOT NULL,
  `solarVoltage` float NOT NULL,
  `solarCurrent` float NOT NULL,
  `loadVoltage` float NOT NULL,
  `loadCurrent` float NOT NULL,
  `batteryPower` float NOT NULL,
  `solarPower` float NOT NULL,
  `loadPower` float NOT NULL,
  `batteryCharge` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `SystemLog`
--

CREATE TABLE `SystemLog` (
  `ID` int(11) NOT NULL,
  `Level` int(11) NOT NULL,
  `SystemText` text NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `WeatherData`
--

CREATE TABLE `WeatherData` (
  `ID` int(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ,
  `OutdoorTemperature` float NOT NULL,
  `OutdoorHumidity` float NOT NULL,
  `IndoorTemperature` float NOT NULL,
  `IndoorHumidity` float NOT NULL,
  `TotalRain` float NOT NULL,
  `SunlightVisible` float NOT NULL,
  `SunlightUVIndex` float NOT NULL,
  `WindGust` float NOT NULL,
  `WindDirection` float NOT NULL,
  `WindSpeed` float NOT NULL,
  `BarometricPressure` float NOT NULL,
  `BarometricPressureSeaLevel` float NOT NULL,
  `BarometricTemperature` float NOT NULL,
  `AQI` float NOT NULL,
  `AQI24Average` float NOT NULL DEFAULT 0,
  `BatteryOK` text NOT NULL,
  `CPUTemperature` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `IndoorTHSensors`
--
ALTER TABLE `IndoorTHSensors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `PowerSystem`
--
ALTER TABLE `PowerSystem`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `SystemLog`
--
ALTER TABLE `SystemLog`
  ADD KEY `ID` (`ID`);

--
-- Indexes for table `WeatherData`
--
ALTER TABLE `WeatherData`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `IndoorTHSensors`
--
ALTER TABLE `IndoorTHSensors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `PowerSystem`
--
ALTER TABLE `PowerSystem`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `SystemLog`
--
ALTER TABLE `SystemLog`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `WeatherData`
--
ALTER TABLE `WeatherData`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
