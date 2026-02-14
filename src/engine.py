import os
import subprocess
import webbrowser

class ShellieEngine:
    def __init__(self):
        self.src_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.dirname(self.src_path)
        self.run_bat = os.path.join(self.root_path, "run.bat")  # run.bat yolu
        self.log_file = os.path.join(self.root_path, "log.txt")  # log.txt yolu

    def get_initial_state(self):
        return {
            "title": "Kontrol Merkezi",
            "message": "Dashboard sistemini yönet.",
            "buttons": [
                {"label": "📊 Dashboard'a Git", "id": "cmd_dashboard"},
                {"label": "❌ Kapat", "id": "cmd_close_menu"}
            ]
        }

    def execute_command(self, command_id):
        print(f"\n[DEBUG ENGINE] Komut geldi: {command_id}")
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"Komut geldi: {command_id}\n")
        except Exception as e:
            print(f"[LOG HATA] {e}")

        if command_id == "cmd_dashboard":
            if not os.path.exists(self.run_bat):
                print(f"[HATA] run.bat bulunamadı: {self.run_bat}")
                return {"title": "Hata", "message": "run.bat bulunamadı!"}

            try:
                subprocess.Popen(
                    [self.run_bat],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                return {
                    "title": "Sistem Çalışıyor",
                    "message": "Dashboard başlatıldı. Tarayıcı açılıyor...",
                    "buttons": [{"label": "🔙 Ana Menü", "id": "cmd_home"}]
                }
            except Exception as e:
                print(f"[HATA] {e}")
                return {"title": "Hata", "message": str(e)}

        if command_id == "cmd_home":
            return self.get_initial_state()

        if command_id == "cmd_close_menu":
            return None

        return None
