# reCAPTCHA Website Scraper

A Python-based web scraper that checks websites for the presence of Google reCAPTCHA (both Standard and Enterprise versions).

## Features

- Multi-process scanning of URLs
- SQLite database storage
- Detects both Enterprise and Standard reCAPTCHA implementations
- Handles URL redirects
- Performance optimized with parallel processing

## Prerequisites

- Python 3.12+
- Playwright
- SQLite3

## Installation

- Clone the repository:
```bash
git clone https://github.com/yourusername/recaptcha-webscraper.git
```

- Go into the directory
```bash
cd recaptcha-webscraper
```


- Install requirements
```bash
poetry install
```

- Install playwright
```bash
poetry run playwright install
```

## Running

Prepare your input file:

- Create a urls.csv file with one URL per line in the first column
- Run the python file with
```bash
poetry run python main.py
```
