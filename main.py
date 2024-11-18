import sqlite3
import csv
from playwright.sync_api import sync_playwright
import multiprocessing
import os
import time


def check_url(url, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    captcha_type = "None"

    with sync_playwright() as p:
        extra = None
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until='networkidle')
            # page.wait_for_load_state('domcontentloaded')
            page.wait_for_timeout(2000)

            final_url = page.url
            if final_url != url:
                extra = f"Redirected from {url} to {final_url}"

        except Exception as e:
            extra = f"Failed to load {url}: {str(e)}"

        try:
            content = page.content()
            enterprise_indicators = [
                'www.google.com/recaptcha/enterprise',
                'enterprise.js',
                'grecaptcha.enterprise'
            ]
            standard_indicators = [
                'www.google.com/recaptcha/api.js',
                'class="g-recaptcha"',
                'data-sitekey'
            ]

            if any(indicator in content for indicator in enterprise_indicators):
                captcha_type = "Enterprise reCAPTCHA"
            elif any(indicator in content for indicator in standard_indicators):
                captcha_type = "Standard reCAPTCHA"
        except Exception as e:
            extra = f"no content found for {url} as {e}"

        browser.close()

        cursor.execute("INSERT INTO results_mp (url, recaptcha_type, extra) VALUES (?, ?, ?)", (url, captcha_type, extra))
        conn.commit()
        conn.close()


def main():
    start_time = time.time()
    
    db_path = 'recaptcha_results.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results_mp (
            url TEXT NOT NULL,
            recaptcha_type TEXT,
            extra TEXT
        )
    ''')
    conn.close()

    with open('urls.csv', 'r') as file:
        csv_reader = csv.reader(file)
        urls = [row[0] for row in csv_reader]

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.starmap(check_url, [(url, db_path) for url in urls])
    
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()