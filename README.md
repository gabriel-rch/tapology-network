# From Tapology to Topology: Mapping MMA's Fighter Network

> How data scraped from Tapology — one of the largest online MMA databases — can be used to build and visualize a fighter network graph. By turning fight records into network data, we can explore patterns that reveal unexpected connections, influential fighters, and the structure of the MMA world as a living, breathing ecosystem.

## 🥊 Overview

**Tapology Network** is a data science project that scrapes fighter data from [Tapology.com](https://www.tapology.com/) to build and analyze MMA fighter networks. The project models the MMA world as a graph where fighters are nodes and fights are edges, enabling quantitative analysis of connectivity, centrality, and community structure in the fighter ecosystem.

### What is Tapology?

**Tapology** (_"Tap" — the act of submitting, surrender + "-ology" — from the Greek -λογία (-logia), "the study of"_) is one of the largest online repositories of fighter profiles, fight histories, and event details on the web, serving as an unofficial encyclopedia of the MMA world.

## 🚀 Features

- **Web Scraping**: Intelligent scraping of Tapology fighter profiles with rotation of User-Agent headers
- **Network Building**: Depth-limited recursive crawling to build connected fighter networks
- **Interactive UI**: Streamlit-based web interface for searching fighters and exploring networks
- **Graph Analysis**: NetworkX-powered graph analysis and statistics
- **Data Export**: Export network data for further analysis

## 📊 Project Structure

```
tapology-network/
├── article.ipynb          # Research article and methodology
├── README.md             # This file
├── requirements.txt      # Python dependencies
└── app/
    ├── main.py          # Streamlit web application
    ├── core/
    │   ├── graph.py     # Network graph creation and analysis
    │   └── scraper.py   # Core scraping functionality
    └── services/
        ├── crawler.py   # Fighter network crawling service
        └── tapology.py  # Tapology API interactions
```

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd tapology-network
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Running the Web Application

Launch the Streamlit interface to interactively explore fighter networks:

```bash
streamlit run app/main.py
```

This will open a web interface where you can:

- Search for MMA fighters by name
- Select fighters to explore their networks
- Visualize fight connections and relationships
- Export network data for analysis

### Using the Jupyter Notebook

Explore the research methodology and analysis:

```bash
jupyter notebook article.ipynb
```

### Programmatic Usage

```python
from app.services.crawler import scrape_fighter_network
from app.core.graph import FighterGraph

# Scrape a fighter network (depth=5 means 5 levels of connections)
network_data = scrape_fighter_network("charles-oliveira-do-bronx", depth=5)

# Build a graph from the scraped data
import pandas as pd
df = pd.DataFrame(network_data)
graph = FighterGraph()
graph.build_from_dataframe(df)

# Get network statistics
stats = graph.get_stats()
print(stats)
```

## 🧮 Methodology

### Data Collection

The project uses a **depth-limited Depth-First Search (DFS)** approach to recursively scrape fight data:

1. **Starting Point**: Begin with a chosen fighter (e.g., Charles Oliveira "Do Bronx")
2. **Recursive Exploration**: Extract fight history and explore opponents' profiles
3. **Depth Control**: Continue up to a specified recursion depth (typically 5 levels)
4. **Loop Prevention**: Use visited sets to prevent infinite loops and excessive requests

### Data Structure

For each fight, the following information is captured:

- Fighter names and IDs
- Fight outcome (win/loss)
- Method of victory/defeat (KO, submission, decision, etc.)
- Event information
- Opponent details

### Network Analysis

The scraped data is modeled as an undirected graph where:

- **Nodes**: Individual MMA fighters
- **Edges**: Fights between fighters
- **Edge Attributes**: Fight outcomes, methods, events

## 📦 Dependencies

- **beautifulsoup4**: HTML parsing for web scraping
- **httpx**: Async HTTP client for web requests
- **tenacity**: Retry logic for robust scraping
- **fake-useragent**: User-Agent rotation to avoid blocking
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **networkx**: Graph creation and analysis

## ⚠️ Important Notes

### Ethical Scraping

- The project respects Tapology's robots.txt and implements reasonable delays
- User-Agent rotation is used to mimic normal browser behavior
- Rate limiting prevents overwhelming the server

### Limitations

- **Depth Limit**: Due to computational constraints, network depth is limited to 5 levels
- **Data Coverage**: Only publicly available data from Tapology is used
- **Real-time Data**: Data is scraped at the time of execution and may not reflect recent fights

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is intended for educational and research purposes. Please respect Tapology's terms of service when using this tool.

## 🎖️ Acknowledgments

- **Tapology.com** for providing comprehensive MMA data
- **Charles Oliveira ("Do Bronx")** for being the inspiration and starting point for this network analysis
- The MMA community for creating such a rich, interconnected ecosystem worth studying

---

_CHAMA 🔥_
