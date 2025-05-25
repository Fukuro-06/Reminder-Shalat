# 🕌 Reminder Jadwal Sholat Otomatis

Program reminder jadwal sholat berbasis Python yang menggunakan konsep **Array** dan **Queue** untuk mengelola dan mengingatkan waktu sholat secara otomatis.

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Struktur Proyek](#-struktur-proyek)
- [Konsep Array dan Queue](#-konsep-array-dan-queue)
- [Instalasi](#-instalasi)
- [Cara Penggunaan](#-cara-penggunaan)
- [Struktur File](#-struktur-file)
- [Konfigurasi](#-konfigurasi)
- [Troubleshooting](#-troubleshooting)

## 🌟 Fitur Utama

- **Reminder Otomatis**: Memberikan notifikasi suara dan visual ketika waktu sholat tiba
- **Queue Management**: Menggunakan queue untuk mengelola urutan reminder berdasarkan waktu
- **Array-based Schedule**: Menyimpan jadwal sholat dalam array untuk akses yang efisien
- **Real-time Monitoring**: Monitoring waktu secara real-time menggunakan threading
- **Customizable Times**: Dapat mengubah waktu sholat sesuai kebutuhan
- **Export/Import**: Menyimpan dan memuat jadwal sholat dari file JSON
- **User-friendly Interface**: Interface menu yang mudah digunakan
- **Cross-platform Sound**: Dukungan notifikasi suara untuk berbagai sistem operasi

## 📁 Struktur Proyek

```
sholat-reminder/
├── main.py              # File utama program (entry point)
├── sholat_reminder.py   # Class utama SholatReminder
├── config.py            # Konfigurasi dan data statis
├── utils.py             # Fungsi-fungsi utility
└── README.md            # Dokumentasi proyek
```

## 🔄 Konsep Array dan Queue

### Array Implementation
Program menggunakan **Array** (Python List) untuk:
- **Menyimpan nama sholat**: `["Subuh", "Dzuhur", "Ashar", "Maghrib", "Isya"]`
- **Menyimpan waktu default**: `[[4,30], [12,15], [15,30], [18,45], [20,0]]`
- **Menyimpan jadwal harian**: Array tuple `(nama_sholat, datetime_object)`

**Keuntungan Array:**
- Akses langsung berdasarkan indeks O(1)
- Update waktu sholat tertentu dengan mudah
- Iterasi yang efisien untuk membangun queue

### Queue Implementation
Program menggunakan **Queue** (collections.deque) untuk:
- **Mengelola antrian reminder** berdasarkan urutan waktu
- **FIFO processing** - sholat yang waktunya lebih dekat diproses dulu
- **Efficient enqueue/dequeue** operations

**Alur Kerja Queue:**
1. **Build Queue**: Ambil dari array jadwal → filter yang belum lewat → sort berdasarkan waktu → enqueue
2. **Monitor Queue**: Cek head queue → jika waktu tiba → dequeue → proses reminder
3. **Update Queue**: Rebuild otomatis saat ada perubahan jadwal

## 🚀 Instalasi

### Persyaratan Sistem
- Python 3.6 atau lebih baru
- Windows/Linux/macOS

### Langkah Instalasi

1. **Download semua file**:
   ```bash
   # Simpan keempat file Python dalam satu folder
   main.py
   sholat_reminder.py  
   config.py
   utils.py
   ```

2. **Buka terminal/command prompt** di folder tersebut

3. **Jalankan program**:
   ```bash
   python main.py
   ```

### Dependencies
Program ini hanya menggunakan library bawaan Python:
- `datetime` - untuk manajemen waktu
- `threading` - untuk monitoring background
- `collections.deque` - untuk implementasi queue
- `json` - untuk export/import data
- `winsound` (Windows) - untuk notifikasi suara

## 📖 Cara Penggunaan

### 1. Menjalankan Program
```bash
python main.py
```

### 2. Menu Utama
Program akan menampilkan 5 menu utama:

**1. Tampilkan Jadwal Sholat**
- Melihat jadwal sholat hari ini
- Status sholat yang sudah lewat/tersisa
- Info sholat berikutnya

**2. Update Waktu Sholat**
- Pilih sholat yang ingin diubah (0-4)
- Masukkan jam dan menit baru
- Konfirmasi perubahan

**3. Mulai Reminder**
- Memulai sistem monitoring otomatis
- Build queue dari jadwal saat ini
- Mulai thread background monitoring

**4. Status Reminder**
- Cek apakah reminder aktif/tidak
- Lihat statistik sholat hari ini
- Tampilan queue reminder
- Opsi stop/restart reminder

**5. Keluar**
- Keluar dari program
- Otomatis stop reminder jika aktif

### 3. Menu Lanjutan (Hidden)
Ketik `advanced` di menu utama untuk mengakses:
- Reset jadwal ke default
- Export jadwal ke JSON
- Import jadwal dari JSON
- Clear screen

### 4. Alur Penggunaan Typical

1. **Jalankan program** → lihat jadwal default
2. **Update waktu** jika perlu sesuai lokasi
3. **Mulai reminder** → sistem aktif di background
4. **Program memberikan notifikasi** saat waktu sholat tiba
5. **Cek status** kapan saja untuk melihat reminder yang tersisa

## 🏗️ Struktur File

### `main.py`
- **Entry point** program
- **Interface pengguna** dan menu system
- **Koordinasi** dengan class SholatReminder
- **Error handling** dan exception management

### `sholat_reminder.py`
- **Class SholatReminder** - logika bisnis utama
- **Array management** untuk jadwal sholat
- **Queue operations** untuk reminder system
- **Threading** untuk monitoring real-time
- **Notification system** suara dan visual

### `config.py`
- **Konfigurasi statis** (nama sholat, waktu default)
- **Settings** sistem (interval check, toleransi, format)
- **UI constants** (emoji, separator, pesan)
- **Validasi konfigurasi** otomatis

### `utils.py`
- **Utility functions** untuk operasi umum
- **Time formatting** dan calculations  
- **Input validation** dan safe input
- **Sound notification** cross-platform
- **Display helpers** untuk UI

## ⚙️ Konfigurasi

### Mengubah Waktu Default
Edit `config.py` bagian `DEFAULT_PRAYER_TIMES`:
```python
DEFAULT_PRAYER_TIMES = [
    [4, 30],   # Subuh
    [12, 15],  # Dzuhur  
    [15, 30],  # Ashar
    [18, 45],  # Maghrib
    [20, 0]    # Isya
]
```

### Mengubah Interval Monitoring
Edit `config.py` bagian `REMINDER_CONFIG`:
```python
REMINDER_CONFIG = {
    'check_interval': 30,      # Check setiap 30 detik
    'reminder_tolerance': 60,  # Toleransi 1 menit
    'sound_enabled': True,     # Enable/disable suara
    # ...
}
```

### Kustomisasi Display
Edit `config.py` bagian `DISPLAY_CONFIG` untuk mengubah emoji, separator, dll.

## 🐛 Troubleshooting

### Problem: Import Error
**Gejala**: `ImportError: No module named 'config'`
**Solusi**: 
- Pastikan semua 4 file berada dalam folder yang sama
- Pastikan nama file sesuai: `config.py`, `utils.py`, `sholat_reminder.py`

### Problem: Suara tidak keluar
**Gejala**: Reminder muncul tapi tidak ada suara
**Solusi**:
- **Windows**: Pastikan `winsound` tersedia
- **Linux/Mac**: Program akan fallback ke system bell
- **Disable**: Set `sound_enabled: False` di `config.py`

### Problem: Queue kosong
**Gejala**: "Tidak ada sholat yang perlu diingatkan"
**Solusi**:
- Cek apakah semua waktu sholat sudah terlewat
- Update waktu sholat ke waktu yang akan datang
- Reset jadwal ke default

### Problem: Thread tidak berhenti
**Gejala**: Program tidak keluar dengan benar
**Solusi**:
- Gunakan Ctrl+C untuk force quit
- Pastikan selalu stop reminder sebelum keluar
- Restart terminal jika perlu

### Problem: Waktu tidak akurat
**Gejala**: Reminder terlambat atau terlalu cepat
**Solusi**:
- Adjust `reminder_tolerance` di config
- Cek sistem clock komputer
- Reduce `check_interval` untuk response lebih cepat

## 🔧 Pengembangan Lebih Lanjut

### Fitur yang Bisa Ditambahkan:
- **GPS Integration**: Auto-detect lokasi untuk waktu sholat akurat
- **Multiple Timezone**: Support untuk berbagai zona waktu
- **Audio Adzan**: Putar file audio adzan sebagai reminder
- **Web Interface**: GUI berbasis web dengan Flask/Django  
- **Mobile App**: Konversi ke aplikasi mobile
- **Database Storage**: Simpan jadwal dan history dalam database
- **Network Sync**: Sinkronisasi jadwal dengan server online