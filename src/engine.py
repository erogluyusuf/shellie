import os
import subprocess
import webbrowser
import tempfile
import psutil


class ShellieEngine:
    def __init__(self):
        self.src_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.dirname(self.src_path)

        self.php_exe = os.path.join(self.root_path, "php", "php.exe")
        self.dashboard_path = os.path.join(self.root_path, "dashboard")
        self.log_file = os.path.join(self.root_path, "log.txt")

        self.port = "8080"
        self.url = f"http://localhost:{self.port}"

    # ----------------------------------------------------

    def get_initial_state(self):
        return {
            "buttons": [
                {"label": "Dashboard", "id": "cmd_dashboard"},
                {"label": "Cache", "id": "cmd_cache"},
                {"label": "Shock", "id": "cmd_shock"},
                {"label": "Close", "id": "cmd_close_menu"}
            ]
        }


    # ----------------------------------------------------

    def execute_command(self, command_id):
        self._log_action(command_id)

        if command_id == "cmd_dashboard":
            return self._run_dashboard()

        if command_id == "cmd_cache":
            return self._cache_clean()

        if command_id == "cmd_shock":
            return self._shock()

        if command_id == "cmd_home":
            return self.get_initial_state()

        return None

    # ----------------------------------------------------

    def _log_action(self, command_id):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"command: {command_id}\n")
        except:
            pass

    # ----------------------------------------------------

    def _is_php_running(self):
        try:
            output = subprocess.check_output(
                'tasklist /FI "IMAGENAME eq php.exe"',
                shell=True
            ).decode()
            return "php.exe" in output
        except:
            return False

    # ----------------------------------------------------

    def _run_dashboard(self):

        if not os.path.exists(self.php_exe):
            return {
                "title": "Hata",
                "message": f"php.exe not found.!\n{self.php_exe}",
                "buttons": [{"label": "Home", "id": "cmd_home"}]
            }

        if not os.path.exists(self.dashboard_path):
            return {
                "title": "Hata",
                "message": f"Dashboard directory not found.!\n{self.dashboard_path}",
                "buttons": [{"label": "Home", "id": "cmd_home"}]
            }

        try:
            if not self._is_php_running():
                subprocess.Popen(
                    [
                        self.php_exe,
                        "-S",
                        f"localhost:{self.port}",
                        "-t",
                        self.dashboard_path
                    ],
                    cwd=self.root_path,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

            webbrowser.open(self.url)

            return {
                "title": "Success",
                "message": "Dashboard has been launched.",
                "buttons": [{"label": "Home", "id": "cmd_home"}]
            }

        except Exception as e:
            return {
                "title": "Hata",
                "message": str(e),
                "buttons": [{"label": "Home", "id": "cmd_home"}]
            }

    # ----------------------------------------------------

    def _cache_clean(self):
        deleted = 0

        def safe_delete(path):
            nonlocal deleted
            if not os.path.exists(path):
                return

            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        deleted += 1
                    except:
                        pass

        # 1️⃣ User TEMP
        safe_delete(tempfile.gettempdir())

        # 2️⃣ Windows TEMP
        safe_delete(r"C:\Windows\Temp")

        # 3️⃣ Thumbnail cache
        thumb_cache = os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            r"Microsoft\Windows\Explorer"
        )
        safe_delete(thumb_cache)

        # 4️⃣ Recent files (shortcut history)
        recent_path = os.path.join(
            os.environ.get("APPDATA", ""),
            r"Microsoft\Windows\Recent"
        )
        safe_delete(recent_path)

        # 5️⃣ DNS flush
        try:
            subprocess.call("ipconfig /flushdns", shell=True)
        except:
            pass

        return {
            "title": "Cleanup Complete",
            "message": f"{deleted} unnecessary files removed.\nDNS cache flushed.",
            "buttons": [{"label": "Home", "id": "cmd_home"}]
        }

    # ----------------------------------------------------

    def _shock(self):
        try:
            processes = sorted(
                psutil.process_iter(['pid', 'name', 'memory_info']),
                key=lambda p: p.info['memory_info'].rss if p.info['memory_info'] else 0,
                reverse=True
            )

            for proc in processes:
                name = proc.info['name'].lower()

                if name not in ["system", "explorer.exe"]:
                    try:
                        proc.kill()
                        return {
                            "title": "Process Terminated",
                            "message": f"{proc.info['name']} has been closed.",
                            "buttons": [{"label": "Home", "id": "cmd_home"}]
                        }
                    except:
                        continue

            return {
                "title": "No Action Required",
                "message": "No terminable application was found.",
                "buttons": [{"label": "Home", "id": "cmd_home"}]
            }

        except Exception as e:
            return {
                "title": "Hata",
                "message": str(e),
                "buttons": [{"label": "Home", "id": "cmd_home"}]
            }
