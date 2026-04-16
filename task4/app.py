from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html, callback, Output, Input
import plotly.graph_objects as go

REPO = Path(__file__).parent.parent
DATA_FILE = REPO / "task2" / "formatted_output.csv"
PRICE_INCREASE_DATE = "2021-01-15"

df = pd.read_csv(DATA_FILE, parse_dates=["date"])

app = Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "'Segoe UI', Arial, sans-serif",
        "background": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
        "minHeight": "100vh",
        "padding": "40px 20px",
    },
    children=[
        # Card container
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "background": "rgba(255,255,255,0.05)",
                "borderRadius": "16px",
                "padding": "36px 40px",
                "boxShadow": "0 8px 32px rgba(0,0,0,0.4)",
                "backdropFilter": "blur(10px)",
                "border": "1px solid rgba(255,255,255,0.1)",
            },
            children=[
                # Header
                html.H1(
                    "Pink Morsel Sales Visualiser",
                    style={
                        "textAlign": "center",
                        "color": "#f9a8d4",
                        "fontSize": "2.2rem",
                        "marginBottom": "6px",
                        "letterSpacing": "1px",
                    },
                ),
                html.P(
                    "Daily Pink Morsel sales across all regions — did the January 2021 price increase affect demand?",
                    style={
                        "textAlign": "center",
                        "color": "#94a3b8",
                        "marginBottom": "28px",
                        "fontSize": "0.95rem",
                    },
                ),

                # Radio buttons
                html.Div(
                    style={"display": "flex", "justifyContent": "center", "marginBottom": "24px"},
                    children=[
                        html.Div(
                            style={
                                "background": "rgba(255,255,255,0.07)",
                                "borderRadius": "50px",
                                "padding": "6px 10px",
                                "display": "inline-flex",
                                "alignItems": "center",
                                "gap": "4px",
                            },
                            children=[
                                html.Span(
                                    "Region:",
                                    style={"color": "#94a3b8", "fontSize": "0.85rem", "marginRight": "8px", "paddingLeft": "6px"},
                                ),
                                dcc.RadioItems(
                                    id="region-filter",
                                    options=[
                                        {"label": "All", "value": "all"},
                                        {"label": "North", "value": "north"},
                                        {"label": "East", "value": "east"},
                                        {"label": "South", "value": "south"},
                                        {"label": "West", "value": "west"},
                                    ],
                                    value="all",
                                    inline=True,
                                    inputStyle={"display": "none"},
                                    labelStyle={
                                        "cursor": "pointer",
                                        "padding": "6px 18px",
                                        "borderRadius": "50px",
                                        "color": "#cbd5e1",
                                        "fontSize": "0.88rem",
                                        "fontWeight": "500",
                                        "transition": "all 0.2s",
                                    },
                                    style={"display": "flex", "gap": "4px"},
                                ),
                            ],
                        )
                    ],
                ),

                # Chart
                dcc.Graph(
                    id="sales-chart",
                    style={"height": "480px"},
                    config={"displayModeBar": False},
                ),
            ],
        )
    ],
)


@callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
def update_chart(region):
    filtered = df if region == "all" else df[df["region"] == region]
    daily = filtered.groupby("date")["sales"].sum().reset_index().sort_values("date")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["date"],
        y=daily["sales"],
        mode="lines",
        name="Sales",
        line=dict(color="#f9a8d4", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(249,168,212,0.08)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>",
    ))

    fig.add_shape(
        type="line",
        x0=PRICE_INCREASE_DATE, x1=PRICE_INCREASE_DATE,
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(color="#fb7185", dash="dash", width=1.8),
    )
    fig.add_annotation(
        x=PRICE_INCREASE_DATE,
        y=0.97,
        xref="x", yref="paper",
        text="▲ Price increase",
        showarrow=False,
        font=dict(color="#fb7185", size=11),
        xanchor="left",
        xshift=8,
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        hovermode="x unified",
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            linecolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="#64748b"),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            linecolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="#64748b"),
            tickprefix="$",
        ),
        margin=dict(t=10, l=60, r=20, b=50),
        legend=dict(font=dict(color="#94a3b8")),
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
