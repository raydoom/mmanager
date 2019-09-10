# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 192.168.0.64 (MySQL 5.7.19)
# Database: mmanager
# Generation Time: 2019-04-30 06:43:43 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table app_action_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_action_log`;

CREATE TABLE `app_action_log` (
  `action_log_id` int(11) NOT NULL AUTO_INCREMENT,
  `log_time` datetime(6) NOT NULL,
  `log_user` varchar(50) NOT NULL,
  `log_detail` varchar(256) NOT NULL,
  PRIMARY KEY (`action_log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table app_container_info_cache
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_container_info_cache`;

CREATE TABLE `app_container_info_cache` (
  `container_info_cache_id` int(11) NOT NULL AUTO_INCREMENT,
  `host` varchar(128) NOT NULL DEFAULT '',
  `host_port` int(11) NOT NULL,
  `container_id` varchar(128) NOT NULL DEFAULT '',
  `image` varchar(128) NOT NULL DEFAULT '',
  `command` varchar(128) NOT NULL DEFAULT '',
  `created` varchar(128) NOT NULL DEFAULT '',
  `statename` varchar(128) NOT NULL DEFAULT '',
  `status` varchar(128) NOT NULL DEFAULT '',
  `port` varchar(128) NOT NULL DEFAULT '',
  `name` varchar(128) NOT NULL DEFAULT '',
  `current_user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`container_info_cache_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table app_job_info_cache
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_job_info_cache`;

CREATE TABLE `app_job_info_cache` (
  `job_info_cache_id` int(11) NOT NULL AUTO_INCREMENT,
  `host` varchar(128) DEFAULT '',
  `host_port_api` int(11) DEFAULT NULL,
  `color` varchar(128) DEFAULT '',
  `name` varchar(128) DEFAULT '',
  `host_protocal_api` varchar(128) DEFAULT NULL,
  `current_user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`job_info_cache_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table app_process_info_cache
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_process_info_cache`;

CREATE TABLE `app_process_info_cache` (
  `process_info_cache_id` int(11) NOT NULL AUTO_INCREMENT,
  `host` varchar(128) NOT NULL DEFAULT '',
  `host_port` int(11) NOT NULL,
  `statename` varchar(128) NOT NULL DEFAULT '',
  `name` varchar(128) NOT NULL DEFAULT '',
  `description` varchar(128) DEFAULT NULL,
  `current_user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`process_info_cache_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table app_server
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_server`;

CREATE TABLE `app_server` (
  `server_id` int(11) NOT NULL AUTO_INCREMENT,
  `host` varchar(50) NOT NULL DEFAULT '',
  `port` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `file_path_root` varchar(128) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `password_api` varchar(128) DEFAULT '',
  `username_api` varchar(50) DEFAULT '',
  `server_type_id` int(11) DEFAULT NULL,
  `port_api` int(11) DEFAULT NULL,
  `protocal_api` varchar(50) DEFAULT '',
  PRIMARY KEY (`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table app_server_info_cache
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_server_info_cache`;

CREATE TABLE `app_server_info_cache` (
  `server_info_cache_id` int(11) NOT NULL AUTO_INCREMENT,
  `server_id` int(11) DEFAULT NULL,
  `host` varchar(50) NOT NULL DEFAULT '',
  `port` int(11) NOT NULL,
  `server_type` varchar(50) NOT NULL,
  `description` varchar(128) NOT NULL,
  `port_api` int(11) DEFAULT NULL,
  `protocal_api` varchar(50) NOT NULL DEFAULT '',
  `status` varchar(50) NOT NULL DEFAULT '',
  `current_user_id` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`server_info_cache_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table app_server_type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_server_type`;

CREATE TABLE `app_server_type` (
  `server_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `server_type` varchar(50) NOT NULL,
  PRIMARY KEY (`server_type_id`),
  UNIQUE KEY `server_type` (`server_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table app_user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_user`;

CREATE TABLE `app_user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `email` varchar(128) NOT NULL,
  `role` varchar(32) DEFAULT NULL,
  `description` varchar(128) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `app_user_info_username_d91fc6b7_uniq` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_group
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_group_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_permission
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_user_groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_user_user_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_admin_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_content_type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_migrations
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_session
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- ----------------------------
-- Records of app_server_type
-- ----------------------------
INSERT INTO `app_server_type` VALUES (1, 'docker');
INSERT INTO `app_server_type` VALUES (3, 'jenkins');
INSERT INTO `app_server_type` VALUES (2, 'supervisor');
INSERT INTO `app_server_type` VALUES (4, 'file');
-- ----------------------------
-- Records of app_user
-- ----------------------------
INSERT INTO `app_user` VALUES (1, 'admin', 'pbkdf2_sha256$120000$KFtImf0nFm7v$qKB3DqkO5R23M9ffM1G33kdC/ZWgMnCsZSq4Bgkxdh0=', 'admin@localhost.com', 'admin', 'admin');
