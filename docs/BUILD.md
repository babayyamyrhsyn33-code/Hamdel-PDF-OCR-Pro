# راهنمای ساخت نسخه نهایی

## برای کاربر نهایی

کافی است از صفحه Releases فایل را دانلود کنید. نیازی به نصب پایتون یا هیچ کتابخانه‌ای نیست.

## برای توسعه‌دهنده (ساخت روی ویندوز)

1. پایتون ۳.۱۲ نصب باشد.
2. Tesseract OCR و Poppler را نصب کنید (یا از باندل آماده استفاده کنید).
3. دستورات:

```
pip install -r requirements.txt
pyinstaller --noconfirm --clean --windowed --name HamdelPDFOCRPro --onedir --add-data "app;app" --add-data "voices;voices" run.py
```

4. برای ساخت فایل نصب گرافیکی از Inno Setup و فایل `installer/HamdelPDFOCRPro.iss` استفاده کنید.

## ساخت خودکار

ورک‌فلو GitHub Actions روی `windows-latest` تنظیم شده است.
از تب Actions می‌توانید workflow را دستی اجرا کنید (workflow_dispatch) یا تگ نسخه بزنید.
