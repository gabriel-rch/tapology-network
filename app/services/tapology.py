from core.scraper import Scraper


def search_fighter_by_name(fighter_name: str) -> str:
    """
    Search for a fighter by name and return their fighter ID.
    """
    url = f"/search?term={fighter_name}&commit=&model%5Bfighters%5D=fightersSearch"

    with Scraper() as scraper:
        soup = scraper.get(url)

    results = soup.find("div", {"class": "searchResultsFighter"})
    fighters = [
        {"name": a.text.strip(), "link": a.get("href")} for a in results.find_all("a")
    ]
    return fighters


def fetch_fighter_page(fighter_id):
    with Scraper() as scraper:
        url = f"/fightcenter/fighters/{fighter_id}"
        soup = scraper.get(url)
        return soup


def scrape_fighter_page(fighter_id):
    soup = fetch_fighter_page(fighter_id)
    bouts = soup.find("div", id="proResults")
    if not bouts:
        print(f"No professional bouts found for fighter ID {fighter_id}")
        return None

    fighter_name = soup.select_one(
        "#fighterPageHeader > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2)"
    ).text.strip()

    results = []
    professional_bouts = bouts.find_all("div", {"data-division": "pro"})
    for bout in professional_bouts:
        # The first div contains bout information
        bout_info = bout.find("div")
        sections = bout_info.find_all("div", recursive=False)

        # The second section contains the win/loss method
        method_div = sections[1].find("div")
        if not method_div:
            # Skip cancelled or upcoming bouts
            continue
        method = method_div.get_text(strip=True)
        # The first section contains Win/Loss
        decision = sections[0].get_text(strip=True)

        # The third section contains opponent information
        opponent = sections[2].find("a")
        if not opponent:
            # Skip bouts without an opponent
            continue

        opponent_name = opponent.get_text(strip=True)
        opponent_fighter_id = opponent["href"].split("/")[-1]
        # It also contains event information
        banner = sections[2].find("img")
        event = banner.get("alt", "Unknown Event") if banner else "Unknown Event"

        results.append(
            {
                "fighter_name": fighter_name,
                "opponent_name": opponent_name,
                "decision": decision,
                "method": method,
                "event": event,
                "fighter_id": fighter_id,
                "opponent_fighter_id": opponent_fighter_id,
            }
        )

    return results
