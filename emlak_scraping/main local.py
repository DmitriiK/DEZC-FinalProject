
from emlak_scraping_modules.scrape_and_store import load_to_db
from emlak_scraping_modules.calculate_geo import calc_and_save


def refresh_primary_data(SCRAPING_DEPTH: int, REQUEST_DELAY: int):
    load_to_db(SCRAPING_DEPTH, REQUEST_DELAY, '', '')


def recalculate():
    calc_and_save()


def main_task(SCRAPING_DEPTH: int = -1, REQUEST_DELAY: int = 1):
    refresh_primary_data(SCRAPING_DEPTH, REQUEST_DELAY)
    recalculate()


if __name__ == '__main__':
    main_task(-1, 1)
