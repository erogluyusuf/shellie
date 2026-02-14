import sys
import os

# src klasörünü path'e ekle (Import hatalarını önlemek için)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui import ShellieUI

def main():
    app = QApplication(sys.argv)
    
    window = ShellieUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()