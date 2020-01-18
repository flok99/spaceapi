CREATE TABLE `spaces` (
  `key` varchar(32) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `url` text DEFAULT NULL,
  `logo` text NOT NULL,
  `get_ok` int(6) NOT NULL DEFAULT 0,
  `get_err` int(6) NOT NULL DEFAULT 0,
  `get_total` int(6) NOT NULL DEFAULT 0,
  `sa` text NOT NULL DEFAULT '',
  `lns` tinyint(1) NOT NULL DEFAULT 0,
  `timezone` varchar(32) DEFAULT NULL,
  `timezone_long` text DEFAULT NULL,
  `offset` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
