CREATE TEMPORARY TABLE `test`.`temptable_calldata_temptable` (
  `callsign` varchar(20) DEFAULT NULL,
  `aliases` text DEFAULT NULL,
  `trustee` text DEFAULT NULL,
  `nickname` text DEFAULT NULL,
  `firstname` text DEFAULT NULL,
  `lastname` text DEFAULT NULL,
  `grid` varchar(6) DEFAULT NULL,
  `lattitude` text DEFAULT NULL,
  `longitude` text DEFAULT NULL,
  `ituzone` int(32) DEFAULT NULL,
  `cqzone` int(32) DEFAULT NULL,
  `dxcc` int(32) DEFAULT NULL,
  `county` text DEFAULT NULL,
  `continent` text DEFAULT NULL,
  `street1` text DEFAULT NULL,
  `city` text DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `postalcode` varchar(80) DEFAULT NULL,
  `country` text DEFAULT NULL,
  `licclass` text DEFAULT NULL,
  `qrz_email` text DEFAULT NULL,
  `email` text DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `fullname` text GENERATED ALWAYS AS
        (if(`firstname` is null and `lastname` is null and `nickname` is null,NULL,
        concat(if(`nickname` is null,if(`firstname` is null,'',concat(`firstname`,' ')),
        concat(`nickname`,' ')),'',if(`lastname` is null,'',`lastname`))))
        VIRTUAL,
  `location` text GENERATED ALWAYS AS
        (if(`country` is null,'',if(`country` = 'United States' or `country` = 'USA',concat(`state`,', USA'),`country`)))
        VIRTUAL,
  PRIMARY KEY (`callsign`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
COMMENT='Details from QRZ and other sources for each callsign'
;
