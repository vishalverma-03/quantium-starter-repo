import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import pkgutil

# --- Fix for Python 3.14 removal of find_loader ---
if not hasattr(pkgutil, "find_loader"):
    import importlib.util
    pkgutil.find_loader = importlib.util.find_spec

# --- Load the cleaned data ---
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_sales_data.csv")
df = pd.read_csv(data_path)

# --- Convert and sort dates ---
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# --- Define price increase date ---
price_increase_date = datetime(2021, 1, 15)

# --- Initialize Dash app ---
app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Dashboard"

# --- App Layout ---
app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Dashboard", style={
        "textAlign": "center",
        "color": "#2c3e50",
        "marginBottom": "10px"
    }),

    html.P(
        "Visualizing the impact of the January 15, 2021 price increase on sales performance.",
        style={"textAlign": "center", "color": "gray", "marginBottom": "30px"}
    ),

    html.Div([
        html.Label("Select Region:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            options=[{"label": region, "value": region} for region in sorted(df["region"].unique())] + [
                {"label": "All Regions", "value": "All"}
            ],
            value="All",
            id="region-dropdown",
            clearable=False,
            style={"width": "50%"}
        )
    ], style={"textAlign": "center", "marginBottom": "20px"}),

    dcc.Graph(id="sales-line-chart")
])

# --- Callbacks ---
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-dropdown", "value")
)
def update_chart(selected_region):
    if selected_region == "All":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    fig = px.line(
        filtered_df,
        x="date",
        y="Sales",
        color="region" if selected_region == "All" else None,
        title="Sales Trend Over Time" if selected_region == "All" else f"Sales Trend - {selected_region}",
        labels={"date": "Date", "Sales": "Total Sales ($)"}
    )

    # Add the vertical line
    fig.add_vline(
        x=price_increase_date,
        line_width=2,
        line_dash="dash",
        line_color="red"
    )

    # Add annotation
    fig.add_annotation(
        x=price_increase_date,
        y=filtered_df["Sales"].max(),
        text="Price Increase (Jan 15, 2021)",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        font=dict(color="red", size=12)
    )

    fig.update_layout(
        title_x=0.5,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="lightgray"),
        yaxis=dict(showgrid=True, gridcolor="lightgray")
    )

    return fig


# --- Run the server ---
if __name__ == "__main__":
    app.run(debug=False, port=8050)
