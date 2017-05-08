
create table tb_user(
usr_1 int auto_increment primary key,
usr_2 varchar(30),
usr_3 varchar(128),
usr_4 varchar(30),
usr_5 text,
usr_6 varchar(15),
usr_7 datetime default now()
);

create table tb_fasilitas(
fst_1 int auto_increment primary key,
fst_2 varchar(50),
fst_3 varchar(100)
);

create table tb_kategori_kamar(
ktg_kmr_1 int auto_increment primary key, 
ktg_kmr_2 varchar(50),
ktg_kmr_3 int,
ktg_kmr_4 varchar(100)
);

create table tb_kategori_kamar_detail(
ktg_kmr_det_1 int auto_increment primary key,
ktg_kmr_1 int,
fst_1 int,
foreign key (ktg_kmr_1) references tb_kategori_kamar(ktg_kmr_1),
foreign key (fst_1) references tb_fasilitas(fst_1)
);

create table tb_kamar(
kmr_1 int auto_increment primary key,
kmr_2 varchar(10),
ktg_kmr_1 int,
foreign key (ktg_kmr_1) references tb_kategori_kamar(ktg_kmr_1)
);

create table tb_booking(
bkg_1 int auto_increment primary key,
bkg_2 datetime,
usr_1 int,
bkg_3 int,
bkg_4 varchar(128),
bkg_5 boolean,
foreign key (usr_1) references tb_user(usr_1)
);

create table tb_booking_detail(
bkg_det_1 int auto_increment primary key,
bkg_1 int,
kmr_1 int,
bkg_det_2 datetime,
bkg_det_3 datetime,
bkg_det_4 int,
foreign key (bkg_1) references tb_booking(bkg_1),
foreign key (kmr_1) references tb_kamar(kmr_1) 
);

create table tb_pembayaran(
byr_1 int auto_increment primary key,
bkg_1 int,
byr_2 datetime,
foreign key (bkg_1) references tb_booking(bkg_1)
);

create view detail_kategori
as
select tb_kategori_kamar_detail.ktg_kmr_det_1, tb_kategori_kamar_detail.ktg_kmr_1, tb_fasilitas.fst_2, tb_fasilitas.fst_3
from tb_kategori_kamar_detail inner join tb_fasilitas on tb_kategori_kamar_detail.fst_1 = tb_fasilitas.fst_1;


SELECT * FROM detail_kategori WHERE ktg_kmr_1 = 3;

drop database db_hotel;

use db_hotel;

select * from tb_kategori_kamar;
select * from tb_kategori_kamar_detail;
select * from tb_kamar;

