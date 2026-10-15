# Hamdel PDF OCR Pro 🚀

**برنامه دسکتاپ ویندوزی فوق‌العاده پیشرفته تبدیل PDF به متن با OCR کامل آفلاین**

ساخته‌شده توسط **گروه تکنولوژی همدل** - [آکادمی همدل](https://t.me/Akademi_hamdel)

## ویژگی‌ها

- ✅ OCR فوق‌العاده قوی حتی روی PDFهای اسکن‌شده و تصویری (Tesseract)
- ✅ کاملاً آفلاین
- ✅ تبدیل به TXT، HTML، Markdown
- ✅ موتور صوتی طبیعی آفلاین (Piper TTS با صدای پارسی)
- ✅ دسترسی‌پذیری کامل برای نابینایان (سازگار با NVDA + میانبرهای کامل کیبورد)
- ✅ میانبرهای کیبورد فراوان (Ctrl+O, Ctrl+E, Ctrl+P, F1 و ...)
- ✅ بخش کتابخانه برای مدیریت فایل‌های تبدیل‌شده
- ✅ رابط کاربری مدرن RTL با PyQt6
- ✅ پیام خوش‌آمدگویی طولانی در اولین اجرا با دعوت به کانال + دکمه عضویت مستقیم + گزینه «دیگر نشان نده»
- ✅ بخش درباره ما با متن طولانی و کلاس + دکمه‌های عضویت و کپی لینک

## نصب روی ویندوز

1. پایتون ۳.۱۰+ نصب کنید.
2. Tesseract OCR را از [اینجا](https://github.com/UB-Mannheim/tesseract/wiki) نصب کنید و زبان‌های `fas` و `eng` را اضافه کنید.
3. Poppler را برای pdf2image نصب کنید (و به PATH اضافه کنید).
4. سپس:

```bash
pip install -r requirements.txt
python main.py
```

## ساخت فایل .exe

```bash
pyinstaller --onefile --windowed --name "HamdelPDFOCRPro" --add-data "voices;voices" main.py
```

فایل exe در پوشه `dist` ساخته می‌شود.

برای کاهش هشدار Windows SmartScreen نیاز به گواهی Code Signing دارید (مثل گواهی‌های پولی یا self-signed با هشدار کمتر).

## مدل صوتی پارسی

مدل Piper را از Hugging Face دانلود کنید و فایل‌های `.onnx` و `.json` را در پوشه `voices` قرار دهید:

- https://huggingface.co/MahtaFetrat/Mana-Persian-Piper
- یا https://huggingface.co/rhasspy/piper-voices (جستجوی fa)

## لینک کانال

https://t.me/Akademi_hamdel

---
ساخته‌شده با ❤️ توسط گروه تکنولوژی همدل
