# Smart Parking System Using Raspberry Pi and Flask

Sistem parkir pintar berbasis Raspberry Pi yang memanfaatkan sensor jarak inframerah untuk mendeteksi keberadaan kendaraan, menghitung biaya parkir secara otomatis, serta menampilkan informasi parkir secara real-time melalui dashboard web.

---

## Deskripsi Proyek

Smart Parking System merupakan sistem parkir pintar yang dirancang untuk memonitor ketersediaan slot parkir secara otomatis menggunakan sensor jarak inframerah.

Sistem mendeteksi kendaraan yang masuk dan keluar dari area parkir, mencatat waktu masuk dan keluar kendaraan, menghitung biaya parkir secara otomatis, serta menyimpan seluruh data ke database PostgreSQL.

Informasi parkir kemudian ditampilkan secara real-time melalui dashboard web berbasis Flask sehingga memudahkan proses monitoring dan pengelolaan parkir.

---

## Fitur Utama

* Deteksi kendaraan secara otomatis menggunakan sensor inframerah
* Monitoring slot parkir secara real-time
* Pencatatan waktu masuk kendaraan
* Pencatatan waktu keluar kendaraan
* Perhitungan biaya parkir otomatis
* Penyimpanan data ke PostgreSQL
* Dashboard monitoring berbasis web
* Riwayat transaksi parkir
* Statistik penggunaan slot parkir
* Total pendapatan parkir

---

## Teknologi yang Digunakan

### Hardware

* Raspberry Pi
* SHARP GP2Y0A41SK0F Infrared Distance Sensor
* PCF8591 ADC Converter
* Breadboard
* Jumper Wire
* Miniatur Area Parkir

### Software

* Python
* Flask
* PostgreSQL
* Psycopg2
* SMBus2
* HTML
* CSS
* JavaScript

---

## Arsitektur Sistem

```text
Sensor Infrared
        │
        ▼
PCF8591 ADC Converter
        │
        ▼
 Raspberry Pi
        │
        ▼
 Sensor Monitor (Python)
        │
        ▼
 PostgreSQL Database
        │
        ▼
 Flask Dashboard
        │
        ▼
     User
```

---

## Cara Kerja Sistem

### 1. Deteksi Kendaraan

Sensor SHARP membaca jarak objek pada setiap slot parkir.

Apabila nilai sensor melebihi ambang batas (threshold), sistem menganggap terdapat kendaraan pada slot tersebut.

### 2. Pencatatan Kendaraan Masuk

Ketika kendaraan terdeteksi memasuki slot parkir:

* Sistem membuat ID kendaraan otomatis
* Waktu masuk dicatat
* Data disimpan ke database

### 3. Monitoring Kendaraan

Selama kendaraan masih berada di slot parkir:

* Status slot menjadi **Occupied**
* Dashboard diperbarui secara real-time

### 4. Pencatatan Kendaraan Keluar

Ketika kendaraan meninggalkan slot:

* Waktu keluar dicatat
* Durasi parkir dihitung
* Biaya parkir dihitung otomatis
* Status slot berubah menjadi **Vacant**

### 5. Dashboard Monitoring

Dashboard menampilkan:

* Status setiap slot
* Slot terisi
* Slot kosong
* Total pendapatan parkir
* Riwayat parkir terbaru

---

## Struktur Project

```text
Smart-Parking-System/
│
├── app.py
├── sensor_monitor.py
├── templates/
│   └── dashboard.html
│
├── static/
│   ├── css/
│   └── js/
│
├── database/
│   └── schema.sql
│
└── README.md
```

---

## Database

Tabel utama yang digunakan:

### parking_sessions

| Field       | Keterangan        |
| ----------- | ----------------- |
| car_id      | ID kendaraan      |
| slot_number | Nomor slot parkir |
| entry_time  | Waktu masuk       |
| exit_time   | Waktu keluar      |
| fee         | Biaya parkir      |

---

## Konfigurasi Sistem

Parameter yang dapat diubah:

```python
THRESHOLD = 130
ENTRY_TIME = 2.5
EXIT_TIME = 3.0
RATE_PER_MINUTE = 1000
MAX_FEE = 50000
```

Keterangan:

* THRESHOLD → Nilai sensor untuk mendeteksi kendaraan
* ENTRY_TIME → Waktu konfirmasi kendaraan masuk
* EXIT_TIME → Waktu konfirmasi kendaraan keluar
* RATE_PER_MINUTE → Tarif parkir per menit
* MAX_FEE → Batas maksimum biaya parkir

---

## Instalasi

### Clone Repository

```bash
git clone https://github.com/MBAHSINGO22/Embedded-System.git
```

### Install Dependency

```bash
pip install flask
pip install psycopg2-binary
pip install smbus2
```

### Jalankan PostgreSQL

Pastikan database PostgreSQL telah dibuat:

```sql
CREATE DATABASE smart_parking;
```

### Jalankan Sensor Monitor

```bash
python sensor_monitor.py
```

### Jalankan Dashboard

```bash
python app.py
```

Dashboard dapat diakses melalui:

```text
http://localhost:5000
```

---

## Output Sistem

Sistem menghasilkan:

* Status slot parkir secara real-time
* Data kendaraan masuk
* Data kendaraan keluar
* Riwayat parkir
* Perhitungan biaya parkir
* Statistik penggunaan parkir
* Total pendapatan parkir

---

## Pengembangan Selanjutnya

* Integrasi kamera dan OCR plat nomor
* Notifikasi slot kosong otomatis
* Mobile application monitoring
* Sistem reservasi parkir online
* Dashboard analitik berbasis grafik
* Integrasi IoT Cloud Platform
* Multi-area parking management

---

## Author

**Eugenius Kriswinar Adi Cahya**
