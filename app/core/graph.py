import pandas as pd
import networkx as nx
from pyvis.network import Network
import json


class FighterGraph:
    """
    Class to handle fighter network graph creation and analysis.
    This is a placeholder for future graph visualization features.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def _filter_ufc_bouts(self, df: pd.DataFrame):
        """
        Filter the DataFrame to include only UFC bouts with clear win/loss results.
        """
        return df[(df["event"] == "UFC") & (df["decision"].isin(["W", "L"]))]

    def build_from_dataframe(self, df: pd.DataFrame):
        """
        Build a network graph from fighter bout data.
        Creates directed edges from winner to loser.
        """
        filtered_df = self._filter_ufc_bouts(df)

        for _, row in filtered_df.iterrows():
            fighter = row["fighter_name"]
            opponent = row["opponent_name"]
            decision = row["decision"]

            # Determine winner and loser based on decision
            if decision == "W":
                # Fighter won, so edge goes from fighter to opponent
                winner, loser = fighter, opponent
            elif decision == "L":
                # Fighter lost, so edge goes from opponent to fighter
                winner, loser = opponent, fighter
            else:
                # For draws or unclear decisions, skip or handle differently
                # You could add undirected edge or skip entirely
                continue

            # Add directed edge from winner to loser
            self.graph.add_edge(
                winner,
                loser,
                event=row["event"],
                decision=decision,
                method=row["method"],
            )

    def get_stats(self):
        """
        Get basic graph statistics for directed graph.
        """
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
            "is_directed": self.graph.is_directed(),
        }

    def get_fighter_stats(self, fighter_name: str):
        """
        Get win/loss statistics for a specific fighter.
        """
        if fighter_name not in self.graph:
            return None

        wins = self.graph.out_degree(fighter_name)  # Outgoing edges = wins
        losses = self.graph.in_degree(fighter_name)  # Incoming edges = losses

        return {
            "fighter": fighter_name,
            "wins": wins,
            "losses": losses,
            "total_fights": wins + losses,
            "win_rate": wins / (wins + losses) if (wins + losses) > 0 else 0,
        }

    def get_top_fighters_by_wins(self, top_n: int = 10):
        """
        Get fighters with the most wins (highest out-degree).
        """
        out_degrees = dict(self.graph.out_degree())
        sorted_fighters = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)
        return sorted_fighters[:top_n]

    def export_to_html(
        self,
        filename: str = "fighter_network.html",
        height: str = "600px",
        width: str = "100%",
        background_color: str = "#0e1117",
    ) -> str:
        """
        Export the fighter network graph to an interactive HTML file using Pyvis.

        Args:
            filename: Name of the HTML file to save
            height: Height of the visualization
            width: Width of the visualization
            background_color: Background color for the HTML document (default matches Streamlit dark theme)

        Returns:
            HTML string content of the generated file
        """
        net = Network(
            height=height,
            width=width,
            notebook=False,
            bgcolor="#222222",
            font_color="white",
            directed=True,
        )

        # Add nodes
        for node in self.graph.nodes():
            net.add_node(node, label=node)

        # Add edges with fight details
        for source, target, data in self.graph.edges(data=True):
            label = f"{data.get('decision', '')} ({data.get('method', '')})"
            net.add_edge(source, target, title=label, arrows="to")

        # Set visualization options
        options = {
            "nodes": {"font": {"size": 18, "color": "white"}},
            "edges": {
                "color": {"color": "#AAAAAA"},
                "arrows": {"to": {"enabled": True, "scaleFactor": 1.2}},
            },
            "physics": {
                "barnesHut": {
                    "gravitationalConstant": -8000,
                    "centralGravity": 0.3,
                    "springLength": 95,
                }
            },
        }
        net.set_options(f"var options = {json.dumps(options)}")

        # Save and return HTML content
        net.save_graph(filename)
        with open(filename, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Inject custom CSS to fix the white background issue
        custom_css = f"""
        <style>
        body {{
            background-color: {background_color} !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        html {{
            background-color: {background_color} !important;
        }}
        #mynetworkid {{
            background-color: #222222 !important;
        }}
        </style>
        """

        # Insert the CSS right after the <head> tag
        if "<head>" in html_content:
            html_content = html_content.replace("<head>", f"<head>{custom_css}")
        else:
            # Fallback: add it at the beginning of the HTML
            html_content = custom_css + html_content

        return html_content
