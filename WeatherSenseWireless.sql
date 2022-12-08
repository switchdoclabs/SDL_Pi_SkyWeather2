-- phpMyAdmin SQL Dump

-- TimeStamp fix

alter table AQI433MHZ change column `TimeStamp` `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp();
alter table Generic change column `TimeStamp` `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp();
alter table IndoorTHSensors change column `TimeStamp` `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp();
alter table SolarMax433MHZ change column `TimeStamp` `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp();
alter table TB433MHZ change column `TimeStamp` `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp();
alter table WeatherData change column `TimeStamp` `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp();

-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 09, 2021 at 05:18 PM
-- Server version: 10.3.25-MariaDB-0+deb10u1
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

-- --------------------------------------------------------

--
-- Table structure for table `AS433MHZ`
--

CREATE TABLE IF NOT EXISTS `AS433MHZ` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `messageID` int(11) NOT NULL,
  `deviceid` int(11) NOT NULL,
  `protocolversion` int(11) NOT NULL,
  `softwareversion` int(11) NOT NULL,
  `weathersenseprotocol` int(11) NOT NULL,
  `eqcount` int(11) NOT NULL,
  `finaleq_si` float NOT NULL,
  `finaleq_pga` float NOT NULL,
  `instanteq_si` float NOT NULL,
  `instanteq_pga` float NOT NULL,
  `batteryvoltage` float NOT NULL,
  `batterycurrent` float NOT NULL,
  `loadvoltage` float NOT NULL,
  `loadcurrent` float NOT NULL,
  `solarvoltage` float NOT NULL,
  `solarcurrent` float NOT NULL,
  `auxa` int(11) NOT NULL,
  `solarpresent` int(11) NOT NULL,
  `aftershockpresent` int(11) NOT NULL,
  `keepalivemessage` int(11) NOT NULL,
  `lowbattery` int(11) NOT NULL,
  `batterycharge` float NOT NULL,
  `batterypower` float NOT NULL,
  `loadpower` float NOT NULL,
  `solarpower` float NOT NULL,
  `test` text NOT NULL,
  `testdescription` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


-- --------------------------------------------------------

--
-- Table structure for table `SkyCamPictures`
--

CREATE TABLE IF NOT EXISTS `SkyCamPictures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `messageID` int(11) NOT NULL DEFAULT -1,
  `cameraID` varchar(10) NOT NULL,
  `picturename` varchar(100) NOT NULL,
  `picturesize` int(11) NOT NULL,
  `resends` int(11) NOT NULL,
  `resolution` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


-- --------------------------------------------------------

--
-- Table structure for table `SkyCamSensors`
--

CREATE TABLE IF NOT EXISTS `SkyCamSensors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `cameraID` varchar(11) NOT NULL,
  `messageID` int(11) NOT NULL,
  `softwareversion` int(11) NOT NULL,
  `messagetype` int(11) NOT NULL,
  `rssi` int(11) NOT NULL,
  `internaltemperature` float NOT NULL,
  `internalhumidity` int(11) NOT NULL,
  `batteryvoltage` float NOT NULL,
  `batterycurrent` float NOT NULL,
  `loadvoltage` float NOT NULL,
  `loadcurrent` float NOT NULL,
  `solarvoltage` float NOT NULL,
  `solarcurrent` float NOT NULL,
  `batterypower` float NOT NULL,
  `loadpower` float NOT NULL,
  `solarpower` float NOT NULL,
  `gndrreboots` int(11) DEFAULT 0,
  `batterycharge` float DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------

--
-- Table structure for table `RAD433MHZ`
--

CREATE TABLE IF NOT EXISTS `RAD433MHZ` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `messageID` int(11) NOT NULL,
  `deviceid` int(11) NOT NULL,
  `protocolversion` int(11) NOT NULL,
  `softwareversion` int(11) NOT NULL,
  `weathersenseprotocol` int(11) NOT NULL,
  `CPM` int(11) NOT NULL,
  `nSVh` int(11) NOT NULL,
  `uSVh` float NOT NULL,
  `uSVh24Hour` float NOT NULL,
  `batteryvoltage` float NOT NULL,
  `batterycurrent` float NOT NULL,
  `loadvoltage` float NOT NULL,
  `loadcurrent` float NOT NULL,
  `solarvoltage` float NOT NULL,
  `solarcurrent` float NOT NULL,
  `auxa` int(11) NOT NULL,
  `keepalivemessage` int(11) NOT NULL,
  `lowbattery` int(11) NOT NULL,
  `solarpresent` int(11) NOT NULL,
  `radiationpresent` int(11) NOT NULL,
  `batterycharge` float NOT NULL,
  `batterypower` float NOT NULL,
  `loadpower` float NOT NULL,
  `solarpower` float NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

