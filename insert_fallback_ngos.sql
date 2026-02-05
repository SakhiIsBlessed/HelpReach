-- Insert 50 fallback NGOs into the database
-- These are pre-loaded NGOs from the static JSON in Directory_ngo.html
-- Run this script to populate the database if it's empty

INSERT INTO ngos (name, description, address, category, contact_person, contact_email, phone, verified, password_hash, registration_number) VALUES

-- 1. Mumbai Roti Bank
('Mumbai Roti Bank', 'Surplus Food Collection, Direct Distribution, Monetary Donations', '1701, One World Centre, Tower 2B, Floor 17, 841, Senapati Bapat Marg, Elphinstone Road, Mumbai 400013, India', 'Food Distribution', 'Mumbai Roti Bank', 'teamrotibank@gmail.com', '+91 86555 80001', 1, '', ''),

-- 2. Apna Shelter India Foundation
('Apna Shelter India Foundation', 'Food Help, Child Education, Women Support, Health Care, Environment Care, Social Help', '303, 3rd Floor, Krishna Plaza, Near Thane Railway Station, Thane West 400602', 'Multi-Service', 'Apna Shelter India Foundation', '', '+91 70211 56564', 1, '', ''),

-- 3. Goodwill India Upkaram
('Goodwill India Upkaram', 'Clothes Donation, Toys Donation, Computer Donation, Goodwill Thali', 'More Petrol Pump, Shivane, Pune, Maharashtra', 'Donations', 'Goodwill India Upkaram', 'goodwillpune01@gmail.com', '020 25290909', 1, '', ''),

-- 4. Pephands Foundation
('Pephands Foundation', 'Food Donation, Nutrition Kits, Grocery Kits, Student Education', 'Pune', 'Education & Food', 'Pephands Foundation', 'info@pephands.org', '+91 7305009919', 1, '', ''),

-- 5. Sahyadri Jankalyan Sanstha
('Sahyadri Jankalyan Sanstha', 'Clothes, Used Items, Essentials Redistribution', 'Katraj, Pune', 'Essential Supplies', 'Sahyadri Jankalyan Sanstha', '', '9823679878', 1, '', ''),

-- 6. Akanksha Organization
('Akanksha Organization', 'Community Service / Public Utility', 'Bhalekar Chawl, Erandwane, Pune 411004', 'Community Service', 'Akanksha Organization', '', '020 660513801', 1, '', ''),

-- 7. S N Shirke Charitable Foundation
('S N Shirke Charitable Foundation', 'Donations (Clothes, Food, Essentials)', 'Office No. 11, Navrang Plaza, Air Port Road, Vishrantwadi, Pune 411015', 'Donations', 'S N Shirke Charitable Foundation', '', '+91 9421230510', 1, '', ''),

-- 8. Global Vision NGO
('Global Vision NGO', 'Community Service, Potential Donations', 'Office No. 513/515, 5th Floor, Sterling Center, Opp. Hotel Arora Tower, MG Road, Camp, Pune 411001', 'Community Service', 'Global Vision NGO', '', '022 4127 0773', 1, '', ''),

-- 9. Children's Future India
('Children''s Future India', 'Child Welfare, Clothes, Essentials, Food', 'Prashant Nagar, Lokamanya Nagar, Navi Peth / Sadashiv Peth, Pune 411030', 'Child Welfare', 'Children''s Future India', '', '090280 03613', 1, '', ''),

-- 10. Chetana Mahila Vikas Kendra
('Chetana Mahila Vikas Kendra', 'Women''s & Community Welfare, Clothes & Essentials', '9 NPS Line, Behind Wonder Car Garage, Pulgate, Pune 411001', 'Women Welfare', 'Chetana Mahila Vikas Kendra', '', '020 2635 4946', 1, '', ''),

-- 11. Bharatiya Samaj Seva Kendra
('Bharatiya Samaj Seva Kendra', 'Social Service, Donations', 'Plot 373, 6th Lane, North Main Road, Koregaon Park, Pune 411001', 'Social Service', 'Bharatiya Samaj Seva Kendra', '', '020 2615 9314', 1, '', ''),

-- 12. Mukul Madhav Foundation
('Mukul Madhav Foundation', 'Education, Rural Development, Farmer & Animal Welfare, Food Donations', 'Harmony, 5, off Ganeshkhind Road, ICS Colony, Ashok Nagar, Pune 411007', 'Multi-Service', 'Mukul Madhav Foundation', '', '020 2552 8075', 1, '', ''),

-- 13. Save The Humanity Organisation
('Save The Humanity Organisation', 'Animal Welfare, Child Welfare, Disaster Relief, Education', 'C Block, Sector 6, Noida, Uttar Pradesh 201301', 'Multi-Service', 'Save The Humanity Organisation', '', '093159 46703', 1, '', ''),

-- 14. Marpu Foundation (NGO)
('Marpu Foundation', 'Environment, Veteran & Women Empowerment, Women Education', '10-82, Gaondevi Marg, NL - 1 Type, Sector 20, Nerul, Navi Mumbai, Maharashtra 400706', 'Women & Environment', 'Marpu Foundation', '', '079978 01001', 1, '', ''),

-- 15. Manpravah Foundation
('Manpravah Foundation', 'Orphanage Food Donation, Feeding the Hungry', '502 Tulsi Height, Sector 10E, Plot 8, Near Dmart, Roadpali, Kalamboli, Navi Mumbai 410218', 'Food Distribution', 'Manpravah Foundation', '', '+91 9987987557', 1, '', ''),

-- 16. Uday Foundation
('Uday Foundation', 'Clothes, Medicine, Environmental & Homeless Support, Human Rights, Skill Development', 'D-233 (LGF, Block D), Sarvodaya Enclave, New Delhi 110017', 'Multi-Service', 'Uday Foundation', 'info@udayfoundation.org', '011 2656 1333', 1, '', ''),

-- 17. SevaDeep
('SevaDeep', 'Old Toys, Clothes, Stationery, Furniture', '14th, SKY ONE, Relfor Foundation, Kalyani Nagar, Pune, Maharashtra 411006', 'Donations', 'SevaDeep', '', '095185 41719', 1, '', ''),

-- 18. Farmers Needs Help Foundation
('Farmers Needs Help Foundation', 'Clothes, Food, Miscellaneous Donations', 'Shivangan Society, Lokmanya Tilak Rd, Jaihind Colony, Tata Colony, Mulund East, Mumbai 400081', 'Donations', 'Farmers Needs Help Foundation', '', '096641 18631', 1, '', ''),

-- 19. Roadside Family Foundation
('Roadside Family Foundation', 'Animal Welfare, Child Welfare, Education, Donations', 'CEO 95 122, Unit 29, Box A4, Aarey Milk Colony, Goregaon, Mumbai 400065', 'Multi-Service', 'Roadside Family Foundation', '', '086574 57237', 1, '', ''),

-- 20. SYJ Organization
('SYJ Organization', 'Animal Welfare, Child Welfare, Donations, Education', 'Mega Center, C-511, Magarpatta, Hadapsar, Pune 411013', 'Multi-Service', 'SYJ Organization', '', '074700 59595', 1, '', ''),

-- 21. FilledTummy Pune
('FilledTummy Pune', 'Food Donation', 'Flat 2, Shangrila Apt, Shantisheela Society, Law College Rd, Pune 411038', 'Food Distribution', 'FilledTummy Pune', '', '095615 51292', 1, '', ''),

-- 22. Sanjivani NGO
('Sanjivani NGO', 'Food, Medical, Education Support', 'SR NO 59/1A, Sulai Complex, Flat No 17, near Desai Hospital, Mohammed Wadi, Pune 411060', 'Multi-Service', 'Sanjivani NGO', '', '089562 53672', 1, '', ''),

-- 23. Abhisree Foundation
('Abhisree Foundation', 'Disability & Women Empowerment', 'Road 13, Shanti Nagar, Uppal, Hyderabad, Telangana 500039', 'Disability Support', 'Abhisree Foundation', '', '080089 62108', 1, '', ''),

-- 24. Abhilasha Foundation NGO
('Abhilasha Foundation NGO', 'Child Welfare, Skill Development', 'Laxmi Chhaya Bungalow, Plot No. 27-27, RSC 11, Gorai 2, Borivali West, Mumbai 400091', 'Child Welfare', 'Abhilasha Foundation NGO', '', '097699 86440', 1, '', ''),

-- 25. Ratna Nidhi Charitable Trust
('Ratna Nidhi Charitable Trust', 'Books, Tablets, Toys, Clothes Distribution', '16-A, 12th Ln, Opp. Pavari School, Khetwadi, Girgaon, Mumbai 400004', 'Donations', 'Ratna Nidhi Charitable Trust', '', '085304 85324', 1, '', ''),

-- 26. SAAD Foundation
('SAAD Foundation', 'Education, Health, Community & Rural Development', 'Bungalow No. 62E, Kamgar Nagar Rd, Kurla, Mumbai 400024', 'Multi-Service', 'SAAD Foundation', '', '080820 54301', 1, '', ''),

-- 27. Responsible Charity
('Responsible Charity', 'Clothes & Food Donation', 'Shop No. 15, Sunshine Greens, Opp. Khadki Station, Off Aundh Rd, Pune 411020', 'Donations', 'Responsible Charity', '', '020 2580 6256', 1, '', ''),

-- 28. A Ray Of Hope Charitable Trust
('A Ray Of Hope Charitable Trust', 'Child Welfare, Animal Welfare, Education, Donations', 'B4, Sheikh Safa Complex, 2, Waghmare Rd, Shankar Kalat Nagar, Wakad, Pune, Pimpri-Chinchwad 411057', 'Multi-Service', 'A Ray Of Hope Charitable Trust', '', '097302 55167', 1, '', ''),

-- 29. VARA Foundations (R)
('VARA Foundations (R)', 'Child Welfare, Donation, Skill Development', 'No.7, 5th Main Rd, Jagruthi Colony, Puttenahalli, JP Nagar 7th Phase, Bengaluru 560078', 'Child Welfare', 'VARA Foundations', '', '099002 27171', 1, '', ''),

-- 30. Helping Hand Foundation
('Helping Hand Foundation', 'Children, Disability, Homeless, Social Services', 'Near Army Garden, Shivdatta Nagar, Pimpri Gaon, Pimpri Colony, Pimpri-Chinchwad 411017', 'Multi-Service', 'Helping Hand Foundation', '', '070380 16790', 1, '', ''),

-- 31. Aarogya Social Welfare International Foundation
('Aarogya Social Welfare International Foundation', 'Education', '24-3-271, Main Road, FCI Colony, Police Colony, Subedari, Hanamkonda, Telangana 506001', 'Education', 'Aarogya Social Welfare International Foundation', '', '', 1, '', ''),

-- 32. Eric Boys Welfare Association
('Eric Boys Welfare Association', 'Education, Skill Development', 'Block No - 5, R/2, 17, Block Number 7, Transit Camp, Rajiv Gandhi Nagar, Dharavi, Mumbai 400017', 'Education', 'Eric Boys Welfare Association', '', '', 1, '', ''),

-- 33. Snehwan - Official
('Snehwan - Official', 'Child & Girls Education, Food & Grocery Donation', 'Snehwan, Koyali Phata, Near Koyali Forest, Chakan, Khed, Maharashtra 410501', 'Education & Food', 'Snehwan', '', '082372 77615', 1, '', ''),

-- 34. KIDS Foundation
('KIDS Foundation', 'Children Charities, Education, Skill Development', 'Manas Mandir, Rashtrasant Tukdoji Maharaj Square, Old SBI Colony, Pratapnagar, Wardha 442001', 'Education', 'KIDS Foundation', '', '095955 40771', 1, '', ''),

-- 35. Child Safe Foundation
('Child Safe Foundation', 'Animal Welfare, Child Welfare, Donations, Education, Homeless', 'G/50, Arihant Shopping Centre, Achole Rd, near Anita Palace, Nalasopara East, Maharashtra 401209', 'Multi-Service', 'Child Safe Foundation', '', '084839 68879', 1, '', ''),

-- 36. Sparsh Shelter Home
('Sparsh Shelter Home', 'Education, Old Age Home, Health Care', 'Sparsh House, Shrushti Chowk, Lane No. 2, near Mamta Sweet, Prabhat Nagar, Pimple Gurav, Pune, Pimpri-Chinchwad 411061', 'Multi-Service', 'Sparsh Shelter Home', '', '076200 40230', 1, '', ''),

-- 37. Ghar - Sant Ishwar Foundation
('Ghar - Sant Ishwar Foundation', 'Child Care, Orphanage for Girls', 'Plot No. 30 179, Deccan College Rd, Opposite Dashmesh Gurudwara, Jai Jawan Nagar, Ranjeet Nagar, Yerawada, Pune 411006', 'Child Welfare', 'Ghar - Sant Ishwar Foundation', '', '093724 68457', 1, '', ''),

-- 38. RESQ Charitable Trust
('RESQ Charitable Trust', 'Dog Adoption, Medical Care, Aid, Treatment', 'Plot No. 3906, Paud, 115, Mulshi Rd, Hill Town, Chandani Chowk, Bavdhan, Pune 411023', 'Animal Welfare', 'RESQ Charitable Trust', '', '098909 99111', 1, '', ''),

-- 39. Majha Ghar Foundation
('Majha Ghar Foundation', 'Child Welfare, Homeless, Donation, Skill Development', 'Plot No.50, Behind Gurukrupa Hospital, Near Brahma PG, Laxmi Chowk, Marunji Road, Hinjawadi, Pune 411057', 'Multi-Service', 'Majha Ghar Foundation', '', '074985 50554', 1, '', ''),

-- 40. Riddhi Siddhi Charitable Trust
('Riddhi Siddhi Charitable Trust', 'Food Donation', 'Office No. 20, Swapnadeep Apartment, Poonam Sagar Complex, Mira Road East, Mumbai 401107', 'Food Distribution', 'Riddhi Siddhi Charitable Trust', '', '098207 37415', 1, '', ''),

-- 41. Happy Faces Vadodara
('Happy Faces Vadodara', 'Nonprofit, Social Services', '309, Vinayak Commercial Complex, Next to Saraswati Complex, Vaishnavdevi Society, Manjalpur, Vadodara, Gujarat 390011', 'Social Service', 'Happy Faces Vadodara', '', '098795 40744', 1, '', ''),

-- 42. Ek Parivartan Foundation
('Ek Parivartan Foundation', 'Community Support, Education, Food & Clothing Distribution', 'Street No. 13, Veer Savarkar Block, Block E, Laxmi Nagar, Delhi, 110092', 'Multi-Service', 'Ek Parivartan Foundation', 'info@epfngo.org', '099537 56764', 1, '', ''),

-- 43. NAR FOUNDATION
('NAR FOUNDATION', 'Education, Food Distribution, Clothes Distribution, Job References, Old Age Home Visits', 'Sunder Nagar, Ekta Nagar Rd New Link Road Mahavir Nagar, near Kandivali, Mumbai, Maharashtra 400067', 'Multi-Service', 'NAR FOUNDATION', '', '080821 40693', 1, '', ''),

-- 44. HWCT India Foundation - Human Welfare Charitable Trust
('HWCT India Foundation - Human Welfare Charitable Trust', 'POSHAN Project - Nutrition & Health for rural children, Food & Nutrition Programs', 'Khandelwal Layout, Evershine Nagar, Malad West, Mumbai, Maharashtra 400064', 'Health & Nutrition', 'HWCT India Foundation', '', '098207 37841', 1, '', ''),

-- 45. Save Tears Foundation
('Save Tears Foundation', 'Support for underprivileged children, Medical aid for critical ailments, Women empowerment, Elderly support, Orphan care', 'Building No A-1, Laram Center, 302 (West Side, Andheri West, above Sunil Jeweler''s, next to NADCO Shopping Centre), Railway Colony, Andheri East, Mumbai, Maharashtra 400058', 'Multi-Service', 'Save Tears Foundation', 'info@savetears.org', '078886 76667', 1, '', ''),

-- 46. Tejaswini Samajik Sanstha
('Tejaswini Samajik Sanstha', 'Food Donation, School Kit Donation, Healthcare Donation, Sponsorships, Clothing & Blankets, Medical & Educational Supplies, Hygiene Products', 'near Wagheshwar Temple, beside Jama Masjid, Wageshwar Nagar, Wagholi, Pune, Maharashtra 412207', 'Multi-Service', 'Tejaswini Samajik Sanstha', '', '098900 01164', 1, '', ''),

-- 47. Sukachi Sawali Welfare Foundation
('Sukachi Sawali Welfare Foundation', 'Community Welfare, Food & Essentials Distribution', '1408, Bldg no 2, Morarji Mill Compound, Kandivali, Ashok Nagar, Kandivali East, Mumbai, Maharashtra 400101', 'Multi-Service', 'Sukachi Sawali Welfare Foundation', '', '097022 26444', 1, '', ''),

-- 48. Aarna Foundation NGO
('Aarna Foundation NGO', 'Vidyadaan, Nutritious Meal Distribution to hungry and homeless', 'Shop no -1, Gulmohar Society, Patilwadi Rd, near Sankalp School, Patil Wadi, Sawarkar Nagar, Savarkar Nagar, Thane West, Thane, Maharashtra 400606', 'Food Distribution', 'Aarna Foundation NGO', '', '095940 96655', 1, '', ''),

-- 49. Feeding India
('Feeding India', 'Large-scale meal programs; helped serve 23+ crore meals via 1100+ centres across 150+ cities', '2nd Floor, Plot No. 13, Local Shopping Center, Pocket 1, Sector B, Vasant Kunj, New Delhi, Delhi 110070', 'Food Distribution', 'Feeding India', '', '098711 78810', 1, '', ''),

-- 50. Nirankar Vastigruh
('Nirankar Vastigruh', 'Accommodation, Education, Dance & Singing Lessons, Events, Health Care, Summer Camps', 'Near Gaikwad Society, Lane No - 1 A Railway Crossing, Sasane Nagar Bypass Rd, Sayyed Nagar, Hadapsar, Pune, Maharashtra 411028', 'Multi-Service', 'Nirankar Vastigruh', '', '095618 16451', 1, '', '');
