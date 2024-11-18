
CREATE TABLE `data_log` (
 `rowID` int(11) NOT NULL AUTO_INCREMENT,
 `responses` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`responses`)),
 `question_order` text DEFAULT NULL,
 `trial_type` varchar(45) DEFAULT NULL,
 `trial_index` int(11) DEFAULT NULL,
 `rt` int(20) DEFAULT NULL,
 `condition` text DEFAULT NULL,
 `repetition` varchar(20) DEFAULT NULL,
 `label_options` text DEFAULT NULL,
 `bar_cols` text DEFAULT NULL,
 `answer_key` text DEFAULT NULL,
 `label_responses` text DEFAULT NULL,
 `category` varchar(45) DEFAULT NULL,
 `accuracies` text DEFAULT NULL,
 `pal_source` varchar(45) DEFAULT NULL,
 `total_accuracy` float DEFAULT NULL,
 `order_num` varchar(15) DEFAULT NULL,
 `subject_id` text DEFAULT NULL,
 `workerID` varchar(100) DEFAULT NULL,
 PRIMARY KEY (`rowID`)
);


CREATE TABLE `register_log` (
 `row` int(11) NOT NULL AUTO_INCREMENT,
 `completionCode` varchar(45) DEFAULT NULL,
 `workerID` varchar(45) DEFAULT NULL,
 PRIMARY KEY (`row`)
);




