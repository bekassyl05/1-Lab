# Books Scraper

**Full name:** _Жомартұлы Бекасыл_  
**Student ID:** _051209551500_  
**Subject:** _Анализ и обработка веб данных_

## Description
This small Python project scrapes product data (books) from the demo site **books.toscrape.com**. The script visits multiple category pages, follows pagination where available, and extracts for each product:

- **Title**
- **Price**
- **Availability**
- **Rating** (mapped from CSS class to numeric value)

The output is saved as `books.csv` (and optionally `books.json`).

## Repository contents
- `scraper.py` — main scraping script (uses `requests` and `BeautifulSoup`)  
- `requirements.txt` — Python dependencies  
- `books.csv` — scraped output example  
- `report.pdf` — one-page report for submission  
- `README.md` — this file  
- `.gitignore` — recommended to ignore `venv/`, `.idea/`, `__pycache__/`

## Requirements
- Python 3.8+  
- Install dependencies:
```bash
python -m pip install -r requirements.txt
