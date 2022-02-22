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
  KEY `comment_FK_1` (`tweet_id`),
  KEY `comment_FK` (`user_id`),
  CONSTRAINT `comment_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweet_like` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
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
  `follower_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `follows_un` (`follower_id`,`user_id`),
  KEY `follow_FK` (`user_id`),
  CONSTRAINT `follow_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follow_FK_1` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follow`
--

LOCK TABLES `follow` WRITE;
/*!40000 ALTER TABLE `follow` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (1,'dI1K41mAMTFBcNbjQ2Fc1hzZMWX4Vhbg4OfZXmdha7QT6VXc5JDslpC_u_ERcPqSmzB0kQ9hHNKv6q88KAIi2Q',1606,'2022-02-21 15:59:38'),(2,'Sl57g0K7TGt-1HKyQKj6t3am13H3rJzKdfWCzM7NFUJYMHdt4UkFIo_ljLONrNRk5roUaoYMgrCmt5u0HeWRaA',1610,'2022-02-21 16:07:59'),(3,'momZgXMgp2eTG4V_YTpZZcVI9vGa3WhY8iPgo2AYDxQ_X3hsceavMDteWg1P5VvdA1yD6001B4HVSbD3YDc6Qw',1611,'2022-02-21 16:32:15'),(4,'rcNwsXhGBeredzwtewFiHqrDdnG4GDsXmWeXvYTOocInGl--DHY3t523fl_JGyM8hkwohO7mWrPvDh-Yxs-aOg',1613,'2022-02-21 16:44:22'),(5,'XKTvdfRnLoXKbqQhFHGrRwY9YiD8Jy4AearAN06Pfz552Urd7dc9plvX7iMx6E5ZNixlGnmTMOz9534bgrpTmQ',1614,'2022-02-21 16:48:28'),(6,'tBlJ7h9VYzZER21UEVRSxhqLKOygLL5nd_YD8vDpXNPhgOVLhlI1GMTyKSRT8ezjoHr49KTplB8dVpvzf6-Xtg',1615,'2022-02-21 17:53:59'),(7,'1XMdnkTR1J9ONiexFLmN5eu6U_s9zXpdy8oQUeAPFYiQ9Iv4YBlbiu8Am8o4z4S52XYPdPVVmr9KCiCdr2wbnQ',1616,'2022-02-21 17:57:55'),(8,'xVJCKIDx6NfdCj0Jo662HNidNfku2niCvSYu4Hts6VviBEkNRpoXOSKVc2HdKRw1c7MTJSC1Pu3K_RtKhgGDUw',1620,'2022-02-21 18:03:07'),(9,'ocxCGEEcpCAvoTgOQUobEZEqGqZxDV3ulyQe5_BPBz3KKpGo5rJzzKnR9mGGw6gF6RcyuaftJRB9HVkSDRkzUQ',1621,'2022-02-21 18:34:34'),(10,'K5SNA6_8peAnBRRvt6kyK14_rBzjGxyEgD5v2pCPuCN_Hoyz3iwIyB4vJjEDlL71Fw9GlyRO5OzIjGuJ20Z6Vg',1628,'2022-02-21 18:53:24');
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
  `content` varchar(150) NOT NULL,
  `image_url` varchar(150) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `tweet_FK` (`user_id`),
  CONSTRAINT `tweet_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet`
--

LOCK TABLES `tweet` WRITE;
/*!40000 ALTER TABLE `tweet` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet_like`
--

LOCK TABLES `tweet_like` WRITE;
/*!40000 ALTER TABLE `tweet_like` DISABLE KEYS */;
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
  UNIQUE KEY `users_un` (`username`),
  UNIQUE KEY `user_un` (`email`),
  CONSTRAINT `user_check` CHECK (`username`  not like '% %' and year(`created_at`) - year(`birthdate`) > 13)
) ENGINE=InnoDB AUTO_INCREMENT=1629 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1601,'testUser','dkjfa;gheo;hagjdl;agjdhoanekjh;iohabkh','1970-01-01','default image link','default banner url link','2022-02-21 13:10:38','random@email.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1602,'badUsername','bio insert here','2008-04-04','default image link','default banner url link','2022-02-21 15:52:40','random3@email.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1603,'baddUsername','bio insert here','2008-04-04','default image link','default banner url link','2022-02-21 15:55:02','rando3m3@email.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1605,'baddUsername0','bio insert here','2008-04-04','default image link','default banner url link','2022-02-21 15:57:16','ranrdo3m3@email.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1606,'editPostmanUsr','change biotoo','2008-04-04','default image link','default banner url link','2022-02-21 15:59:36','newemail@email.domain','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1607,'baddUsername2','bio insert here','2008-04-04','default image link','default banner url link','2022-02-21 16:00:49','ranrdo3m3@femgail.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1610,'baddUsername3','bio insert here','2008-04-04','default image link','default banner url link','2022-02-21 16:07:51','ranro3m3@femgail.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1611,'baddUsername4','this is a long bio!','2007-04-04','default image link','default banner url link','2022-02-21 16:32:15','random@esfmail.com','21e5d6a1efed429c523d1de1255f30091b2fb63d5c92a2a530ad28b0463db795d216aa3bb3895052ef01399d867208b993bccf65b0483021152fa37ec2062923','eDukaUz-asT5gw'),(1613,'testUsername','this is a long bio!','2004-04-04','https://images.unsplash.com/photo-1644094877479-facb0d5fc7da?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80','default banner url link','2022-02-21 16:44:22','random2@esfmail.com','5386fc05bfde57de7629f7c47b07bdbc0f4aa40c581f8269d053e403394f329e1a991dd06a5905bfeb85bddf12b1dc1a3e6a0ba9691b565878ec2ed02c1aee05','aG57UnJ030oHpw'),(1614,'testUsername2','this is a long bio!','2004-04-04','default image url profile','default image url for banner','2022-02-21 16:48:28','random21@esfmail.com','26c00cab81f4812ed1066037da7509cf63fcc487d8ad97192d0ef5e24e45bf071651e7033eb3ce24219e68b8e955119757ea140c46f6a5a9f284b99c650d4af1','2AdP-QpQI6hPaQ'),(1615,'testUsername22','this is a long bio!','2004-04-04','default image link','default banner url link','2022-02-21 17:53:59','random221@esfmail.com','d1a039a71ca4fdcdfd9d541f46842ea418c518264e3b594d292094f8c95c54c9723866ba82133f9ab22f8f908fd4ed6d61000e5f3d88c425e6d594b9ff855c93','bqOeYS9GtI_lhw'),(1616,'newTestUser','bio','1999-09-09','default image link','default banner url link','2022-02-21 17:57:55','newUser@email.com','password','salt'),(1620,'testUsername212','this is a long bio!','2004-04-04','https://images.unsplash.com/photo-1644094877479-facb0d5fc7da?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80','default banner url link','2022-02-21 18:03:07','random221@fmail.com','952b9453bbcb9c8265bec45401c28f00d3f473c25a9d97ac181576e839fda587ddf9b40295b73bd6bc0c93d493b736a55ad39101cdeef974c93cee4795f1d7d4','IDsF44exrBTElg'),(1621,'testUsername112','this is a long bio!','2004-04-04','default image link','https://images.unsplash.com/photo-1644094877479-facb0d5fc7da?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80','2022-02-21 18:34:34','random1221@fmail.com','5453ea98c8bf02379759abf71fa8be2e5b6b20fe51dbb23b81cb5994d6589f41bd3b6bee9b06f57414c154f971e04004b5751a2361efbc736e8533b77edf2303','ncvHK-VrOCG3Gg'),(1628,'testUsername111','this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio! this is a long bio!','2004-04-04','default image link','https://images.unsplash.com/photo-1644094877479-facb0d5fc7da?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80','2022-02-21 18:53:24','random12121@efmail.com','aca7b0a74b070b495b51b61bde44dbfa5d69a953ec5eb99fc6e7cfb7d5909a4fff441ec63a4a832fb02ffec48e09a19591155c984009721ef8f13fbec3cc9c21','OapPPLbkAKaoQw');
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

-- Dump completed on 2022-02-21 21:50:39
