from bs4 import BeautifulSoup
# simport urllib.request
import requests

url_base = "https://www.equibase.com"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}


def get_track(track_id: str = "LRL", country_id: str = "USA") -> BeautifulSoup:
    """ Loads a soup of the Track overview page on Equibase """
    url = f"{url_base}/profiles/Results.cfm?type=Track&trk={track_id}&cy={country_id}"
    response = requests.get(url, headers=headers)
    html = response.text
    return BeautifulSoup(html, 'html.parser')


def find_entries_links(track_soup):
    """ Finds links for the Entries pages for each upcoming race day for the given track"""
    entries_tds = track_soup.find_all("td", {"class": "entryUrl"})
    return [url_base + td.a["href"] for td in entries_tds]


if __name__ == "__main__":
    laurel_track_soup = get_track()
    entries_links = find_entries_links(laurel_track_soup)
    print(entries_links)
