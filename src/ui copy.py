import sys
import os
import psutil
from PyQt6.QtWidgets import (QMainWindow, QLabel, QApplication, QGraphicsDropShadowEffect, 
                             QWidget, QVBoxLayout)
from PyQt6.QtCore import Qt, QPoint, QTimer, QSize, pyqtSignal
from PyQt6.QtGui import QMovie, QFont, QColor

# --- HARİCİ DOSYA KONTROLÜ ---
try:
    from engine import ShellieEngine
except ImportError:
    ShellieEngine = None 

# ---------------------------------------------------------
# ÖZEL BALON SINIFI
# ---------------------------------------------------------
class BubbleWindow(QWidget):
    on_close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # Odaklanma açık

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20) 

        self.label = QLabel()
        self.label.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.72);
                color: #1a1a1a;
                border: 1px solid rgba(255, 255, 255, 220);
                border-radius: 12px;
                padding: 8px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.label.setGraphicsEffect(shadow)

        layout.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)
        self.label.adjustSize()
        self.adjustSize()

    # Dışarı tıklandığında (veya tavşana tıklandığında) çalışır
    def focusOutEvent(self, event):
        self.hide()
        self.on_close.emit()
        super().focusOutEvent(event)

# ---------------------------------------------------------
# ANA TAVŞAN SINIFI
# ---------------------------------------------------------
class ShellieUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        if ShellieEngine:
            self.engine = ShellieEngine()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.anim_label = QLabel(self)

        self.run_right = os.path.join("assets", "Rabbit.gif")
        self.run_left = os.path.join("assets", "Rabbit-re.gif")
        self.stop_right = os.path.join("assets", "Rabbit-stop.gif")
        self.stop_left = os.path.join("assets", "Rabbit-re-stop.gif")

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
        
        # [YENİ] Çakışmayı önlemek için koruma bayrağı
        self.ignore_next_click = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.walk)
        self.timer.start(50)

        self.bubble = BubbleWindow()
        self.bubble.hide()
        self.bubble.on_close.connect(self.resume_walking)

        self.update_gif()

    # Yürümeye devam ettiren fonksiyon
    def resume_walking(self):
        if self.is_stopped:
            self.is_stopped = False
            self.update_gif()
            
            # [YENİ] Balon kapandığında, bir anlığına tıklamaları görmezden gel.
            # Böylece Tavşana tıkladığında tekrar menü açılmaz.
            self.ignore_next_click = True
            QTimer.singleShot(200, self.reset_click_flag)

    # [YENİ] Bayrağı sıfırlayan fonksiyon
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

    # -------------------------
    # TIKLAMA MANTIĞI (GÜNCELLENDİ)
    # -------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            
            # [YENİ] Eğer balon yeni kapandıysa bu tıklamayı yut (işlem yapma)
            if self.ignore_next_click:
                return

            # Eğer zaten duruyorsa (ve balon açık değilse - örn: manuel kapatıldıysa)
            if self.is_stopped:
                self.resume_walking()
                self.bubble.hide()
                return

            # Durdurma ve Balon Açma
            self.is_stopped = True
            self.update_gif()

            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            
            self.bubble.setText(f" Sistem Durumu\nCPU: %{cpu}\nRAM: %{ram}")
            
            geo = self.geometry() 
            bubble_x = geo.x() + (geo.width() // 2) - (self.bubble.width() // 2)
            bubble_y = geo.y() - self.bubble.height() + 10 

            self.bubble.move(bubble_x, bubble_y)
            self.bubble.show()
            self.bubble.raise_()
            self.bubble.activateWindow() # Odağı balona ver

    def mouseMoveEvent(self, event):
        if self.is_stopped:
            return 

        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(
                event.globalPosition().toPoint() - QPoint(self.width() // 2, self.height() // 2)
            )

    def closeEvent(self, event):
        self.bubble.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShellieUI()
    window.show()
    sys.exit(app.exec())