import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px


df = pd.read_csv("data/output.csv")

df["date"] = pd.to_datetime(df["date"])

app = Dash(__name__)

app.layout = html.Div(

    className="container",

    children=[

        html.H1(
            "Soul Foods Pink Morsel Sales Visualiser",
            className="title"
        ),

        html.Div([

            html.Label("Select Region"),

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
                inline=True
            )

        ], className="radio-container"),

        dcc.Graph(id="sales-chart")

    ]
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):

    if selected_region == "all":
        filtered = df
    else:
        filtered = df[df["region"].str.lower() == selected_region]

    daily_sales = (
        filtered.groupby("date")["sales"]
        .sum()
        .reset_index()
        .sort_values("date")
    )

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time",
        labels={
            "date": "Date",
            "sales": "Sales"
        }
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)