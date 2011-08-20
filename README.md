# ppbot - a python IRC bot #
# created by billy <billyvg/gmail/com> #

# Information #
This project started as a school assignment which I will continue to
work on for fun... I'm choosing to make pgsql as a requirement because
I want to learn it and move away from mysql. Portability may be 
something that I will worry about later.

# Install #
pip install -r requirements.txt

# PostgreSQL #
CREATE USER psql; 
insert into access (access) values ('master');
insert into access (access) values ('owner');
insert into access (access) values ('op');
insert into access (access) values ('user');
insert into access (access) values ('guest');
insert into access (access) values ('all');

