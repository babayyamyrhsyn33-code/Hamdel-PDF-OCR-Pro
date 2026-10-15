#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hamdel PDF OCR Pro
برنامه فوق‌العاده پیشرفته تبدیل PDF به متن با OCR آفلاین
ساخته‌شده توسط گروه تکنولوژی همدل - آکادمی همدل
https://t.me/Akademi_hamdel
"""

import sys
import os
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTextEdit, QComboBox,
    QProgressBar, QTabWidget, QListWidget, QListWidgetItem,
    QMessageBox, QDialog, QCheckBox, QGroupBox, QFormLayout,
    QSpinBox, QSlider, QStatusBar, QToolBar, QMenuBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings, QUrl, QSize
from PyQt6.QtGui import QAction, QKeySequence, QFont, QDesktopServices, QShortcut

try:
    import pytesseract
    from pdf2image import convert_from_path
    from pypdf import PdfReader
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    from piper import PiperVoice
    import wave
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

APP_NAME = "Hamdel PDF OCR Pro"
APP_VERSION = "1.0.0"
CHANNEL_URL = "https://t.me/Akademi_hamdel"
CHANNEL_NAME = "آکادمی همدل"
ORG_NAME = "گروه تکنولوژی همدل"
SETTINGS_ORG = "HamdelTech"
SETTINGS_APP = "PDFOCRPro"

BASE_DIR = Path(__file__).parent.resolve()
VOICES_DIR = BASE_DIR / "voices"
LIBRARY_DIR = Path.home() / "Documents" / "HamdelPDFOCR" / "Library"
LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR = Path.home() / ".hamdel_pdf_ocr"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)


class FirstRunDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("خوش آمدید به Hamdel PDF OCR Pro")
        self.setMinimumSize(700, 500)
        self.setModal(True)
        layout = QVBoxLayout(self)
        title = QLabel("🎉 به برنامه Hamdel PDF OCR Pro خوش آمدید!")
        title.setFont(QFont("Tahoma", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1a73e8; margin: 15px;")
        layout.addWidget(title)
        message = QTextEdit()
        message.setReadOnly(True)
        message.setFont(QFont("Tahoma", 11))
        message.setHtml(f"""
        <div style="direction: rtl; text-align: right; line-height: 1.8; padding: 10px;">
        <p><b>سلام دوست عزیز!</b></p>
        <p>از اینکه برنامه فوق‌العاده پیشرفته <b>Hamdel PDF OCR Pro</b> را انتخاب کردید، بسیار سپاسگزاریم.</p>
        <p>این برنامه توسط <b>{ORG_NAME}</b> با عشق و دقت بسیار بالا طراحی و ساخته شده است تا بتواند حتی سخت‌ترین فایل‌های PDF اسکن‌شده را به متن قابل ویرایش و خواندن تبدیل کند.</p>
        <p>ما تمام تلاش خود را کرده‌ایم تا این برنامه کاملاً آفلاین، سریع، دقیق و از همه مهم‌تر <b>کاملاً دسترسی‌پذیر برای کاربران نابینا و کم‌بینا</b> باشد (سازگار با NVDA و میانبرهای کامل کیبورد).</p>
        <hr>
        <p style="font-size: 14px; color: #d93025;"><b>🙏 لطفاً عضو کانال آکادمی همدل شوید!</b></p>
        <p>با عضویت در کانال ما از آخرین به‌روزرسانی‌ها، آموزش‌های رایگان، ترفندهای دسترسی‌پذیری و برنامه‌های جدید مطلع شوید.</p>
        <p>لینک کانال: <a href="{CHANNEL_URL}">{CHANNEL_URL}</a></p>
        <p>حمایت شما انگیزه ما برای ساخت ابزارهای بهتر و بیشتر است. ❤️</p>
        <p>با سپاس فراوان<br>{ORG_NAME}</p>
        </div>
        """)
        layout.addWidget(message)
        self.dont_show = QCheckBox("دیگر این پیام را نشان نده")
        self.dont_show.setFont(QFont("Tahoma", 10))
        layout.addWidget(self.dont_show)
        btn_layout = QHBoxLayout()
        self.join_btn = QPushButton("🚀 عضویت در کانال آکادمی همدل")
        self.join_btn.setFont(QFont("Tahoma", 12, QFont.Weight.Bold))
        self.join_btn.setStyleSheet("QPushButton { background-color: #0088cc; color: white; padding: 12px 20px; border-radius: 8px; } QPushButton:hover { background-color: #006699; } QPushButton:focus { border: 3px solid #ff9800; }")
        self.join_btn.clicked.connect(self.join_channel)
        self.join_btn.setDefault(True)
        btn_layout.addWidget(self.join_btn)
        close_btn = QPushButton("بستن و ادامه")
        close_btn.setFont(QFont("Tahoma", 11))
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        self.setAccessibleName("دیالوگ خوش‌آمدگویی و دعوت به عضویت")
        self.join_btn.setAccessibleName("دکمه عضویت در کانال آکادمی همدل")
        self.dont_show.setAccessibleName("دیگر این پیام را نشان نده")

    def join_channel(self):
        QDesktopServices.openUrl(QUrl(CHANNEL_URL))
        QMessageBox.information(self, "عضویت", f"در حال باز کردن کانال {CHANNEL_NAME} در تلگرام...")


class OCRWorker(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str, str)

    def __init__(self, pdf_path, lang="fas+eng", dpi=300, parent=None):
        super().__init__(parent)
        self.pdf_path = pdf_path
        self.lang = lang
        self.dpi = dpi
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        try:
            self.progress.emit(5, "در حال آماده‌سازی PDF...")
            text_parts = []
            try:
                reader = PdfReader(self.pdf_path)
                total_pages = len(reader.pages)
                for i, page in enumerate(reader.pages):
                    if self._is_cancelled:
                        self.finished.emit("", "عملیات لغو شد")
                        return
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        text_parts.append(f"--- صفحه {i+1} ---\n{page_text}")
                    self.progress.emit(10 + int(20 * (i+1)/total_pages), f"استخراج متن صفحه {i+1}/{total_pages}")
                if text_parts and sum(len(t) for t in text_parts) > 100:
                    full_text = "\n\n".join(text_parts)
                    self.progress.emit(100, "متن با موفقیت استخراج شد")
                    self.finished.emit(full_text, "")
                    return
            except Exception:
                pass
            self.progress.emit(30, "PDF اسکن‌شده تشخیص داده شد. شروع OCR...")
            images = convert_from_path(self.pdf_path, dpi=self.dpi)
            total = len(images)
            ocr_texts = []
            for i, img in enumerate(images):
                if self._is_cancelled:
                    self.finished.emit("", "عملیات لغو شد")
                    return
                self.progress.emit(30 + int(60 * (i+1)/total), f"OCR صفحه {i+1} از {total}...")
                page_text = pytesseract.image_to_string(img, lang=self.lang, config=r'--oem 3 --psm 6')
                ocr_texts.append(f"--- صفحه {i+1} ---\n{page_text}")
            full_text = "\n\n".join(ocr_texts)
            self.progress.emit(100, "OCR با موفقیت انجام شد!")
            self.finished.emit(full_text, "")
        except Exception as e:
            self.finished.emit("", f"خطا در پردازش: {str(e)}")


class TTSWorker(QThread):
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, text, voice_path, output_path, parent=None):
        super().__init__(parent)
        self.text = text
        self.voice_path = voice_path
        self.output_path = output_path

    def run(self):
        try:
            self.progress.emit("در حال بارگذاری مدل صوتی...")
            if not Path(self.voice_path).exists():
                self.finished.emit("مدل صوتی پیدا نشد.")
                return
            voice = PiperVoice.load(self.voice_path)
            self.progress.emit("در حال تولید صدا...")
            with wave.open(str(self.output_path), "wb") as wav_file:
                voice.synthesize_wav(self.text[:3000], wav_file)
            self.finished.emit(str(self.output_path))
        except Exception as e:
            self.finished.emit(f"خطا در تولید صدا: {str(e)}")


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("درباره ما - About")
        self.setMinimumSize(650, 550)
        layout = QVBoxLayout(self)
        title = QLabel(f"{APP_NAME} v{APP_VERSION}")
        title.setFont(QFont("Tahoma", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1a73e8;")
        layout.addWidget(title)
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setFont(QFont("Tahoma", 11))
        about_text.setHtml(f"""
        <div style="direction: rtl; text-align: right; line-height: 1.9; padding: 15px;">
        <h2 style="color: #1a73e8;">درباره {APP_NAME}</h2>
        <p>این برنامه توسط <b>{ORG_NAME}</b> با هدف خدمت به جامعه فارسی‌زبان و به ویژه کاربران نابینا و کم‌بینا طراحی و توسعه یافته است.</p>
        <h3>🎯 مأموریت ما</h3>
        <p>ما معتقدیم که دسترسی به اطلاعات باید برای همه انسان‌ها، بدون توجه به محدودیت‌های جسمی، آسان و ممکن باشد. به همین دلیل این ابزار را با تمرکز ویژه روی دسترسی‌پذیری، عملکرد آفلاین و کیفیت بالای OCR ساخته‌ایم.</p>
        <h3>✨ ویژگی‌های برجسته</h3>
        <ul>
        <li>موتور OCR قدرتمند مبتنی بر Tesseract با پشتیبانی از زبان پارسی و انگلیسی</li>
        <li>تشخیص خودکار متن انتخاب‌پذیر یا اسکن‌شده</li>
        <li>موتور صوتی طبیعی آفلاین (Piper TTS)</li>
        <li>رابط کاربری کاملاً کیبوردمحور و سازگار با NVDA</li>
        <li>کتابخانه شخصی برای مدیریت فایل‌های تبدیل‌شده</li>
        <li>خروجی در فرمت‌های مختلف (TXT, HTML, Markdown)</li>
        </ul>
        <h3>📢 کانال ما</h3>
        <p>برای دریافت به‌روزرسانی‌ها، آموزش‌ها و برنامه‌های جدید حتماً در کانال <b>{CHANNEL_NAME}</b> عضو شوید:</p>
        <p style="font-size: 14px;"><a href="{CHANNEL_URL}">{CHANNEL_URL}</a></p>
        <p style="margin-top: 20px; color: #555;">با احترام و سپاس<br><b>{ORG_NAME}</b><br>نسخه {APP_VERSION}</p>
        </div>
        """)
        layout.addWidget(about_text)
        btn_layout = QHBoxLayout()
        join_btn = QPushButton("عضویت در کانال")
        join_btn.setStyleSheet("background-color: #0088cc; color: white; padding: 10px; border-radius: 6px;")
        join_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(CHANNEL_URL)))
        btn_layout.addWidget(join_btn)
        copy_btn = QPushButton("کپی لینک کانال")
        copy_btn.clicked.connect(self.copy_link)
        btn_layout.addWidget(copy_btn)
        close_btn = QPushButton("بستن")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def copy_link(self):
        QApplication.clipboard().setText(CHANNEL_URL)
        QMessageBox.information(self, "کپی شد", "لینک کانال در کلیپ‌بورد کپی شد.")


class ShortcutsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("میانبرهای کیبورد")
        self.setMinimumSize(500, 450)
        layout = QVBoxLayout(self)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setFont(QFont("Consolas", 11))
        text.setHtml("""
        <div style="direction: rtl; text-align: right; line-height: 1.7;">
        <h2>میانبرهای کیبورد برنامه</h2>
        <table border="1" cellpadding="6" style="width:100%; border-collapse: collapse;">
        <tr style="background:#e3f2fd;"><th>میانبر</th><th>عملکرد</th></tr>
        <tr><td><b>Ctrl+O</b></td><td>باز کردن فایل PDF</td></tr>
        <tr><td><b>Ctrl+S</b></td><td>ذخیره متن استخراج‌شده</td></tr>
        <tr><td><b>Ctrl+Shift+S</b></td><td>ذخیره به عنوان HTML</td></tr>
        <tr><td><b>Ctrl+E</b></td><td>شروع OCR / تبدیل</td></tr>
        <tr><td><b>Ctrl+P</b></td><td>پخش صدای متن (TTS)</td></tr>
        <tr><td><b>Ctrl+L</b></td><td>رفتن به بخش کتابخانه</td></tr>
        <tr><td><b>Ctrl+1 / 2 / 3</b></td><td>تب تبدیل / کتابخانه / تنظیمات</td></tr>
        <tr><td><b>F1</b></td><td>نمایش میانبرها</td></tr>
        <tr><td><b>Ctrl+Q</b></td><td>خروج از برنامه</td></tr>
        <tr><td><b>Esc</b></td><td>لغو عملیات جاری</td></tr>
        </table>
        <p style="margin-top:15px;">این برنامه کاملاً با صفحه‌خوان NVDA سازگار است.</p>
        </div>
        """)
        layout.addWidget(text)
        close = QPushButton("بستن")
        close.clicked.connect(self.accept)
        layout.addWidget(close)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION} - ساخته‌شده توسط {ORG_NAME}")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        self.settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        self.current_pdf = None
        self.current_text = ""
        self.ocr_worker = None
        self.tts_worker = None
        self.init_ui()
        self.setup_shortcuts()
        self.apply_styles()
        self.check_first_run()
        self.setAccessibleName(APP_NAME)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        self.create_menus()
        toolbar = QToolBar("نوار ابزار اصلی")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        open_action = QAction("📂 باز کردن PDF", self)
        open_action.triggered.connect(self.open_pdf)
        toolbar.addAction(open_action)
        convert_action = QAction("⚡ تبدیل / OCR", self)
        convert_action.triggered.connect(self.start_ocr)
        toolbar.addAction(convert_action)
        save_action = QAction("💾 ذخیره", self)
        save_action.triggered.connect(self.save_text)
        toolbar.addAction(save_action)
        tts_action = QAction("🔊 پخش صدا", self)
        tts_action.triggered.connect(self.play_tts)
        toolbar.addAction(tts_action)
        toolbar.addSeparator()
        about_action = QAction("ℹ️ درباره ما", self)
        about_action.triggered.connect(self.show_about)
        toolbar.addAction(about_action)
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Tahoma", 11))
        main_layout.addWidget(self.tabs)
        self.convert_tab = QWidget()
        self.setup_convert_tab()
        self.tabs.addTab(self.convert_tab, "📄 تبدیل PDF")
        self.library_tab = QWidget()
        self.setup_library_tab()
        self.tabs.addTab(self.library_tab, "📚 کتابخانه")
        self.settings_tab = QWidget()
        self.setup_settings_tab()
        self.tabs.addTab(self.settings_tab, "⚙️ تنظیمات")
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("آماده | برای شروع یک فایل PDF باز کنید (Ctrl+O)")
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMaximumWidth(300)
        self.status.addPermanentWidget(self.progress)

    def create_menus(self):
        menubar = self.menuBar()
        menubar.setFont(QFont("Tahoma", 10))
        file_menu = menubar.addMenu("پرونده")
        open_act = QAction("باز کردن PDF...", self)
        open_act.setShortcut(QKeySequence("Ctrl+O"))
        open_act.triggered.connect(self.open_pdf)
        file_menu.addAction(open_act)
        save_act = QAction("ذخیره متن...", self)
        save_act.setShortcut(QKeySequence("Ctrl+S"))
        save_act.triggered.connect(self.save_text)
        file_menu.addAction(save_act)
        save_html = QAction("ذخیره به عنوان HTML...", self)
        save_html.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_html.triggered.connect(lambda: self.save_text(fmt="html"))
        file_menu.addAction(save_html)
        file_menu.addSeparator()
        exit_act = QAction("خروج", self)
        exit_act.setShortcut(QKeySequence("Ctrl+Q"))
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)
        tools_menu = menubar.addMenu("ابزارها")
        ocr_act = QAction("شروع OCR / تبدیل", self)
        ocr_act.setShortcut(QKeySequence("Ctrl+E"))
        ocr_act.triggered.connect(self.start_ocr)
        tools_menu.addAction(ocr_act)
        tts_act = QAction("پخش صدای متن", self)
        tts_act.setShortcut(QKeySequence("Ctrl+P"))
        tts_act.triggered.connect(self.play_tts)
        tools_menu.addAction(tts_act)
        help_menu = menubar.addMenu("راهنما")
        shortcuts_act = QAction("میانبرهای کیبورد", self)
        shortcuts_act.setShortcut(QKeySequence("F1"))
        shortcuts_act.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_act)
        about_act = QAction("درباره ما", self)
        about_act.triggered.connect(self.show_about)
        help_menu.addAction(about_act)
        channel_act = QAction("عضویت در کانال آکادمی همدل", self)
        channel_act.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(CHANNEL_URL)))
        help_menu.addAction(channel_act)

    def setup_convert_tab(self):
        layout = QVBoxLayout(self.convert_tab)
        top = QHBoxLayout()
        self.file_label = QLabel("هیچ فایلی انتخاب نشده")
        self.file_label.setFont(QFont("Tahoma", 10))
        self.file_label.setStyleSheet("padding: 8px; background: #f0f0f0; border-radius: 4px;")
        top.addWidget(self.file_label, stretch=1)
        open_btn = QPushButton("📂 انتخاب PDF")
        open_btn.setFont(QFont("Tahoma", 11))
        open_btn.clicked.connect(self.open_pdf)
        top.addWidget(open_btn)
        self.convert_btn = QPushButton("⚡ شروع تبدیل / OCR")
        self.convert_btn.setFont(QFont("Tahoma", 11, QFont.Weight.Bold))
        self.convert_btn.setStyleSheet("background-color: #1a73e8; color: white; padding: 10px 18px; border-radius: 6px;")
        self.convert_btn.clicked.connect(self.start_ocr)
        top.addWidget(self.convert_btn)
        layout.addLayout(top)
        options = QHBoxLayout()
        options.addWidget(QLabel("زبان OCR:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["fas+eng (پارسی + انگلیسی)", "fas (فقط پارسی)", "eng (فقط انگلیسی)", "ara+eng (عربی + انگلیسی)"])
        options.addWidget(self.lang_combo)
        options.addWidget(QLabel("کیفیت (DPI):"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(150, 600)
        self.dpi_spin.setValue(300)
        options.addWidget(self.dpi_spin)
        options.addStretch()
        layout.addLayout(options)
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Tahoma", 12))
        self.text_edit.setPlaceholderText("متن استخراج‌شده اینجا نمایش داده می‌شود...")
        layout.addWidget(self.text_edit)
        bottom = QHBoxLayout()
        save_txt = QPushButton("💾 ذخیره TXT")
        save_txt.clicked.connect(lambda: self.save_text("txt"))
        bottom.addWidget(save_txt)
        save_html = QPushButton("🌐 ذخیره HTML")
        save_html.clicked.connect(lambda: self.save_text("html"))
        bottom.addWidget(save_html)
        save_md = QPushButton("📝 ذخیره Markdown")
        save_md.clicked.connect(lambda: self.save_text("md"))
        bottom.addWidget(save_md)
        add_lib = QPushButton("📚 افزودن به کتابخانه")
        add_lib.clicked.connect(self.add_to_library)
        bottom.addWidget(add_lib)
        self.tts_btn = QPushButton("🔊 پخش با صدای طبیعی")
        self.tts_btn.setStyleSheet("background-color: #34a853; color: white; padding: 8px;")
        self.tts_btn.clicked.connect(self.play_tts)
        bottom.addWidget(self.tts_btn)
        layout.addLayout(bottom)

    def setup_library_tab(self):
        layout = QVBoxLayout(self.library_tab)
        header = QLabel("📚 کتابخانه فایل‌های تبدیل‌شده")
        header.setFont(QFont("Tahoma", 14, QFont.Weight.Bold))
        layout.addWidget(header)
        self.library_list = QListWidget()
        self.library_list.setFont(QFont("Tahoma", 11))
        self.library_list.itemDoubleClicked.connect(self.open_library_item)
        layout.addWidget(self.library_list)
        btns = QHBoxLayout()
        refresh_btn = QPushButton("🔄 تازه‌سازی")
        refresh_btn.clicked.connect(self.refresh_library)
        btns.addWidget(refresh_btn)
        open_btn = QPushButton("باز کردن")
        open_btn.clicked.connect(self.open_selected_library)
        btns.addWidget(open_btn)
        delete_btn = QPushButton("حذف")
        delete_btn.clicked.connect(self.delete_library_item)
        btns.addWidget(delete_btn)
        open_folder = QPushButton("📁 باز کردن پوشه کتابخانه")
        open_folder.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(LIBRARY_DIR))))
        btns.addWidget(open_folder)
        layout.addLayout(btns)
        self.refresh_library()

    def setup_settings_tab(self):
        layout = QVBoxLayout(self.settings_tab)
        voice_group = QGroupBox("تنظیمات موتور صوتی (TTS)")
        voice_group.setFont(QFont("Tahoma", 11))
        voice_layout = QFormLayout(voice_group)
        self.voice_combo = QComboBox()
        self.populate_voices()
        voice_layout.addRow("صدای انتخاب‌شده:", self.voice_combo)
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(50, 200)
        self.speed_slider.setValue(100)
        voice_layout.addRow("سرعت پخش (%):", self.speed_slider)
        layout.addWidget(voice_group)
        ocr_group = QGroupBox("تنظیمات OCR")
        ocr_layout = QFormLayout(ocr_group)
        self.default_lang = QComboBox()
        self.default_lang.addItems(["fas+eng", "fas", "eng", "ara+eng"])
        ocr_layout.addRow("زبان پیش‌فرض:", self.default_lang)
        layout.addWidget(ocr_group)
        acc_group = QGroupBox("دسترسی‌پذیری")
        acc_layout = QVBoxLayout(acc_group)
        acc_info = QLabel("این برنامه با صفحه‌خوان NVDA کاملاً سازگار است.\nاز Tab برای جابجایی، Space/Enter برای فعال‌سازی استفاده کنید.")
        acc_info.setWordWrap(True)
        acc_layout.addWidget(acc_info)
        layout.addWidget(acc_group)
        ch_group = QGroupBox("کانال آکادمی همدل")
        ch_layout = QHBoxLayout(ch_group)
        ch_layout.addWidget(QLabel(CHANNEL_URL))
        join = QPushButton("عضویت")
        join.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(CHANNEL_URL)))
        ch_layout.addWidget(join)
        copy = QPushButton("کپی لینک")
        copy.clicked.connect(lambda: (QApplication.clipboard().setText(CHANNEL_URL), self.status.showMessage("لینک کپی شد", 3000)))
        ch_layout.addWidget(copy)
        layout.addWidget(ch_group)
        layout.addStretch()

    def populate_voices(self):
        self.voice_combo.clear()
        found = False
        if VOICES_DIR.exists():
            for onnx in VOICES_DIR.rglob("*.onnx"):
                self.voice_combo.addItem(onnx.stem, str(onnx))
                found = True
        if not found:
            self.voice_combo.addItem("مدل صوتی پیدا نشد - لطفاً مدل را در پوشه voices قرار دهید", "")

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+1"), self, lambda: self.tabs.setCurrentIndex(0))
        QShortcut(QKeySequence("Ctrl+2"), self, lambda: self.tabs.setCurrentIndex(1))
        QShortcut(QKeySequence("Ctrl+3"), self, lambda: self.tabs.setCurrentIndex(2))
        QShortcut(QKeySequence("Ctrl+L"), self, lambda: self.tabs.setCurrentIndex(1))
        QShortcut(QKeySequence("Esc"), self, self.cancel_operation)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #f8f9fa; }
            QTabWidget::pane { border: 1px solid #dee2e6; border-radius: 6px; background: white; }
            QTabBar::tab { padding: 10px 20px; margin-right: 2px; background: #e9ecef; border-top-left-radius: 6px; border-top-right-radius: 6px; }
            QTabBar::tab:selected { background: white; border-bottom: 3px solid #1a73e8; }
            QPushButton { padding: 8px 14px; border-radius: 5px; border: 1px solid #ced4da; background: white; }
            QPushButton:hover { background: #e9ecef; }
            QPushButton:focus { border: 2px solid #1a73e8; }
            QTextEdit, QListWidget { border: 1px solid #ced4da; border-radius: 4px; padding: 6px; }
            QComboBox, QSpinBox { padding: 6px; border-radius: 4px; border: 1px solid #ced4da; }
        """)

    def check_first_run(self):
        if not self.settings.value("first_run_shown", False, type=bool):
            dlg = FirstRunDialog(self)
            dlg.exec()
            if dlg.dont_show.isChecked():
                self.settings.setValue("first_run_shown", True)

    def open_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "انتخاب فایل PDF", "", "PDF Files (*.pdf)")
        if path:
            self.current_pdf = path
            self.file_label.setText(f"📄 {Path(path).name}")
            self.status.showMessage(f"فایل انتخاب شد: {Path(path).name}")
            self.text_edit.clear()

    def start_ocr(self):
        if not self.current_pdf:
            QMessageBox.warning(self, "هشدار", "لطفاً ابتدا یک فایل PDF انتخاب کنید.")
            return
        if not OCR_AVAILABLE:
            QMessageBox.critical(self, "خطا", "کتابخانه‌های OCR نصب نیستند.")
            return
        lang_map = {0: "fas+eng", 1: "fas", 2: "eng", 3: "ara+eng"}
        lang = lang_map.get(self.lang_combo.currentIndex(), "fas+eng")
        dpi = self.dpi_spin.value()
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.convert_btn.setEnabled(False)
        self.status.showMessage("در حال پردازش...")
        self.ocr_worker = OCRWorker(self.current_pdf, lang, dpi)
        self.ocr_worker.progress.connect(self.on_ocr_progress)
        self.ocr_worker.finished.connect(self.on_ocr_finished)
        self.ocr_worker.start()

    def on_ocr_progress(self, value, message):
        self.progress.setValue(value)
        self.status.showMessage(message)

    def on_ocr_finished(self, text, error):
        self.progress.setVisible(False)
        self.convert_btn.setEnabled(True)
        if error:
            QMessageBox.critical(self, "خطا", error)
            self.status.showMessage("خطا در پردازش")
            return
        self.current_text = text
        self.text_edit.setPlainText(text)
        self.status.showMessage(f"تبدیل موفق | {len(text)} کاراکتر")
        QMessageBox.information(self, "موفق", "تبدیل PDF به متن با موفقیت انجام شد!")

    def cancel_operation(self):
        if self.ocr_worker and self.ocr_worker.isRunning():
            self.ocr_worker.cancel()
            self.status.showMessage("در حال لغو...")

    def save_text(self, fmt="txt"):
        if not self.current_text:
            QMessageBox.warning(self, "هشدار", "متنی برای ذخیره وجود ندارد.")
            return
        filters = {"txt": "Text Files (*.txt)", "html": "HTML Files (*.html)", "md": "Markdown Files (*.md)"}
        path, _ = QFileDialog.getSaveFileName(self, "ذخیره فایل", "", filters.get(fmt, "All Files (*)"))
        if not path:
            return
        try:
            if fmt == "html":
                content = f"""<!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>خروجی OCR</title><style>body{{font-family:Tahoma,Arial;line-height:1.8;padding:20px;}}</style></head><body><pre style="white-space:pre-wrap;">{self.current_text}</pre></body></html>"""
            elif fmt == "md":
                content = f"# خروجی OCR\n\n{self.current_text}"
            else:
                content = self.current_text
            Path(path).write_text(content, encoding="utf-8")
            self.status.showMessage(f"فایل ذخیره شد: {path}")
            QMessageBox.information(self, "موفق", f"فایل با موفقیت ذخیره شد:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "خطا", str(e))

    def add_to_library(self):
        if not self.current_text:
            QMessageBox.warning(self, "هشدار", "متنی برای افزودن وجود ندارد.")
            return
        name = Path(self.current_pdf).stem if self.current_pdf else "untitled"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.txt"
        dest = LIBRARY_DIR / filename
        dest.write_text(self.current_text, encoding="utf-8")
        self.refresh_library()
        self.status.showMessage(f"به کتابخانه اضافه شد: {filename}")
        QMessageBox.information(self, "موفق", f"فایل به کتابخانه اضافه شد:\n{dest}")

    def refresh_library(self):
        self.library_list.clear()
        for f in sorted(LIBRARY_DIR.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True):
            item = QListWidgetItem(f"📄 {f.name}  ({f.stat().st_size // 1024} KB)")
            item.setData(Qt.ItemDataRole.UserRole, str(f))
            self.library_list.addItem(item)

    def open_library_item(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        if path:
            text = Path(path).read_text(encoding="utf-8")
            self.current_text = text
            self.text_edit.setPlainText(text)
            self.tabs.setCurrentIndex(0)
            self.status.showMessage(f"باز شد از کتابخانه: {Path(path).name}")

    def open_selected_library(self):
        item = self.library_list.currentItem()
        if item:
            self.open_library_item(item)

    def delete_library_item(self):
        item = self.library_list.currentItem()
        if not item:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(self, "تأیید حذف", f"آیا از حذف این فایل مطمئن هستید؟\n{Path(path).name}")
        if reply == QMessageBox.StandardButton.Yes:
            Path(path).unlink(missing_ok=True)
            self.refresh_library()

    def play_tts(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "هشدار", "متنی برای پخش وجود ندارد.")
            return
        voice_path = self.voice_combo.currentData()
        if not voice_path or not Path(voice_path).exists():
            QMessageBox.warning(self, "هشدار", "مدل صوتی پیدا نشد.\nلطفاً مدل Piper را در پوشه voices قرار دهید.")
            return
        out_path = CONFIG_DIR / "tts_output.wav"
        self.status.showMessage("در حال تولید صدا...")
        self.tts_btn.setEnabled(False)
        self.tts_worker = TTSWorker(text, voice_path, out_path)
        self.tts_worker.progress.connect(lambda m: self.status.showMessage(m))
        self.tts_worker.finished.connect(self.on_tts_finished)
        self.tts_worker.start()

    def on_tts_finished(self, result):
        self.tts_btn.setEnabled(True)
        if result.endswith(".wav") and Path(result).exists():
            self.status.showMessage("صدا تولید شد.")
            if sys.platform == "win32":
                os.startfile(result)
            else:
                import subprocess
                subprocess.Popen(["xdg-open", result])
            QMessageBox.information(self, "پخش", "فایل صوتی تولید شد و در حال پخش است.")
        else:
            QMessageBox.warning(self, "خطا", result)
            self.status.showMessage("خطا در تولید صدا")

    def show_about(self):
        AboutDialog(self).exec()

    def show_shortcuts(self):
        ShortcutsDialog(self).exec()

    def closeEvent(self, event):
        if self.ocr_worker and self.ocr_worker.isRunning():
            self.ocr_worker.cancel()
            self.ocr_worker.wait(2000)
        event.accept()


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORG_NAME)
    app.setStyle("Fusion")
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
