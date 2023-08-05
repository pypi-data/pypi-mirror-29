PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "django_geo_db_country" ("country_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL UNIQUE, "abbreviation" varchar(2) NOT NULL UNIQUE, "continent_id" integer NOT NULL REFERENCES "django_geo_db_continent" ("continent_id"), "geocoordinate_id" integer NOT NULL REFERENCES "django_geo_db_geocoordinate" ("geocoordinate_id"));
INSERT INTO "django_geo_db_country" VALUES(1,'Afghanistan','AF',1,1);
INSERT INTO "django_geo_db_country" VALUES(2,'Åland Islands','AW',2,2);
INSERT INTO "django_geo_db_country" VALUES(3,'Albania','AL',2,3);
INSERT INTO "django_geo_db_country" VALUES(4,'Algeria','DZ',3,4);
INSERT INTO "django_geo_db_country" VALUES(5,'American Samoa','AR',4,5);
INSERT INTO "django_geo_db_country" VALUES(6,'Andorra','AD',2,6);
INSERT INTO "django_geo_db_country" VALUES(7,'Angola','AN',3,7);
INSERT INTO "django_geo_db_country" VALUES(8,'Anguilla','AI',5,8);
INSERT INTO "django_geo_db_country" VALUES(9,'Antigua and Barbuda','AG',5,9);
INSERT INTO "django_geo_db_country" VALUES(10,'Argentina','AQ',6,10);
INSERT INTO "django_geo_db_country" VALUES(11,'Armenia','AM',1,11);
INSERT INTO "django_geo_db_country" VALUES(12,'Aruba','AU',5,12);
INSERT INTO "django_geo_db_country" VALUES(13,'Australia','AT',7,13);
INSERT INTO "django_geo_db_country" VALUES(14,'Austria','AS',2,14);
INSERT INTO "django_geo_db_country" VALUES(15,'Azerbaijan','AZ',1,15);
INSERT INTO "django_geo_db_country" VALUES(16,'Bahamas','BS',5,16);
INSERT INTO "django_geo_db_country" VALUES(17,'Bahrain','BH',1,17);
INSERT INTO "django_geo_db_country" VALUES(18,'Bangladesh','BD',1,18);
INSERT INTO "django_geo_db_country" VALUES(19,'Barbados','BB',5,19);
INSERT INTO "django_geo_db_country" VALUES(20,'Belarus','BY',2,20);
INSERT INTO "django_geo_db_country" VALUES(21,'Belgium','BE',2,21);
INSERT INTO "django_geo_db_country" VALUES(22,'Belize','BZ',5,22);
INSERT INTO "django_geo_db_country" VALUES(23,'Benin','BJ',3,23);
INSERT INTO "django_geo_db_country" VALUES(24,'Bermuda','BM',5,24);
INSERT INTO "django_geo_db_country" VALUES(25,'Bhutan','BT',1,25);
INSERT INTO "django_geo_db_country" VALUES(26,'Bolivia (Plurinational State of)','BO',6,26);
INSERT INTO "django_geo_db_country" VALUES(27,'Bosnia and Herzegovina','BA',2,27);
INSERT INTO "django_geo_db_country" VALUES(28,'Botswana','BW',3,28);
INSERT INTO "django_geo_db_country" VALUES(29,'Brazil','BR',6,29);
INSERT INTO "django_geo_db_country" VALUES(30,'Brunei Darussalam','BN',1,30);
INSERT INTO "django_geo_db_country" VALUES(31,'Bulgaria','BG',2,31);
INSERT INTO "django_geo_db_country" VALUES(32,'Burkina Faso','BF',3,32);
INSERT INTO "django_geo_db_country" VALUES(33,'Burundi','BI',3,33);
INSERT INTO "django_geo_db_country" VALUES(34,'Cabo Verde','CV',3,34);
INSERT INTO "django_geo_db_country" VALUES(35,'Cambodia','KH',1,35);
INSERT INTO "django_geo_db_country" VALUES(36,'Cameroon','CM',3,36);
INSERT INTO "django_geo_db_country" VALUES(37,'Canada','CA',5,37);
INSERT INTO "django_geo_db_country" VALUES(38,'Cayman Islands','KY',5,38);
INSERT INTO "django_geo_db_country" VALUES(39,'Central African Republic','CF',3,39);
INSERT INTO "django_geo_db_country" VALUES(40,'Chad','TD',3,40);
INSERT INTO "django_geo_db_country" VALUES(41,'Chile','CL',6,41);
INSERT INTO "django_geo_db_country" VALUES(42,'China','CN',1,42);
INSERT INTO "django_geo_db_country" VALUES(43,'Colombia','CO',6,43);
INSERT INTO "django_geo_db_country" VALUES(44,'Comoros','KM',3,44);
INSERT INTO "django_geo_db_country" VALUES(45,'Congo','CG',3,45);
INSERT INTO "django_geo_db_country" VALUES(46,'Congo (Democratic Republic of the)','CD',3,46);
INSERT INTO "django_geo_db_country" VALUES(47,'Cook Islands','CK',4,47);
INSERT INTO "django_geo_db_country" VALUES(48,'Costa Rica','CR',5,48);
INSERT INTO "django_geo_db_country" VALUES(49,'Côte d''Ivoire','CI',3,49);
INSERT INTO "django_geo_db_country" VALUES(50,'Croatia','HR',2,50);
INSERT INTO "django_geo_db_country" VALUES(51,'Cuba','CU',5,51);
INSERT INTO "django_geo_db_country" VALUES(52,'Cyprus','CY',1,52);
INSERT INTO "django_geo_db_country" VALUES(53,'Czech Republic','CZ',2,53);
INSERT INTO "django_geo_db_country" VALUES(54,'Denmark','DK',2,54);
INSERT INTO "django_geo_db_country" VALUES(55,'Djibouti','DJ',3,55);
INSERT INTO "django_geo_db_country" VALUES(56,'Dominica','DM',5,56);
INSERT INTO "django_geo_db_country" VALUES(57,'Dominican Republic','DO',5,57);
INSERT INTO "django_geo_db_country" VALUES(58,'Ecuador','EC',6,58);
INSERT INTO "django_geo_db_country" VALUES(59,'Egypt','EG',3,59);
INSERT INTO "django_geo_db_country" VALUES(60,'El Salvador','SV',5,60);
INSERT INTO "django_geo_db_country" VALUES(61,'Equatorial Guinea','GQ',3,61);
INSERT INTO "django_geo_db_country" VALUES(62,'Eritrea','ER',3,62);
INSERT INTO "django_geo_db_country" VALUES(63,'Estonia','EE',2,63);
INSERT INTO "django_geo_db_country" VALUES(64,'Ethiopia','ET',3,64);
INSERT INTO "django_geo_db_country" VALUES(65,'Falkland Islands (Malvinas)','FK',6,65);
INSERT INTO "django_geo_db_country" VALUES(66,'Faroe Islands','FO',2,66);
INSERT INTO "django_geo_db_country" VALUES(67,'Fiji','FJ',4,67);
INSERT INTO "django_geo_db_country" VALUES(68,'Finland','FI',2,68);
INSERT INTO "django_geo_db_country" VALUES(69,'France','FR',2,69);
INSERT INTO "django_geo_db_country" VALUES(70,'French Guiana','GF',6,70);
INSERT INTO "django_geo_db_country" VALUES(71,'French Polynesia','PF',4,71);
INSERT INTO "django_geo_db_country" VALUES(72,'Gabon','GA',3,72);
INSERT INTO "django_geo_db_country" VALUES(73,'Gambia','GM',3,73);
INSERT INTO "django_geo_db_country" VALUES(74,'Georgia','GE',1,74);
INSERT INTO "django_geo_db_country" VALUES(75,'Germany','DE',2,75);
INSERT INTO "django_geo_db_country" VALUES(76,'Ghana','GH',3,76);
INSERT INTO "django_geo_db_country" VALUES(77,'Gibraltar','GI',2,77);
INSERT INTO "django_geo_db_country" VALUES(78,'Greece','GR',2,78);
INSERT INTO "django_geo_db_country" VALUES(79,'Greenland','GL',5,79);
INSERT INTO "django_geo_db_country" VALUES(80,'Grenada','GD',5,80);
INSERT INTO "django_geo_db_country" VALUES(81,'Guadeloupe','GP',5,81);
INSERT INTO "django_geo_db_country" VALUES(82,'Guam','GU',4,82);
INSERT INTO "django_geo_db_country" VALUES(83,'Guatemala','GT',5,83);
INSERT INTO "django_geo_db_country" VALUES(84,'Guernsey','GG',2,84);
INSERT INTO "django_geo_db_country" VALUES(85,'Guinea','GN',3,85);
INSERT INTO "django_geo_db_country" VALUES(86,'Guinea-Bissau','GW',3,86);
INSERT INTO "django_geo_db_country" VALUES(87,'Guyana','GY',6,87);
INSERT INTO "django_geo_db_country" VALUES(88,'Haiti','HT',5,88);
INSERT INTO "django_geo_db_country" VALUES(89,'Holy See','VA',2,89);
INSERT INTO "django_geo_db_country" VALUES(90,'Honduras','HN',5,90);
INSERT INTO "django_geo_db_country" VALUES(91,'Hong Kong','HK',1,91);
INSERT INTO "django_geo_db_country" VALUES(92,'Hungary','HU',2,92);
INSERT INTO "django_geo_db_country" VALUES(93,'Iceland','IS',2,93);
INSERT INTO "django_geo_db_country" VALUES(94,'India','IN',1,94);
INSERT INTO "django_geo_db_country" VALUES(95,'Indonesia','ID',1,95);
INSERT INTO "django_geo_db_country" VALUES(96,'Iran (Islamic Republic of)','IR',1,96);
INSERT INTO "django_geo_db_country" VALUES(97,'Iraq','IQ',1,97);
INSERT INTO "django_geo_db_country" VALUES(98,'Ireland','IE',2,98);
INSERT INTO "django_geo_db_country" VALUES(99,'Isle of Man','IM',2,99);
INSERT INTO "django_geo_db_country" VALUES(100,'Israel','IL',1,100);
INSERT INTO "django_geo_db_country" VALUES(101,'Italy','IT',2,101);
INSERT INTO "django_geo_db_country" VALUES(102,'Jamaica','JM',5,102);
INSERT INTO "django_geo_db_country" VALUES(103,'Japan','JP',1,103);
INSERT INTO "django_geo_db_country" VALUES(104,'Jersey','JE',2,104);
INSERT INTO "django_geo_db_country" VALUES(105,'Jordan','JO',1,105);
INSERT INTO "django_geo_db_country" VALUES(106,'Kazakhstan','KZ',1,106);
INSERT INTO "django_geo_db_country" VALUES(107,'Kenya','KE',3,107);
INSERT INTO "django_geo_db_country" VALUES(108,'Kiribati','KI',4,108);
INSERT INTO "django_geo_db_country" VALUES(109,'Korea (Democratic People''s Republic of)','KP',1,109);
INSERT INTO "django_geo_db_country" VALUES(110,'Korea (Republic of)','KR',1,110);
INSERT INTO "django_geo_db_country" VALUES(111,'Kuwait','KW',1,111);
INSERT INTO "django_geo_db_country" VALUES(112,'Kyrgyzstan','KG',1,112);
INSERT INTO "django_geo_db_country" VALUES(113,'Lao People''s Democratic Republic','LA',1,113);
INSERT INTO "django_geo_db_country" VALUES(114,'Latvia','LV',2,114);
INSERT INTO "django_geo_db_country" VALUES(115,'Lebanon','LB',1,115);
INSERT INTO "django_geo_db_country" VALUES(116,'Lesotho','LS',3,116);
INSERT INTO "django_geo_db_country" VALUES(117,'Liberia','LR',3,117);
INSERT INTO "django_geo_db_country" VALUES(118,'Libya','LY',3,118);
INSERT INTO "django_geo_db_country" VALUES(119,'Liechtenstein','LI',2,119);
INSERT INTO "django_geo_db_country" VALUES(120,'Lithuania','LT',2,120);
INSERT INTO "django_geo_db_country" VALUES(121,'Luxembourg','LU',2,121);
INSERT INTO "django_geo_db_country" VALUES(122,'Macao','MO',1,122);
INSERT INTO "django_geo_db_country" VALUES(123,'Macedonia (the former Yugoslav Republic of)','MK',2,123);
INSERT INTO "django_geo_db_country" VALUES(124,'Madagascar','MG',3,124);
INSERT INTO "django_geo_db_country" VALUES(125,'Malawi','MW',3,125);
INSERT INTO "django_geo_db_country" VALUES(126,'Malaysia','MY',1,126);
INSERT INTO "django_geo_db_country" VALUES(127,'Maldives','MV',1,127);
INSERT INTO "django_geo_db_country" VALUES(128,'Mali','ML',3,128);
INSERT INTO "django_geo_db_country" VALUES(129,'Malta','MT',2,129);
INSERT INTO "django_geo_db_country" VALUES(130,'Marshall Islands','MH',4,130);
INSERT INTO "django_geo_db_country" VALUES(131,'Martinique','MQ',5,131);
INSERT INTO "django_geo_db_country" VALUES(132,'Mauritania','MR',3,132);
INSERT INTO "django_geo_db_country" VALUES(133,'Mauritius','MU',3,133);
INSERT INTO "django_geo_db_country" VALUES(134,'Mayotte','YT',3,134);
INSERT INTO "django_geo_db_country" VALUES(135,'Mexico','MX',5,135);
INSERT INTO "django_geo_db_country" VALUES(136,'Micronesia (Federated States of)','FM',4,136);
INSERT INTO "django_geo_db_country" VALUES(137,'Moldova (Republic of)','MD',2,137);
INSERT INTO "django_geo_db_country" VALUES(138,'Monaco','MC',2,138);
INSERT INTO "django_geo_db_country" VALUES(139,'Mongolia','MN',1,139);
INSERT INTO "django_geo_db_country" VALUES(140,'Montenegro','ME',2,140);
INSERT INTO "django_geo_db_country" VALUES(141,'Montserrat','MS',5,141);
INSERT INTO "django_geo_db_country" VALUES(142,'Morocco','MA',3,142);
INSERT INTO "django_geo_db_country" VALUES(143,'Mozambique','MZ',3,143);
INSERT INTO "django_geo_db_country" VALUES(144,'Myanmar','MM',1,144);
INSERT INTO "django_geo_db_country" VALUES(145,'Namibia','NA',3,145);
INSERT INTO "django_geo_db_country" VALUES(146,'Nauru','NR',4,146);
INSERT INTO "django_geo_db_country" VALUES(147,'Nepal','NP',1,147);
INSERT INTO "django_geo_db_country" VALUES(148,'Netherlands','NL',2,148);
INSERT INTO "django_geo_db_country" VALUES(149,'New Caledonia','NC',4,149);
INSERT INTO "django_geo_db_country" VALUES(150,'New Zealand','NZ',4,150);
INSERT INTO "django_geo_db_country" VALUES(151,'Nicaragua','NI',5,151);
INSERT INTO "django_geo_db_country" VALUES(152,'Niger','NE',3,152);
INSERT INTO "django_geo_db_country" VALUES(153,'Nigeria','NG',3,153);
INSERT INTO "django_geo_db_country" VALUES(154,'Niue','NU',4,154);
INSERT INTO "django_geo_db_country" VALUES(155,'Norfolk Island','NF',4,155);
INSERT INTO "django_geo_db_country" VALUES(156,'Northern Mariana Islands','MP',4,156);
INSERT INTO "django_geo_db_country" VALUES(157,'Norway','NO',2,157);
INSERT INTO "django_geo_db_country" VALUES(158,'Oman','OM',1,158);
INSERT INTO "django_geo_db_country" VALUES(159,'Pakistan','PK',1,159);
INSERT INTO "django_geo_db_country" VALUES(160,'Palau','PW',4,160);
INSERT INTO "django_geo_db_country" VALUES(161,'Palestine, State of','PS',1,161);
INSERT INTO "django_geo_db_country" VALUES(162,'Panama','PA',5,162);
INSERT INTO "django_geo_db_country" VALUES(163,'Papua New Guinea','PG',4,163);
INSERT INTO "django_geo_db_country" VALUES(164,'Paraguay','PY',6,164);
INSERT INTO "django_geo_db_country" VALUES(165,'Peru','PE',6,165);
INSERT INTO "django_geo_db_country" VALUES(166,'Philippines','PH',1,166);
INSERT INTO "django_geo_db_country" VALUES(167,'Pitcairn','PN',4,167);
INSERT INTO "django_geo_db_country" VALUES(168,'Poland','PL',2,168);
INSERT INTO "django_geo_db_country" VALUES(169,'Portugal','PT',2,169);
INSERT INTO "django_geo_db_country" VALUES(170,'Puerto Rico','PR',5,170);
INSERT INTO "django_geo_db_country" VALUES(171,'Qatar','QA',1,171);
INSERT INTO "django_geo_db_country" VALUES(172,'Réunion','RE',3,172);
INSERT INTO "django_geo_db_country" VALUES(173,'Romania','RO',2,173);
INSERT INTO "django_geo_db_country" VALUES(174,'Russian Federation','RU',2,174);
INSERT INTO "django_geo_db_country" VALUES(175,'Rwanda','RW',3,175);
INSERT INTO "django_geo_db_country" VALUES(176,'Saint Helena, Ascension and Tristan da Cunha','SH',3,176);
INSERT INTO "django_geo_db_country" VALUES(177,'Saint Kitts and Nevis','KN',5,177);
INSERT INTO "django_geo_db_country" VALUES(178,'Saint Lucia','LC',5,178);
INSERT INTO "django_geo_db_country" VALUES(179,'Saint Pierre and Miquelon','PM',5,179);
INSERT INTO "django_geo_db_country" VALUES(180,'Saint Vincent and the Grenadines','VC',5,180);
INSERT INTO "django_geo_db_country" VALUES(181,'Samoa','WS',4,181);
INSERT INTO "django_geo_db_country" VALUES(182,'San Marino','SM',2,182);
INSERT INTO "django_geo_db_country" VALUES(183,'Sao Tome and Principe','ST',3,183);
INSERT INTO "django_geo_db_country" VALUES(184,'Saudi Arabia','SA',1,184);
INSERT INTO "django_geo_db_country" VALUES(185,'Senegal','SN',3,185);
INSERT INTO "django_geo_db_country" VALUES(186,'Serbia','RS',2,186);
INSERT INTO "django_geo_db_country" VALUES(187,'Seychelles','SC',3,187);
INSERT INTO "django_geo_db_country" VALUES(188,'Sierra Leone','SL',3,188);
INSERT INTO "django_geo_db_country" VALUES(189,'Singapore','SG',1,189);
INSERT INTO "django_geo_db_country" VALUES(190,'Slovakia','SK',2,190);
INSERT INTO "django_geo_db_country" VALUES(191,'Slovenia','SI',2,191);
INSERT INTO "django_geo_db_country" VALUES(192,'Solomon Islands','SB',4,192);
INSERT INTO "django_geo_db_country" VALUES(193,'Somalia','SO',3,193);
INSERT INTO "django_geo_db_country" VALUES(194,'South Africa','ZA',3,194);
INSERT INTO "django_geo_db_country" VALUES(195,'Spain','ES',2,195);
INSERT INTO "django_geo_db_country" VALUES(196,'Sri Lanka','LK',1,196);
INSERT INTO "django_geo_db_country" VALUES(197,'Sudan','SD',3,197);
INSERT INTO "django_geo_db_country" VALUES(198,'Suriname','SR',6,198);
INSERT INTO "django_geo_db_country" VALUES(199,'Svalbard and Jan Mayen','SJ',2,199);
INSERT INTO "django_geo_db_country" VALUES(200,'Swaziland','SZ',3,200);
INSERT INTO "django_geo_db_country" VALUES(201,'Sweden','SE',2,201);
INSERT INTO "django_geo_db_country" VALUES(202,'Switzerland','CH',2,202);
INSERT INTO "django_geo_db_country" VALUES(203,'Syrian Arab Republic','SY',1,203);
INSERT INTO "django_geo_db_country" VALUES(204,'Taiwan, Province of China','TW',1,204);
INSERT INTO "django_geo_db_country" VALUES(205,'Tajikistan','TJ',1,205);
INSERT INTO "django_geo_db_country" VALUES(206,'Tanzania, United Republic of','TZ',3,206);
INSERT INTO "django_geo_db_country" VALUES(207,'Thailand','TH',1,207);
INSERT INTO "django_geo_db_country" VALUES(208,'Timor-Leste','TL',1,208);
INSERT INTO "django_geo_db_country" VALUES(209,'Togo','TG',3,209);
INSERT INTO "django_geo_db_country" VALUES(210,'Tokelau','TK',4,210);
INSERT INTO "django_geo_db_country" VALUES(211,'Tonga','TO',4,211);
INSERT INTO "django_geo_db_country" VALUES(212,'Trinidad and Tobago','TT',5,212);
INSERT INTO "django_geo_db_country" VALUES(213,'Tunisia','TN',3,213);
INSERT INTO "django_geo_db_country" VALUES(214,'Turkey','TR',1,214);
INSERT INTO "django_geo_db_country" VALUES(215,'Turkmenistan','TM',1,215);
INSERT INTO "django_geo_db_country" VALUES(216,'Turks and Caicos Islands','TC',5,216);
INSERT INTO "django_geo_db_country" VALUES(217,'Tuvalu','TV',4,217);
INSERT INTO "django_geo_db_country" VALUES(218,'Uganda','UG',3,218);
INSERT INTO "django_geo_db_country" VALUES(219,'Ukraine','UA',2,219);
INSERT INTO "django_geo_db_country" VALUES(220,'United Arab Emirates','AE',1,220);
INSERT INTO "django_geo_db_country" VALUES(221,'United Kingdom of Great Britain and Northern Ireland','GB',2,221);
INSERT INTO "django_geo_db_country" VALUES(222,'United States of America','US',5,222);
INSERT INTO "django_geo_db_country" VALUES(223,'Uruguay','UY',6,223);
INSERT INTO "django_geo_db_country" VALUES(224,'Uzbekistan','UZ',1,224);
INSERT INTO "django_geo_db_country" VALUES(225,'Vanuatu','VU',4,225);
INSERT INTO "django_geo_db_country" VALUES(226,'Venezuela (Bolivarian Republic of)','VE',6,226);
INSERT INTO "django_geo_db_country" VALUES(227,'Viet Nam','VN',1,227);
INSERT INTO "django_geo_db_country" VALUES(228,'Virgin Islands (British)','VG',5,228);
INSERT INTO "django_geo_db_country" VALUES(229,'Virgin Islands (U.S.)','VI',5,229);
INSERT INTO "django_geo_db_country" VALUES(230,'Wallis and Futuna','WF',4,230);
INSERT INTO "django_geo_db_country" VALUES(231,'Western Sahara','EH',3,231);
INSERT INTO "django_geo_db_country" VALUES(232,'Yemen','YE',1,232);
INSERT INTO "django_geo_db_country" VALUES(233,'Zambia','ZM',3,233);
INSERT INTO "django_geo_db_country" VALUES(234,'Zimbabwe','ZW',3,234);
CREATE INDEX "django_geo_db_country_071e6d87" ON "django_geo_db_country" ("continent_id");
CREATE INDEX "django_geo_db_country_c2ff64a1" ON "django_geo_db_country" ("geocoordinate_id");
COMMIT;
