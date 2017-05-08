create view detail_kategori
as
select tb_kategori_kamar_detail.ktg_kmr_det_1, tb_kategori_kamar_detail.ktg_kmr_1, tb_fasilitas.fst_2, tb_fasilitas.fst_3
from tb_kategori_kamar_detail inner join tb_fasilitas on tb_kategori_kamar_detail.fst_1 = tb_fasilitas.fst_1
