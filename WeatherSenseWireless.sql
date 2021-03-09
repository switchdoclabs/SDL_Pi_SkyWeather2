-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 30, 2021 at 10:00 AM
-- Server version: 10.3.23-MariaDB-0+deb10u1
-- PHP Version: 7.3.19-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `WeatherSenseWireless`
--
CREATE DATABASE IF NOT EXISTS `WeatherSenseWireless` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `WeatherSenseWireless`;

-- --------------------------------------------------------

--
-- Table structure for table `AQI433MHZ`
--

CREATE TABLE `AQI433MHZ` (
  `ID` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `messageID` int(11) NOT NULL,
  `deviceid` int(11) NOT NULL,
  `protocolversion` int(11) NOT NULL,
  `softwareversion` int(11) NOT NULL,
  `weathersenseprotocol` int(11) NOT NULL,
  `PM1_0S` int(11) NOT NULL,
  `PM2_5S` int(11) NOT NULL,
  `PM10S` int(11) NOT NULL,
  `PM1_0A` int(11) NOT NULL,
  `PM2_5A` int(11) NOT NULL,
  `PM10A` int(11) NOT NULL,
  `AQI` int(11) NOT NULL,
  `AQI24Hour` float NOT NULL,
  `batteryvoltage` float NOT NULL,
  `batterycurrent` float NOT NULL,
  `loadvoltage` float NOT NULL,
  `loadcurrent` float NOT NULL,
  `solarvoltage` float NOT NULL,
  `solarcurrent` float NOT NULL,
  `auxa` int(11) NOT NULL,
  `batterycharge` float NOT NULL,
  `batterypower` float NOT NULL,
  `loadpower` float NOT NULL,
  `solarpower` float NOT NULL,
  `test` text NOT NULL,
  `testdescription` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Generic`
--

CREATE TABLE `Generic` (
  `id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `messageID` int(11) NOT NULL,
  `deviceid` int(11) NOT NULL,
  `protocolversion` int(11) NOT NULL,
  `softwareversion` int(11) NOT NULL,
  `weathersenseprotocol` int(11) NOT NULL,
  `data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `IndoorTHSensors`
--

CREATE TABLE `IndoorTHSensors` (
  `id` int(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `DeviceID` int(11) NOT NULL,
  `ChannelID` int(11) NOT NULL,
  `Temperature` float NOT NULL,
  `Humidity` int(11) NOT NULL,
  `BatteryOK` text NOT NULL,
  `TimeRead` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------


--
-- Table structure for table `SolarMax433MHZ`
--

CREATE TABLE `SolarMax433MHZ` (
  `ID` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `messageID` int(11) NOT NULL,
  `deviceid` int(11) NOT NULL,
  `protocolversion` int(11) NOT NULL,
  `softwareversion` int(11) NOT NULL,
  `weathersenseprotocol` int(11) NOT NULL,
  `batteryvoltage` float NOT NULL,
  `batterycurrent` float NOT NULL,
  `loadvoltage` float NOT NULL,
  `loadcurrent` float NOT NULL,
  `solarvoltage` float NOT NULL,
  `solarcurrent` float NOT NULL,
  `auxa` int(11) NOT NULL,
  `internaltemperature` float NOT NULL,
  `internalhumidity` float NOT NULL,
  `batterycharge` float NOT NULL,
  `batterypower` float NOT NULL,
  `loadpower` float NOT NULL,
  `solarpower` float NOT NULL,
  `test` text NOT NULL,
  `testdescription` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `TB433MHZ`
--

CREATE TABLE `TB433MHZ` (
  `ID` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `messageID` int(11) NOT NULL,
  `deviceid` int(11) NOT NULL,
  `protocolversion` int(11) NOT NULL,
  `softwareversion` int(11) NOT NULL,
  `weathersenseprotocol` int(11) NOT NULL,
  `irqsource` int(11) NOT NULL,
  `previousinterruptresult` int(11) NOT NULL,
  `lightninglastdistance` int(11) NOT NULL,
  `sparebyte` int(11) NOT NULL,
  `lightningcount` int(11) NOT NULL,
  `interruptcount` int(11) NOT NULL,
  `batteryvoltage` float NOT NULL,
  `batterycurrent` float NOT NULL,
  `loadvoltage` float NOT NULL,
  `loadcurrent` float NOT NULL,
  `solarvoltage` float NOT NULL,
  `solarcurrent` float NOT NULL,
  `auxa` int(11) NOT NULL,
  `batterycharge` float NOT NULL,
  `batterypower` float NOT NULL,
  `loadpower` float NOT NULL,
  `solarpower` float NOT NULL,
  `test` text NOT NULL,
  `testdescription` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `WeatherData`
--

CREATE TABLE `WeatherData` (
  `ID` int(11) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
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
-- Indexes for table `AQI433MHZ`
--
ALTER TABLE `AQI433MHZ`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Generic`
--
ALTER TABLE `Generic`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `IndoorTHSensors`
--
ALTER TABLE `IndoorTHSensors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `SolarMax433MHZ`
--
ALTER TABLE `SolarMax433MHZ`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `TB433MHZ`
--
ALTER TABLE `TB433MHZ`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `WeatherData`
--
ALTER TABLE `WeatherData`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `AQI433MHZ`
--
ALTER TABLE `AQI433MHZ`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Generic`
--
ALTER TABLE `Generic`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `IndoorTHSensors`
--
ALTER TABLE `IndoorTHSensors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


--
-- AUTO_INCREMENT for table `SolarMax433MHZ`
--
ALTER TABLE `SolarMax433MHZ`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `TB433MHZ`
--
ALTER TABLE `TB433MHZ`
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
