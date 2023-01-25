from bs4 import BeautifulSoup
# simport urllib.request
import requests
from typing import List
import pandas as pd

url_base = "https://www.equibase.com"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/" \
             "537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
headers = {'User-Agent': user_agent}


def get_track(track_id: str = "LRL", country_id: str = "USA") -> BeautifulSoup:
    """ Loads a soup of the Track overview page on Equibase """
    url = f"{url_base}/profiles/Results.cfm?type=Track&trk={track_id}&cy={country_id}"
    print(f"Loading url: {url}")
    response = requests.get(url, headers=headers)
    html = response.text
    return BeautifulSoup(html, 'html.parser')


def find_entries_links(track_soup: BeautifulSoup) -> List[str]:
    """ Finds links for the Entries pages for each upcoming race day for the given track"""
    entries_tds = track_soup.find_all("td", {"class": "entryUrl"})
    print(track_soup.prettify())
    return [url_base + td.a["href"] for td in entries_tds]


def yield_race_entry_rows(table_soup: BeautifulSoup) -> List[str]:
    rows = table_soup.find_all("tr")
    for tr in rows:
        values = [td.text.strip() for td in tr.find_all("td")]
        if values:
            yield values


def yield_race_entries(entry_link: str):
    print(f"Loading url: {entry_link}")
    response = requests.get(entry_link, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    for table_soup in soup.find_all("table", {"class": "fullwidth table-hover text-center"}):
        table_headers = [th.text for th in table_soup.find_all("th")]
        table_data = list(yield_race_entry_rows(table_soup))
        yield pd.DataFrame(table_data, columns=table_headers)


if __name__ == "__main__":
    track = "LRL"
    laurel_track_soup = get_track(track)
    entries_links = find_entries_links(laurel_track_soup)
    print(f"Found {len(entries_links)} entries links for track {track}")
    for entry_link in entries_links:
        for table in yield_race_entries(entry_link):
            print(table)
