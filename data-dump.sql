-- MariaDB dump 10.17  Distrib 10.4.7-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: evant
-- ------------------------------------------------------
-- Server version	10.4.7-MariaDB-1:10.4.7+maria~bionic

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('8885a3295859');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `preference` varchar(100) NOT NULL,
  `category` varchar(100) NOT NULL,
  PRIMARY KEY (`preference`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES ('Bogor','hiking'),('Cafes','eat'),('Dinner','eat'),('Jakarta','vacation'),('Kuala Lumpur','hiking'),('Medan','vacation'),('Surakarta','vacation');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dates`
--

DROP TABLE IF EXISTS `dates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dates` (
  `user_id` int(11) NOT NULL,
  `date` varchar(25) NOT NULL,
  PRIMARY KEY (`user_id`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dates`
--

LOCK TABLES `dates` WRITE;
/*!40000 ALTER TABLE `dates` DISABLE KEYS */;
INSERT INTO `dates` VALUES (1,'27/09/2019'),(1,'28/09/2019'),(2,'27/09/2019'),(2,'28/09/2019'),(2,'29/09/2019'),(4,'03/10/2019'),(5,'03/10/2019'),(5,'04/10/2019'),(6,'03/10/2019'),(6,'04/10/2019');
/*!40000 ALTER TABLE `dates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `creator_id` int(11) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `event_name` varchar(100) NOT NULL,
  `start_date_parameter` varchar(100) DEFAULT NULL,
  `end_date_parameter` varchar(100) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `status` int(11) NOT NULL,
  `place_name` varchar(100) DEFAULT NULL,
  `place_location` varchar(100) DEFAULT NULL,
  `start_date` varchar(100) DEFAULT NULL,
  `end_date` varchar(100) DEFAULT NULL,
  `preference` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,1,'LIBURAN','jalan-jalan ke mall','2019-09-26','2019-10-03',3,0,NULL,NULL,NULL,NULL,'cultural'),(2,2,'MAKAN','pingin makan-makan','2019/09/26','2019/10/03',2,0,NULL,NULL,NULL,NULL,'Dinner'),(3,1,'LIBURAN','Pingin Liburan ke Bali','2019/09/26','2019/10/03',3,0,NULL,NULL,NULL,NULL,NULL),(5,5,'eat','liburan keals alta','01/10/2019','04/10/2019',2,0,'WAKI Japanese BBQ Dining','Lantai 1, Jl. Tanjung Karang No. 5, Thamrin, Jakarta','01/10/2019','02/10/2019','Cafes'),(6,5,'eat','asfdgfg','05/10/2019','10/10/2019',2,0,'','','01/10/2019','01/10/2019','Cafes');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invitations`
--

DROP TABLE IF EXISTS `invitations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `invitations` (
  `event_id` int(11) NOT NULL,
  `invited_id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`event_id`,`invited_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invitations`
--

LOCK TABLES `invitations` WRITE;
/*!40000 ALTER TABLE `invitations` DISABLE KEYS */;
INSERT INTO `invitations` VALUES (1,1,0),(2,2,0),(3,5,0),(5,4,1),(6,4,0),(6,6,0);
/*!40000 ALTER TABLE `invitations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_preferences`
--

DROP TABLE IF EXISTS `user_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_preferences` (
  `user_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `preference` varchar(50) NOT NULL,
  `confirmation` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_preferences`
--

LOCK TABLES `user_preferences` WRITE;
/*!40000 ALTER TABLE `user_preferences` DISABLE KEYS */;
INSERT INTO `user_preferences` VALUES (1,1,'cultural',0),(1,2,'Dinner',0),(2,1,'cultural',0),(2,2,'Dinner',0),(4,4,'Bogor',0),(4,5,'Cafes',1),(5,4,'Dinner',0),(5,5,'Dinner',1),(5,6,'Cafes',-1),(6,4,'Dinner',0),(6,5,'Cafes',-1);
/*!40000 ALTER TABLE `user_preferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `gender` tinyint(1) DEFAULT NULL,
  `status_first_login` tinyint(1) DEFAULT NULL,
  `fullname` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`gender` in (0,1)),
  CONSTRAINT `CONSTRAINT_2` CHECK (`status_first_login` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'tes2','tes2@tes2.com','$5$rounds=535000$vlAebaAHbAwbkksu$9C2xbeY2yVv8D/t9ieo/RMdh1TrkyUmcRYhajT79SZ6',1,1,'tes2','tes2','08560123456'),(5,'tes3','tes3@tes3.com','$5$rounds=535000$2TVtPaZVHEKzueS3$lxMlNjMeS8gwjw2pL4k643q9U/zsgYQc4T0tFmU4aY9',1,1,'tes3','tes3','01234567890'),(6,'tes4','tes4@tes4.com','$5$rounds=535000$nBWgmbkfyKKm.PO0$Ll8YRKogZZ5W//B8eKovvGuurabxCF4Xwkba7/2E.YA',0,1,'tes4','tes4','1234567890'),(7,'tes5','tes5@tes5.com','$5$rounds=535000$a6lomuJ5i3hpE7Kg$eKumyD2lcX9WUo6lWTvo5D9uRAmsncSn6MOgH7.ShU7',1,1,'tes5','tes5','1234567890');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-16 16:53:14
