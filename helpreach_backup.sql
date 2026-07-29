SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `claim_status`;
CREATE TABLE `claim_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `claim_id` int(11) NOT NULL,
  `status` enum('Pending','Approved','PickedUp','Completed') COLLATE utf8mb4_unicode_ci DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `claim_id` (`claim_id`),
  CONSTRAINT `claim_status_ibfk_1` FOREIGN KEY (`claim_id`) REFERENCES `claimed_donations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `claimed_donations`;
CREATE TABLE `claimed_donations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `donation_id` int(11) NOT NULL,
  `ngo_id` int(11) NOT NULL,
  `claimed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `received_at` timestamp NULL DEFAULT NULL,
  `status` enum('Pending','Approved','PickedUp','Completed') COLLATE utf8mb4_unicode_ci DEFAULT 'Pending',
  `is_double_claimed` tinyint(1) DEFAULT '0',
  `picked_up_at` timestamp NULL DEFAULT NULL,
  `pickup_date` date DEFAULT NULL,
  `pickup_time` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `donor_confirmation` tinyint(1) DEFAULT '0',
  `approval_notes` text COLLATE utf8mb4_unicode_ci,
  `scheduled_at` timestamp NULL DEFAULT NULL,
  `approved_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_claim` (`donation_id`,`ngo_id`),
  KEY `ngo_id` (`ngo_id`),
  CONSTRAINT `claimed_donations_ibfk_1` FOREIGN KEY (`donation_id`) REFERENCES `donations` (`id`) ON DELETE CASCADE,
  CONSTRAINT `claimed_donations_ibfk_2` FOREIGN KEY (`ngo_id`) REFERENCES `ngos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `claimed_donations` (`id`,`donation_id`,`ngo_id`,`claimed_at`,`received_at`,`status`,`is_double_claimed`,`picked_up_at`,`pickup_date`,`pickup_time`,`donor_confirmation`,`approval_notes`,`scheduled_at`,`approved_at`) VALUES
('35','55','53','2026-01-24 22:32:59','2026-01-24 22:37:48','Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('36','57','53','2026-01-31 11:05:20','2026-01-31 11:11:19','Completed','0','2026-01-31 11:11:09',NULL,NULL,'0',NULL,NULL,NULL),
('37','56','53','2026-01-31 12:42:14','2026-01-31 12:44:56','Completed','0','2026-01-31 12:44:49',NULL,NULL,'0',NULL,NULL,NULL),
('38','60','53','2026-02-01 20:13:50','2026-02-01 20:14:54','Completed','0','2026-02-01 20:14:47',NULL,NULL,'0',NULL,NULL,NULL),
('39','62','53','2026-02-02 10:59:38','2026-02-03 13:49:02','Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('40','90','53','2026-02-03 13:48:48','2026-02-03 13:55:53','Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('41','86','53','2026-02-03 14:10:25',NULL,'Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('42','93','53','2026-02-03 20:48:46','2026-02-03 20:49:18','Completed','0','2026-02-03 20:49:12',NULL,NULL,'0',NULL,NULL,NULL),
('43','96','53','2026-02-03 21:37:35','2026-02-05 11:15:50','Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('44','110','53','2026-02-04 20:38:13','2026-02-04 20:38:39','Completed','0','2026-02-04 20:38:34',NULL,NULL,'0',NULL,NULL,NULL),
('45','111','53','2026-02-04 21:04:33','2026-02-04 21:04:47','Completed','0','2026-02-04 21:04:39',NULL,NULL,'0',NULL,NULL,NULL),
('46','112','53','2026-02-04 23:19:30',NULL,'PickedUp','0','2026-02-04 23:36:47',NULL,NULL,'0',NULL,NULL,NULL),
('47','109','52','2026-02-05 11:55:35','2026-02-05 11:56:21','Completed','0','2026-02-05 11:56:17',NULL,NULL,'0',NULL,NULL,NULL),
('48','116','54','2026-02-05 21:14:23','2026-02-05 21:15:15','Completed','0','2026-02-05 21:15:10',NULL,NULL,'0',NULL,NULL,NULL),
('49','123','52','2026-02-05 22:19:48',NULL,'Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('50','122','53','2026-02-05 22:20:57',NULL,'Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('51','121','55','2026-02-06 12:10:07','2026-02-06 12:12:43','Completed','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('52','127','53','2026-02-06 12:24:54','2026-02-06 12:25:16','Completed','0','2026-02-06 12:25:11',NULL,NULL,'0',NULL,NULL,NULL),
('53','128','53','2026-02-06 21:04:59',NULL,'Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('54','92','53','2026-02-07 09:44:48',NULL,'Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('55','131','53','2026-03-10 12:12:03','2026-03-10 12:12:20','Completed','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('56','132','53','2026-04-14 13:15:25',NULL,'Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL),
('57','134','53','2026-04-15 12:36:04','2026-04-15 12:36:36','Pending','0',NULL,NULL,NULL,'0',NULL,NULL,NULL);

DROP TABLE IF EXISTS `claims`;
CREATE TABLE `claims` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `donation_id` int(11) NOT NULL,
  `ngo_id` int(11) NOT NULL,
  `status` enum('pending','accepted','rejected','picked_up') COLLATE utf8mb4_unicode_ci DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `donation_id` (`donation_id`),
  KEY `ngo_id` (`ngo_id`),
  CONSTRAINT `claims_ibfk_1` FOREIGN KEY (`donation_id`) REFERENCES `donations` (`id`) ON DELETE CASCADE,
  CONSTRAINT `claims_ibfk_2` FOREIGN KEY (`ngo_id`) REFERENCES `ngos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `donations`;
CREATE TABLE `donations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `quantity` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `images` text COLLATE utf8mb4_unicode_ci,
  `donor_id` int(11) NOT NULL,
  `status` enum('available','claimed','completed','cancelled') COLLATE utf8mb4_unicode_ci DEFAULT 'available',
  `pickup_info` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pickup_location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo_filename` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `priority` enum('Low','Normal','Urgent') COLLATE utf8mb4_unicode_ci DEFAULT 'Normal',
  `expiry_date` datetime DEFAULT NULL,
  `is_perishable` tinyint(1) DEFAULT '0',
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `donor_latitude` decimal(10,8) DEFAULT NULL COMMENT 'Donor latitude',
  `donor_longitude` decimal(11,8) DEFAULT NULL COMMENT 'Donor longitude',
  `expired_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_donor` (`donor_id`),
  CONSTRAINT `fk_donor` FOREIGN KEY (`donor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `donations` (`id`,`title`,`description`,`quantity`,`images`,`donor_id`,`status`,`pickup_info`,`created_at`,`updated_at`,`category`,`pickup_location`,`photo_filename`,`priority`,`expiry_date`,`is_perishable`,`latitude`,`longitude`,`city`,`donor_latitude`,`donor_longitude`,`expired_at`) VALUES
('55','dd','food','21',NULL,'16','available','dd | 2026-01-24 21:21','2026-01-24 22:30:44',NULL,'Food','dd',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('56','kjj','food','545',NULL,'17','available','jkk | 2026-01-31 12:12','2026-01-31 09:54:37',NULL,'Clothes','jhj',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('57','kjj','food','545',NULL,'17','available','jkk | 2026-01-31 12:12','2026-01-31 09:54:41',NULL,'Clothes','jhj',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('58','kjj','food','545',NULL,'17','available','jkk | 2026-01-31 12:12','2026-01-31 14:46:05',NULL,'Food','jhj','1cdd4e04-01ee-48a5-8f64-3eab035d0a4b_t_shirt.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('59','air','food','99999999999999999999999999999999999999999999999999999999999999999999999999999',NULL,'17','available','s | 2026-01-06 21:12','2026-02-01 16:46:41',NULL,'Clothes','d',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('60','aircfdf','food','99999999999999999999999999999999999999999999999999999999999999999999999999999',NULL,'17','available','s | 2026-01-06 21:21','2026-02-01 20:07:59',NULL,'Food','d','57282bb8-c77c-4dfb-a113-73fe017d6274_biryani.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('61','aircfdfdfdf','food','434',NULL,'17','available','sfdf | 2026-02-01 21:34','2026-02-01 21:34:28',NULL,'Food','drerf','78b2daad-c720-47a3-89ee-73760e9995f3_beach.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('62','dfe','food','22',NULL,'17','available','ffwf | 2026-02-01 21:02','2026-02-01 22:46:25',NULL,'Food','cc2xx',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('63','dfe','food','22',NULL,'17','available','ffwf | 2026-02-01 12:12','2026-02-02 11:03:29',NULL,'Food','cc2xx','0c30e18e-f100-478f-ba63-56cf332c315a_WhatsApp_Image_2025-07-28_at_10.29.20_PM.jpeg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('64','dfe','food','22',NULL,'17','available','ffwf | 2026-02-01 12:12','2026-02-02 11:50:44',NULL,'Food','cc2xx',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('65','dfe','food','22',NULL,'17','available','ffwf | 2026-02-01 21:21','2026-02-02 12:15:24',NULL,'Food','cc2xx',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('66','dfe','food','22',NULL,'17','available','ffwf | 2026-02-01 12:12','2026-02-02 12:22:13',NULL,'Food','cc2xx',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('67','b iasagsd','food','54',NULL,'17','available','sss | 2025-12-09 12:21','2026-02-02 14:22:58',NULL,'Food','ssd',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('68','b iasagsd','food','54',NULL,'17','available','sss | 2025-12-09 21:21','2026-02-02 14:38:23',NULL,'Food','ssd',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('69','b iasagsd','food','54',NULL,'17','available','sss | 2025-12-09 21:21','2026-02-02 14:38:25',NULL,'Food','ssd',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('70','b iasagsdkjkkjk','food','54',NULL,'17','available','sss | 2025-12-09 12:12','2026-02-02 14:41:40',NULL,'Food','ssd',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('71','biryani','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 12:12','2026-02-02 14:55:44',NULL,'Food','Mumbai','f32b36ab-ca5c-42b7-b447-b7e767418852_biryani.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('72','biryani','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 12:12','2026-02-02 15:01:30',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('73','biryani','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 12:12','2026-02-02 15:06:01',NULL,'Food','Mumbai','cf7a03c9-0390-4542-bde1-baf1da792e4c_t_shirt.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('74','biryani','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 12:12','2026-02-02 15:09:02',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('75','biryani','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 21:21','2026-02-02 19:01:50',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('76','biryanieeeee','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 21:21','2026-02-02 19:09:40',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('77','birya','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 12:12','2026-02-02 19:49:50',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('78','biryattttt','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 12:12','2026-02-02 19:56:34',NULL,'Food','Mumbai','1df52363-472a-42ca-9bbc-bd0576d75b6d_helpreach.jpeg.jpeg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('79','biryattttt','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 12:12','2026-02-02 20:03:54',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('80','biryattttt','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 12:32','2026-02-02 20:08:58',NULL,'Food','Mumbai','f67eeed0-34db-4819-90b2-b76c4c231fc0__.png','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('81','jhghjgj','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 21:21','2026-02-02 20:21:50',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('82','jhghjgj','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 21:21','2026-02-02 20:22:22',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('83','ffff','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 21:21','2026-02-02 20:31:38',NULL,'Food','Mumbai','28ccb0e0-75f5-4024-becd-905cb3c452f7_sky.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('84','ffff','food','21',NULL,'17','available','kothrud,pune | 2026-02-02 12:12','2026-02-02 20:35:47',NULL,'Food','Mumbai','49e651ac-97e8-4f30-ad2f-88629219fb2a_biryani.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('85','pani puri','food','21',NULL,'17','available','thane | 2026-02-02 21:17','2026-02-02 21:18:07',NULL,'Food','Mumbai','4d1a2082-19a6-40ba-9f73-c288a3082bf8_UZmWAD7Fqq4uE2VIO9RQh.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('86','pani puri','food','21',NULL,'17','available','thane | 2026-02-02 12:12','2026-02-02 21:55:45',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('87','Sweater','clothes','50',NULL,'17','available','narhe | 2026-02-03 12:27','2026-02-03 12:27:35',NULL,'Clothes','pune','38c100bb-ead1-4f5b-89e6-79f45238993d_t_shirt.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('88','samosa','food','50',NULL,'17','available','narhe | 2026-02-03 12:28','2026-02-03 12:28:25',NULL,'Food','pune','ba3568b8-9f3d-42f6-9e5a-bfd8c477058f_Samosa-Chaat.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 20:47:45'),
('89','Pen','other','1000',NULL,'17','available','Narhe | 2026-02-03 13:31','2026-02-03 13:31:44',NULL,'Other','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('90','Pen','other','1000',NULL,'17','available','Narhe | 2026-02-03 13:31','2026-02-03 13:31:51',NULL,'Other','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('91','Vadapav','food','1000',NULL,'17','available','Narhe | 2026-02-03 13:31','2026-02-03 13:32:29',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-03 21:01:00'),
('92','Pencil','food','1000',NULL,'17','available','Narhe | 2026-02-03 20:32','2026-02-03 20:32:56',NULL,'Other','Mumbai','34abf208-bff2-452d-b1d3-4fd052af7e32_u7l8xm.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('93','Pencil','other','1000',NULL,'17','available','Narhe | 2026-02-03 20:34','2026-02-03 20:34:29',NULL,'Other','Mumbai','f7069a2e-ed0b-4cd2-b354-ca7e385aee8d_skbily.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('94','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 20:57','2026-02-03 20:57:15',NULL,'Food','Mumbai','4ea27d4c-e305-42b3-af2c-88e6b5d543c2_helpreach.jpeg.jpeg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 11:30:17'),
('95','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 21:05','2026-02-03 21:05:30',NULL,'Food','Mumbai','44883448-c304-4748-bbe1-204de2af669e_t_shirt.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 11:30:17'),
('96','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 21:11','2026-02-03 21:11:22',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('97','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 11:39','2026-02-04 11:44:39',NULL,'Food','Mumbai','43d8862b-0f3f-48c3-9138-62647b9d14ca_biryani.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 11:44:39'),
('98','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 11:46','2026-02-04 11:46:27',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 11:46:29'),
('99','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 11:57','2026-02-04 11:57:14',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 11:57:22'),
('100','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 11:57','2026-02-04 11:57:34',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 11:57:37'),
('101','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 11:57','2026-02-04 11:57:58',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 11:58:07'),
('102','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 11:57','2026-02-04 11:58:00',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 11:58:07'),
('103','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 11:59','2026-02-04 11:59:45',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 11:59:54'),
('104','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 12:06','2026-02-04 12:06:22',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 12:06:25'),
('105','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 19:53','2026-02-04 19:54:09',NULL,'Food','Mumbai','e8cceec1-f8ad-4dd5-8225-50a8ddfcd639_biryani.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 19:54:09'),
('106','Bun maska','food','22',NULL,'17','available','Narhe | 2026-02-03 19:59','2026-02-04 19:59:12',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-04 19:59:19'),
('107','Bun maskaaa','food','22',NULL,'17','available','Narhe | 2026-02-04 21:15','2026-02-04 20:15:41',NULL,'Food','Mumbai','62c0696c-5d6d-40b8-8f17-0704c7561de8_creative_reuse_and_upcycling.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-05 10:46:46'),
('108','biryani','food','22',NULL,'17','available','Narhe | 2026-02-04 20:16','2026-02-04 20:16:22',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-05 10:46:46'),
('109','pen','clothes','22',NULL,'17','available','Narhe | 2026-02-04 20:17','2026-02-04 20:17:04',NULL,'Other','Mumbai','cbe512dd-7bf5-4eed-94cb-e52ac9b83901_sky.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('110','Thali','food','200',NULL,'17','available','kothrud,pune | 2026-02-04 20:27','2026-02-04 20:37:14',NULL,'Food','Pune','8b6b025d-a643-4107-aa24-cf32916df343_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('111','Jeven','food','200',NULL,'17','available','kothrud,pune | 2026-02-04 21:06','2026-02-04 21:03:49',NULL,'Food','Pune','af344aec-5642-4dc5-a0dc-6963e7ffc168_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('112','Pani puri','food','12',NULL,'17','available','thane | 2026-02-04 22:18','2026-02-04 21:17:41',NULL,'Food','Mumbai','e9741475-ca52-4caf-a280-cf900d14a125_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('113','Pani puri','food','15',NULL,'17','available','thane | 2026-02-04 23:37','2026-02-04 23:27:49',NULL,'Food','Mumbai','3560826a-fcf5-4186-8f59-23bfd38944e8_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-05 10:46:46'),
('114','Pani puri','food','15',NULL,'17','available','thane | 2026-02-05 21:25','2026-02-05 20:25:46',NULL,'Food','Mumbai','a81ded83-ce43-45c8-b0f8-a3e69d899435_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-06 09:59:28'),
('115','Pani puriiiiii','food','15',NULL,'17','available','thane | 2026-02-05 21:31','2026-02-05 20:31:49',NULL,'Food','Mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-06 09:59:28'),
('116','tshirttt','food','12121',NULL,'17','available','kasba Peth | 2026-02-05 22:09','2026-02-05 21:09:45',NULL,'Food','mumbai','c663547a-9b79-46e2-a652-d29b4abcc53d_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('117','tshirttt','food','112',NULL,'17','available','kasba Peth | 2026-02-05 22:20','2026-02-05 21:20:36',NULL,'Food','mumbai','3229b75e-256b-4a6c-8bf2-a0f980b55dfc_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-06 09:59:28'),
('118','tshirttt','food','112',NULL,'17','available','kasba Peth | 2026-02-05 22:20','2026-02-05 21:20:39',NULL,'Food','mumbai','bdd5da2b-7563-4db0-ba2f-10b7b91c81df_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-06 09:59:28'),
('119','thali','food','15',NULL,'17','available','thane | 2026-02-05 22:14','2026-02-05 21:53:22',NULL,'Food','Mumbai','3f49f183-8d48-4a25-b9f9-485cebcbe578_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-06 09:59:28'),
('120','Bun maska','food','1212',NULL,'17','available','kasba Peth | 2026-02-05 23:45','2026-02-05 21:54:12',NULL,'Food','mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-06 09:59:28'),
('121','tshirttt','clothes','222',NULL,'17','available','kasba Peth | 2026-02-05 23:55','2026-02-05 21:55:25',NULL,'Clothes','mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('122','tshirt','clothes','15',NULL,'17','available','thane | 2026-02-05 23:59','2026-02-05 21:56:30',NULL,'Clothes','Mumbai','0fc20504-0e9b-4eff-8bd8-2b36de095747_t_shirt.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('123','pant','food','332',NULL,'17','available','kasba Peth | 2026-02-05 23:55','2026-02-05 21:57:15',NULL,'Clothes','mumbai','65ae6e25-b222-4aab-bbcd-ec13ca2280ba_biryani.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('124','Vadapav','food','32',NULL,'17','available','thane | 2026-02-05 23:23','2026-02-05 22:28:19',NULL,'Food','Mumbai','49088eda-fba2-40e3-af90-eacd90a1c755_tumblr_a5ec0472edc357aaa8449b21271284ae_c84cc87a_640.gif','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-06 09:59:28'),
('125','tshirttt','food','121',NULL,'17','available','kasba Peth | 2026-02-05 23:25','2026-02-05 23:09:57',NULL,'Food','mumbai','0ca7b355-b54b-4a03-b94a-2a7ffdbff4bc_WhatsApp_Image_2026-02-04_at_10.45.06_AM.jpeg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-06 09:59:28'),
('126','Vadapav','food','32',NULL,'17','available','thane | 2026-02-07 05:25','2026-02-06 12:17:13',NULL,'Food','Mumbai','74cf63d0-1910-45a2-a32a-94045ffc14eb_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-07 20:39:10'),
('127','tshirttt','food','1212',NULL,'17','available','kasba Peth | 2026-02-06 12:45','2026-02-06 12:23:34',NULL,'Food','mumbai',NULL,'Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('128','phione','other','21',NULL,'17','available','thane | 2026-02-06 21:12','2026-02-06 21:00:53',NULL,'Other','mumbai','030d01e1-0b54-4dee-bf6f-4645cc618147_download.gif','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('129','Vadapav','food','32',NULL,'17','available','thane | 2026-02-08 23:14','2026-02-08 23:05:15',NULL,'Food','Mumbai','f17fcb91-b004-45c5-b486-1b52e0ced935_thali.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-02-09 14:35:05'),
('130','Vadapav','food','32',NULL,'17','available','thane | 2026-03-09 20:20','2026-03-09 20:01:55',NULL,'Food','Mumbai','fb9491eb-b4fa-497a-92c6-8bbeca84ba89_vada_pav.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-03-10 09:05:21'),
('131','Vadapav','food','32',NULL,'17','available','thane | 2026-03-10 12:20','2026-03-10 11:52:03',NULL,'Food','Mumbai','3f5ddd48-a6ff-40fb-85b1-82702d83daf2_vada_pav.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('132','Vadapav','food','32',NULL,'17','available','thane | 2026-04-14 12:30','2026-04-14 11:51:36',NULL,'Food','Mumbai','9c503745-4f75-406d-abc4-fbf3e3455401_vada_pav.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('133','Vadapav','food','32',NULL,'17','available','thane | 2026-04-15 12:30','2026-04-15 12:04:33',NULL,'Food','Mumbai','6011e2de-4ed5-4256-ad1c-c5bef8ceba2d_vada_pav.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-07-27 19:36:32'),
('134','Clothes','clothes','50',NULL,'17','available','thane | 2026-04-15 12:43','2026-04-15 12:33:39',NULL,'Clothes','Mumbai','d157dbd4-8177-4c71-8f47-51967e924284_Guidelines_for_donating_gently_used_clothing.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL),
('135','vadapav','food','32',NULL,'17','available','thane | 2026-04-15 15:56','2026-04-15 14:56:37',NULL,'Food','Mumbai','babdcf0c-f77f-48c8-9186-79a817384969_vada_pav.jpg','Normal',NULL,'0',NULL,NULL,NULL,NULL,NULL,'2026-07-27 19:36:32');

DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_user` int(11) NOT NULL,
  `to_user` int(11) NOT NULL,
  `body` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `from_user` (`from_user`),
  KEY `to_user` (`to_user`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`from_user`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`to_user`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `ngo_documents`;
CREATE TABLE `ngo_documents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ngo_id` int(11) NOT NULL,
  `filename` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `original_filename` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `uploaded_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `ngo_documents` (`id`,`ngo_id`,`filename`,`original_filename`,`uploaded_at`) VALUES
('1','53','3f1257d4-8209-4828-ac55-2e27e88a1881_HelpReach_kjj_1769843747012.pdf','HelpReach_kjj_1769843747012.pdf','2026-01-31 14:48:39'),
('2','53','576ff053-79b5-4799-8372-4635199945bf_HelpReach_Donation_History_1769843723549.pdf','HelpReach_Donation_History_1769843723549.pdf','2026-01-31 14:59:29'),
('3','53','843ac8be-1348-4fe7-b6ce-aedc84fb043a_HelpReach_Donation_History_1769838133680.pdf','HelpReach_Donation_History_1769838133680.pdf','2026-01-31 14:59:51'),
('4','53','caa77bba-cf8c-4700-b248-2c874e774f8f_HelpReach_kjj_1769843747012.pdf','HelpReach_kjj_1769843747012.pdf','2026-01-31 15:07:52'),
('5','53','182f8ea4-ad87-44d5-b797-912b8c6cbdfb_HelpReach_kjj_1769843747012.pdf','HelpReach_kjj_1769843747012.pdf','2026-01-31 15:08:19'),
('6','53','33d3c4a9-1c8d-40ce-8210-1c468b73c2d9_HelpReach_Donation_History_1769838133680.pdf','HelpReach_Donation_History_1769838133680.pdf','2026-01-31 15:08:30'),
('7','53','63170279-294f-4872-a478-aec14a3861f4_NIS_Unit_2.pdf','NIS_Unit_2.pdf','2026-01-31 23:25:31'),
('8','53','8cf6b3d1-d8ef-40a9-b668-2d86e5260855_thali.jpg','thali.jpg','2026-02-05 00:03:23'),
('9','55','429c4d90-244a-4ae7-9eba-7c04df0dfde7_Test_Report_pract_14.pdf','Test_Report_pract_14.pdf','2026-02-06 20:38:49');

DROP TABLE IF EXISTS `ngo_ratings`;
CREATE TABLE `ngo_ratings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ngo_id` int(11) NOT NULL,
  `donor_id` int(11) NOT NULL,
  `claim_id` int(11) NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `review` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ngo_id` (`ngo_id`),
  KEY `donor_id` (`donor_id`),
  KEY `claim_id` (`claim_id`),
  CONSTRAINT `ngo_ratings_ibfk_1` FOREIGN KEY (`ngo_id`) REFERENCES `ngos` (`id`),
  CONSTRAINT `ngo_ratings_ibfk_2` FOREIGN KEY (`donor_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ngo_ratings_ibfk_3` FOREIGN KEY (`claim_id`) REFERENCES `claimed_donations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `ngo_trust_score`;
CREATE TABLE `ngo_trust_score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ngo_id` int(11) NOT NULL,
  `average_rating` decimal(3,2) DEFAULT '0.00',
  `total_ratings` int(11) DEFAULT '0',
  `total_completed` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ngo_id` (`ngo_id`),
  CONSTRAINT `ngo_trust_score_ibfk_1` FOREIGN KEY (`ngo_id`) REFERENCES `ngos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `ngos`;
CREATE TABLE `ngos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `contact_email` varchar(190) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `verified` tinyint(1) DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `registration_number` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact_person` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location` text COLLATE utf8mb4_unicode_ci,
  `services` text COLLATE utf8mb4_unicode_ci,
  `address` text COLLATE utf8mb4_unicode_ci,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL COMMENT 'Latitude of NGO location',
  `longitude` decimal(11,8) DEFAULT NULL COMMENT 'Longitude of NGO location',
  `city` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'NGO city/location',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ngos_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `ngos` (`id`,`user_id`,`name`,`description`,`contact_email`,`verified`,`created_at`,`registration_number`,`category`,`contact_person`,`phone`,`location`,`services`,`address`,`password_hash`,`latitude`,`longitude`,`city`) VALUES
('1',NULL,'Mumbai Roti Bank','Surplus Food Collection, Direct Distribution, Monetary Donations','teamrotibank@gmail.com','1','2026-01-20 23:23:31','','Food Distribution','Mumbai Roti Bank','+91 86555 80001',NULL,NULL,'1701, One World Centre, Tower 2B, Floor 17, 841, Senapati Bapat Marg, Elphinstone Road, Mumbai 400013, India','','18.53000000','73.86000000',NULL),
('2',NULL,'Apna Shelter India Foundation','Food Help, Child Education, Women Support, Health Care, Environment Care, Social Help','','1','2026-01-20 23:23:31','','Multi-Service','Apna Shelter India Foundation','+91 70211 56564',NULL,NULL,'303, 3rd Floor, Krishna Plaza, Near Thane Railway Station, Thane West 400602','','18.53000000','73.86000000',NULL),
('3',NULL,'Goodwill India Upkaram','Clothes Donation, Toys Donation, Computer Donation, Goodwill Thali','goodwillpune01@gmail.com','1','2026-01-20 23:23:31','','Donations','Goodwill India Upkaram','020 25290909',NULL,NULL,'More Petrol Pump, Shivane, Pune, Maharashtra','','18.53000000','73.86000000',NULL),
('4',NULL,'Pephands Foundation','Food Donation, Nutrition Kits, Grocery Kits, Student Education','info@pephands.org','1','2026-01-20 23:23:31','','Education & Food','Pephands Foundation','+91 7305009919',NULL,NULL,'Pune','','28.65187119','77.05940892','Delhi'),
('5',NULL,'Sahyadri Jankalyan Sanstha','Clothes, Used Items, Essentials Redistribution','','1','2026-01-20 23:23:31','','Essential Supplies','Sahyadri Jankalyan Sanstha','9823679878',NULL,NULL,'Katraj, Pune','','19.14400301','72.86810100','Mumbai'),
('6',NULL,'Akanksha Organization','Community Service / Public Utility','','1','2026-01-20 23:23:31','','Community Service','Akanksha Organization','020 660513801',NULL,NULL,'Bhalekar Chawl, Erandwane, Pune 411004','','12.95626977','77.65579108','Bangalore'),
('7',NULL,'S N Shirke Charitable Foundation','Donations (Clothes, Food, Essentials)','','1','2026-01-20 23:23:31','','Donations','S N Shirke Charitable Foundation','+91 9421230510',NULL,NULL,'Office No. 11, Navrang Plaza, Air Port Road, Vishrantwadi, Pune 411015','','17.32421733','78.44882527','Hyderabad'),
('8',NULL,'Global Vision NGO','Community Service, Potential Donations','','1','2026-01-20 23:23:31','','Community Service','Global Vision NGO','022 4127 0773',NULL,NULL,'Office No. 513/515, 5th Floor, Sterling Center, Opp. Hotel Arora Tower, MG Road, Camp, Pune 411001','','13.11199124','80.27419096','Chennai'),
('9',NULL,'Children\'s Future India','Child Welfare, Clothes, Essentials, Food','','1','2026-01-20 23:23:31','','Child Welfare','Children\'s Future India','090280 03613',NULL,NULL,'Prashant Nagar, Lokamanya Nagar, Navi Peth / Sadashiv Peth, Pune 411030','','22.60512454','88.33730937','Kolkata'),
('10',NULL,'Chetana Mahila Vikas Kendra','Women\'s & Community Welfare, Clothes & Essentials','','1','2026-01-20 23:23:31','','Women Welfare','Chetana Mahila Vikas Kendra','020 2635 4946',NULL,NULL,'9 NPS Line, Behind Wonder Car Garage, Pulgate, Pune 411001','','18.45373627','73.91232877','Pune'),
('11',NULL,'Bharatiya Samaj Seva Kendra','Social Service, Donations','','1','2026-01-20 23:23:31','','Social Service','Bharatiya Samaj Seva Kendra','020 2615 9314',NULL,NULL,'Plot 373, 6th Lane, North Main Road, Koregaon Park, Pune 411001','','22.99704241','72.53584339','Ahmedabad'),
('12',NULL,'Mukul Madhav Foundation','Education, Rural Development, Farmer & Animal Welfare, Food Donations','','1','2026-01-20 23:23:31','','Multi-Service','Mukul Madhav Foundation','020 2552 8075',NULL,NULL,'Harmony, 5, off Ganeshkhind Road, ICS Colony, Ashok Nagar, Pune 411007','','26.98701020','75.82219119','Jaipur'),
('13',NULL,'Save The Humanity Organisation','Animal Welfare, Child Welfare, Disaster Relief, Education','','1','2026-01-20 23:23:31','','Multi-Service','Save The Humanity Organisation','093159 46703',NULL,NULL,'C Block, Sector 6, Noida, Uttar Pradesh 201301','','26.82247169','80.94944878','Lucknow'),
('14',NULL,'Marpu Foundation','Environment, Veteran & Women Empowerment, Women Education','','1','2026-01-20 23:23:31','','Women & Environment','Marpu Foundation','079978 01001',NULL,NULL,'10-82, Gaondevi Marg, NL - 1 Type, Sector 20, Nerul, Navi Mumbai, Maharashtra 400706','','30.80817971','76.73449711','Chandigarh'),
('15',NULL,'Manpravah Foundation','Orphanage Food Donation, Feeding the Hungry','','1','2026-01-20 23:23:31','','Food Distribution','Manpravah Foundation','+91 9987987557',NULL,NULL,'502 Tulsi Height, Sector 10E, Plot 8, Near Dmart, Roadpali, Kalamboli, Navi Mumbai 410218','','22.75551704','75.92383123','Indore'),
('16',NULL,'Uday Foundation','Clothes, Medicine, Environmental & Homeless Support, Human Rights, Skill Development','info@udayfoundation.org','1','2026-01-20 23:23:31','','Multi-Service','Uday Foundation','011 2656 1333',NULL,NULL,'D-233 (LGF, Block D), Sarvodaya Enclave, New Delhi 110017','','21.21867216','72.78455511','Surat'),
('17',NULL,'SevaDeep','Old Toys, Clothes, Stationery, Furniture','','1','2026-01-20 23:23:31','','Donations','SevaDeep','095185 41719',NULL,NULL,'14th, SKY ONE, Relfor Foundation, Kalyani Nagar, Pune, Maharashtra 411006','','22.30028922','73.28000993','Vadodara'),
('18',NULL,'Farmers Needs Help Foundation','Clothes, Food, Miscellaneous Donations','','1','2026-01-20 23:23:31','','Donations','Farmers Needs Help Foundation','096641 18631',NULL,NULL,'Shivangan Society, Lokmanya Tilak Rd, Jaihind Colony, Tata Colony, Mulund East, Mumbai 400081','','28.59267334','77.54062702','Ghaziabad'),
('19',NULL,'Roadside Family Foundation','Animal Welfare, Child Welfare, Education, Donations','','1','2026-01-20 23:23:31','','Multi-Service','Roadside Family Foundation','086574 57237',NULL,NULL,'CEO 95 122, Unit 29, Box A4, Aarey Milk Colony, Goregaon, Mumbai 400065','',NULL,NULL,NULL),
('20',NULL,'SYJ Organization','Animal Welfare, Child Welfare, Donations, Education','','1','2026-01-20 23:23:31','','Multi-Service','SYJ Organization','074700 59595',NULL,NULL,'Mega Center, C-511, Magarpatta, Hadapsar, Pune 411013','',NULL,NULL,NULL),
('21',NULL,'FilledTummy Pune','Food Donation','','1','2026-01-20 23:23:31','','Food Distribution','FilledTummy Pune','095615 51292',NULL,NULL,'Flat 2, Shangrila Apt, Shantisheela Society, Law College Rd, Pune 411038','',NULL,NULL,NULL),
('22',NULL,'Sanjivani NGO','Food, Medical, Education Support','','1','2026-01-20 23:23:31','','Multi-Service','Sanjivani NGO','089562 53672',NULL,NULL,'SR NO 59/1A, Sulai Complex, Flat No 17, near Desai Hospital, Mohammed Wadi, Pune 411060','',NULL,NULL,NULL),
('23',NULL,'Abhisree Foundation','Disability & Women Empowerment','','1','2026-01-20 23:23:31','','Disability Support','Abhisree Foundation','080089 62108',NULL,NULL,'Road 13, Shanti Nagar, Uppal, Hyderabad, Telangana 500039','',NULL,NULL,NULL),
('24',NULL,'Abhilasha Foundation NGO','Child Welfare, Skill Development','','1','2026-01-20 23:23:31','','Child Welfare','Abhilasha Foundation NGO','097699 86440',NULL,NULL,'Laxmi Chhaya Bungalow, Plot No. 27-27, RSC 11, Gorai 2, Borivali West, Mumbai 400091','',NULL,NULL,NULL),
('25',NULL,'Ratna Nidhi Charitable Trust','Books, Tablets, Toys, Clothes Distribution','','1','2026-01-20 23:23:31','','Donations','Ratna Nidhi Charitable Trust','085304 85324',NULL,NULL,'16-A, 12th Ln, Opp. Pavari School, Khetwadi, Girgaon, Mumbai 400004','',NULL,NULL,NULL),
('26',NULL,'SAAD Foundation','Education, Health, Community & Rural Development','','1','2026-01-20 23:23:31','','Multi-Service','SAAD Foundation','080820 54301',NULL,NULL,'Bungalow No. 62E, Kamgar Nagar Rd, Kurla, Mumbai 400024','',NULL,NULL,NULL),
('27',NULL,'Responsible Charity','Clothes & Food Donation','','1','2026-01-20 23:23:31','','Donations','Responsible Charity','020 2580 6256',NULL,NULL,'Shop No. 15, Sunshine Greens, Opp. Khadki Station, Off Aundh Rd, Pune 411020','',NULL,NULL,NULL),
('28',NULL,'A Ray Of Hope Charitable Trust','Child Welfare, Animal Welfare, Education, Donations','','1','2026-01-20 23:23:31','','Multi-Service','A Ray Of Hope Charitable Trust','097302 55167',NULL,NULL,'B4, Sheikh Safa Complex, 2, Waghmare Rd, Shankar Kalat Nagar, Wakad, Pune, Pimpri-Chinchwad 411057','',NULL,NULL,NULL),
('29',NULL,'VARA Foundations (R)','Child Welfare, Donation, Skill Development','','1','2026-01-20 23:23:31','','Child Welfare','VARA Foundations','099002 27171',NULL,NULL,'No.7, 5th Main Rd, Jagruthi Colony, Puttenahalli, JP Nagar 7th Phase, Bengaluru 560078','',NULL,NULL,NULL),
('30',NULL,'Helping Hand Foundation','Children, Disability, Homeless, Social Services','','1','2026-01-20 23:23:31','','Multi-Service','Helping Hand Foundation','070380 16790',NULL,NULL,'Near Army Garden, Shivdatta Nagar, Pimpri Gaon, Pimpri Colony, Pimpri-Chinchwad 411017','',NULL,NULL,NULL),
('31',NULL,'Aarogya Social Welfare International Foundation','Education','','1','2026-01-20 23:23:31','','Education','Aarogya Social Welfare International Foundation','',NULL,NULL,'24-3-271, Main Road, FCI Colony, Police Colony, Subedari, Hanamkonda, Telangana 506001','',NULL,NULL,NULL),
('32',NULL,'Eric Boys Welfare Association','Education, Skill Development','','1','2026-01-20 23:23:31','','Education','Eric Boys Welfare Association','',NULL,NULL,'Block No - 5, R/2, 17, Block Number 7, Transit Camp, Rajiv Gandhi Nagar, Dharavi, Mumbai 400017','',NULL,NULL,NULL),
('33',NULL,'Snehwan - Official','Child & Girls Education, Food & Grocery Donation','','1','2026-01-20 23:23:31','','Education & Food','Snehwan','082372 77615',NULL,NULL,'Snehwan, Koyali Phata, Near Koyali Forest, Chakan, Khed, Maharashtra 410501','',NULL,NULL,NULL),
('34',NULL,'KIDS Foundation','Children Charities, Education, Skill Development','','1','2026-01-20 23:23:31','','Education','KIDS Foundation','095955 40771',NULL,NULL,'Manas Mandir, Rashtrasant Tukdoji Maharaj Square, Old SBI Colony, Pratapnagar, Wardha 442001','',NULL,NULL,NULL),
('35',NULL,'Child Safe Foundation','Animal Welfare, Child Welfare, Donations, Education, Homeless','','1','2026-01-20 23:23:31','','Multi-Service','Child Safe Foundation','084839 68879',NULL,NULL,'G/50, Arihant Shopping Centre, Achole Rd, near Anita Palace, Nalasopara East, Maharashtra 401209','',NULL,NULL,NULL),
('36',NULL,'Sparsh Shelter Home','Education, Old Age Home, Health Care','','1','2026-01-20 23:23:31','','Multi-Service','Sparsh Shelter Home','076200 40230',NULL,NULL,'Sparsh House, Shrushti Chowk, Lane No. 2, near Mamta Sweet, Prabhat Nagar, Pimple Gurav, Pune, Pimpri-Chinchwad 411061','',NULL,NULL,NULL),
('37',NULL,'Ghar - Sant Ishwar Foundation','Child Care, Orphanage for Girls','','1','2026-01-20 23:23:31','','Child Welfare','Ghar - Sant Ishwar Foundation','093724 68457',NULL,NULL,'Plot No. 30 179, Deccan College Rd, Opposite Dashmesh Gurudwara, Jai Jawan Nagar, Ranjeet Nagar, Yerawada, Pune 411006','',NULL,NULL,NULL),
('38',NULL,'RESQ Charitable Trust','Dog Adoption, Medical Care, Aid, Treatment','','1','2026-01-20 23:23:31','','Animal Welfare','RESQ Charitable Trust','098909 99111',NULL,NULL,'Plot No. 3906, Paud, 115, Mulshi Rd, Hill Town, Chandani Chowk, Bavdhan, Pune 411023','',NULL,NULL,NULL),
('39',NULL,'Majha Ghar Foundation','Child Welfare, Homeless, Donation, Skill Development','','1','2026-01-20 23:23:31','','Multi-Service','Majha Ghar Foundation','074985 50554',NULL,NULL,'Plot No.50, Behind Gurukrupa Hospital, Near Brahma PG, Laxmi Chowk, Marunji Road, Hinjawadi, Pune 411057','',NULL,NULL,NULL),
('40',NULL,'Riddhi Siddhi Charitable Trust','Food Donation','','1','2026-01-20 23:23:31','','Food Distribution','Riddhi Siddhi Charitable Trust','098207 37415',NULL,NULL,'Office No. 20, Swapnadeep Apartment, Poonam Sagar Complex, Mira Road East, Mumbai 401107','',NULL,NULL,NULL),
('41',NULL,'Happy Faces Vadodara','Nonprofit, Social Services','','1','2026-01-20 23:23:31','','Social Service','Happy Faces Vadodara','098795 40744',NULL,NULL,'309, Vinayak Commercial Complex, Next to Saraswati Complex, Vaishnavdevi Society, Manjalpur, Vadodara, Gujarat 390011','',NULL,NULL,NULL),
('42',NULL,'Ek Parivartan Foundation','Community Support, Education, Food & Clothing Distribution','info@epfngo.org','1','2026-01-20 23:23:31','','Multi-Service','Ek Parivartan Foundation','099537 56764',NULL,NULL,'Street No. 13, Veer Savarkar Block, Block E, Laxmi Nagar, Delhi, 110092','',NULL,NULL,NULL),
('43',NULL,'NAR FOUNDATION','Education, Food Distribution, Clothes Distribution, Job References, Old Age Home Visits','','1','2026-01-20 23:23:31','','Multi-Service','NAR FOUNDATION','080821 40693',NULL,NULL,'Sunder Nagar, Ekta Nagar Rd New Link Road Mahavir Nagar, near Kandivali, Mumbai, Maharashtra 400067','',NULL,NULL,NULL),
('44',NULL,'HWCT India Foundation - Human Welfare Charitable Trust','POSHAN Project - Nutrition & Health for rural children, Food & Nutrition Programs','','1','2026-01-20 23:23:31','','Health & Nutrition','HWCT India Foundation','098207 37841',NULL,NULL,'Khandelwal Layout, Evershine Nagar, Malad West, Mumbai, Maharashtra 400064','',NULL,NULL,NULL),
('45',NULL,'Save Tears Foundation','Support for underprivileged children, Medical aid for critical ailments, Women empowerment, Elderly support, Orphan care','info@savetears.org','1','2026-01-20 23:23:31','','Multi-Service','Save Tears Foundation','078886 76667',NULL,NULL,'Building No A-1, Laram Center, 302 (West Side, Andheri West, above Sunil Jeweler\'s, next to NADCO Shopping Centre), Railway Colony, Andheri East, Mumbai, Maharashtra 400058','',NULL,NULL,NULL),
('46',NULL,'Tejaswini Samajik Sanstha','Food Donation, School Kit Donation, Healthcare Donation, Sponsorships, Clothing & Blankets, Medical & Educational Supplies, Hygiene Products','','1','2026-01-20 23:23:31','','Multi-Service','Tejaswini Samajik Sanstha','098900 01164',NULL,NULL,'near Wagheshwar Temple, beside Jama Masjid, Wageshwar Nagar, Wagholi, Pune, Maharashtra 412207','',NULL,NULL,NULL),
('47',NULL,'Sukachi Sawali Welfare Foundation','Community Welfare, Food & Essentials Distribution','','1','2026-01-20 23:23:31','','Multi-Service','Sukachi Sawali Welfare Foundation','097022 26444',NULL,NULL,'1408, Bldg no 2, Morarji Mill Compound, Kandivali, Ashok Nagar, Kandivali East, Mumbai, Maharashtra 400101','',NULL,NULL,NULL),
('48',NULL,'Aarna Foundation NGO','Vidyadaan, Nutritious Meal Distribution to hungry and homeless','','1','2026-01-20 23:23:31','','Food Distribution','Aarna Foundation NGO','095940 96655',NULL,NULL,'Shop no -1, Gulmohar Society, Patilwadi Rd, near Sankalp School, Patil Wadi, Sawarkar Nagar, Savarkar Nagar, Thane West, Thane, Maharashtra 400606','',NULL,NULL,NULL),
('49',NULL,'Feeding India','Large-scale meal programs; helped serve 23+ crore meals via 1100+ centres across 150+ cities','','1','2026-01-20 23:23:31','','Food Distribution','Feeding India','098711 78810',NULL,NULL,'2nd Floor, Plot No. 13, Local Shopping Center, Pocket 1, Sector B, Vasant Kunj, New Delhi, Delhi 110070','',NULL,NULL,NULL),
('50',NULL,'Nirankar Vastigruh','Accommodation, Education, Dance & Singing Lessons, Events, Health Care, Summer Camps','','1','2026-01-20 23:23:31','','Multi-Service','Nirankar Vastigruh','095618 16451',NULL,NULL,'Near Gaikwad Society, Lane No - 1 A Railway Crossing, Sasane Nagar Bypass Rd, Sayyed Nagar, Hadapsar, Pune, Maharashtra 411028','',NULL,NULL,NULL),
('51',NULL,'Prachi Ngo','cvbgvb','sakhitapre9@gmail.com','1','2026-01-21 00:03:04','dvsdv','food','sakhi','2888888888',NULL,NULL,'kothrud,pune','c6b3491f15b3f66f30c82b87431e60114de8abe2e423cb5fdb5ae856b6f64279',NULL,NULL,NULL),
('52',NULL,'Snehadhar Sankul','szdgdrhgfnhtrhjtr','prachipawar5133@gmail.com','1','2026-01-21 12:54:57','dvsdv','food','Prachi','2888888888',NULL,NULL,'prachipawar5133@gmail.com','c6b3491f15b3f66f30c82b87431e60114de8abe2e423cb5fdb5ae856b6f64279',NULL,NULL,NULL),
('53',NULL,'Smita Tapre','Register Your NGO\nJoin our community and make a difference','smitatapre2104@gmail.com','1','2026-01-23 20:55:42','12A/80G','food','Smita','1234567891',NULL,NULL,'kothrud,pune','4700b1e6eff15da757835567c686da0f7c606e64ae0d9fa5471548039fae2c43',NULL,NULL,NULL),
('54',NULL,'Sakhi Ghar','Register Your NGO\nJoin our community and make a difference','aayeinbaigan7@gmail.com','1','2026-02-05 19:51:20','12A/80G','food','sakhi','1234567894',NULL,NULL,'gananjay society ganesh colony kothrud','7d8c7fb2a9dec3619484d829d9f8b74051b1400d0830eda3d92c35009e86b6de',NULL,NULL,NULL),
('55',NULL,'poonam chavhan','abc','poonam.chavhan@zealeducation.com','1','2026-02-06 12:07:23','13tgy','food','poonam','9324567823',NULL,NULL,'Narhe','7fc3377bf8db2b55efc80c845238faf853dc2c8d30ac5e095360fdb6bce1cbc2',NULL,NULL,NULL),
('56',NULL,'poonam chavhan','abc','poonam.chavhan@zealeducation.com','1','2026-02-06 12:07:27','13tgy','food','poonam','9324567823',NULL,NULL,'Narhe','7fc3377bf8db2b55efc80c845238faf853dc2c8d30ac5e095360fdb6bce1cbc2',NULL,NULL,NULL);

DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ngo_id` int(11) NOT NULL,
  `donation_id` int(11) NOT NULL,
  `message` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `donation_id` (`donation_id`),
  KEY `idx_ngo_read` (`ngo_id`,`is_read`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`ngo_id`) REFERENCES `ngos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`donation_id`) REFERENCES `donations` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `pickup_schedules`;
CREATE TABLE `pickup_schedules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `claim_id` int(11) NOT NULL,
  `pickup_date` date NOT NULL,
  `time_slot` enum('Morning','Afternoon','Evening') COLLATE utf8mb4_unicode_ci DEFAULT 'Afternoon',
  `pickup_notes` text COLLATE utf8mb4_unicode_ci,
  `scheduled_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `claim_id` (`claim_id`),
  CONSTRAINT `pickup_schedules_ibfk_1` FOREIGN KEY (`claim_id`) REFERENCES `claimed_donations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `push_subscriptions`;
CREATE TABLE `push_subscriptions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `endpoint` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `p256dh` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `auth` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(190) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(190) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('donor','ngo','admin') COLLATE utf8mb4_unicode_ci DEFAULT 'donor',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL,
  `latitude` decimal(10,8) DEFAULT NULL COMMENT 'Latitude of donor location',
  `longitude` decimal(11,8) DEFAULT NULL COMMENT 'Longitude of donor location',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `users` (`id`,`name`,`email`,`location`,`phone`,`password_hash`,`role`,`created_at`,`updated_at`,`latitude`,`longitude`) VALUES
('1','smitaaaa','sakhitapre9@gmail.com','pune/kasba','2222255555','c6b3491f15b3f66f30c82b87431e60114de8abe2e423cb5fdb5ae856b6f64279','donor','2026-01-24 11:23:36',NULL,NULL,NULL),
('2','varun','sathevarun3@gmail.com','s','4444444444','e83bd2de038d25b9c98c3c50a10cd3e26fd249a4aa4ae6c387acfd805cbb25e3','donor','2026-01-24 12:39:55',NULL,NULL,NULL),
('11','Test User','testuser999@example.com','Test City','9876543210','d519397a4e89a7a66d28a266ed00a679bdee93fddec9ebba7d01ff27c39c1a99','donor','2026-01-24 19:37:35',NULL,NULL,NULL),
('13','Test User','testuser_1769263845241@example.com','Test City','9876543210','d519397a4e89a7a66d28a266ed00a679bdee93fddec9ebba7d01ff27c39c1a99','donor','2026-01-24 19:40:45',NULL,NULL,NULL),
('15','sakhitapre','smitatapre2104@gmail.com','tt','2222266666','55b6dc1364bcea5a848ca794492f5972a30509583334eee3379e728215c4d1a2','donor','2026-01-24 19:42:04',NULL,NULL,NULL),
('16','Era','aayeinbaigan7@gmail.com','sss','9999922222','fea674873750f90de5fcdfd07903d1bb416ed2f5ad743de1d79636106a20d3c5','donor','2026-01-24 20:11:48',NULL,NULL,NULL),
('17','payal y','yadavpayal001212@gmail.com','khadakwasla','9373322038','1a91f68151ee656f13b76d045d196a9181b45fce2c7901c4496f94ec7b083dbf','donor','2026-01-31 08:51:05',NULL,NULL,NULL);

SET FOREIGN_KEY_CHECKS=1;
