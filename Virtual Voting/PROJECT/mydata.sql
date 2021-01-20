CREATE TABLE `user` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT ;

CREATE TABLE `admin` (
  `aid` int  NOT NULL,
  `adminname` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `admin`
  ADD PRIMARY KEY (`aid`);

ALTER TABLE `admin`
  MODIFY `aid` int NOT NULL AUTO_INCREMENT ; 

CREATE TABLE `post` (
  `pid` int  NOT NULL,
  `name` varchar(80) NOT NULL
  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `post`
  ADD PRIMARY KEY (`pid`),
  ADD UNIQUE KEY `name` (`name`);

INSERT INTO `post` (`pid`, `name`) VALUES
(1, 'President');
INSERT INTO `post` (`pid`, `name`) VALUES
(4, 'Vice President');
INSERT INTO `post` (`pid`, `name`) VALUES
(2, 'Secretary');
INSERT INTO `post` (`pid`, `name`) VALUES
(3, 'Treasurer');

CREATE TABLE `candidate` (
  `email` varchar(80) NOT NULL,
  `username` varchar(80) NOT NULL,
  `pid` int NOT NULL,
  PRIMARY KEY (`email`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 


CREATE TABLE `vote` (
  `vid` int NOT NULL,
  `username` varchar(80) NOT NULL,
   PRIMARY KEY (`vid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

DELIMITER $$
CREATE TRIGGER del_cand
AFTER DELETE ON candidate
FOR EACH ROW BEGIN
INSERT INTO cand_deleted VALUES(OLD.email);
END $$
  
COMMIT;  