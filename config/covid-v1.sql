--- Countries Table
CREATE TABLE `countries` (
  `Country` varchar(200) NOT NULL,
  `Slug` varchar(200) NOT NULL,
  `ISO2` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--- Countries daily summary

CREATE TABLE `dailysummary` (
  `ID` varchar(50) NOT NULL,
  `Country` varchar(50) NOT NULL,
  `CoutryCode` varchar(2) NOT NULL,
  `Slug` varchar(50) NOT NULL,
  `NewConfirmed` bigint(20) NOT NULL,
  `TotalConfirmed` bigint(20) NOT NULL,
  `NewDeaths` bigint(20) NOT NULL,
  `TotalDeaths` bigint(20) NOT NULL,
  `NewRecovered` bigint(20) NOT NULL,
  `TotalRecovered` bigint(20) NOT NULL,
  `Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--- Perform dumb testing if needed.