import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os

# --- Load the cleaned data ---
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_sales_data.csv")
df = pd.read_csv(data_path)

# --- Prepare and sort the data ---
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# --- Initialize Dash app ---
app = dash.Dash(__name__)
app.title = "Soul Foods Pink Morsel Sales Dashboard"

# --- Layout ---
app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f9fafc",
        "padding": "20px",
        "maxWidth": "900px",
        "margin": "auto",
        "borderRadius": "12px",
        "boxShadow": "0 4px 10px rgba(0,0,0,0.1)",
    },
    children=[
        html.H1(
            "Soul Foods Pink Morsel Sales Dashboard",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": "10px",
            },
        ),
        html.P(
            "Visualising the impact of the January 15, 2021 price increase on sales, with region-specific insights.",
            style={
                "textAlign": "center",
                "color": "#7f8c8d",
                "marginBottom": "30px",
                "fontSize": "16px",
            },
        ),

        html.Div(
            [
                html.Label("Select Region:", style={"fontWeight": "bold", "color": "#34495e"}),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All Regions", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    labelStyle={
                        "display": "inline-block",
                        "marginRight": "15px",
                        "color": "#2c3e50",
                        "cursor": "pointer",
                    },
                    inputStyle={"marginRight": "5px"},
                    style={"marginBottom": "20px"},
                ),
            ],
            style={"textAlign": "center"},
        ),

        dcc.Graph(id="sales-chart", style={"backgroundColor": "white", "borderRadius": "10px"}),
    ],
)

# --- Callback for interactive filtering ---
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df
        title = "Pink Morsel Sales Across All Regions"
    else:
        filtered_df = df[df["region"].str.lower() == selected_region.lower()]
        title = f"Pink Morsel Sales - {selected_region.title()} Region"

    fig = px.line(
        filtered_df,
        x="date",
        y="Sales",
        color="region" if selected_region == "all" else None,
        title=title,
        labels={"date": "Date", "Sales": "Total Sales ($)", "region": "Region"},
    )

    # Add vertical line for price increase
    price_increase_date = pd.to_datetime("2021-01-15")
    fig.add_vline(
        x=price_increase_date,
        line_width=2,
        line_dash="dash",
        line_color="red"
    )

    # Annotation for the price increase
    fig.add_annotation(
        x=price_increase_date,
        y=filtered_df["Sales"].max() if not filtered_df.empty else 0,
        text="Price Increase (Jan 15, 2021)",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        font=dict(color="red", size=12)
    )

    # Layout tweaks
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#ecf0f1"),
        yaxis=dict(showgrid=True, gridcolor="#ecf0f1"),
    )

    return fig


# --- Run the app ---
if __name__ == "__main__":
    app.run(debug=False)
