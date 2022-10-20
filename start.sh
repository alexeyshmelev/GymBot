mysql -u root --password='###your_password###' -e "CREATE USER '###username###'@'%' IDENTIFIED WITH caching_sha2_password BY '###user_password###'"
mysql -u root --password='###your_password###' -e "CREATE DATABASE sport_club"
mysql -u root --password='###your_password###' -e "GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, CREATE TEMPORARY TABLES, CREATE VIEW, EVENT, TRIGGER, SHOW VIEW, REFERENCES ON sport_club.* TO ##username###@'%'"
mysql -u root --password='###your_password###' sport_club < /home/SportClub.sql
