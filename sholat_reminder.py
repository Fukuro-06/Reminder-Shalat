# sholat_reminder.py
# File berisi class utama untuk sistem reminder sholat

"""
File ini berisi implementasi class SholatReminder yang mengelola
seluruh logika bisnis program reminder sholat menggunakan 
struktur data Array dan Queue.
"""

import datetime
import time
import threading
from collections import deque

# Import dari file-file lain dalam proyek
from config import (
    SHOLAT_NAMES, 
    DEFAULT_PRAYER_TIMES, 
    REMINDER_CONFIG, 
    MESSAGES
)
from utils import (
    format_time,
    format_date,
    calculate_time_difference,
    play_reminder_sound,
    print_header,
    print_separator,
    create_datetime_from_time,
    is_time_in_range,
    format_prayer_notification,
    get_current_time_info
)

class SholatReminder:
    """
    Class utama untuk mengelola sistem reminder jadwal sholat.
    
    Menggunakan:
    - Array untuk menyimpan jadwal sholat
    - Queue untuk mengelola antrian reminder
    - Threading untuk monitoring real-time
    """
    
    def __init__(self):
        """
        Inisialisasi objek SholatReminder.
        Menyiapkan array jadwal dan queue reminder.
        """
        # Array untuk menyimpan nama-nama sholat (dari config)
        self.sholat_names = SHOLAT_NAMES.copy()
        
        # Array untuk menyimpan waktu default (dari config)
        self.default_times = [time_pair.copy() for time_pair in DEFAULT_PRAYER_TIMES]
        
        # Array untuk menyimpan jadwal sholat hari ini
        # Format: [(nama_sholat, datetime_object), ...]
        self.today_schedule = []
        
        # Queue untuk menyimpan reminder yang akan datang
        # Menggunakan deque untuk operasi queue yang efisien
        self.reminder_queue = deque()
        
        # Flag untuk mengontrol thread monitoring
        self.is_running = False
        
        # Thread object untuk monitoring
        self.monitor_thread = None
        
        # Inisialisasi jadwal hari ini
        self.initialize_today_schedule()
    
    def initialize_today_schedule(self):
        """
        Menginisialisasi array jadwal sholat untuk hari ini.
        Mengonversi waktu default menjadi objek datetime.
        """
        print(MESSAGES['initialization'])
        
        today = datetime.date.today()
        self.today_schedule = []  # Reset array jadwal
        
        # Mengisi array jadwal dengan iterasi melalui waktu default
        for i in range(len(self.sholat_names)):
            sholat_name = self.sholat_names[i]
            hour, minute = self.default_times[i]
            
            # Membuat objek datetime untuk waktu sholat
            sholat_time = create_datetime_from_time(hour, minute, today)
            
            # Menyimpan dalam array sebagai tuple (nama, waktu)
            self.today_schedule.append((sholat_name, sholat_time))
        
        print(MESSAGES['init_success'])
        self.display_schedule()
    
    def display_schedule(self):
        """
        Menampilkan jadwal sholat dengan iterasi melalui array.
        """
        print_header("📅 JADWAL SHOLAT HARI INI", 'schedule')
        
        # Iterasi melalui array jadwal sholat
        for i in range(len(self.today_schedule)):
            sholat_name, sholat_time = self.today_schedule[i]
            formatted_time = format_time(sholat_time)
            print(f"{i+1}. {sholat_name:<8} : {formatted_time}")
        
        print_separator('schedule')
    
    def update_sholat_time(self, sholat_index, hour, minute):
        """
        Mengupdate waktu sholat tertentu dalam array berdasarkan indeks.
        
        Args:
            sholat_index (int): Indeks sholat dalam array (0-4)
            hour (int): Jam baru (0-23)
            minute (int): Menit baru (0-59)
        
        Returns:
            bool: True jika berhasil diupdate
        """
        # Validasi indeks array
        if not (0 <= sholat_index < len(self.today_schedule)):
            print("❌ Indeks sholat tidak valid!")
            return False
        
        try:
            today = datetime.date.today()
            new_time = create_datetime_from_time(hour, minute, today)
            
            # Update array pada indeks tertentu
            sholat_name = self.today_schedule[sholat_index][0]
            self.today_schedule[sholat_index] = (sholat_name, new_time)
            
            print(f"✅ Waktu {sholat_name} berhasil diupdate menjadi {hour:02d}:{minute:02d}")
            
            # Rebuild queue jika sistem sedang berjalan
            if self.is_running:
                self.build_reminder_queue()
            
            return True
        
        except Exception as e:
            print(f"❌ Error saat update waktu: {e}")
            return False
    
    def build_reminder_queue(self):
        """
        Membangun queue reminder dari array jadwal sholat.
        Queue diurutkan berdasarkan waktu (FIFO untuk waktu yang sama).
        """
        print(MESSAGES['building_queue'])
        
        # Kosongkan queue yang lama
        self.reminder_queue.clear()
        
        current_time = get_current_time_info()['datetime']
        upcoming_reminders = []
        
        # Iterasi melalui array jadwal untuk mencari sholat yang belum lewat
        for i in range(len(self.today_schedule)):
            sholat_name, sholat_time = self.today_schedule[i]
            
            # Hanya masukkan sholat yang waktunya belum lewat
            if sholat_time > current_time:
                # Hitung selisih waktu untuk sorting
                time_diff = (sholat_time - current_time).total_seconds()
                upcoming_reminders.append((time_diff, sholat_name, sholat_time))
        
        # Sort berdasarkan waktu (ascending) - yang terdekat di awal
        upcoming_reminders.sort(key=lambda x: x[0])
        
        # Enqueue reminder ke dalam queue sesuai urutan waktu
        for _, sholat_name, sholat_time in upcoming_reminders:
            self.reminder_queue.append((sholat_name, sholat_time))
        
        queue_size = len(self.reminder_queue)
        print(f"{MESSAGES['queue_built']} {queue_size} sholat yang akan datang")
        
        if queue_size > 0:
            self.display_queue()
        
        return queue_size > 0
    
    def display_queue(self):
        """
        Menampilkan isi queue reminder tanpa mengubah urutan.
        Menggunakan list conversion untuk menampilkan tanpa dequeue.
        """
        if not self.reminder_queue:
            print("📭 Queue reminder kosong")
            return
        
        print_header("📋 QUEUE REMINDER SHOLAT", 'queue')
        
        # Konversi queue ke list untuk ditampilkan tanpa mengubah queue
        temp_queue = list(self.reminder_queue)
        
        for i, (sholat_name, sholat_time) in enumerate(temp_queue):
            formatted_time = format_time(sholat_time)
            
            # Tampilkan status khusus untuk reminder berikutnya
            if i == 0:
                status = "⏰ BERIKUTNYA"
            else:
                status = f"   Urutan {i+1}"
            
            print(f"{status} | {sholat_name} ({formatted_time})")
        
        print_separator('queue')
    
    def get_next_prayer_info(self):
        """
        Mendapatkan informasi sholat berikutnya dari head queue.
        
        Returns:
            dict atau None: Informasi sholat berikutnya
        """
        if not self.reminder_queue:
            return None
        
        # Peek queue tanpa dequeue
        next_sholat_name, next_sholat_time = self.reminder_queue[0]
        
        # Hitung countdown
        time_info = calculate_time_difference(next_sholat_time)
        
        return {
            'name': next_sholat_name,
            'time': format_time(next_sholat_time),
            'countdown': time_info['formatted'],
            'is_past': time_info['is_past']
        }
    
    def process_prayer_reminder(self, sholat_name, sholat_time):
        """
        Memproses reminder sholat yang telah tiba.
        
        Args:
            sholat_name (str): Nama sholat
            sholat_time (datetime): Waktu sholat
        """
        # Format dan tampilkan notifikasi
        notification = format_prayer_notification(sholat_name, sholat_time)
        print(notification)
        
        # Mainkan suara reminder
        play_reminder_sound()
        
        print(f"✅ Reminder {sholat_name} telah diproses dan dihapus dari queue")
    
    def monitor_prayer_times(self):
        """
        Thread function untuk memantau waktu sholat secara real-time.
        Menggunakan queue untuk mengelola reminder yang akan datang.
        """
        print(MESSAGES['monitoring_start'])
        
        while self.is_running:
            # Periksa apakah queue masih berisi reminder
            if self.reminder_queue:
                # Peek head queue tanpa dequeue
                next_sholat_name, next_sholat_time = self.reminder_queue[0]
                
                # Cek apakah waktu sholat sudah tiba dengan toleransi
                if is_time_in_range(next_sholat_time):
                    # Dequeue reminder yang sudah tiba
                    completed_reminder = self.reminder_queue.popleft()
                    sholat_name, sholat_time = completed_reminder
                    
                    # Proses reminder
                    self.process_prayer_reminder(sholat_name, sholat_time)
                    
                    # Tampilkan status queue yang tersisa
                    if self.reminder_queue:
                        remaining = len(self.reminder_queue)
                        print(f"📋 Sisa {remaining} reminder dalam queue")
                        self.display_queue()
                    else:
                        print(MESSAGES['all_prayers_done'])
            
            # Sleep sesuai interval konfigurasi
            time.sleep(REMINDER_CONFIG['check_interval'])
    
    def start_reminder(self):
        """
        Memulai sistem reminder sholat.
        
        Returns:
            bool: True jika berhasil dimulai
        """
        if self.is_running:
            print(MESSAGES['already_running'])
            return False
        
        print_header("🚀 MEMULAI SISTEM REMINDER SHOLAT", 'menu')
        
        # Build queue dari array jadwal
        if not self.build_reminder_queue():
            print(MESSAGES['no_reminders'])
            print("💡 Mungkin semua waktu sholat sudah terlewat")
            return False
        
        # Start monitoring thread
        self.is_running = True
        self.monitor_thread = threading.Thread(
            target=self.monitor_prayer_times,
            daemon=True
        )
        self.monitor_thread.start()
        
        print(MESSAGES['system_active'])
        print("💡 Tekan Ctrl+C untuk menghentikan")
        
        return True
    
    def stop_reminder(self):
        """
        Menghentikan sistem reminder.
        """
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Tunggu thread selesai dengan timeout
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1)
        
        print(MESSAGES['system_stopped'])
    
    def get_system_status(self):
        """
        Mendapatkan status sistem reminder.
        
        Returns:
            dict: Informasi status sistem
        """
        status = {
            'is_running': self.is_running,
            'queue_size': len(self.reminder_queue),
            'total_prayers': len(self.today_schedule),
            'next_prayer': self.get_next_prayer_info()
        }
        
        # Hitung berapa sholat yang sudah lewat
        current_time = get_current_time_info()['datetime']
        passed_prayers = 0
        
        for _, sholat_time in self.today_schedule:
            if sholat_time <= current_time:
                passed_prayers += 1
        
        status['passed_prayers'] = passed_prayers
        status['remaining_prayers'] = status['total_prayers'] - passed_prayers
        
        return status
    
    def reset_schedule(self):
        """
        Reset jadwal ke pengaturan default.
        """
        print("🔄 Mereset jadwal ke pengaturan default...")
        
        # Stop reminder jika sedang berjalan
        if self.is_running:
            self.stop_reminder()
        
        # Reset ke waktu default
        self.initialize_today_schedule()
        
        print("✅ Jadwal berhasil direset")
    
    def export_schedule(self):
        """
        Export jadwal sholat ke format yang bisa disimpan.
        
        Returns:
            dict: Data jadwal yang bisa diserialisasi
        """
        schedule_data = {
            'date': get_current_time_info()['formatted_date'],
            'prayers': []
        }
        
        for i, (sholat_name, sholat_time) in enumerate(self.today_schedule):
            schedule_data['prayers'].append({
                'index': i,
                'name': sholat_name,
                'time': format_time(sholat_time),
                'hour': sholat_time.hour,
                'minute': sholat_time.minute
            })
        
        return schedule_data
    
    def import_schedule(self, schedule_data):
        """
        Import jadwal sholat dari data yang disimpan.
        
        Args:
            schedule_data (dict): Data jadwal untuk diimport
        
        Returns:
            bool: True jika berhasil diimport
        """
        try:
            if 'prayers' not in schedule_data:
                raise ValueError("Format data tidak valid")
            
            # Stop reminder jika sedang berjalan
            if self.is_running:
                self.stop_reminder()
            
            # Clear schedule lama
            self.today_schedule = []
            
            # Import setiap waktu sholat
            for prayer_data in schedule_data['prayers']:
                sholat_name = prayer_data['name']
                hour = prayer_data['hour']
                minute = prayer_data['minute']
                
                today = datetime.date.today()
                sholat_time = create_datetime_from_time(hour, minute, today)
                
                self.today_schedule.append((sholat_name, sholat_time))
            
            print("✅ Jadwal berhasil diimport")
            self.display_schedule()
            
            return True
        
        except Exception as e:
            print(f"❌ Error saat import jadwal: {e}")
            # Kembalikan ke schedule default jika import gagal
            self.initialize_today_schedule()
            return False