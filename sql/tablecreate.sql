-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: ustutor
-- ------------------------------------------------------
-- Server version	5.7.12

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `state` int(11) NOT NULL,
  `account_name` varchar(50) NOT NULL,
  `account_no` varchar(50) NOT NULL,
  `owner_role` int(11) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_control`
--

DROP TABLE IF EXISTS `acl_control`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_control` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sid` varchar(255) NOT NULL,
  `oid` varchar(255) NOT NULL,
  `ctrl` enum('FULLCTRL','ALLOWEDIT','ALLOWVIEW','NOTALLOW') NOT NULL DEFAULT 'FULLCTRL',
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_control`
--

LOCK TABLES `acl_control` WRITE;
/*!40000 ALTER TABLE `acl_control` DISABLE KEYS */;
/*!40000 ALTER TABLE `acl_control` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('a808e3458270');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attachment`
--

DROP TABLE IF EXISTS `attachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attachment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `attachment_type` int(11) DEFAULT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `mime_type` varchar(255) DEFAULT NULL,
  `url_path` varchar(255) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `meta_info` int(11) DEFAULT NULL,
  `content_type` varchar(50) DEFAULT NULL,
  `refer_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attachment`
--

LOCK TABLES `attachment` WRITE;
/*!40000 ALTER TABLE `attachment` DISABLE KEYS */;
/*!40000 ALTER TABLE `attachment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificate`
--

DROP TABLE IF EXISTS `certificate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `certificate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `cert_name` varchar(120) NOT NULL,
  `cert_desc` varchar(120) DEFAULT NULL,
  `cert_name_zh` varchar(120) DEFAULT NULL,
  `cert_desc_zh` varchar(120) DEFAULT NULL,
  `cert_level` varchar(120) DEFAULT NULL,
  `teacher_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `certificate_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificate`
--

LOCK TABLES `certificate` WRITE;
/*!40000 ALTER TABLE `certificate` DISABLE KEYS */;
/*!40000 ALTER TABLE `certificate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channel`
--

DROP TABLE IF EXISTS `channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `channel_name` varchar(255) NOT NULL,
  `channel_desc` varchar(255) DEFAULT NULL,
  `contact_tel` varchar(255) DEFAULT NULL,
  `contact_email` varchar(255) DEFAULT NULL,
  `contact_address` varchar(255) DEFAULT NULL,
  `logo_url` varchar(255) DEFAULT NULL,
  `domain_address` varchar(255) DEFAULT NULL,
  `service_helper` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `service_helper` (`service_helper`),
  CONSTRAINT `channel_ibfk_1` FOREIGN KEY (`service_helper`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channel`
--

LOCK TABLES `channel` WRITE;
/*!40000 ALTER TABLE `channel` DISABLE KEYS */;
/*!40000 ALTER TABLE `channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `course_name` varchar(120) NOT NULL,
  `course_name_zh` varchar(120) DEFAULT NULL,
  `course_type` int(11) NOT NULL,
  `class_type` int(11) NOT NULL,
  `classes_number` int(11) NOT NULL,
  `open_grade` varchar(120) DEFAULT NULL,
  `course_desc` varchar(120) DEFAULT NULL,
  `course_desc_zh` varchar(120) DEFAULT NULL,
  `difficult_level` int(11) DEFAULT NULL,
  `critical_level` int(11) DEFAULT NULL,
  `course_requirements` varchar(120) DEFAULT NULL,
  `course_requirements_zh` varchar(120) DEFAULT NULL,
  `state` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `primary_teacher_id` int(11) NOT NULL,
  `assist_teacher_id` int(11) DEFAULT NULL,
  `subject_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `assist_teacher_id` (`assist_teacher_id`),
  KEY `primary_teacher_id` (`primary_teacher_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`assist_teacher_id`) REFERENCES `teacher` (`id`),
  CONSTRAINT `course_ibfk_2` FOREIGN KEY (`primary_teacher_id`) REFERENCES `teacher` (`id`),
  CONSTRAINT `course_ibfk_3` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_appointment`
--

DROP TABLE IF EXISTS `course_appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_appointment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `open_time_start` datetime NOT NULL,
  `open_time_end` datetime NOT NULL,
  `teacher_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `course_appointment_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_appointment`
--

LOCK TABLES `course_appointment` WRITE;
/*!40000 ALTER TABLE `course_appointment` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_appraisal`
--

DROP TABLE IF EXISTS `course_appraisal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_appraisal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `course_study_result` varchar(255) DEFAULT NULL,
  `course_study_result_zh` varchar(255) DEFAULT NULL,
  `course_credit` float DEFAULT NULL,
  `course_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `course_appraisal_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `course_appraisal_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_appraisal`
--

LOCK TABLES `course_appraisal` WRITE;
/*!40000 ALTER TABLE `course_appraisal` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_appraisal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_class_participant`
--

DROP TABLE IF EXISTS `course_class_participant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_class_participant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `role_in_course` enum('AUDIENCE','TEACHER','STUDENT','SIT_IN','ASSISTANT') NOT NULL DEFAULT 'ASSISTANT',
  `role_uid` varchar(255) DEFAULT NULL,
  `access_url` varchar(255) DEFAULT NULL,
  `device_type` enum('PC','PHONE') NOT NULL DEFAULT 'PC',
  `role_id` varchar(255) DEFAULT NULL,
  `role_table` varchar(60) DEFAULT NULL,
  `role_table_id` int(11) DEFAULT NULL,
  `role_username` varchar(60) DEFAULT NULL,
  `attend_start` datetime DEFAULT NULL,
  `attend_end` datetime DEFAULT NULL,
  `assessment` varchar(2000) DEFAULT NULL,
  `remark` varchar(2000) DEFAULT NULL,
  `course_classroom_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_classroom_id` (`course_classroom_id`),
  CONSTRAINT `course_class_participant_ibfk_1` FOREIGN KEY (`course_classroom_id`) REFERENCES `course_classroom` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_class_participant`
--

LOCK TABLES `course_class_participant` WRITE;
/*!40000 ALTER TABLE `course_class_participant` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_class_participant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_classroom`
--

DROP TABLE IF EXISTS `course_classroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_classroom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `provider` int(11) NOT NULL,
  `room_title` varchar(255) NOT NULL,
  `video_ready` int(11) NOT NULL,
  `room_url` varchar(4000) DEFAULT NULL,
  `room_id` varchar(120) DEFAULT NULL,
  `room_type` enum('ONE_VS_ONE','ONE_VS_MANY','PRIVATE_CLASS','PUBLIC_CLASS') NOT NULL DEFAULT 'ONE_VS_ONE',
  `room_uid` varchar(255) DEFAULT NULL,
  `host_code` varchar(255) DEFAULT NULL,
  `state` enum('CREATED','DELETED','IN_USE','USED') NOT NULL DEFAULT 'CREATED',
  `duration_start` datetime DEFAULT NULL,
  `duration_end` datetime DEFAULT NULL,
  `course_schedule_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_schedule_id` (`course_schedule_id`),
  KEY `ix_course_classroom_room_id` (`room_id`),
  CONSTRAINT `course_classroom_ibfk_1` FOREIGN KEY (`course_schedule_id`) REFERENCES `course_schedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_classroom`
--

LOCK TABLES `course_classroom` WRITE;
/*!40000 ALTER TABLE `course_classroom` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_classroom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_exam`
--

DROP TABLE IF EXISTS `course_exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_exam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `state` int(11) NOT NULL,
  `exam_form` varchar(255) DEFAULT NULL,
  `exam_desc` varchar(255) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `course_exam_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_exam`
--

LOCK TABLES `course_exam` WRITE;
/*!40000 ALTER TABLE `course_exam` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_schedule`
--

DROP TABLE IF EXISTS `course_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `state` int(11) NOT NULL,
  `override_course_type` int(11) DEFAULT NULL,
  `progress` varchar(255) DEFAULT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `course_schedule_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_schedule`
--

LOCK TABLES `course_schedule` WRITE;
/*!40000 ALTER TABLE `course_schedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware`
--

DROP TABLE IF EXISTS `courseware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `ware_desc` varchar(2000) NOT NULL,
  `ware_url` varchar(255) DEFAULT NULL,
  `ware_uid` varchar(120) DEFAULT NULL,
  `room_id` varchar(2000) DEFAULT NULL,
  `other_desc` varchar(2000) DEFAULT NULL,
  `checked_result` enum('BEFORE_CHECK','CHECK_PASSED','CHECK_DENY') DEFAULT 'BEFORE_CHECK',
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `ix_courseware_ware_uid` (`ware_uid`),
  CONSTRAINT `courseware_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware`
--

LOCK TABLES `courseware` WRITE;
/*!40000 ALTER TABLE `courseware` DISABLE KEYS */;
/*!40000 ALTER TABLE `courseware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curriculum`
--

DROP TABLE IF EXISTS `curriculum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `curriculum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `full_name` varchar(120) NOT NULL,
  `desc` varchar(255) DEFAULT NULL,
  `cover_url` varchar(255) DEFAULT NULL,
  `prerequisite` varchar(255) DEFAULT NULL,
  `language_requirement` varchar(255) DEFAULT NULL,
  `full_name_zh` varchar(120) DEFAULT NULL,
  `desc_zh` varchar(255) DEFAULT NULL,
  `prerequisite_zh` varchar(255) DEFAULT NULL,
  `language_requirement_zh` varchar(255) DEFAULT NULL,
  `state` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curriculum`
--

LOCK TABLES `curriculum` WRITE;
/*!40000 ALTER TABLE `curriculum` DISABLE KEYS */;
/*!40000 ALTER TABLE `curriculum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollment`
--

DROP TABLE IF EXISTS `enrollment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enrollment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `student_id` int(11) NOT NULL,
  `channel_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `channel_id` (`channel_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`channel_id`) REFERENCES `channel` (`id`),
  CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollment`
--

LOCK TABLES `enrollment` WRITE;
/*!40000 ALTER TABLE `enrollment` DISABLE KEYS */;
/*!40000 ALTER TABLE `enrollment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_log`
--

DROP TABLE IF EXISTS `event_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `event_type` int(11) DEFAULT NULL,
  `event_content` varchar(8000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_log`
--

LOCK TABLES `event_log` WRITE;
/*!40000 ALTER TABLE `event_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feed_back`
--

DROP TABLE IF EXISTS `feed_back`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feed_back` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `feed_back` varchar(2000) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `process_by` varchar(50) DEFAULT NULL,
  `progress` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feed_back`
--

LOCK TABLES `feed_back` WRITE;
/*!40000 ALTER TABLE `feed_back` DISABLE KEYS */;
/*!40000 ALTER TABLE `feed_back` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `homework`
--

DROP TABLE IF EXISTS `homework`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `homework` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `homework_type` int(11) NOT NULL,
  `question_text` varchar(2000) DEFAULT NULL,
  `question_attachment_url` varchar(255) DEFAULT NULL,
  `answer_text` varchar(2000) DEFAULT NULL,
  `answer_attachment_url` varchar(255) DEFAULT NULL,
  `score` float DEFAULT NULL,
  `score_remark` varchar(2000) DEFAULT NULL,
  `score_reason` varchar(2000) DEFAULT NULL,
  `study_schedule_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `study_schedule_id` (`study_schedule_id`),
  CONSTRAINT `homework_ibfk_1` FOREIGN KEY (`study_schedule_id`) REFERENCES `study_schedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homework`
--

LOCK TABLES `homework` WRITE;
/*!40000 ALTER TABLE `homework` DISABLE KEYS */;
/*!40000 ALTER TABLE `homework` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interview`
--

DROP TABLE IF EXISTS `interview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `state` int(11) NOT NULL,
  `reason` varchar(2000) DEFAULT NULL,
  `result` varchar(2000) DEFAULT NULL,
  `interviewer_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `interviewer_id` (`interviewer_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `interview_ibfk_1` FOREIGN KEY (`interviewer_id`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `interview_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interview`
--

LOCK TABLES `interview` WRITE;
/*!40000 ALTER TABLE `interview` DISABLE KEYS */;
/*!40000 ALTER TABLE `interview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `menu_name` varchar(255) DEFAULT NULL,
  `menu_name_zh` varchar(255) DEFAULT NULL,
  `state` int(11) NOT NULL,
  `parent_id` int(11) NOT NULL,
  `menu_type` int(11) NOT NULL,
  `icon_class` varchar(255) DEFAULT NULL,
  `expand` int(11) NOT NULL,
  `sort_no` int(11) NOT NULL,
  `is_show` int(11) NOT NULL,
  `permission` varchar(255) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `notice` varchar(255) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `start` datetime DEFAULT NULL,
  `end` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `order_type` int(11) NOT NULL,
  `order_desc` varchar(255) NOT NULL,
  `state` int(11) NOT NULL,
  `cancel_checkby` varchar(120) DEFAULT NULL,
  `payment_state` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `discount` int(11) NOT NULL,
  `promotion` varchar(255) NOT NULL,
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `channel_id` (`channel_id`),
  KEY `course_id` (`course_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`channel_id`) REFERENCES `channel` (`id`),
  CONSTRAINT `order_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `order_ibfk_3` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pay_log`
--

DROP TABLE IF EXISTS `pay_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pay_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `direction` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `state_reason` varchar(255) NOT NULL,
  `amount` int(11) NOT NULL,
  `result` int(11) NOT NULL,
  `payment_method` int(11) NOT NULL,
  `payment_fee` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `pay_log_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `pay_log_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pay_log`
--

LOCK TABLES `pay_log` WRITE;
/*!40000 ALTER TABLE `pay_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `pay_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `name_zh` varchar(255) DEFAULT NULL,
  `name_pinyin` varchar(255) DEFAULT NULL,
  `code` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region`
--

LOCK TABLES `region` WRITE;
/*!40000 ALTER TABLE `region` DISABLE KEYS */;
/*!40000 ALTER TABLE `region` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_auth`
--

DROP TABLE IF EXISTS `role_auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `role_definition_id` int(11) NOT NULL,
  `auth_target_type` int(11) NOT NULL,
  `auth_target_value` varchar(2000) NOT NULL,
  `auth_level` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `role_definition_id` (`role_definition_id`),
  CONSTRAINT `role_auth_ibfk_1` FOREIGN KEY (`role_definition_id`) REFERENCES `role_definition` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_auth`
--

LOCK TABLES `role_auth` WRITE;
/*!40000 ALTER TABLE `role_auth` DISABLE KEYS */;
/*!40000 ALTER TABLE `role_auth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_definition`
--

DROP TABLE IF EXISTS `role_definition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_definition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `role_name` varchar(50) DEFAULT NULL,
  `role_desc` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_definition`
--

LOCK TABLES `role_definition` WRITE;
/*!40000 ALTER TABLE `role_definition` DISABLE KEYS */;
/*!40000 ALTER TABLE `role_definition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_log`
--

DROP TABLE IF EXISTS `sms_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `sms_channel` varchar(50) DEFAULT NULL,
  `country_code` varchar(50) DEFAULT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `state` int(11) NOT NULL,
  `fee` int(11) NOT NULL,
  `result_code` int(11) NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_log`
--

LOCK TABLES `sms_log` WRITE;
/*!40000 ALTER TABLE `sms_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `sms_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `username` varchar(60) NOT NULL,
  `password` varchar(255) NOT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `email` varchar(60) DEFAULT NULL,
  `gender` int(11) DEFAULT NULL,
  `birth` datetime DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `lang` varchar(20) DEFAULT NULL,
  `verify_type` varchar(20) DEFAULT NULL,
  `nickname` varchar(20) DEFAULT NULL,
  `user_tag` varchar(20) DEFAULT NULL,
  `last_login_ip` varchar(20) DEFAULT NULL,
  `last_login_time` datetime DEFAULT NULL,
  `last_login_device` varchar(50) DEFAULT NULL,
  `family_name` varchar(50) DEFAULT NULL,
  `given_name` varchar(50) DEFAULT NULL,
  `govtid_type` int(11) DEFAULT NULL,
  `govtid` varchar(50) DEFAULT NULL,
  `profession` varchar(50) DEFAULT NULL,
  `profile` varchar(255) DEFAULT NULL,
  `organization` varchar(255) DEFAULT NULL,
  `home_address` varchar(255) DEFAULT NULL,
  `office_address` varchar(255) DEFAULT NULL,
  `location_lng` float DEFAULT NULL,
  `location_lat` float DEFAULT NULL,
  `social_token` varchar(255) DEFAULT NULL,
  `im_token` varchar(255) DEFAULT NULL,
  `class_token` varchar(255) DEFAULT NULL,
  `state` enum('FRESH','BASIC_INFO','DISTRIBUTION_ADVISER','PERFECT_INFORMATION','DISTRIBUTION_HEADMASTER','HAVE_HEADMASTER','NOORDER','INSTUDY','GRADUATED','INVALID') NOT NULL DEFAULT 'FRESH',
  `level` varchar(50) DEFAULT NULL,
  `nation` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `cur_school` varchar(50) DEFAULT NULL,
  `grade` int(11) DEFAULT NULL,
  `requirements` varchar(2000) DEFAULT NULL,
  `requirements_zh` varchar(2000) DEFAULT NULL,
  `parent` varchar(50) DEFAULT NULL,
  `parent_mobile` varchar(20) DEFAULT NULL,
  `parent_email` varchar(60) DEFAULT NULL,
  `parent_role` varchar(20) DEFAULT NULL,
  `consultant_id` int(11) DEFAULT NULL,
  `student_helper_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `consultant_id` (`consultant_id`),
  KEY `student_helper_id` (`student_helper_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`consultant_id`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `student_ibfk_2` FOREIGN KEY (`student_helper_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_appraisal`
--

DROP TABLE IF EXISTS `student_appraisal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_appraisal` (
  `id` int(11) NOT NULL,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `form_no` int(11) NOT NULL,
  `form_submitted` varchar(255) DEFAULT NULL,
  `provider` varchar(255) DEFAULT NULL,
  `result` varchar(4000) DEFAULT NULL,
  `form_submitted_zh` varchar(255) DEFAULT NULL,
  `provider_zh` varchar(255) DEFAULT NULL,
  `result_zh` varchar(4000) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`form_no`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `student_appraisal_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `student_appraisal_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_appraisal`
--

LOCK TABLES `student_appraisal` WRITE;
/*!40000 ALTER TABLE `student_appraisal` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_appraisal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_subject`
--

DROP TABLE IF EXISTS `student_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_subject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `optional` int(11) NOT NULL,
  `desc` varchar(2000) DEFAULT NULL,
  `desc_zh` varchar(2000) DEFAULT NULL,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `student_subject_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `student_subject_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_subject`
--

LOCK TABLES `student_subject` WRITE;
/*!40000 ALTER TABLE `student_subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `study_appointment`
--

DROP TABLE IF EXISTS `study_appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `study_appointment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `student_requirements` varchar(2000) NOT NULL,
  `course_appointment_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_appointment_id` (`course_appointment_id`),
  CONSTRAINT `study_appointment_ibfk_1` FOREIGN KEY (`course_appointment_id`) REFERENCES `course_appointment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `study_appointment`
--

LOCK TABLES `study_appointment` WRITE;
/*!40000 ALTER TABLE `study_appointment` DISABLE KEYS */;
/*!40000 ALTER TABLE `study_appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `study_result`
--

DROP TABLE IF EXISTS `study_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `study_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `score` float DEFAULT NULL,
  `score_type` varchar(60) DEFAULT NULL,
  `score_full_mark` float DEFAULT NULL,
  `score_reason` varchar(2000) DEFAULT NULL,
  `score_remark` varchar(2000) DEFAULT NULL,
  `score_comment` varchar(2000) DEFAULT NULL,
  `student_id` int(11) NOT NULL,
  `course_exam_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_exam_id` (`course_exam_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `study_result_ibfk_1` FOREIGN KEY (`course_exam_id`) REFERENCES `course_exam` (`id`),
  CONSTRAINT `study_result_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `study_result`
--

LOCK TABLES `study_result` WRITE;
/*!40000 ALTER TABLE `study_result` DISABLE KEYS */;
/*!40000 ALTER TABLE `study_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `study_schedule`
--

DROP TABLE IF EXISTS `study_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `study_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `actual_start` datetime NOT NULL,
  `actual_end` datetime NOT NULL,
  `study_state` int(11) NOT NULL,
  `evaluation` varchar(255) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `homework` varchar(255) DEFAULT NULL,
  `test` varchar(255) DEFAULT NULL,
  `class_score` float DEFAULT NULL,
  `teacher_score` float DEFAULT NULL,
  `order_id` int(11) NOT NULL,
  `course_schedule_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_schedule_id` (`course_schedule_id`),
  KEY `order_id` (`order_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `study_schedule_ibfk_1` FOREIGN KEY (`course_schedule_id`) REFERENCES `course_schedule` (`id`),
  CONSTRAINT `study_schedule_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `study_schedule_ibfk_3` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `study_schedule`
--

LOCK TABLES `study_schedule` WRITE;
/*!40000 ALTER TABLE `study_schedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `study_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `subject_name` varchar(120) NOT NULL,
  `subject_desc` varchar(120) DEFAULT NULL,
  `subject_open_grade` varchar(120) DEFAULT NULL,
  `subject_requirements` varchar(120) DEFAULT NULL,
  `subject_name_zh` varchar(120) DEFAULT NULL,
  `subject_desc_zh` varchar(120) DEFAULT NULL,
  `subject_open_grade_zh` varchar(120) DEFAULT NULL,
  `subject_requirements_zh` varchar(120) DEFAULT NULL,
  `cover_url` varchar(255) DEFAULT NULL,
  `state` int(11) NOT NULL,
  `curriculum_id` int(11) DEFAULT NULL,
  `subject_category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `curriculum_id` (`curriculum_id`),
  KEY `subject_category_id` (`subject_category_id`),
  CONSTRAINT `subject_ibfk_1` FOREIGN KEY (`curriculum_id`) REFERENCES `curriculum` (`id`),
  CONSTRAINT `subject_ibfk_2` FOREIGN KEY (`subject_category_id`) REFERENCES `subject_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject_category`
--

DROP TABLE IF EXISTS `subject_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subject_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `subject_category` varchar(120) NOT NULL,
  `subject_category_zh` varchar(120) DEFAULT NULL,
  `desc` varchar(255) DEFAULT NULL,
  `desc_zh` varchar(255) DEFAULT NULL,
  `cover_url` varchar(255) DEFAULT NULL,
  `state` int(11) NOT NULL,
  `curriculum_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `curriculum_id` (`curriculum_id`),
  CONSTRAINT `subject_category_ibfk_1` FOREIGN KEY (`curriculum_id`) REFERENCES `curriculum` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject_category`
--

LOCK TABLES `subject_category` WRITE;
/*!40000 ALTER TABLE `subject_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `subject_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_control`
--

DROP TABLE IF EXISTS `sys_control`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_control` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `current_pid` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_control`
--

LOCK TABLES `sys_control` WRITE;
/*!40000 ALTER TABLE `sys_control` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_control` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `username` varchar(60) NOT NULL,
  `password` varchar(255) NOT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `email` varchar(60) DEFAULT NULL,
  `gender` int(11) DEFAULT NULL,
  `birth` datetime DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `lang` varchar(20) DEFAULT NULL,
  `verify_type` varchar(20) DEFAULT NULL,
  `nickname` varchar(20) DEFAULT NULL,
  `user_tag` varchar(20) DEFAULT NULL,
  `last_login_ip` varchar(20) DEFAULT NULL,
  `last_login_time` datetime DEFAULT NULL,
  `last_login_device` varchar(50) DEFAULT NULL,
  `family_name` varchar(50) DEFAULT NULL,
  `given_name` varchar(50) DEFAULT NULL,
  `govtid_type` int(11) DEFAULT NULL,
  `govtid` varchar(50) DEFAULT NULL,
  `profession` varchar(50) DEFAULT NULL,
  `profile` varchar(255) DEFAULT NULL,
  `organization` varchar(255) DEFAULT NULL,
  `home_address` varchar(255) DEFAULT NULL,
  `office_address` varchar(255) DEFAULT NULL,
  `location_lng` float DEFAULT NULL,
  `location_lat` float DEFAULT NULL,
  `social_token` varchar(255) DEFAULT NULL,
  `im_token` varchar(255) DEFAULT NULL,
  `class_token` varchar(255) DEFAULT NULL,
  `menus` varchar(2000) DEFAULT NULL,
  `state` enum('TRAINING','WORKING') NOT NULL DEFAULT 'WORKING',
  `user_type` int(11) DEFAULT NULL,
  `level` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_role`
--

DROP TABLE IF EXISTS `sys_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `sys_user_id` int(11) NOT NULL,
  `role_definition_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `role_definition_id` (`role_definition_id`),
  KEY `sys_user_id` (`sys_user_id`),
  CONSTRAINT `sys_user_role_ibfk_1` FOREIGN KEY (`role_definition_id`) REFERENCES `role_definition` (`id`),
  CONSTRAINT `sys_user_role_ibfk_2` FOREIGN KEY (`sys_user_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_role`
--

LOCK TABLES `sys_user_role` WRITE;
/*!40000 ALTER TABLE `sys_user_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_user_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `username` varchar(60) NOT NULL,
  `password` varchar(255) NOT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `email` varchar(60) DEFAULT NULL,
  `gender` int(11) DEFAULT NULL,
  `birth` datetime DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `lang` varchar(20) DEFAULT NULL,
  `verify_type` varchar(20) DEFAULT NULL,
  `nickname` varchar(20) DEFAULT NULL,
  `user_tag` varchar(20) DEFAULT NULL,
  `last_login_ip` varchar(20) DEFAULT NULL,
  `last_login_time` datetime DEFAULT NULL,
  `last_login_device` varchar(50) DEFAULT NULL,
  `family_name` varchar(50) DEFAULT NULL,
  `given_name` varchar(50) DEFAULT NULL,
  `govtid_type` int(11) DEFAULT NULL,
  `govtid` varchar(50) DEFAULT NULL,
  `profession` varchar(50) DEFAULT NULL,
  `profile` varchar(255) DEFAULT NULL,
  `organization` varchar(255) DEFAULT NULL,
  `home_address` varchar(255) DEFAULT NULL,
  `office_address` varchar(255) DEFAULT NULL,
  `location_lng` float DEFAULT NULL,
  `location_lat` float DEFAULT NULL,
  `social_token` varchar(255) DEFAULT NULL,
  `im_token` varchar(255) DEFAULT NULL,
  `class_token` varchar(255) DEFAULT NULL,
  `state` enum('RECRUIT','BASIC_INFO','WAIT_FOR_CHECK','CHECK_PASS','CHECK_ERROR','WAIT_FOR_INTERVIEW','INTERVIEW_PASS','INTERVIEW_ERROR','CONTRACTOR','WAIT_FOR_TRAIN','TRAIN_PASS','TRAIN_ERROR','WORKING','NO_WORK','INVALID') NOT NULL DEFAULT 'RECRUIT',
  `level` varchar(50) DEFAULT NULL,
  `nation` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `timezone` int(11) DEFAULT NULL,
  `contract` varchar(255) DEFAULT NULL,
  `cur_school` varchar(50) DEFAULT NULL,
  `race` varchar(120) DEFAULT NULL,
  `ancestral` varchar(120) DEFAULT NULL,
  `contract_url` varchar(255) DEFAULT NULL,
  `contract_dollar_price` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_subject`
--

DROP TABLE IF EXISTS `teacher_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher_subject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` enum('IN_FORCE','DELETED') NOT NULL DEFAULT 'IN_FORCE',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by` varchar(60) DEFAULT NULL,
  `advantage` varchar(120) NOT NULL,
  `desc` varchar(255) DEFAULT NULL,
  `advantage_zh` varchar(120) DEFAULT NULL,
  `desc_zh` varchar(255) DEFAULT NULL,
  `teacher_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subject_id` (`subject_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `teacher_subject_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`),
  CONSTRAINT `teacher_subject_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_subject`
--

LOCK TABLES `teacher_subject` WRITE;
/*!40000 ALTER TABLE `teacher_subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `teacher_subject` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-19 13:42:43
