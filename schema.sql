drop table otp_requests;
drop table users;
drop table complains;

create table otp_requests (
  token varchar(256) not null,
  otp int not null
);

create table users (
  id integer primary key autoincrement,
  email varchar(256),
  name varchar(256) not null,
  password_hash varchar(256) not null,
  is_student int(1) not null
);

create table complains (
  id integer primary key autoincrement,
  fid integer not null,
  sid integer not null,
  title varchar(256) not null,
  body varchar(256) not null,
  status varchar(15) not null default 'Unread',
  foreign key (fid) references users(id),
  foreign key (sid) references users(id)
);
