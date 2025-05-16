from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from threading import Thread, Lock
import time

app = Flask(__name__)

latest_data = []
last_updated = ""
trigger_rescrape = False
scrape_lock = Lock()

def do_scrape():
    global latest_data, last_updated
    print("[Scraper] Scraping now...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://bombayhighcourt.nic.in/displayboard.php")
        time.sleep(5)

        cards = driver.find_elements(By.CLASS_NAME, "card")
        data = []

        for card in cards:
            items = card.find_elements(By.CLASS_NAME, "card-item")
            if len(items) >= 4:
                data.append({
                    "CrNo": items[0].text,
                    "SrNo": items[1].text,
                    "CaseNo": items[2].text,
                    "Coram": items[3].text
                })

        latest_data = data
        last_updated = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[Scraper] Updated at {last_updated}")

    except Exception as e:
        print("[Scraper] Error:", e)

    finally:
        driver.quit()


def background_scraper():
    global trigger_rescrape
    while True:
        with scrape_lock:
            if trigger_rescrape:
                print("[Scraper] Triggered by /force-refresh")
                trigger_rescrape = False
            else:
                print("[Scraper] Auto scrape")

            do_scrape()

        time.sleep(10)


@app.route("/scrape", methods=["GET"])
def get_data():
    return jsonify({
        "status": "success",
        "last_updated": last_updated,
        "data": latest_data
    })


@app.route("/force-refresh", methods=["POST"])
def force_refresh():
    global trigger_rescrape
    trigger_rescrape = True
    return jsonify({"status": "triggered"})


if __name__ == "__main__":
    Thread(target=background_scraper, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
