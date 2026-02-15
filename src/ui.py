import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QLabel, QApplication, QGraphicsDropShadowEffect, 
                             QWidget, QVBoxLayout, QPushButton, QFrame)
from PyQt6.QtCore import Qt, QPoint, QTimer, QSize, pyqtSignal
from PyQt6.QtGui import QMovie, QFont, QColor, QCursor
from functools import partial
from PyQt6.QtCore import QPropertyAnimation
# --- HARİCİ DOSYA KONTROLÜ ---
try:
    from engine import ShellieEngine
except ImportError:
    ShellieEngine = None 

# ---------------------------------------------------------
# DİNAMİK BALON SINIFI
# ---------------------------------------------------------
class BubbleWindow(QWidget):
    on_close = pyqtSignal()
    action_triggered = pyqtSignal(str) 
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint|
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.auto_close_timer = QTimer(self)
        self.auto_close_timer.setSingleShot(True)
        self.auto_close_timer.timeout.connect(self.auto_close)
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(200)  # 200 ms
        self.fade_anim.finished.connect(self._final_close)
        # [ÖNEMLİ] Pencerenin odaklanabilir olması lazım ki dışarı tıklandığını anlasın.
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Ana Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Tasarım Container
        self.container = QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.75);
                border: 1px solid rgba(200, 200, 200, 150);
                border-radius: 15px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.container.setGraphicsEffect(shadow)
        
        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setSpacing(5)
        
        self.main_layout.addWidget(self.container)

    def update_content(self, data):
        """Engine'den gelen veriyi çizer."""
        self.clear_layout(self.content_layout)
        
        if not data:
            self.hide()
            self.on_close.emit()
            return

        # Başlık
        if "title" in data and data["title"]:
            title_lbl = QLabel(data["title"])
            title_lbl.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
            title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_lbl.setStyleSheet("color: #333; margin-bottom: 2px;")
            self.content_layout.addWidget(title_lbl)

        # Mesaj
        if "message" in data:
            msg_lbl = QLabel(data["message"])
            msg_lbl.setFont(QFont('Segoe UI', 9))
            msg_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            msg_lbl.setWordWrap(True)
            msg_lbl.setStyleSheet("color: #555;")
            self.content_layout.addWidget(msg_lbl)

        # Butonlar
        if "buttons" in data and len(data["buttons"]) > 0:
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setStyleSheet("color: #ccc;")
            self.content_layout.addWidget(line)

        for btn_data in data["buttons"]:
            btn = QPushButton(btn_data["label"])
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: none;
                    border-radius: 5px;
                    padding: 6px;
                    color: #333;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            # Burada lambda yerine partial kullanıyoruz
            btn.clicked.connect(partial(self.action_triggered.emit, btn_data["id"]))
            self.content_layout.addWidget(btn)

        self.adjustSize()


    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    def auto_close(self):
        if not self.isVisible():
            return

        self.fade_anim.stop()
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.start()
   
    def _final_close(self):
        self.hide()
        self.setWindowOpacity(1.0)
        self.on_close.emit()



    def enterEvent(self, event):
        self.auto_close_timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.auto_close_timer.start(4000)
        super().leaveEvent(event)


# ---------------------------------------------------------
# ANA TAVŞAN ARAYÜZÜ
# ---------------------------------------------------------
class ShellieUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.engine = None
        if ShellieEngine:
            self.engine = ShellieEngine()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.anim_label = QLabel(self)

        base_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.dirname(base_path)
        assets_path = os.path.join(root_path, "assets")

        self.run_right = os.path.join(assets_path, "Rabbit.gif")
        self.run_left = os.path.join(assets_path, "Rabbit-re.gif")
        self.stop_right = os.path.join(assets_path, "Rabbit-stop.gif")
        self.stop_left = os.path.join(assets_path, "Rabbit-re-stop.gif")

        self.target_size = QSize(70, 70)
        self.movie = QMovie(self.run_right)
        self.movie.setScaledSize(self.target_size)
        self.anim_label.setMovie(self.movie)
        self.anim_label.setFixedSize(self.target_size)
        self.movie.start()

        self.resize(self.target_size)
        screen = self.screen().availableGeometry()
        self.x_limit = screen.width() - self.width()
        self.y_pos = screen.height() - self.height() + 15 
        self.move(self.x_limit, self.y_pos)

        self.direction = -1 
        self.speed = 4
        self.is_stopped = False
        
        # [ÖNEMLİ] Balon kapanırken yanlışlıkla tavşana tıklamayı önlemek için
        self.ignore_next_click = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.walk)
        self.timer.start(50)

        self.bubble = BubbleWindow()
        self.bubble.hide()
        self.bubble.on_close.connect(self.resume_walking)
        self.bubble.action_triggered.connect(self.handle_bubble_action)

        self.update_gif()
    
    def resume_walking(self):
        if self.is_stopped:
            self.is_stopped = False
            self.update_gif()
            
            # Balon kapandığında, anlık olarak tıklamayı yoksay
            # (Eğer kullanıcı balonu kapatmak için tavşanın üzerine tıkladıysa menü tekrar açılmasın)
            self.ignore_next_click = True
            QTimer.singleShot(200, self.reset_click_flag)

    def reset_click_flag(self):
        self.ignore_next_click = False

    def walk(self):
        if self.is_stopped:
            return
        new_x = self.x() + (self.direction * self.speed)
        if new_x >= self.x_limit:
            self.direction = -1
            self.update_gif()
        elif new_x <= 0:
            self.direction = 1
            self.update_gif()
        self.move(new_x, self.y_pos)

    def update_gif(self):
        if self.is_stopped:
            target = self.stop_right if self.direction == 1 else self.stop_left
        else:
            target = self.run_right if self.direction == 1 else self.run_left

        if self.movie.fileName() != target:
            self.movie.stop()
            self.movie.setFileName(target)
            self.movie.setScaledSize(self.target_size)
            self.movie.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            
            # Eğer balon yeni kapandıysa bu tıklamayı yut
            if self.ignore_next_click:
                return

            if self.is_stopped:
                # Eğer zaten duruyorsa (balon açık olabilir veya manuel kapanmış olabilir)
                # Sadece yürütmeye devam et
                self.resume_walking()
                self.bubble.hide()
                return

            # Durdur ve Menüyü Aç
            self.is_stopped = True
            self.update_gif()

            if self.engine:
                data = self.engine.get_initial_state()
                self.show_bubble(data)
            else:
                self.show_bubble({"message": "Motor Bağlanamadı"})

    def handle_bubble_action(self, command_id):
            # Kapat butonu basıldıysa direkt menüyü kapat ve yürüt
            if command_id == "cmd_close_menu":
                self.bubble.hide()
                self.resume_walking()
                return

            if self.engine:
                response = self.engine.execute_command(command_id)
                if response is None:
                    self.bubble.hide()
                    self.resume_walking()
                else:
                    # Yeni bir state geldiyse (örn: "Başlatıldı" mesajı) onu göster
                    self.show_bubble(response)

    def show_bubble(self, data):
        self.bubble.update_content(data)

        geo = self.geometry()
        bubble_geo = self.bubble.geometry()
        bubble_x = geo.x() + (geo.width() // 2) - (bubble_geo.width() // 2)
        bubble_y = geo.y() - bubble_geo.height() - 5

        screen_geo = self.screen().availableGeometry()
        if bubble_x < 0:
            bubble_x = 10
        if bubble_x + bubble_geo.width() > screen_geo.width():
            bubble_x = screen_geo.width() - bubble_geo.width() - 10

        self.bubble.move(bubble_x, bubble_y)

        self.bubble.show()
        self.bubble.raise_()
        self.bubble.activateWindow()
        self.bubble.setFocus()
        self.bubble.auto_close_timer.start(4000)


    def mouseMoveEvent(self, event):
        if self.is_stopped: return 
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - QPoint(self.width() // 2, self.height() // 2))

    def closeEvent(self, event):
        self.bubble.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShellieUI()
    window.show()
    sys.exit(app.exec())