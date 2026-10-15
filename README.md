# Hamdel PDF OCR Pro

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D6)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-yellow)]()

برنامه دسکتاپ ویندوزی برای تبدیل فایل‌های PDF (حتی اسکن‌شده) به متن قابل ویرایش.

کاملاً آفلاین • سازگار با صفحه‌خوان NVDA • دو زبانه (فارسی / انگلیسی)

**توسعه‌دهنده:** گروه تکنولوژی همدل  
**کانال:** [آکادمی همدل](https://t.me/Akademi_hamdel)

---

## ویژگی‌ها

- OCR دقیق روی PDFهای متنی و اسکن‌شده
- پشتیبانی از زبان‌های پارسی، انگلیسی و عربی
- خروجی TXT / HTML / Markdown
- تبدیل متن به گفتار آفلاین (Piper)
- رابط دو زبانه
- سازگاری کامل با NVDA و کنترل کیبورد
- کتابخانه شخصی فایل‌های تبدیل‌شده
- بررسی به‌روزرسانی خودکار از GitHub
- میانبرهای کیبورد متعدد
- نصب‌کننده گرافیکی (Setup Wizard)

---

## دانلود برای کاربر نهایی

آخرین نسخه را از صفحه [Releases](https://github.com/babayyamyrhsyn33-code/Hamdel-PDF-OCR-Pro/releases) دانلود کنید.

فایل را از حالت فشرده خارج کنید و `HamdelPDFOCRPro.exe` را اجرا کنید.  
هیچ نصب اضافی لازم نیست.

اگر فایل Setup (جادوگر نصب) در ریلیز موجود باشد، آن را اجرا کنید تا میانبر دسکتاپ و منوی استارت ساخته شود.

---

## ساخت از سورس

```bash
git clone https://github.com/babayyamyrhsyn33-code/Hamdel-PDF-OCR-Pro.git
cd Hamdel-PDF-OCR-Pro
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

راهنمای کامل ساخت نسخه قابل توزیع در `docs/BUILD.md` آمده است.

ساخت خودکار روی GitHub Actions (ویندوز) تنظیم شده است. با زدن تگ نسخه (`v1.3.0`) بیلد اجرا می‌شود.

---

## ساختار پروژه

```
├── app/                    # کد اصلی
│   ├── main.py
│   ├── i18n.py
│   └── updater.py
├── installer/              # اسکریپت Inno Setup
├── .github/workflows/      # ساخت خودکار
├── assets/
├── voices/
├── docs/
├── LICENSE
├── CHANGELOG.md
└── README.md
```

---

## مشارکت و پشتیبانی

Issue و Pull Request خوش‌آمد است.  
پشتیبانی و اخبار: [آکادمی همدل](https://t.me/Akademi_hamdel)

---

## مجوز

MIT License – جزئیات در فایل LICENSE.
