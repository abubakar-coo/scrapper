from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import re

# ====== SETTINGS - apne hisaab se change karo ======
PROFILE_URL = "https://www.instagram.com/muhammadluqman427/"
NUM_POSTS = 10

# IMPORTANT: Apni Chrome user-data-dir ka path yahan daalo.
# Windows pe usually: C:\\Users\\<YourName>\\AppData\\Local\\Google\\Chrome\\User Data
# Mac pe: /Users/<YourName>/Library/Application Support/Google/Chrome
# Profile name (e.g. "Default" ya "Profile 1") bhi check karo us folder ke andar.
CHROME_USER_DATA_DIR = r"E:\projects\scrapper\insta_scraper\MyInstaProfile"
CHROME_PROFILE_NAME = "Default"
# =====================================================

options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
options.add_argument(f"--profile-directory={CHROME_PROFILE_NAME}")
options.add_argument("--disable-notifications")
options.add_argument("--lang=en")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

print("Opening Chrome with your logged-in profile...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

posts_data = []

try:
    driver.get(PROFILE_URL)
    time.sleep(5)

    # Profile ka basic info nikalo
    try:
        bio = driver.find_element(By.XPATH, "//header//section//h1").text
    except:
        bio = "N/A"

    print("Profile loaded. Collecting post links...")

    # Post links collect karo - scroll kar ke
    post_links = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(post_links) < NUM_POSTS:
        links = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/') or contains(@href, '/reel/')]")
        for link in links:
            href = link.get_attribute("href")
            if href:
                post_links.add(href)
        if len(post_links) >= NUM_POSTS:
            break
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    post_links = list(post_links)[:NUM_POSTS]
    print(f"{len(post_links)} post links found. Extracting data for each post...")

    for i, link in enumerate(post_links):
        print(f"\nPost #{i+1} -> {link}")
        driver.get(link)
        time.sleep(4)

        post_info = {
            "post_number": i + 1,
            "post_url": link,
            "caption": "N/A",
            "likes": "N/A",
            "comments_count": "N/A",
            "timestamp": "N/A",
            "media_type": "N/A",
            "thumbnail_url": "N/A",
            "hashtags": [],
            "comments_sample": []
        }

        # ---- Meta tags se reliable data nikalna (og:description mein likes/comments/caption sab hota hai) ----
        try:
            og_desc = driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute("content")
        except:
            og_desc = ""

        try:
            og_title = driver.find_element(By.XPATH, "//meta[@property='og:title']").get_attribute("content")
        except:
            og_title = ""

        try:
            og_image = driver.find_element(By.XPATH, "//meta[@property='og:image']").get_attribute("content")
            post_info["thumbnail_url"] = og_image
        except:
            pass

        # og_desc ka format usually: "123 likes, 5 comments - username on Month Day, Year: "caption text""
        if og_desc:
            likes_match = re.search(r"([\d,\.]+[KkMm]?)\s+likes", og_desc)
            comments_match = re.search(r"([\d,\.]+[KkMm]?)\s+comments", og_desc)
            caption_match = re.search(r':\s*"(.+)"\s*$', og_desc)

            if likes_match:
                post_info["likes"] = likes_match.group(1)
            if comments_match:
                post_info["comments_count"] = comments_match.group(1)
            if caption_match:
                post_info["caption"] = caption_match.group(1).strip()
            elif og_title:
                post_info["caption"] = og_title.strip()
        elif og_title:
            post_info["caption"] = og_title.strip()

        # Agar likes meta se na milein to page pe directly try karo (logged-in view mein kabhi number dikhta hai)
        if post_info["likes"] == "N/A":
            try:
                likes_el = driver.find_element(By.XPATH, "//a[contains(@href,'/liked_by/')]//span[@title]")
                post_info["likes"] = likes_el.get_attribute("title")
            except:
                try:
                    likes_el = driver.find_element(By.XPATH, "//section//span[contains(text(),'likes') or contains(text(),'others')]")
                    post_info["likes"] = likes_el.text.strip()
                except:
                    pass

        # Hashtags caption se nikalna
        if post_info["caption"] != "N/A":
            post_info["hashtags"] = re.findall(r"#\w+", post_info["caption"])

        # Timestamp
        try:
            time_el = driver.find_element(By.XPATH, "//time")
            post_info["timestamp"] = time_el.get_attribute("datetime")
        except:
            pass

        # Media type (video ya image)
        try:
            driver.find_element(By.XPATH, "//video")
            post_info["media_type"] = "video"
        except:
            post_info["media_type"] = "image"

        # ---- Extract comments (username + text) ----
        try:
            time.sleep(2)
            comment_blocks = driver.find_elements(By.XPATH, "//ul//li[.//time]")
            comments = []
            for block in comment_blocks[:15]:
                try:
                    spans = block.find_elements(By.XPATH, ".//span")
                    texts = [s.text.strip() for s in spans if s.text.strip()]
                    if texts:
                        username = texts[0]
                        comment_text = " ".join(texts[1:2]) if len(texts) > 1 else ""
                        comments.append({
                            "username": username,
                            "comment": comment_text
                        })
                except:
                    continue
            post_info["comments_sample"] = comments[:10]
            if post_info["comments_count"] == "N/A":
                post_info["comments_count"] = len(comments)
        except:
            pass

        posts_data.append(post_info)
        print(f"  Caption: {post_info['caption'][:60]}")
        print(f"  Likes: {post_info['likes']}")
        print(f"  Comments count: {post_info['comments_count']}")
        print(f"  Comments captured: {len(post_info['comments_sample'])}")
        print(f"  Hashtags: {post_info['hashtags']}")

    with open("instagram_data.json", "w", encoding="utf-8") as f:
        json.dump({"profile_url": PROFILE_URL, "posts": posts_data}, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Data for {len(posts_data)} posts saved to instagram_data.json")

finally:
    print("\nScript finished. Browser will stay open (you can close it manually).")
