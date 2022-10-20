-- MySQL dump 10.13  Distrib 8.0.29, for macos12 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Coach`
--

DROP TABLE IF EXISTS `Coach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Coach` (
  `tgname` varchar(32) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Qulification_Type` varchar(32) NOT NULL,
  `Sport_Type` varchar(32) NOT NULL,
  `MainCoach_tgname` varchar(32) NOT NULL,
  PRIMARY KEY (`tgname`,`Qulification_Type`,`Sport_Type`,`MainCoach_tgname`),
  KEY `fk_Coach_Qulification1_idx` (`Qulification_Type`),
  KEY `fk_Coach_Sport1_idx` (`Sport_Type`),
  KEY `fk_Coach_MainCoach1_idx` (`MainCoach_tgname`),
  CONSTRAINT `fk_Coach_MainCoach1` FOREIGN KEY (`MainCoach_tgname`) REFERENCES `MainCoach` (`tgname`),
  CONSTRAINT `fk_Coach_Qulification1` FOREIGN KEY (`Qulification_Type`) REFERENCES `Qualification` (`Type`),
  CONSTRAINT `fk_Coach_Sport1` FOREIGN KEY (`Sport_Type`) REFERENCES `Sport` (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Coach`
--

LOCK TABLES `Coach` WRITE;
/*!40000 ALTER TABLE `Coach` DISABLE KEYS */;
/*!40000 ALTER TABLE `Coach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Coach_Training`
--

DROP TABLE IF EXISTS `Coach_Training`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Coach_Training` (
  `idTeam` int unsigned NOT NULL AUTO_INCREMENT,
  `Coach_tgname` varchar(32) NOT NULL,
  `Training_idTraining` int unsigned NOT NULL,
  PRIMARY KEY (`idTeam`,`Coach_tgname`,`Training_idTraining`),
  KEY `fk_Coach_Training_Coach1_idx` (`Coach_tgname`),
  KEY `fk_Coach_Training_Training1_idx` (`Training_idTraining`),
  CONSTRAINT `fk_Coach_Training_Coach1` FOREIGN KEY (`Coach_tgname`) REFERENCES `Coach` (`tgname`),
  CONSTRAINT `fk_Coach_Training_Training1` FOREIGN KEY (`Training_idTraining`) REFERENCES `Training` (`idTraining`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Coach_Training`
--

LOCK TABLES `Coach_Training` WRITE;
/*!40000 ALTER TABLE `Coach_Training` DISABLE KEYS */;
/*!40000 ALTER TABLE `Coach_Training` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Gym`
--

DROP TABLE IF EXISTS `Gym`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Gym` (
  `Number` int unsigned NOT NULL,
  `StartTimeWorking` time NOT NULL,
  `FinishTimeWorking` time NOT NULL,
  PRIMARY KEY (`Number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gym`
--

LOCK TABLES `Gym` WRITE;
/*!40000 ALTER TABLE `Gym` DISABLE KEYS */;
/*!40000 ALTER TABLE `Gym` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MainCoach`
--

DROP TABLE IF EXISTS `MainCoach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MainCoach` (
  `tgname` varchar(32) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Qulification_Type` varchar(32) NOT NULL,
  `Sport_Type` varchar(32) NOT NULL,
  `SportDoctor_tgname` varchar(32) NOT NULL,
  PRIMARY KEY (`tgname`,`Qulification_Type`,`Sport_Type`,`SportDoctor_tgname`),
  KEY `fk_MainCoach_Qulification1_idx` (`Qulification_Type`),
  KEY `fk_MainCoach_Sport1_idx` (`Sport_Type`),
  KEY `fk_MainCoach_SportDoctor1_idx` (`SportDoctor_tgname`),
  CONSTRAINT `fk_MainCoach_Qulification1` FOREIGN KEY (`Qulification_Type`) REFERENCES `Qualification` (`Type`),
  CONSTRAINT `fk_MainCoach_Sport1` FOREIGN KEY (`Sport_Type`) REFERENCES `Sport` (`Type`),
  CONSTRAINT `fk_MainCoach_SportDoctor1` FOREIGN KEY (`SportDoctor_tgname`) REFERENCES `SportDoctor` (`tgname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MainCoach`
--

LOCK TABLES `MainCoach` WRITE;
/*!40000 ALTER TABLE `MainCoach` DISABLE KEYS */;
/*!40000 ALTER TABLE `MainCoach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Qualification`
--

DROP TABLE IF EXISTS `Qualification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Qualification` (
  `Type` varchar(32) NOT NULL,
  PRIMARY KEY (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Qualification`
--

LOCK TABLES `Qualification` WRITE;
/*!40000 ALTER TABLE `Qualification` DISABLE KEYS */;
/*!40000 ALTER TABLE `Qualification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sport`
--

DROP TABLE IF EXISTS `Sport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sport` (
  `Type` varchar(32) NOT NULL,
  PRIMARY KEY (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sport`
--

LOCK TABLES `Sport` WRITE;
/*!40000 ALTER TABLE `Sport` DISABLE KEYS */;
/*!40000 ALTER TABLE `Sport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SportDoctor`
--

DROP TABLE IF EXISTS `SportDoctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SportDoctor` (
  `tgname` varchar(32) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Qualification` varchar(45) NOT NULL,
  PRIMARY KEY (`tgname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SportDoctor`
--

LOCK TABLES `SportDoctor` WRITE;
/*!40000 ALTER TABLE `SportDoctor` DISABLE KEYS */;
/*!40000 ALTER TABLE `SportDoctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sportsmen`
--

DROP TABLE IF EXISTS `Sportsmen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sportsmen` (
  `tgname` varchar(32) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Sport_Type` varchar(32) NOT NULL,
  `SportDoctor_tgname` varchar(32) NOT NULL,
  PRIMARY KEY (`tgname`,`Sport_Type`,`SportDoctor_tgname`),
  KEY `fk_Sportsmen_Sport1_idx` (`Sport_Type`),
  KEY `fk_Sportsmen_SportDoctor1_idx` (`SportDoctor_tgname`),
  CONSTRAINT `fk_Sportsmen_Sport1` FOREIGN KEY (`Sport_Type`) REFERENCES `Sport` (`Type`),
  CONSTRAINT `fk_Sportsmen_SportDoctor1` FOREIGN KEY (`SportDoctor_tgname`) REFERENCES `SportDoctor` (`tgname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sportsmen`
--

LOCK TABLES `Sportsmen` WRITE;
/*!40000 ALTER TABLE `Sportsmen` DISABLE KEYS */;
/*!40000 ALTER TABLE `Sportsmen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Trainer`
--

DROP TABLE IF EXISTS `Trainer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Trainer` (
  `Type` varchar(32) NOT NULL,
  PRIMARY KEY (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Trainer`
--

LOCK TABLES `Trainer` WRITE;
/*!40000 ALTER TABLE `Trainer` DISABLE KEYS */;
/*!40000 ALTER TABLE `Trainer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TrainerInGym`
--

DROP TABLE IF EXISTS `TrainerInGym`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TrainerInGym` (
  `idTrainer` int unsigned NOT NULL AUTO_INCREMENT,
  `Trainer_Type` varchar(32) NOT NULL,
  `Gym_Number` int unsigned NOT NULL,
  PRIMARY KEY (`idTrainer`,`Trainer_Type`,`Gym_Number`),
  KEY `fk_TrainerInGym_Trainer1_idx` (`Trainer_Type`),
  KEY `fk_TrainerInGym_Gym1_idx` (`Gym_Number`),
  CONSTRAINT `fk_TrainerInGym_Gym1` FOREIGN KEY (`Gym_Number`) REFERENCES `Gym` (`Number`),
  CONSTRAINT `fk_TrainerInGym_Trainer1` FOREIGN KEY (`Trainer_Type`) REFERENCES `Trainer` (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TrainerInGym`
--

LOCK TABLES `TrainerInGym` WRITE;
/*!40000 ALTER TABLE `TrainerInGym` DISABLE KEYS */;
/*!40000 ALTER TABLE `TrainerInGym` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Training`
--

DROP TABLE IF EXISTS `Training`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Training` (
  `idTraining` int unsigned NOT NULL AUTO_INCREMENT,
  `Gym_Number` int unsigned NOT NULL,
  `StartTime` datetime NOT NULL,
  `FinishTime` datetime NOT NULL,
  `TrainerInGym_idTrainer` int unsigned DEFAULT NULL,
  `Sportsmen_tgname` varchar(32) NOT NULL,
  `MainCoach_tgname` varchar(32) NOT NULL,
  PRIMARY KEY (`idTraining`,`Gym_Number`,`Sportsmen_tgname`),
  KEY `fk_Training_Gym1_idx` (`Gym_Number`),
  KEY `fk_Training_TrainerInGym1_idx` (`TrainerInGym_idTrainer`),
  KEY `fk_Training_Sportsmen1_idx` (`Sportsmen_tgname`),
  KEY `fk_Training_MainCoach1_idx` (`MainCoach_tgname`),
  CONSTRAINT `fk_Training_Gym1` FOREIGN KEY (`Gym_Number`) REFERENCES `Gym` (`Number`),
  CONSTRAINT `fk_Training_MainCoach1` FOREIGN KEY (`MainCoach_tgname`) REFERENCES `MainCoach` (`tgname`),
  CONSTRAINT `fk_Training_Sportsmen1` FOREIGN KEY (`Sportsmen_tgname`) REFERENCES `Sportsmen` (`tgname`),
  CONSTRAINT `fk_Training_TrainerInGym1` FOREIGN KEY (`TrainerInGym_idTrainer`) REFERENCES `TrainerInGym` (`idTrainer`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Training`
--

LOCK TABLES `Training` WRITE;
/*!40000 ALTER TABLE `Training` DISABLE KEYS */;
/*!40000 ALTER TABLE `Training` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-15 16:14:06
