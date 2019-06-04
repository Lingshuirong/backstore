/*
 Navicat MySQL Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : localhost:3306
 Source Schema         : backstore

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 04/06/2019 19:02:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for order_tb
-- ----------------------------
DROP TABLE IF EXISTS `order_tb`;
CREATE TABLE `order_tb`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `id_card_number` varchar(18) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `bank_card_number` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mobile` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `recommand_job_number` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pre_paid_amount` int(11) NULL DEFAULT NULL,
  `paid_status` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '待支付',
  `paid_datetime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `commit_datetime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `update_datetime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of order_tb
-- ----------------------------
INSERT INTO `order_tb` VALUES (1, '12312', '2131', '12121', '13421421421', '123456', 398, '已支付', NULL, '2019-05-31 19:38:56', '2019-05-31 19:38:56');
INSERT INTO `order_tb` VALUES (2, '12312', '2131', '12121', '13421421421', '123456', 398, '已支付', NULL, '2019-05-31 19:40:04', '2019-05-31 19:40:04');
INSERT INTO `order_tb` VALUES (3, '12312', '2131', '12121', '13421421421', '123456', 398, '已支付', NULL, '2019-05-31 19:41:19', '2019-05-31 19:41:19');
INSERT INTO `order_tb` VALUES (4, '12312', '2131', '12121', '13421421421', '123456', 398, '已支付', NULL, '2019-05-31 19:42:37', '2019-05-31 19:42:37');
INSERT INTO `order_tb` VALUES (5, '12312', '2131', '12121', '13421421421', '123456', 398, '已支付', NULL, '2019-05-31 19:42:49', '2019-05-31 19:42:49');
INSERT INTO `order_tb` VALUES (6, '12312', '2131', '12121', '13421421421', '123456', 398, '已支付', NULL, '2019-05-31 19:44:25', '2019-05-31 19:44:25');
INSERT INTO `order_tb` VALUES (7, '121', '111', '132', '13254449448', '123456', 398, '已支付', NULL, '2019-05-31 20:06:51', '2019-05-31 20:06:51');
INSERT INTO `order_tb` VALUES (8, '121', '111', '132', '13254449448', '123456', 398, '已支付', NULL, '2019-05-31 20:06:55', '2019-05-31 20:06:55');
INSERT INTO `order_tb` VALUES (9, '121', '111', '132', '13254449448', '123456', 398, '已支付', NULL, '2019-05-31 20:06:59', '2019-05-31 20:06:59');
INSERT INTO `order_tb` VALUES (10, '121', '111', '132', '13254449448', '123456', 398, '已支付', NULL, '2019-05-31 20:07:57', '2019-05-31 20:07:57');
INSERT INTO `order_tb` VALUES (11, '121', '111', '132', '13254449448', '123456', 398, '已支付', NULL, '2019-05-31 20:08:02', '2019-05-31 20:08:02');
INSERT INTO `order_tb` VALUES (12, '121', '111', '132', '13254449448', '123456', 398, '已支付', NULL, '2019-05-31 20:08:06', '2019-05-31 20:08:06');
INSERT INTO `order_tb` VALUES (13, '121', '111', '132', '13254449448', '123456', 398, '已支付', NULL, '2019-05-31 20:09:20', '2019-05-31 20:09:20');
INSERT INTO `order_tb` VALUES (14, '121', '111', '132', '13254449448', '123456', 398, '已支付', NULL, '2019-05-31 20:11:32', '2019-05-31 20:11:32');
INSERT INTO `order_tb` VALUES (15, '123', '12313', '123321', '13424242424', '123456', 398, '待支付', NULL, '2019-05-31 20:16:49', '2019-05-31 20:16:49');
INSERT INTO `order_tb` VALUES (16, '卢布', '1458656', '1234656', '18122702544', '111111', 398, '待支付', NULL, '2019-06-03 22:09:05', '2019-06-03 22:09:05');
INSERT INTO `order_tb` VALUES (17, '111111111111111', '111111111111', '1456898747', '13533838536', '111111', 498, '待支付', NULL, '2019-06-03 22:11:20', '2019-06-03 22:11:20');
INSERT INTO `order_tb` VALUES (18, '11111111111111', '122321312', '4324', '13323231323', '111111', 498, '待支付', NULL, '2019-06-03 22:17:20', '2019-06-03 22:17:20');
INSERT INTO `order_tb` VALUES (19, '11123', '1233312312', '2131231', '13432432423', '111111', 398, '已支付', NULL, '2019-06-03 22:19:17', '2019-06-03 22:19:17');
INSERT INTO `order_tb` VALUES (20, '11111111111111', '1113213421', '33333', '13543243243', '111111', 398, '待支付', NULL, '2019-06-03 22:21:19', '2019-06-03 22:21:19');
INSERT INTO `order_tb` VALUES (21, '11111111111', '11111111321', '43', '13424324324', '111111', 398, '待支付', NULL, '2019-06-03 22:24:24', '2019-06-03 22:24:24');
INSERT INTO `order_tb` VALUES (22, '111111321', '3323', '5234523', '13321321321', '111111', 398, '待支付', NULL, '2019-06-03 22:29:20', '2019-06-03 22:29:20');
INSERT INTO `order_tb` VALUES (23, '32131', '132213', '5435', '13421342142', '111111', 398, '待支付', NULL, '2019-06-03 22:31:20', '2019-06-03 22:31:20');
INSERT INTO `order_tb` VALUES (24, '1123', '13231', '123', '13341234214', '111111', 398, '待支付', NULL, '2019-06-04 10:01:24', '2019-06-04 10:01:24');
INSERT INTO `order_tb` VALUES (25, '1111111113', '2321321', '11111', '14432144214', '111111', 398, '待支付', NULL, '2019-06-04 13:59:27', '2019-06-04 13:59:27');
INSERT INTO `order_tb` VALUES (26, '1111111111', '13213213213', '4324', '13242142142', '111111', 398, '待支付', NULL, '2019-06-04 14:01:50', '2019-06-04 14:01:50');
INSERT INTO `order_tb` VALUES (27, '1132', '1321', '121', '13213213213', '111111', 398, '已支付', NULL, '2019-06-04 14:03:11', '2019-06-04 14:03:11');
INSERT INTO `order_tb` VALUES (28, '111', '132131', '34321', '13213213213', '111111', 398, '已支付', NULL, '2019-06-04 14:19:09', '2019-06-04 14:19:09');

-- ----------------------------
-- Table structure for sys_info
-- ----------------------------
DROP TABLE IF EXISTS `sys_info`;
CREATE TABLE `sys_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img_id` smallint(6) NULL DEFAULT NULL,
  `qr_url` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 134 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_info
-- ----------------------------
INSERT INTO `sys_info` VALUES (130, NULL, 'timg (2).jpg');
INSERT INTO `sys_info` VALUES (133, NULL, 'timg (1).jpg');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password_hash` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `job_number` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `real_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `mobile` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `id_card_number` varchar(18) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `role` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `reg_time` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `name`, `job_number`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (29, 'admin', 'pbkdf2:sha256:150000$g2XfpAkt$725b42c99e54d5434b7bb5f1f616ab92004987b68a4c92a372c090687e10ab7d', '100016', '超级管理员', '18122783501', NULL, '管理员', '2019-06-03 22:17:14');

SET FOREIGN_KEY_CHECKS = 1;
