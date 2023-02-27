
drop table if exists users;
create table users (
  user_id integer primary key GENERATED ALWAYS AS IDENTITY,
  username VARCHAR not null,
  email VARCHAR not null,
  pw_hash VARCHAR not null
);

drop table if exists followers;
create table followers (
  who_id integer,
  whom_id integer
);

drop table if exists messages;
create table messages (
  message_id integer primary key GENERATED ALWAYS AS IDENTITY,
  author_id integer not null,
  text VARCHAR not null,
  pub_date integer,
  flagged integer
);
