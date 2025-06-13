# config.py
# File konfigurasi untuk program Reminder Jadwal Sholat

"""
File ini berisi semua konfigurasi, data statis, dan pengaturan
yang digunakan dalam program reminder sholat.
"""

# Array nama-nama sholat dengan urutan tetap
SHOLAT_NAMES = [
    "Subuh", 
    "Dzuhur", 
    "Ashar", 
    "Maghrib", 
    "Isya"
]

# Array waktu sholat default dalam format [jam, menit] (24 jam)
# Bisa disesuaikan dengan lokasi dan preferensi masing-masing
DEFAULT_PRAYER_TIMES = [
    [4, 34],   # Subuh
    [11, 50],  # Dzuhur  
    [15, 12],  # Ashar
    [17, 43],  # Maghrib
    [18, 57]    # Isya
]

# Konfigurasi sistem reminder
REMINDER_CONFIG = {
    # Interval pengecekan dalam detik (30 detik default)
    'check_interval': 30,
    
    # Toleransi waktu reminder dalam detik (60 detik = 1 menit)
    'reminder_tolerance': 60,
    
    # Format tampilan waktu
    'time_format': "%H:%M",
    'date_format': "%d/%m/%Y",
    
    # Pengaturan suara reminder
    'sound_enabled': True,
    'sound_repeat': 2,
    'sound_delay': 0.5
}

# Konfigurasi tampilan interface
DISPLAY_CONFIG = {
    'separator_length': 50,
    'menu_separator': "=" * 40,
    'schedule_separator': "=" * 35,
    'queue_separator': "=" * 30,
    
    # Emoji dan simbol untuk tampilan
    'mosque_emoji': "🕌",
    'clock_emoji': "⏰",
    'calendar_emoji': "📅",
    'bell_emoji': "🔔",
    'check_emoji': "✅",
    'cross_emoji': "❌",
    'warning_emoji': "⚠️",
    'gear_emoji': "🔧",
    'list_emoji': "📋",
    'rocket_emoji': "🚀",
    'stop_emoji': "🛑",
    'wave_emoji': "👋"
}

# Pesan-pesan sistem
MESSAGES = {
    'welcome': f"{DISPLAY_CONFIG['mosque_emoji']} SELAMAT DATANG DI REMINDER JADWAL SHOLAT {DISPLAY_CONFIG['mosque_emoji']}",
    'initialization': f"{DISPLAY_CONFIG['mosque_emoji']} Menginisialisasi jadwal sholat hari ini...",
    'init_success': f"{DISPLAY_CONFIG['check_emoji']} Jadwal sholat hari ini berhasil diinisialisasi",
    'building_queue': f"{DISPLAY_CONFIG['gear_emoji']} Membangun queue reminder...",
    'queue_built': f"{DISPLAY_CONFIG['check_emoji']} Queue reminder berisi",
    'monitoring_start': f"{DISPLAY_CONFIG['rocket_emoji']} Monitoring reminder sholat dimulai...",
    'system_active': f"{DISPLAY_CONFIG['check_emoji']} Sistem reminder aktif!",
    'system_stopped': f"{DISPLAY_CONFIG['stop_emoji']} Sistem reminder dihentikan",
    'prayer_time_arrived': f"{DISPLAY_CONFIG['mosque_emoji']} WAKTU SHOLAT TELAH TIBA! {DISPLAY_CONFIG['mosque_emoji']}",
    'prayer_reminder': f"{DISPLAY_CONFIG['bell_emoji']} Jangan lupa untuk segera melaksanakan sholat {DISPLAY_CONFIG['bell_emoji']}",
    'goodbye': f"{DISPLAY_CONFIG['wave_emoji']} Terima kasih telah menggunakan Reminder Sholat!",
    'invalid_choice': f"{DISPLAY_CONFIG['cross_emoji']} Pilihan tidak valid!",
    'invalid_input': f"{DISPLAY_CONFIG['cross_emoji']} Input tidak valid!",
    'already_running': f"{DISPLAY_CONFIG['warning_emoji']} Reminder sudah berjalan!",
    'no_reminders': f"{DISPLAY_CONFIG['list_emoji']} Tidak ada sholat yang perlu diingatkan hari ini",
    'all_prayers_done': f"{DISPLAY_CONFIG['check_emoji']} Semua reminder hari ini telah selesai!"
}

# Menu utama
MAIN_MENU = [
    "Tampilkan Jadwal Sholat",
    "Update Waktu Sholat", 
    "Mulai Reminder",
    "Status Reminder",
    "Keluar"
]

# Validasi konfigurasi
def validate_config():
    """
    Memvalidasi konfigurasi untuk memastikan konsistensi data.
    """
    # Pastikan jumlah nama sholat sama dengan jumlah waktu default
    if len(SHOLAT_NAMES) != len(DEFAULT_PRAYER_TIMES):
        raise ValueError("Jumlah nama sholat tidak sama dengan jumlah waktu default")
    
    # Validasi format waktu
    for i, time_pair in enumerate(DEFAULT_PRAYER_TIMES):
        if len(time_pair) != 2:
            raise ValueError(f"Format waktu tidak valid untuk {SHOLAT_NAMES[i]}")
        
        hour, minute = time_pair
        if not (0 <= hour <= 23):
            raise ValueError(f"Jam tidak valid untuk {SHOLAT_NAMES[i]}: {hour}")
        
        if not (0 <= minute <= 59):
            raise ValueError(f"Menit tidak valid untuk {SHOLAT_NAMES[i]}: {minute}")
    
    # Validasi konfigurasi reminder
    if REMINDER_CONFIG['check_interval'] <= 0:
        raise ValueError("Interval pengecekan harus lebih dari 0")
    
    if REMINDER_CONFIG['reminder_tolerance'] < 0:
        raise ValueError("Toleransi reminder tidak boleh negatif")

# Jalankan validasi saat import
validate_config()
