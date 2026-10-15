# بررسی به‌روزرسانی از GitHub Releases
# گروه تکنولوژی همدل

import json
import urllib.request

REPO = "babayyamyrhsyn33-code/Hamdel-PDF-OCR-Pro"
CURRENT_VERSION = "1.3.0"

def check_for_update(timeout=8):
    """
    بررسی وجود نسخه جدیدتر در GitHub Releases.
    برمی‌گرداند: (has_update: bool, latest_version: str, download_url: str, notes: str)
    """
    try:
        from packaging import version
        url = f"https://api.github.com/repos/{REPO}/releases/latest"
        req = urllib.request.Request(url, headers={"User-Agent": "HamdelPDFOCRPro"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        latest = data.get("tag_name", "").lstrip("v")
        if not latest:
            return False, CURRENT_VERSION, "", ""
        has_update = version.parse(latest) > version.parse(CURRENT_VERSION)
        assets = data.get("assets", [])
        download_url = ""
        for asset in assets:
            name = asset.get("name", "")
            if name.endswith(".zip") or name.endswith(".exe"):
                download_url = asset.get("browser_download_url", "")
                break
        notes = data.get("body", "") or ""
        return has_update, latest, download_url, notes
    except Exception:
        return False, CURRENT_VERSION, "", ""
