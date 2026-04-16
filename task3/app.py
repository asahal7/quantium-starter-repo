from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go

REPO = Path(__file__).parent.parent
DATA_FILE = REPO / "task2" / "formatted_output.csv"
PRICE_INCREASE_DATE = "2021-01-15"

df = pd.read_csv(DATA_FILE, parse_dates=["date"])
daily = df.groupby("date")["sales"].sum().reset_index().sort_values("date")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=daily["date"],
    y=daily["sales"],
    mode="lines",
    name="Daily Sales",
    line=dict(color="#e05c5c", width=2),
))

fig.add_shape(
    type="line",
    x0=PRICE_INCREASE_DATE, x1=PRICE_INCREASE_DATE,
    y0=0, y1=1,
    xref="x", yref="paper",
    line=dict(color="red", dash="dash", width=2),
)
fig.add_annotation(
    x=PRICE_INCREASE_DATE,
    y=0.97,
    xref="x", yref="paper",
    text="Price increase (15 Jan 2021)",
    showarrow=False,
    font=dict(color="red", size=11),
    xanchor="left",
    xshift=6,
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales ($)",
    plot_bgcolor="white",
    paper_bgcolor="white",
    hovermode="x unified",
    xaxis=dict(showgrid=True, gridcolor="#eeeeee"),
    yaxis=dict(showgrid=True, gridcolor="#eeeeee"),
    margin=dict(t=20, l=60, r=20, b=60),
)

app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1100px", "margin": "0 auto", "padding": "20px"},
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "color": "#2c2c2c"},
        ),
        html.P(
            "Daily total sales of Pink Morsel across all regions. "
            "The dashed line marks the price increase on 15 January 2021.",
            style={"textAlign": "center", "color": "#666", "marginBottom": "24px"},
        ),
        dcc.Graph(
            id="sales-chart",
            figure=fig,
            style={"height": "500px"},
        ),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)
