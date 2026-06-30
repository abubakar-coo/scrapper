from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import re

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--lang=en")

def get_video_id(url):
    if not url:
        return None
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def get_thumbnail_url(video_id):
    if not video_id:
        return "N/A"
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

print("Opening Chrome browser...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

try:
    driver.get("https://www.youtube.com/")
    print("YouTube opened...")
    time.sleep(3)

    try:
        reject_btn = driver.find_element(By.XPATH, '//button[contains(., "Reject all")]')
        reject_btn.click()
        time.sleep(2)
    except:
        pass

    search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
    search_box.clear()
    search_box.send_keys("Trading")
    search_box.send_keys(Keys.RETURN)
    print("Searching for Trading...")
    time.sleep(4)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer")))
    time.sleep(2)

    videos = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")[:10]

    products = []

    for i, video in enumerate(videos):
        try:
            title_el = video.find_element(By.CSS_SELECTOR, "#video-title")
            title = title_el.text.strip()
            video_url = title_el.get_attribute("href")

            video_id = get_video_id(video_url)
            thumbnail = get_thumbnail_url(video_id)

            products.append({
                "video_number": i + 1,
                "title": title,
                "thumbnail": thumbnail,
                "video_url": video_url if video_url else "N/A"
            })

            print(f"  #{i+1} {title}")
            print(f"       Thumbnail: {thumbnail}")

        except Exception as e:
            print(f"  #{i+1} Error: {e}")
            continue

    with open("youtube_trading.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"\nComplete! {len(products)} videos saved in youtube_trading.json")

finally:
    time.sleep(3)
    driver.quit()
    print("Browser closed.")