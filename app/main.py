import streamlit as st
import pandas as pd
from services.tapology import search_fighter_by_name
from services.crawler import scrape_fighter_network
from core.graph import FighterGraph
import streamlit.components.v1 as components

# --- Sidebar ---
st.sidebar.title("About")
st.sidebar.markdown(
    """
    **Tapology Fighter Network Crawler**  
    This tool lets you search for MMA fighters, view their fight history, and explore their network of opponents using data from Tapology.  
    - Search for a fighter by name  
    - Select a fighter to view their fight network  
    - Download the raw fight data as CSV  
    """
)

st.set_page_config(page_title="Tapology Fighter Network Crawler", layout="wide")

st.title("🥊 Tapology Fighter Network Crawler")
st.markdown("Search for MMA fighters and explore their fight networks")

# Initialize session state
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "selected_fighter" not in st.session_state:
    st.session_state.selected_fighter = None
if "network_data" not in st.session_state:
    st.session_state.network_data = None

# Search section
st.header("🔍 Search Fighter")
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input("Enter fighter name:", placeholder="e.g., Ilia Topuria")

with col2:
    st.write("")  # Empty space for alignment
    search_button = st.button("Search", type="primary")

if search_button and search_query:
    with st.spinner("Searching for fighters..."):
        try:
            results = search_fighter_by_name(search_query)
            st.session_state.search_results = results
            st.session_state.selected_fighter = None
            st.session_state.network_data = None
        except Exception as e:
            st.error(f"Error searching for fighters: {str(e)}")

# Display search results
if st.session_state.search_results:
    st.header("📋 Search Results")

    for i, fighter in enumerate(st.session_state.search_results):
        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"**{fighter['name']}**")
            st.write(f"Profile: {fighter['link']}")

        with col2:
            fighter_id = fighter["link"].split("/")[-1]
            if st.button("Select", key=f"select_{i}"):
                st.session_state.selected_fighter = {"name": fighter["name"], "id": fighter_id}
                st.session_state.network_data = None

# Fighter network section
if st.session_state.selected_fighter:
    st.header(f"🕸️ Fighter Network: {st.session_state.selected_fighter['name']}")

    col1, col2 = st.columns([2, 1])

    with col1:
        depth = st.slider("Network Depth", min_value=1, max_value=3, value=1)

    with col2:
        st.write("")  # Empty space for alignment
        generate_button = st.button("Generate Network", type="primary")

    if generate_button:
        with st.spinner("Generating fighter network... This may take a while."):
            try:
                fighter_id = st.session_state.selected_fighter["id"]
                network_data = scrape_fighter_network(fighter_id, depth=depth)
                st.session_state.network_data = network_data
            except Exception as e:
                st.error(f"Error generating network: {str(e)}")

    # Display network graph with Pyvis
    if st.session_state.network_data:
        df = pd.DataFrame(st.session_state.network_data)
        if not df.empty:
            fg = FighterGraph()
            fg.build_from_dataframe(df)
            G = fg.graph

            # Display network statistics
            st.subheader("📊 Network Statistics")
            stats = fg.get_stats()
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Fighters", stats["nodes"])
            with col2:
                st.metric("Fights", stats["edges"])
            with col3:
                st.metric("Density", f"{stats['density']:.3f}")
            with col4:
                st.metric("Graph Type", "Directed" if stats["is_directed"] else "Undirected")

            # Display top fighters by wins
            if G.number_of_nodes() > 0:
                st.subheader("🏆 Top Fighters by Wins")
                top_fighters = fg.get_top_fighters_by_wins(top_n=5)
                for i, (fighter, wins) in enumerate(top_fighters, 1):
                    fighter_stats = fg.get_fighter_stats(fighter)
                    st.write(
                        f"{i}. **{fighter}** - {wins} wins, {fighter_stats['losses']} losses (Win rate: {fighter_stats['win_rate']:.1%})"
                    )

            st.subheader("🕸️ Interactive Network Graph")
            st.info(
                "🔍 **How to read the graph:** Arrows point from winner to loser. Hover over edges to see fight details."
            )

            # Generate and display the interactive network graph
            html_content = fg.export_to_html("fighter_network.html")
            components.html(html_content, height=650, scrolling=True)

            # Download section
            st.subheader("💾 Download Data")
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Download Fight Data as CSV",
                data=csv_data,
                file_name=f"{st.session_state.selected_fighter['name'].replace(' ', '_')}_network.csv",
                mime="text/csv",
            )
        else:
            st.info("No fight data found for this fighter.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Tapology data")
