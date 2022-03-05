-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: tweeter
-- ------------------------------------------------------
-- Server version	5.5.5-10.7.3-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` varchar(150) NOT NULL,
  `tweet_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `comment_FK` (`user_id`),
  KEY `comment_FK_1` (`tweet_id`),
  CONSTRAINT `comment_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweet` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (12,'POSTMAN UPDATE - I love this tweet so much!!',2,1615,'2022-03-03 15:59:59'),(13,'I love this tweet so much!!',2,1615,'2022-03-03 16:01:33'),(14,'I love this tweet so much!!',2,1615,'2022-03-03 16:02:21');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_like`
--

DROP TABLE IF EXISTS `comment_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment_like` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `comment_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_like_un` (`user_id`,`comment_id`),
  KEY `comment_like_FK` (`comment_id`),
  CONSTRAINT `comment_like_FK` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_like_FK_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_like`
--

LOCK TABLES `comment_like` WRITE;
/*!40000 ALTER TABLE `comment_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follow`
--

DROP TABLE IF EXISTS `follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follow` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `follow_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `follows_un` (`follow_id`,`user_id`),
  KEY `follow_FK` (`user_id`),
  CONSTRAINT `follow_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follow_FK_1` FOREIGN KEY (`follow_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `you_cant_follow_yourself` CHECK (`user_id` <> `follow_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follow`
--

LOCK TABLES `follow` WRITE;
/*!40000 ALTER TABLE `follow` DISABLE KEYS */;
INSERT INTO `follow` VALUES (32,1661,1601,'2022-03-01 14:39:10'),(35,1661,1614,'2022-03-01 14:39:54'),(36,1661,1615,'2022-03-01 14:40:00'),(37,1615,1661,'2022-03-01 15:21:41'),(39,1601,1661,'2022-03-01 15:21:52');
/*!40000 ALTER TABLE `follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `login_token` varchar(100) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_un` (`login_token`),
  KEY `login_FK` (`user_id`),
  CONSTRAINT `login_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (2,'Sl57g0K7TGt-1HKyQKj6t3am13H3rJzKdfWCzM7NFUJYMHdt4UkFIo_ljLONrNRk5roUaoYMgrCmt5u0HeWRaA',1610,'2022-02-21 16:07:59'),(4,'rcNwsXhGBeredzwtewFiHqrDdnG4GDsXmWeXvYTOocInGl--DHY3t523fl_JGyM8hkwohO7mWrPvDh-Yxs-aOg',1613,'2022-02-21 16:44:22'),(5,'XKTvdfRnLoXKbqQhFHGrRwY9YiD8Jy4AearAN06Pfz552Urd7dc9plvX7iMx6E5ZNixlGnmTMOz9534bgrpTmQ',1614,'2022-02-21 16:48:28'),(6,'tBlJ7h9VYzZER21UEVRSxhqLKOygLL5nd_YD8vDpXNPhgOVLhlI1GMTyKSRT8ezjoHr49KTplB8dVpvzf6-Xtg',1615,'2022-02-21 17:53:59'),(13,'UOFp7DPfck6n3p9WSW374Q_gRjypPQ4EZcRbGUjcygI1iPrjKCCsQNNvNvSK73-nCwZR-3vi3RvMWd3GXkZfzg',1656,'2022-02-22 19:38:46'),(19,'fOUgGozIbvXVEodxKHGrYD8ZvDQ6JAi1rhz7Bk6ThXQp-iyAeiZ_x-1JZo4IleLRJaX_eU2DTdUXJGwBOHu3Pg',1661,'2022-02-22 20:54:26'),(41,'ebICnrx_AXGuD6mdYrcm6W4q91RC_ScSASJSyf85zqxrOcS1RMhORyMvxZTI-MdOqOHDuBDWWgIrUJj4vCv9fA',1602,'2022-03-02 11:55:56'),(42,'JxXFn8R-A_zWFUicE5WjuJ0JcK408K3KRsHOzHqnaFgIbNUFjPbkWe5_FsXG0sk-Lb2l8YWDALvIMRsyxAH8qA',1602,'2022-03-02 11:56:56'),(43,'9BnawbWVNAGsHWh7f4ZSjTV7alwC4yRPxFwBG2QjGiN-FfAGaKo0AO2rOo8_UVA_6c3zTzHkR-6fNeKyZVJpSQ',1602,'2022-03-02 11:58:07');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet`
--

DROP TABLE IF EXISTS `tweet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `content` varchar(200) NOT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `tweet_FK` (`user_id`),
  CONSTRAINT `tweet_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet`
--

LOCK TABLES `tweet` WRITE;
/*!40000 ALTER TABLE `tweet` DISABLE KEYS */;
INSERT INTO `tweet` VALUES (1,1610,'This is the very first tweet in the system',NULL,'2022-03-01 19:28:44'),(2,1610,'This is the very first tweet in the system',NULL,'2022-03-01 19:34:12'),(3,1610,'This is the very first tweet in the system',NULL,'2022-03-01 19:34:36'),(4,1610,'This is the very first tweet in the system',NULL,'2022-03-01 19:36:36'),(5,1610,'This is the very first tweet in the system',NULL,'2022-03-01 19:37:41'),(6,1613,'no contents needed','tweet image url','2022-03-01 19:40:34');
/*!40000 ALTER TABLE `tweet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet_like`
--

DROP TABLE IF EXISTS `tweet_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_like` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tweet_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `tweet_like_un` (`tweet_id`,`user_id`),
  KEY `tweet_like_FK` (`user_id`),
  CONSTRAINT `tweet_like_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tweet_like_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweet` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet_like`
--

LOCK TABLES `tweet_like` WRITE;
/*!40000 ALTER TABLE `tweet_like` DISABLE KEYS */;
INSERT INTO `tweet_like` VALUES (4,2,1656,'2022-03-03 13:41:26');
/*!40000 ALTER TABLE `tweet_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(65) NOT NULL,
  `bio` varchar(255) NOT NULL,
  `birthdate` date NOT NULL,
  `imageUrl` varchar(500) NOT NULL DEFAULT 'default image link',
  `bannerUrl` varchar(500) NOT NULL DEFAULT 'default banner url link',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `email` varchar(100) NOT NULL,
  `password` varchar(150) NOT NULL DEFAULT '21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923',
  `salt` varchar(50) NOT NULL DEFAULT 'eDukaUz-asT5gw',
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_email_un` (`email`),
  UNIQUE KEY `usrname_un` (`username`),
  CONSTRAINT `birthdate_check` CHECK (year(`created_at`) - year(`birthdate`) > 13)
) ENGINE=InnoDB AUTO_INCREMENT=1666 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1601,'testUser','dkjfa;gheo;hagjdl;agjdhoanekjh;iohabkh','1970-01-01','default image link','default banner url link','2022-02-21 13:10:38','random@email.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1602,'badUsername','bio insert here','2008-04-04','default image link','default banner url link','2022-02-21 15:52:40','random3@email.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1603,'baddUsername','bio insert here','2008-04-04','default image link','default banner url link','2022-02-21 15:55:02','rando3m3@email.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1605,'baddUsername0','bio insert here','2008-04-04','default image link','default banner url link','2022-02-21 15:57:16','ranrdo3m3@email.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1607,'baddUsername2','bio insert here','2008-04-04','default image link','default banner url link','2022-02-21 16:00:49','ranrdo3m3@femgail.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1610,'baddUsername3','bio insert here','2008-04-04','default image link','default banner url link','2022-02-21 16:07:51','ranro3m3@femgail.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1613,'testUsername','this is a long bio!','2004-04-04','https://images.unsplash.com/photo-1644094877479-facb0d5fc7da?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80','default banner url link','2022-02-21 16:44:22','random2@esfmail.com','5386fc05bfde57de7629f7c47b07bdbc0f4aa40c581f8269d053e403394f329e1a991dd06a5905bfeb85bddf12b1dc1a3e6a0ba9691b565878ec2ed02c1aee05','aG57UnJ030oHpw'),(1614,'testUsername2','this is a long bio!','2004-04-04','default image url profile','default image url for banner','2022-02-21 16:48:28','random21@esfmail.com','26c00cab81f4812ed1066037da7509cf63fcc487d8ad97192d0ef5e24e45bf071651e7033eb3ce24219e68b8e955119757ea140c46f6a5a9f284b99c650d4af1','2AdP-QpQI6hPaQ'),(1615,'testUsername22','this is a long bio!','2004-04-04','default image link','default banner url link','2022-02-21 17:53:59','random221@esfmail.com','d1a039a71ca4fdcdfd9d541f46842ea418c518264e3b594d292094f8c95c54c9723866ba82133f9ab22f8f908fd4ed6d61000e5f3d88c425e6d594b9ff855c93','bqOeYS9GtI_lhw'),(1656,'testUsername111','this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio!','2004-04-04','default image link','https://images.unsplash.com/photo-1644094877479-facb0d5fc7da?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80','2022-02-22 19:38:46','random1212@efmail.com','8618570e29e3169e6ca033f277f1530532d17ddbad81761d338ec551c988239a36ae2d5739b95a489d6a6b1f7869997ebb4934a77eba446042989d8b452f5c73','ywfKoHuRUib7Jg'),(1661,'testUsername1111','this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio!','2004-04-04','default image link','https://images.unsplash.com/photo-1644094877479-facb0d5fc7da?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80','2022-02-22 20:54:26','random1212@efmail.coom','8bc49b59cc19d1fff5d28a47476d5cd69c7270824905b9dcac240004d9421b4403094f2397b5d52169b2f295206144f8489e0e5cb493fc0459641c08780402c8','Vtk2U65SBA7wkg');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'tweeter'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-03 21:06:28
