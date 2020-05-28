DROP DATABASE IF EXISTS technoatom;
CREATE DATABASE technoatom;
USE technoatom;
CREATE TABLE IF NOT EXISTS `test_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(16) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(64) NOT NULL,
  `access` smallint DEFAULT NULL,
  `active` smallint DEFAULT NULL,
  `start_active_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `ix_test_users_username` (`username`)
);
INSERT INTO test_users (username, password, email, access, active, start_active_time) values ('ADMIN_USER', 'ADMIN', 'ADM@IN.IN', 1, 1, CURDATE());
commit;