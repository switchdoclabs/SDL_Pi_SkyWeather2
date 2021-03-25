-- column only set at insert
alter table WeatherData change column `TimeStamp` `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp();
