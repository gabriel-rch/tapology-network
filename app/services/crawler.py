import pandas as pd
from services.tapology import scrape_fighter_page


def scrape_fighter_network(fighter_id, depth: int = 1, visited=None):
    if visited is None:
        visited = set()
    if depth <= 0 or fighter_id in visited:
        return []

    visited.add(fighter_id)
    results = scrape_fighter_page(fighter_id)
    if not results:
        return []

    network = []
    for bout in results:
        opponent_id = bout["opponent_fighter_id"]
        network.append(bout)
        # Recursively scrape the opponent's network if not already visited
        network.extend(scrape_fighter_network(opponent_id, depth - 1, visited))

    return network


network = scrape_fighter_network("129278-ilia-topuria", depth=1)

df = pd.DataFrame(network)
df = df.sort_values(by="fighter_id")
df.to_csv("fighter_network.csv", index=False)
