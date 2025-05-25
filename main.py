# main.py
# File utama untuk menjalankan program Reminder Jadwal Sholat

"""
File entry point untuk program Reminder Jadwal Sholat.
Mengelola interface pengguna dan koordinasi dengan class SholatReminder.
"""

import sys
import json
import os
from datetime import datetime

# Import dari file-file dalam proyek
from config import MAIN_MENU, MESSAGES, DISPLAY_CONFIG, SHOLAT_NAMES
from utils import (
    print_header,
    print_separator,
    safe_input,
    validate_time_input,
    validate_sholat_index,
    confirm_action,
    clear_screen
)
from sholat_reminder import SholatReminder

class MainInterface:
    """
    Class untuk mengelola interface utama program.
    """
    
    def __init__(self):
        """
        Inisialisasi interface utama.
        """
        self.reminder = SholatReminder()
        self.running = True
    
    def display_welcome(self):
        """
        Menampilkan pesan selamat datang.
        """
        print_separator('default')
        print(MESSAGES['welcome'])
        print_separator('default')
        print("Program Reminder Jadwal Sholat dengan Array dan Queue")
        print("Dikembangkan untuk membantu mengingatkan waktu sholat")
        print_separator('default')
    
    def display_main_menu(self):
        """
        Menampilkan menu utama.
        """
        print_header(f"{DISPLAY_CONFIG['list_emoji']} MENU UTAMA", 'menu')
        
        for i, menu_item in enumerate(MAIN_MENU, 1):
            print(f"{i}. {menu_item}")
        
        print_separator('menu')
    
    def handle_display_schedule(self):
        """
        Menangani menu tampilan jadwal sholat.
        """
        self.reminder.display_schedule()
        
        # Tampilkan informasi tambahan
        status = self.reminder.get_system_status()
        print(f"\n📊 Status: {status['passed_prayers']} sholat sudah lewat, "
              f"{status['remaining_prayers']} sholat tersisa")
        
        if status['next_prayer']:
            next_info = status['next_prayer']
            if not next_info['is_past']:
                print(f"🔔 Sholat berikutnya: {next_info['name']} "
                      f"({next_info['time']}) - {next_info['countdown']}")
    
    def handle_update_time(self):
        """
        Menangani menu update waktu sholat.
        """
        print_header(f"{DISPLAY_CONFIG['gear_emoji']} UPDATE WAKTU SHOLAT", 'menu')
        
        # Tampilkan pilihan sholat
        print("Pilih sholat yang ingin diupdate:")
        for i, name in enumerate(SHOLAT_NAMES):
            print(f"{i}. {name}")
        
        print_separator('menu')
        
        # Input indeks sholat dengan validasi
        def validate_idx(idx):
            return validate_sholat_index(idx, len(SHOLAT_NAMES))
        
        sholat_idx = safe_input(
            "Masukkan nomor sholat (0-4): ",
            int,
            validate_idx
        )
        
        if sholat_idx is None:  # User membatalkan
            return
        
        print(f"\nMengupdate waktu untuk: {SHOLAT_NAMES[sholat_idx]}")
        
        # Input jam dengan validasi
        def validate_hour(hour):
            return validate_time_input(hour, 0)
        
        hour = safe_input(
            "Masukkan jam baru (0-23): ",
            int,
            lambda h: validate_hour(h)[0:2] if validate_hour(h)[0] else (False, validate_hour(h)[1])
        )
        
        if hour is None:
            return
        
        # Input menit dengan validasi
        def validate_minute(minute):
            return validate_time_input(0, minute)
        
        minute = safe_input(
            "Masukkan menit baru (0-59): ",
            int,
            lambda m: validate_minute(m)[0:2] if validate_minute(m)[0] else (False, validate_minute(m)[1])
        )
        
        if minute is None:
            return
        
        # Konfirmasi perubahan
        old_time = self.reminder.today_schedule[sholat_idx][1]
        old_formatted = old_time.strftime("%H:%M")
        
        print(f"\nKonfirmasi perubahan:")
        print(f"Sholat: {SHOLAT_NAMES[sholat_idx]}")
        print(f"Waktu lama: {old_formatted}")
        print(f"Waktu baru: {hour:02d}:{minute:02d}")
        
        if confirm_action("Lanjutkan update?"):
            success = self.reminder.update_sholat_time(sholat_idx, hour, minute)
            if success:
                print("✅ Waktu berhasil diupdate!")
            else:
                print("❌ Gagal mengupdate waktu!")
        else:
            print("❌ Update dibatalkan")
    
    def handle_start_reminder(self):
        """
        Menangani menu start reminder.
        """
        if self.reminder.is_running:
            print(MESSAGES['already_running'])
            
            # Tampilkan status saat ini
            self.display_reminder_status()
            
            # Tanya apakah ingin restart
            if confirm_action("Restart reminder?"):
                self.reminder.stop_reminder()
                print("⏳ Memulai ulang sistem reminder...")
                if self.reminder.start_reminder():
                    print("🎉 Reminder berhasil dimulai ulang!")
                else:
                    print("❌ Gagal memulai reminder")
            return
        
        # Konfirmasi sebelum memulai
        print("📋 Sistem akan memulai monitoring reminder sholat")
        print("💡 Program akan berjalan di background dan memberikan notifikasi")
        print("💡 Tekan Ctrl+C di menu utama untuk menghentikan")
        
        if confirm_action("Mulai reminder sekarang?"):
            success = self.reminder.start_reminder()
            if success:
                print("🎉 Reminder berhasil dimulai!")
                print("💡 Kembali ke menu utama untuk fungsi lainnya")
            else:
                print("❌ Gagal memulai reminder")
        else:
            print("❌ Start reminder dibatalkan")
    
    def display_reminder_status(self):
        """
        Menampilkan status reminder sistem.
        """
        status = self.reminder.get_system_status()
        
        print_header("📊 STATUS REMINDER SISTEM", 'menu')
        
        # Status sistem
        if status['is_running']:
            print(f"✅ Status: Reminder AKTIF")
        else:
            print(f"❌ Status: Reminder TIDAK AKTIF")
        
        # Statistik
        print(f"📈 Total sholat hari ini: {status['total_prayers']}")
        print(f"✅ Sholat yang sudah lewat: {status['passed_prayers']}")
        print(f"⏰ Sholat yang tersisa: {status['remaining_prayers']}")
        print(f"📋 Reminder dalam queue: {status['queue_size']}")
        
        # Info sholat berikutnya
        if status['next_prayer']:
            next_info = status['next_prayer']
            print(f"\n🔔 Sholat berikutnya: {next_info['name']}")
            print(f"⏰ Waktu: {next_info['time']}")
            
            if not next_info['is_past']:
                print(f"⏳ Waktu tersisa: {next_info['countdown']}")
            else:
                print("⚠️  Waktu sudah terlewat")
        else:
            print("\n📭 Tidak ada sholat yang tersisa hari ini")
        
        print_separator('menu')
        
        # Tampilkan queue jika ada
        if status['queue_size'] > 0:
            self.reminder.display_queue()
    
    def handle_status_reminder(self):
        """
        Menangani menu status reminder.
        """
        self.display_reminder_status()
        
        # Menu tambahan jika reminder aktif
        if self.reminder.is_running:
            print("\n📋 Opsi tambahan:")
            print("1. Stop reminder")
            print("2. Restart reminder")
            print("3. Kembali ke menu utama")
            
            choice = safe_input("Pilih opsi (1-3): ", str)
            
            if choice == "1":
                if confirm_action("Stop reminder?"):
                    self.reminder.stop_reminder()
                    print("🛑 Reminder dihentikan")
            
            elif choice == "2":
                if confirm_action("Restart reminder?"):
                    self.reminder.stop_reminder()
                    print("⏳ Memulai ulang...")
                    if self.reminder.start_reminder():
                        print("🎉 Reminder berhasil dimulai ulang!")
                    else:
                        print("❌ Gagal memulai reminder")
            
            elif choice == "3":
                pass  # Kembali ke menu utama
            
            else:
                print(MESSAGES['invalid_choice'])
    
    def handle_advanced_menu(self):
        """
        Menangani menu lanjutan (hidden menu).
        """
        print_header("🔧 MENU LANJUTAN", 'menu')
        print("1. Reset jadwal ke default")
        print("2. Export jadwal")
        print("3. Import jadwal")
        print("4. Clear screen")
        print("5. Kembali ke menu utama")
        print_separator('menu')
        
        choice = safe_input("Pilih opsi (1-5): ", str)
        
        if choice == "1":
            if confirm_action("Reset semua waktu ke default?"):
                self.reminder.reset_schedule()
        
        elif choice == "2":
            self.export_schedule()
        
        elif choice == "3":
            self.import_schedule()
        
        elif choice == "4":
            clear_screen()
            self.display_welcome()
        
        elif choice == "5":
            pass  # Kembali
        
        else:
            print(MESSAGES['invalid_choice'])
    
    def export_schedule(self):
        """
        Export jadwal ke file JSON.
        """
        try:
            schedule_data = self.reminder.export_schedule()
            filename = f"jadwal_sholat_{datetime.now().strftime('%Y%m%d')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(schedule_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Jadwal berhasil diexport ke: {filename}")
        
        except Exception as e:
            print(f"❌ Error saat export: {e}")
    
    def import_schedule(self):
        """
        Import jadwal dari file JSON.
        """
        filename = safe_input("Masukkan nama file JSON: ", str)
        
        if not filename:
            return
        
        try:
            if not os.path.exists(filename):
                print(f"❌ File tidak ditemukan: {filename}")
                return
            
            with open(filename, 'r', encoding='utf-8') as f:
                schedule_data = json.load(f)
            
            success = self.reminder.import_schedule(schedule_data)
            
            if success:
                print(f"✅ Jadwal berhasil diimport dari: {filename}")
            else:
                print("❌ Gagal import jadwal")
        
        except Exception as e:
            print(f"❌ Error saat import: {e}")
    
    def handle_exit(self):
        """
        Menangani menu keluar program.
        """
        print_header("👋 KELUAR PROGRAM", 'menu')
        
        if self.reminder.is_running:
            print("⚠️  Reminder masih aktif!")
            if confirm_action("Stop reminder dan keluar program?"):
                self.reminder.stop_reminder()
                print(MESSAGES['goodbye'])
                self.running = False
            else:
                print("❌ Keluar dibatalkan")
        else:
            if confirm_action("Keluar dari program?"):
                print(MESSAGES['goodbye'])
                self.running = False
            else:
                print("❌ Keluar dibatalkan")
    
    def run(self):
        """
        Menjalankan loop utama program.
        """
        self.display_welcome()
        
        try:
            while self.running:
                self.display_main_menu()
                
                choice = safe_input("\nPilih menu (1-5): ", str)
                
                if choice == '1':
                    self.handle_display_schedule()
                
                elif choice == '2':
                    self.handle_update_time()
                
                elif choice == '3':
                    self.handle_start_reminder()
                
                elif choice == '4':
                    self.handle_status_reminder()
                
                elif choice == '5':
                    self.handle_exit()
                
                elif choice.lower() == 'advanced':
                    # Hidden advanced menu
                    self.handle_advanced_menu()
                
                else:
                    print(MESSAGES['invalid_choice'])
                
                # Pause sebentar kecuali jika akan keluar
                if self.running:
                    input("\nTekan Enter untuk melanjutkan...")
        
        except KeyboardInterrupt:
            print(f"\n\n{DISPLAY_CONFIG['stop_emoji']} Program dihentikan oleh pengguna")
            self.reminder.stop_reminder()
        
        except Exception as e:
            print(f"❌ Terjadi error: {e}")
            self.reminder.stop_reminder()
        
        finally:
            # Pastikan reminder dihentikan
            if self.reminder.is_running:
                self.reminder.stop_reminder()

def main():
    """
    Fungsi utama untuk menjalankan program.
    """
    try:
        # Cek apakah semua import berhasil
        print("🔄 Memuat komponen program...")
        
        # Inisialisasi interface utama
        interface = MainInterface()
        
        print("✅ Semua komponen berhasil dimuat")
        
        # Jalankan program
        interface.run()
    
    except ImportError as e:
        print(f"❌ Error import module: {e}")
        print("💡 Pastikan semua file (config.py, utils.py, sholat_reminder.py) ada di folder yang sama")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error saat menjalankan program: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()