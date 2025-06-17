import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os
import requests

# ---------- 傳入股票代碼與年度 ----------
stock_id = sys.argv[1]
roc_year = sys.argv[2]

# ---------- 設定下載資料夾 ----------
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'reports')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ---------- 瀏覽器選項 ----------
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

# ---------- 開始爬取 ----------
url = f"https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id={stock_id}&year={roc_year}&seamon=&mtype=A"
driver.get(url)
time.sleep(2)
driver.get(driver.current_url)

rows = driver.find_elements(By.XPATH, "//table//tr")
target_row = next((row for row in rows if "IFRSs合併財報" in row.text and "英文" not in row.text), None)

if not target_row:
    raise Exception("找不到 IFRSs合併財報")

a_tag = target_row.find_element(By.TAG_NAME, "a")
href = a_tag.get_attribute("href")
m = re.search(r'readfile2\("([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\)', href)
if not m:
    raise Exception("無法解析 readfile2() 參數")
kind, co_id, filename = m.groups()

driver.execute_script(f'readfile("{kind}", "{co_id}", "{filename}");')
time.sleep(2)

a_tags = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
download_link = next((a.get_attribute("href") for a in a_tags if a.text.strip() == filename), None)
if not download_link:
    raise Exception("找不到下載連結")

# ---------- 下載 PDF ----------
file_path = os.path.join(DOWNLOAD_DIR, filename)
if download_link.startswith("http"):
    response = requests.get(download_link, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        raise Exception(f"下載失敗，HTTP 狀態碼：{response.status_code}")
else:
    raise Exception("非 HTTP 下載連結")

driver.quit()
print(f"✅ 已下載 PDF：{filename}")
