import requests
import csv
import math
from bs4 import BeautifulSoup
import time

# Functions

# Fetch LOC JSON search results (newspapers only)
def fetch_newspaper_json(query, page=1):
    url = f"https://www.loc.gov/search/?fo=json&q={query}&fa=original-format:newspaper&sp={page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Scrape OCR text from main item page
def fetch_ocr_text(item_url):
    if not item_url:
        return None
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(item_url, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        ocr_div = soup.find("div", class_="ocr_text")
        if ocr_div:
            return ocr_div.get_text(separator="\n").strip()
        return None
    except Exception as e:
        print(f"Failed to fetch OCR text from {item_url}: {e}")
        return None

# Parse newspaper item
def parse_newspaper_item(item):
    image_url = item.get("image_url", [])
    ocr_text = fetch_ocr_text(item.get("url"))
    return {
        "id": item.get("id") or item.get("control_number"),
        "title": item.get("title"),
        "date": item.get("date"),
        "collection": ", ".join(item.get("source_collection", [])) if item.get("source_collection") else None,
        "location": ", ".join(item.get("location", [])) if item.get("location") else None,
        "subjects": ", ".join(item.get("subjects", [])) if item.get("subjects") else None,
        "url": item.get("url"),
        "image_url": image_url[0] if image_url else None,
        "ocr_text": ocr_text,
        "rights": item.get("rights_information"),
        "notes": item.get("notes")
    }

query = "ball society"
results_limit = 15
results_per_page = 25
pages_needed = math.ceil(results_limit / results_per_page)

csv_file = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_1/output/loc_ball_society_newspapers_with_image_text.csv"
fieldnames = ["id", "title", "date", "collection", "location", "subjects",
              "url", "image_url", "ocr_text", "rights", "notes"]

# Fetch items and save CSV


with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    count = 0
    for page in range(1, pages_needed + 1):
        print(f"Fetching page {page}...")
        json_data = fetch_newspaper_json(query, page)
        items = json_data.get("results", [])

        for i, item in enumerate(items, start=1):
            if count >= results_limit:
                break
            parsed_item = parse_newspaper_item(item)
            writer.writerow(parsed_item)
            count += 1
            print(f"  [{count}] Saved item: {parsed_item['title']}")
            time.sleep(0.5)  # polite delay to avoid hammering LOC servers

        if count >= results_limit:
            break

print(f"CSV saved as {csv_file} with {count} items")
