-- DROP DATABASE IF EXISTS `callbook`;

CREATE DATABASE IF NOT EXISTS `callbook`;

-- DROP TABLE IF EXISTS `callbook`.`callinfo`;

 CREATE TABLE IF NOT EXISTS `callbook`.`callinfo` (
  `callsign` varchar(20) NOT NULL COMMENT 'Current callsign',
  `prev_call` varchar(20) COMMENT 'Previous callsign',
  `trustee` text DEFAULT NULL,
  `aliases` text DEFAULT NULL COMMENT 'other identifiers',
  `querycall` text DEFAULT NULL COMMENT 'call used for callbook query that resoved to this call',
  `firstname` text DEFAULT NULL,
  `lastname` text DEFAULT NULL,
  `nickname` text DEFAULT NULL,
  `grid` varchar(6) DEFAULT NULL COMMENT 'maidenhead grid',
  `lattitude` text DEFAULT NULL,
  `longitude` text DEFAULT NULL,
  `ituzone` varchar(6) DEFAULT NULL,
  `cqzone` varchar(6) DEFAULT NULL,
  `dxcc` varchar(6) DEFAULT NULL COMMENT 'dxcc entity number',
  `dxcc_name` TEXt DEFAULT NULL COMMENT 'dxcc entity name',
  `county` text DEFAULT NULL COMMENT 'US county',
  `fips` text DEFAULT NULL COMMENT 'FIPS county identifier',
  `continent` text DEFAULT NULL,
  `utcoffset` text DEFAULT NULL COMMENT 'Timezone offset from UTC',
  `street1` text DEFAULT NULL,
  `street2` text DEFAULT NULL,
  `city` text DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL COMMENT 'US State or Province',
  `postalcode` varchar(80) DEFAULT NULL,
  `country` text DEFAULT NULL COMMENT 'Country used in mailing address',
  `ccode` text DEFAULT NULL COMMENT 'dxcc entity code for the mailing address country',
  `email` text DEFAULT NULL COMMENT 'personal/preferred email address',
  `qrz_email` text DEFAULT NULL COMMENT 'email address on QRZ',
  `licclass` text DEFAULT NULL,
  `birthyear` text DEFAULT NULL ,
  `areacode` text DEFAULT NULL,
  `timezone` text DEFAULT NULL,
  `qsldirect` text DEFAULT NULL,
  `buro` text DEFAULT NULL,
  `lotw` text DEFAULT NULL,
  `eqsl` text DEFAULT NULL,
  `expdate` text DEFAULT NULL COMMENt 'callsign expiration date',
  `biodate` text DEFAULT NULL COMMENT 'last QRZ bio update',
  `moddate` text DEFAULT NULL COMMENT 'last QRZ Modification date',
  `phone` varchar(20) DEFAULT NULL COMMENT 'phone number',
  `qsl_manager` text DEFAULT NULL COMMENT 'QSL manager info',
  `qrz_moddate` text DEFAULt NULL COMMENT 'last modification date of callsign on QRZ',
  `last_updated` timestamp DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP() COMMENT 'timestamp of last update from online callbook',



  `location` text GENERATED ALWAYS AS (
    if(`country` IS NULL,
       if(`dxcc_name` IS NULL,'',`dxcc_name`),
       if(`country` = 'United States' or `country` = 'USA',concat(`state`,', USA'),`country`))) 
       VIRTUAL 
       COMMENT 'generated location information'
       ,
  `fullname` text GENERATED ALWAYS AS (if(`firstname` is null and `lastname` is null and `nickname` is null,NULL,concat(if(`nickname` is null,if(`firstname` is null,'',concat(`firstname`,' ')),concat(`nickname`,' ')),'',if(`lastname` is null,'',`lastname`)))) VIRTUAL,
 
  PRIMARY KEY (`callsign`)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_general_ci 
COMMENT='Details from QRZ and other sources for each callsign'
;

-- DROP TABLE IF EXISTS `callbook`.`dxcc`;

CREATE TABLE IF NOT EXISTS callbook.dxcc
(
`dxcc`          INT(32) NOT NULL        COMMENT 'DXCC entity number for this record',
`cc`            VARCHAR(5) DEFAULT NULL COMMENT '2-letter country code (ISO-3166)',
`ccc`	          VARCHAR(5) DEFAULT NULL COMMENT '3-letter country code (ISO-3166)',
`dxcc_name`	    TEXT NOT NULL           COMMENT 'long name',
`continent`	    VARCHAR(5) DEFAULT NULL COMMENT '2-letter continent designator',
`ituzone`	      INT(32) DEFAULT NULL    COMMENT 'ITU Zone',
`cqzone`	      INT(32) DEFAULT NULL    COMMENT 'CQ Zone',
`utcoffset`     INT(32) DEFAULT NULL    COMMENT 'UTC timezone offset +/-',
`lattitude`     TEXT DEFAULT NULL       COMMENT 'Latitude (approx.)',
`longitude`     TEXT DEFAULT NULL       COMMENT 'Longitude (approx.)',
`notes`	        TEXT DEFAULT NULL       COMMENT 'Special notes and/or exceptions',
`last_updated` timestamp DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP() COMMENT 'timestamp of last update from online callbook',
PRIMARY KEY (`dxcc`)
) COMMENT='Contains information on DXCC entitities';
