from flask import render_template, request, session, redirect, url_for, flash
from app import *
from config import koneksi, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

fasilitas_dir = os.path.join(UPLOAD_FOLDER, "fasilitas")
kategori_kmr_dir = os.path.join(UPLOAD_FOLDER, "kategori_kamar")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def read_session(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        session.permanent = True
        try:
            if session['user'] is False:
                flash('Username or Password is invalid')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        except KeyError:
            flash('Your Session is time out, login first')
            return redirect(url_for('login'))
    return wrap

def check_username_ganda(username):
    conn = koneksi
    cursor = conn.cursor()
    query = """SELECT * FROM tb_user WHERE usr_2 = '%s'""" % (username)
    cursor.execute(query)
    data = cursor.fetchall()
    return len(data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    status = 0
    data_user=[]
    if request.method == 'POST':
        email = request.form['email']
        no_hp = request.form['no_hp']
        alamat = request.form['alamat']
        username = request.form['username']
        password = request.form['password']

        if check_username_ganda(username) == 0:
            conn = koneksi
            cursor = conn.cursor()
            query = """INSERT INTO tb_user (usr_2, usr_3, usr_4, usr_5, usr_6) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (username, generate_password_hash(password), email, alamat, no_hp))
            conn.commit()
            flash ('Akun Anda Berhasil Dibuat!')
            return redirect(url_for('login'))
        else:
            status = 1
            data_user.extend([email, no_hp, alamat])
            flash ('Username tidak tersedia!')

    return render_template('signup.html', status=status, data_user=data_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = koneksi
        cursor = conn.cursor()
        query = """SELECT * FROM tb_user WHERE usr_2='%s' """ % (username)
        cursor.execute(query)
        data = cursor.fetchall()

        if len(data) is 0:
            flash ('Username Belum Terdaftar')
        else:
            for d in data:
                cek = check_password_hash(d[2], password)
                if cek:
                    session['user']=d[1]
                    return redirect(url_for('index'))
                else:
                    flash ('Password Salah!')
    session.pop('user', None)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET'])
@read_session
def index():
    return render_template('admin/home.html')

@app.route('/admin/fasilitas', methods=['GET', 'POST'])
def fasilitas():
    if request.method == 'POST':
        nm_fasilitas = request.form['nama_fasilitas']
        gambar = request.files['gambar']
        try:
            if len(gambar.filename) is 0:
                conn = koneksi
                cursor = conn.cursor()
                query = """INSERT INTO tb_fasilitas (fst_2) VALUES ('%s')""" % (nm_fasilitas)
                cursor.execute(query)
                conn.commit()
                flash ('Data Fasilitas Berhasil Ditambah')
                return redirect(url_for('fasilitas'))
            else:
                if allowed_file(gambar.filename):
                    img_name = gambar.filename
                    gambar.save(os.path.join(fasilitas_dir, img_name))

                    conn = koneksi
                    cursor = conn.cursor()
                    query = """INSERT INTO tb_fasilitas (fst_2, fst_3) VALUES (%s, %s)"""
                    cursor.execute(query, (nm_fasilitas, img_name))
                    conn.commit()
                    flash ('Data Fasilitas Berhasil Ditambah')
                    return redirect(url_for('fasilitas'))
                else:
                    flash ('Jenis File Gambar Tidak Diperbolehkan.')
                    return redirect(url_for('fasilitas'))
        except Exception as e:
            raise e

    conn = koneksi
    cursor = conn.cursor()
    query = """SELECT * FROM tb_fasilitas"""
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template('admin/fasilitas.html', fasilitas=data)

@app.route('/admin/edit-fasilitas', methods=['POST'])
def edit_fasilitas():
    id_fasilitas = request.form['id_fst']
    nm_fasilitas = request.form['nama_fasilitas']
    gambar = request.files['gambar']
    try:
        if len(gambar.filename) is 0:
            conn = koneksi
            cursor = conn.cursor()
            query = """UPDATE tb_fasilitas SET fst_2=%s WHERE fst_1=%s"""
            cursor.execute(query, (nm_fasilitas, id_fasilitas))
            conn.commit()
            flash ('Data Fasilitas Berhasil Diedit')
            return redirect(url_for('fasilitas'))
        else:
            if allowed_file(gambar.filename):
                img_name = gambar.filename
                gambar.save(os.path.join(fasilitas_dir, img_name))

                conn = koneksi
                cursor = conn.cursor()
                query = """UPDATE tb_fasilitas SET fst_2=%s, fst_3=%s WHERE fst_1=%s"""
                cursor.execute(query, (nm_fasilitas, img_name, id_fasilitas))
                conn.commit()
                flash ('Data Fasilitas Berhasil Diedit')
                return redirect(url_for('fasilitas'))
            else:
                flash ('Jenis File Gambar Tidak Diperbolehkan.')
                return redirect(url_for('fasilitas'))
    except Exception as e:
        raise e
    return redirect(url_for('fasilitas'))

@app.route('/admin/del-fasilitas', methods=['POST'])
def del_fasilitas():
    id_fasilitas = request.form['id_fst']

    conn = koneksi
    cursor = conn.cursor()
    query = """DELETE FROM tb_fasilitas WHERE fst_1 = '%s'""" % (id_fasilitas)
    cursor.execute(query)
    conn.commit()
    flash ('Data Berhasil Dihapus.')
    return redirect(url_for('fasilitas'))

@app.route('/admin/kategori', methods=['GET', 'POST'])
def kategori():
    if request.method == 'POST':
        nm_kategori = request.form['nama_kategori']
        harga = request.form['harga']
        gambar = request.files['gambar']
        try:
            if len(gambar.filename) is 0:
                conn = koneksi
                cursor = conn.cursor()
                query = """INSERT INTO tb_kategori_kamar (ktg_kmr_2, ktg_kmr_3) VALUES (%s, %s)"""
                cursor.execute(query, (nm_kategori, harga))
                conn.commit()
                flash ('Data Kategori Berhasil Ditambah')
                return redirect(url_for('kategori'))
            else:
                if allowed_file(gambar.filename):
                    img_name = gambar.filename
                    gambar.save(os.path.join(kategori_kmr_dir, img_name))

                    conn = koneksi
                    cursor = conn.cursor()
                    query = """INSERT INTO tb_kategori_kamar (ktg_kmr_2, ktg_kmr_3, ktg_kmr_4) VALUES (%s, %s, %s)"""
                    cursor.execute(query, (nm_kategori, harga, img_name))
                    conn.commit()
                    flash ('Data Kategori Berhasil Ditambah')
                    return redirect(url_for('kategori'))
                else:
                    flash ('Jenis File Gambar Tidak Diperbolehkan.')
                    return redirect(url_for('kategori'))
        except Exception as e:
            raise e

    conn = koneksi
    cursor = conn.cursor()
    query = """SELECT * FROM tb_kategori_kamar"""
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template('admin/kategori.html', kategori=data)

@app.route('/admin/edit-kategori', methods=['POST'])
def edit_kategori():
    id_kategori = request.form['id_ktg']
    nm_kategori = request.form['nama_kategori']
    harga = request.form['harga']
    gambar = request.files['gambar']
    try:
        if len(gambar.filename) is 0:
            conn = koneksi
            cursor = conn.cursor()
            query = """UPDATE tb_kategori_kamar SET ktg_kmr_2=%s, ktg_kmr_3=%s WHERE ktg_kmr_1=%s"""
            cursor.execute(query, (nm_kategori, harga, id_kategori))
            conn.commit()
            flash ('Data Kategori Berhasil Diedit')
            return redirect(url_for('kategori'))
        else:
            if allowed_file(gambar.filename):
                img_name = gambar.filename
                gambar.save(os.path.join(kategori_kmr_dir, img_name))

                conn = koneksi
                cursor = conn.cursor()
                query = """UPDATE tb_kategori_kamar SET ktg_kmr_2=%s, ktg_kmr_3=%s, ktg_kmr_4=%s WHERE ktg_kmr_1=%s"""
                cursor.execute(query, (nm_kategori, harga, img_name, id_kategori))
                conn.commit()
                flash ('Data Kategori Berhasil Diedit')
                return redirect(url_for('kategori'))
            else:
                flash ('Jenis File Gambar Tidak Diperbolehkan.')
                return redirect(url_for('kategori'))
    except Exception as e:
        print e
    return redirect(url_for('kategori'))

@app.route('/admin/del-kategori', methods=['POST'])
def del_kategori():
    id_kategori = request.form['id_ktg']

    conn = koneksi
    cursor = conn.cursor()
    query = """DELETE FROM tb_kategori_kamar WHERE ktg_kmr_1 = '%s'""" % (id_kategori)
    cursor.execute(query)
    conn.commit()
    flash ('Data Berhasil Dihapus.')
    return redirect(url_for('kategori'))

def info_kategori(id_ktg):
    temp=()
    conn = koneksi
    cursor = conn.cursor()
    query = """SELECT * FROM tb_kategori_kamar WHERE ktg_kmr_1 = '%s'""" % (id_ktg)
    cursor.execute(query)
    data = cursor.fetchall()
    for d in data:
        temp = temp + d
        break
    return temp

def list_fasilitas():
    conn = koneksi
    cursor = conn.cursor()
    query = """SELECT * FROM tb_fasilitas"""
    cursor.execute(query)
    data = cursor.fetchall()
    return data

@app.route('/admin/kategori-detail/<id_kategori>', methods=['GET', 'POST'])
def kategori_detail(id_kategori):
    if request.method == 'POST':
        id_fasilitas = request.form['id_fst']

        conn = koneksi
        cursor = conn.cursor()
        query = """INSERT INTO tb_kategori_kamar_detail (ktg_kmr_1, fst_1) VALUES (%s, %s)"""
        cursor.execute(query, (id_kategori, id_fasilitas))
        conn.commit()

        flash ('Data Berhassil Ditambah.')
        return redirect(url_for('kategori_detail', id_kategori=id_kategori))

    conn = koneksi
    cursor = conn.cursor()
    query = """SELECT * FROM detail_kategori WHERE ktg_kmr_1 = %s""" % (id_kategori)
    cursor.execute(query)
    data = cursor.fetchall()
    data2 =  info_kategori(id_kategori)
    data3 = list_fasilitas()

    return render_template('admin/kategori-detail.html', datail_kategori=data, info_ktg=data2, list_fasilitas=data3)
