# utils.py
# File utility berisi fungsi-fungsi pembantu untuk program Reminder Sholat

"""
File ini berisi fungsi-fungsi utility yang dapat digunakan
di berbagai bagian program untuk operasi umum seperti
formatting, validasi, dan notifikasi.
"""

import datetime
import time
import winsound  # Untuk Windows, bisa diganti dengan alternatif cross-platform
from config import REMINDER_CONFIG, DISPLAY_CONFIG, MESSAGES

def format_time(dt_object, format_string=None):
    """
    Memformat objek datetime menjadi string waktu.
    
    Args:
        dt_object (datetime): Objek datetime yang akan diformat
        format_string (str, optional): Format string. Default dari config
    
    Returns:
        str: Waktu dalam format string
    """
    if format_string is None:
        format_string = REMINDER_CONFIG['time_format']
    
    return dt_object.strftime(format_string)

def format_date(dt_object, format_string=None):
    """
    Memformat objek datetime menjadi string tanggal.
    
    Args:
        dt_object (datetime): Objek datetime yang akan diformat
        format_string (str, optional): Format string. Default dari config
    
    Returns:
        str: Tanggal dalam format string
    """
    if format_string is None:
        format_string = REMINDER_CONFIG['date_format']
    
    return dt_object.strftime(format_string)

def calculate_time_difference(target_time, current_time=None):
    """
    Menghitung selisih waktu antara target dan waktu sekarang.
    
    Args:
        target_time (datetime): Waktu target
        current_time (datetime, optional): Waktu sekarang. Default datetime.now()
    
    Returns:
        dict: Dictionary berisi informasi selisih waktu
    """
    if current_time is None:
        current_time = datetime.datetime.now()
    
    time_diff = target_time - current_time
    total_seconds = int(time_diff.total_seconds())
    
    if total_seconds < 0:
        return {
            'is_past': True,
            'total_seconds': abs(total_seconds),
            'hours': 0,
            'minutes': 0,
            'formatted': "Sudah terlewat"
        }
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    return {
        'is_past': False,
        'total_seconds': total_seconds,
        'hours': hours,
        'minutes': minutes,
        'formatted': f"{hours} jam {minutes} menit"
    }

def validate_time_input(hour, minute):
    """
    Memvalidasi input waktu jam dan menit.
    
    Args:
        hour (int): Jam (0-23)
        minute (int): Menit (0-59)
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        hour = int(hour)
        minute = int(minute)
        
        if not (0 <= hour <= 23):
            return False, f"Jam harus antara 0-23, diberikan: {hour}"
        
        if not (0 <= minute <= 59):
            return False, f"Menit harus antara 0-59, diberikan: {minute}"
        
        return True, "Valid"
    
    except (ValueError, TypeError):
        return False, "Input harus berupa angka"

def validate_sholat_index(index, max_index):
    """
    Memvalidasi indeks sholat.
    
    Args:
        index (int): Indeks yang akan divalidasi
        max_index (int): Indeks maksimum yang diperbolehkan
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        index = int(index)
        
        if not (0 <= index < max_index):
            return False, f"Indeks harus antara 0-{max_index-1}, diberikan: {index}"
        
        return True, "Valid"
    
    except (ValueError, TypeError):
        return False, "Indeks harus berupa angka"

def play_reminder_sound():
    """
    Memainkan suara reminder sesuai konfigurasi.
    Mendukung berbagai platform dengan fallback.
    """
    if not REMINDER_CONFIG['sound_enabled']:
        return
    
    try:
        # Untuk Windows - menggunakan winsound
        for _ in range(REMINDER_CONFIG['sound_repeat']):
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            if REMINDER_CONFIG['sound_repeat'] > 1:
                time.sleep(REMINDER_CONFIG['sound_delay'])
    
    except ImportError:
        # Fallback untuk sistem lain
        try:
            # Coba menggunakan system bell
            import os
            for _ in range(REMINDER_CONFIG['sound_repeat']):
                os.system('echo \a')  # ASCII bell character
                if REMINDER_CONFIG['sound_repeat'] > 1:
                    time.sleep(REMINDER_CONFIG['sound_delay'])
        except:
            # Fallback terakhir - print visual bell
            print(f"{DISPLAY_CONFIG['bell_emoji']} TING! TING!")

def print_separator(separator_type='default'):
    """
    Mencetak separator sesuai tipe.
    
    Args:
        separator_type (str): Tipe separator ('default', 'menu', 'schedule', 'queue')
    """
    separators = {
        'default': "=" * DISPLAY_CONFIG['separator_length'],
        'menu': DISPLAY_CONFIG['menu_separator'],
        'schedule': DISPLAY_CONFIG['schedule_separator'],
        'queue': DISPLAY_CONFIG['queue_separator']
    }
    
    print(separators.get(separator_type, separators['default']))

def print_header(title, separator_type='default'):
    """
    Mencetak header dengan judul dan separator.
    
    Args:
        title (str): Judul header
        separator_type (str): Tipe separator
    """
    print(f"\n{title}")
    print_separator(separator_type)

def get_current_time_info():
    """
    Mendapatkan informasi waktu saat ini.
    
    Returns:
        dict: Dictionary berisi informasi waktu sekarang
    """
    now = datetime.datetime.now()
    today = datetime.date.today()
    
    return {
        'datetime': now,
        'date': today,
        'formatted_time': format_time(now),
        'formatted_date': format_date(now),
        'timestamp': now.timestamp()
    }

def create_datetime_from_time(hour, minute, date_obj=None):
    """
    Membuat objek datetime dari jam dan menit.
    
    Args:
        hour (int): Jam
        minute (int): Menit
        date_obj (date, optional): Objek date. Default hari ini
    
    Returns:
        datetime: Objek datetime yang telah dibuat
    """
    if date_obj is None:
        date_obj = datetime.date.today()
    
    return datetime.datetime.combine(
        date_obj,
        datetime.time(hour, minute)
    )

def is_time_in_range(target_time, current_time=None, tolerance_seconds=None):
    """
    Mengecek apakah waktu target berada dalam rentang toleransi.
    
    Args:
        target_time (datetime): Waktu target
        current_time (datetime, optional): Waktu sekarang
        tolerance_seconds (int, optional): Toleransi dalam detik
    
    Returns:
        bool: True jika dalam rentang toleransi
    """
    if current_time is None:
        current_time = datetime.datetime.now()
    
    if tolerance_seconds is None:
        tolerance_seconds = REMINDER_CONFIG['reminder_tolerance']
    
    time_diff = (target_time - current_time).total_seconds()
    
    # Dalam rentang: dari -tolerance_seconds sampai 0 (sudah lewat tapi masih dalam toleransi)
    return -tolerance_seconds <= time_diff <= 0

def format_prayer_notification(sholat_name, sholat_time):
    """
    Memformat notifikasi sholat dengan template yang menarik.
    
    Args:
        sholat_name (str): Nama sholat
        sholat_time (datetime): Waktu sholat
    
    Returns:
        str: String notifikasi yang diformat
    """
    formatted_time = format_time(sholat_time)
    formatted_date = format_date(sholat_time)
    
    notification = f"""
{print_separator('default')}
{MESSAGES['prayer_time_arrived']}
{print_separator('default')}
   Sholat: {sholat_name}
   Waktu : {formatted_time}
   Tanggal: {formatted_date}
{print_separator('default')}
{MESSAGES['prayer_reminder']}
{print_separator('default')}
"""
    return notification

def safe_input(prompt, input_type=str, validator=None):
    """
    Input yang aman dengan validasi.
    
    Args:
        prompt (str): Pesan prompt
        input_type (type): Tipe data yang diharapkan
        validator (function, optional): Fungsi validator tambahan
    
    Returns:
        Any: Input yang telah divalidasi
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            # Konversi tipe data
            if input_type != str:
                user_input = input_type(user_input)
            
            # Validasi tambahan jika ada
            if validator:
                is_valid, message = validator(user_input)
                if not is_valid:
                    print(f"{DISPLAY_CONFIG['cross_emoji']} {message}")
                    continue
            
            return user_input
        
        except (ValueError, TypeError) as e:
            print(f"{DISPLAY_CONFIG['cross_emoji']} Input tidak valid: {e}")
        except KeyboardInterrupt:
            print(f"\n{DISPLAY_CONFIG['stop_emoji']} Input dibatalkan")
            return None

def clear_screen():
    """
    Membersihkan layar terminal (cross-platform).
    """
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def confirm_action(message="Apakah Anda yakin?"):
    """
    Meminta konfirmasi dari pengguna.
    
    Args:
        message (str): Pesan konfirmasi
    
    Returns:
        bool: True jika pengguna mengkonfirmasi
    """
    response = input(f"{message} (y/n): ").strip().lower()
    return response in ['y', 'yes', 'ya']