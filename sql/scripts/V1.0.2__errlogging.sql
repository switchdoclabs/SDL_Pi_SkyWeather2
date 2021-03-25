-- TEC trap and log errors
CREATE TABLE `error_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `message` varchar(128) NOT NULL,
  `error` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
