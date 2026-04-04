import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Cargar datos
df = pd.read_csv("listings_clean.csv")
reviews = pd.read_csv("reviews.csv")
reviews["date"] = pd.to_datetime(reviews["date"])

# Traducir tipos de habitación
TIPOS_ES = {
    "Entire home/apt": "Casa/Depto completo",
    "Private room": "Habitación privada",
    "Shared room": "Habitación compartida",
    "Hotel room": "Habitación de hotel"
}
df["tipo_es"] = df["room_type"].map(TIPOS_ES).fillna(df["room_type"])

app = dash.Dash(__name__)

COLORS = {
    "bg": "#1a1a2e",
    "card": "#16213e",
    "accent": "#FF5A5F",
    "accent2": "#0f3460",
    "text": "#ffffff",
    "subtext": "#a0a0b0",
    "green": "#00b894"
}

def card(titulo, valor, subtitulo="", color=None):
    return html.Div([
        html.P(titulo, style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0", "textTransform": "uppercase", "letterSpacing": "1px"}),
        html.H2(valor, style={"color": color or COLORS["accent"], "margin": "8px 0 4px 0", "fontSize": "26px", "fontWeight": "bold"}),
        html.P(subtitulo, style={"color": COLORS["subtext"], "fontSize": "11px", "margin": "0"})
    ], style={
        "backgroundColor": COLORS["card"],
        "padding": "20px 25px",
        "borderRadius": "12px",
        "flex": "1",
        "margin": "8px",
        "boxShadow": "0 4px 15px rgba(0,0,0,0.4)",
        "borderLeft": f"4px solid {color or COLORS['accent']}"
    })

def seccion(titulo):
    return html.Div([
        html.H3(titulo, style={"color": COLORS["text"], "margin": "20px 10px 5px 10px",
                               "fontSize": "16px", "textTransform": "uppercase",
                               "letterSpacing": "2px", "borderBottom": f"2px solid {COLORS['accent']}",
                               "paddingBottom": "8px"})
    ])

def calcular_score(data):
    d = data.groupby("neighbourhood_cleansed").agg(
        precio=("price", "mean"),
        disponibilidad=("availability_365", "mean"),
        resenas=("number_of_reviews", "mean"),
        cantidad=("id", "count")
    ).reset_index()
    d = d[d["cantidad"] >= 20]
    for col in ["precio", "disponibilidad", "resenas"]:
        d[f"{col}_norm"] = (d[col] - d[col].min()) / (d[col].max() - d[col].min())
    d["score"] = (d["precio_norm"] * 0.4 + d["disponibilidad_norm"] * 0.3 + d["resenas_norm"] * 0.3) * 100
    return d.sort_values("score", ascending=False).head(5).reset_index(drop=True)

app.layout = html.Div(style={"backgroundColor": COLORS["bg"], "minHeight": "100vh", "padding": "25px", "fontFamily": "'Arial', sans-serif"}, children=[

    html.Div([
        html.H1("🏠 Dashboard Airbnb - Buenos Aires",
                style={"textAlign": "center", "color": COLORS["accent"], "marginBottom": "5px", "fontSize": "32px"}),
        html.P("Análisis de oportunidades de inversión en propiedades · Data actualizada 2020",
               style={"textAlign": "center", "color": COLORS["subtext"], "marginBottom": "25px", "fontSize": "14px"})
    ]),

    seccion("📊 Indicadores Clave"),
    html.Div([
        card("Total Propiedades", f"{len(df):,}", "propiedades analizadas"),
        card("Precio Promedio", f"${df['price'].mean():,.0f} ARS", "por noche", COLORS["accent"]),
        card("Precio Mediano", f"${df['price'].median():,.0f} ARS", "por noche", "#e17055"),
        card("Barrio más caro", df.groupby("neighbourhood_cleansed")["price"].mean().idxmax(), "precio promedio más alto", COLORS["green"]),
        card("Total Barrios", f"{df['neighbourhood_cleansed'].nunique()}", "barrios con propiedades", "#74b9ff"),
        card("Reseñas totales", f"{len(reviews):,}", "reseñas registradas", "#a29bfe"),
    ], style={"display": "flex", "flexWrap": "wrap", "marginBottom": "10px"}),

    seccion("🔍 Filtros"),
    html.Div([
        html.Div([
            html.Label("Tipo de habitación:", style={"color": COLORS["text"], "fontSize": "13px"}),
            dcc.Dropdown(
                id="filtro_tipo",
                options=[{"label": TIPOS_ES.get(t, t), "value": t} for t in df["room_type"].unique()],
                value=None, placeholder="Todos los tipos", multi=True,
                style={"color": "#000", "marginTop": "5px"}
            )
        ], style={"flex": "1", "margin": "10px"}),

        html.Div([
            html.Label("Barrio:", style={"color": COLORS["text"], "fontSize": "13px"}),
            dcc.Dropdown(
                id="filtro_barrio",
                options=[{"label": b, "value": b} for b in sorted(df["neighbourhood_cleansed"].unique())],
                value=None, placeholder="Todos los barrios", multi=True,
                style={"color": "#000", "marginTop": "5px"}
            )
        ], style={"flex": "1", "margin": "10px"}),

        html.Div([
            html.Label("Rango de precio por noche (ARS):", style={"color": COLORS["text"], "fontSize": "13px"}),
            dcc.RangeSlider(
                id="filtro_precio",
                min=0, max=int(df["price"].max()), step=100,
                value=[0, int(df["price"].max())],
                marks={0: {"label": "$0", "style": {"color": "#fff"}},
                       2000: {"label": "$2k", "style": {"color": "#fff"}},
                       4000: {"label": "$4k", "style": {"color": "#fff"}},
                       6000: {"label": "$6k", "style": {"color": "#fff"}}}
            )
        ], style={"flex": "2", "margin": "10px"}),

        html.Div([
            html.Button("🔄 Resetear filtros", id="btn_reset",
                       style={"backgroundColor": COLORS["accent"], "color": "#fff",
                              "border": "none", "padding": "10px 20px",
                              "borderRadius": "8px", "cursor": "pointer",
                              "fontSize": "13px", "marginTop": "20px"})
        ], style={"margin": "10px", "display": "flex", "alignItems": "flex-end"})

    ], style={"display": "flex", "flexWrap": "wrap", "backgroundColor": COLORS["card"],
              "borderRadius": "12px", "padding": "15px", "marginBottom": "20px"}),

    seccion("💰 Análisis de Precios"),
    html.Div([
        html.Div([dcc.Graph(id="grafico_barrios")],
                 style={"flex": "2", "backgroundColor": COLORS["card"], "borderRadius": "12px", "margin": "8px"}),
        html.Div([dcc.Graph(id="grafico_tipo")],
                 style={"flex": "1", "backgroundColor": COLORS["card"], "borderRadius": "12px", "margin": "8px"})
    ], style={"display": "flex"}),

    html.Div([
        html.Div([dcc.Graph(id="grafico_boxplot")],
                 style={"flex": "1", "backgroundColor": COLORS["card"], "borderRadius": "12px", "margin": "8px"}),
    ], style={"display": "flex"}),

    seccion("🗺️ Análisis Geográfico"),
    html.Div([
        html.Div([dcc.Graph(id="grafico_mapa")],
                 style={"flex": "1", "backgroundColor": COLORS["card"], "borderRadius": "12px", "margin": "8px"}),
        html.Div([dcc.Graph(id="grafico_disponibilidad")],
                 style={"flex": "1", "backgroundColor": COLORS["card"], "borderRadius": "12px", "margin": "8px"})
    ], style={"display": "flex"}),

    seccion("📈 Análisis de Demanda"),
    html.Div([
        html.Div([dcc.Graph(id="grafico_scatter")],
                 style={"flex": "1", "backgroundColor": COLORS["card"], "borderRadius": "12px", "margin": "8px"}),
        html.Div([dcc.Graph(id="grafico_resenas")],
                 style={"flex": "1", "backgroundColor": COLORS["card"], "borderRadius": "12px", "margin": "8px"})
    ], style={"display": "flex"}),

    seccion("🏆 Top 5 Barrios Recomendados para Invertir"),
    html.Div(id="tabla_inversion", style={"margin": "8px"}),

    html.Div([
        html.P("Dashboard desarrollado para el Desafío Profesional Data Analyst · Digital House · 2024",
               style={"textAlign": "center", "color": COLORS["subtext"], "fontSize": "12px", "marginTop": "30px"})
    ])
])

TEMPLATE = "plotly_dark"

@app.callback(
    Output("filtro_tipo", "value"),
    Output("filtro_barrio", "value"),
    Output("filtro_precio", "value"),
    Input("btn_reset", "n_clicks"),
    prevent_initial_call=True
)
def reset_filtros(n):
    return None, None, [0, int(df["price"].max())]

@app.callback(
    Output("grafico_barrios", "figure"),
    Output("grafico_tipo", "figure"),
    Output("grafico_mapa", "figure"),
    Output("grafico_disponibilidad", "figure"),
    Output("grafico_scatter", "figure"),
    Output("grafico_resenas", "figure"),
    Output("grafico_boxplot", "figure"),
    Output("tabla_inversion", "children"),
    Input("filtro_tipo", "value"),
    Input("filtro_barrio", "value"),
    Input("filtro_precio", "value")
)
def actualizar(tipos, barrios, rango_precio):
    dff = df.copy()
    if tipos:
        dff = dff[dff["room_type"].isin(tipos)]
    if barrios:
        dff = dff[dff["neighbourhood_cleansed"].isin(barrios)]
    dff = dff[(dff["price"] >= rango_precio[0]) & (dff["price"] <= rango_precio[1])]

    # Gráfico 1 - Barrios por precio
    bp = dff.groupby("neighbourhood_cleansed")["price"].mean().sort_values(ascending=False).head(10).reset_index()
    bp.columns = ["Barrio", "Precio promedio"]
    fig1 = px.bar(bp, x="Precio promedio", y="Barrio", orientation="h",
                  title="Top 10 barrios por precio promedio (ARS)",
                  color="Precio promedio", color_continuous_scale="Reds",
                  template=TEMPLATE)
    fig1.update_traces(hovertemplate="<b>%{y}</b><br>Precio promedio: $%{x:,.0f} ARS<extra></extra>")
    fig1.update_layout(yaxis={"categoryorder": "total ascending"},
                       plot_bgcolor=COLORS["card"], paper_bgcolor=COLORS["card"])

    # Gráfico 2 - Donut
    tc = dff["tipo_es"].value_counts().reset_index()
    tc.columns = ["Tipo", "Cantidad"]
    fig2 = px.pie(tc, names="Tipo", values="Cantidad",
                  title="Distribución por tipo de habitación", hole=0.45,
                  color_discrete_sequence=["#FF5A5F", "#FF8A8E", "#FFB3B5", "#FFD9DA"],
                  template=TEMPLATE)
    fig2.update_traces(hovertemplate="<b>%{label}</b><br>Cantidad: %{value:,}<br>Porcentaje: %{percent}<extra></extra>")
    fig2.update_layout(paper_bgcolor=COLORS["card"])

    # Gráfico 3 - Mapa
    mapa_data = dff.groupby("neighbourhood_cleansed").agg(
        precio=("price", "mean"),
        lat=("latitude", "mean"),
        lon=("longitude", "mean"),
        cantidad=("id", "count")
    ).reset_index()
    mapa_data.columns = ["Barrio", "Precio promedio", "lat", "lon", "Cantidad"]
    fig3 = px.scatter_mapbox(mapa_data, lat="lat", lon="lon",
                             color="Precio promedio", size="Cantidad",
                             hover_name="Barrio",
                             hover_data={"Precio promedio": ":,.0f", "Cantidad": True, "lat": False, "lon": False},
                             color_continuous_scale="Reds",
                             mapbox_style="carto-darkmatter",
                             zoom=10, center={"lat": -34.61, "lon": -58.44},
                             title="Mapa de precios por barrio", template=TEMPLATE)
    fig3.update_layout(paper_bgcolor=COLORS["card"], margin={"r": 0, "t": 40, "l": 0, "b": 0})

    # Gráfico 4 - Disponibilidad
    disp = dff.groupby("neighbourhood_cleansed")["availability_365"].mean().sort_values(ascending=False).head(10).reset_index()
    disp.columns = ["Barrio", "Días disponibles"]
    fig4 = px.bar(disp, x="Barrio", y="Días disponibles",
                  title="Top 10 barrios por disponibilidad anual (días)",
                  color="Días disponibles", color_continuous_scale="Blues",
                  template=TEMPLATE)
    fig4.update_traces(hovertemplate="<b>%{x}</b><br>Días disponibles: %{y:.0f}<extra></extra>")
    fig4.update_layout(plot_bgcolor=COLORS["card"], paper_bgcolor=COLORS["card"])

    # Gráfico 5 - Scatter con tendencia
    sample = dff.sample(min(1500, len(dff))).copy()
    fig5 = px.scatter(sample, x="number_of_reviews", y="price", color="tipo_es",
                      title="Precio vs Número de reseñas",
                      labels={"number_of_reviews": "Número de reseñas", "price": "Precio (ARS)", "tipo_es": "Tipo"},
                      opacity=0.5, trendline="ols", template=TEMPLATE)
    fig5.update_traces(hovertemplate="<b>%{fullData.name}</b><br>Reseñas: %{x}<br>Precio: $%{y:,.0f} ARS<extra></extra>")
    fig5.update_layout(plot_bgcolor=COLORS["card"], paper_bgcolor=COLORS["card"])

    # Gráfico 6 - Evolución reseñas
    resenas_mes = reviews.groupby(reviews["date"].dt.to_period("M")).size().reset_index()
    resenas_mes.columns = ["Mes", "Reseñas"]
    resenas_mes["Mes"] = resenas_mes["Mes"].astype(str)
    fig6 = px.line(resenas_mes, x="Mes", y="Reseñas",
                   title="Evolución de reseñas por mes (2010-2020)",
                   template=TEMPLATE, color_discrete_sequence=["#FF5A5F"])
    fig6.update_traces(hovertemplate="<b>%{x}</b><br>Reseñas: %{y:,}<extra></extra>")
    fig6.update_layout(plot_bgcolor=COLORS["card"], paper_bgcolor=COLORS["card"])

    # Gráfico 7 - Boxplot
    fig7 = go.Figure()
    colores = ["#FF5A5F", "#FF8A8E", "#FFB3B5", "#FFD9DA"]
    for i, tipo in enumerate(dff["tipo_es"].unique()):
        datos_tipo = dff[dff["tipo_es"] == tipo]["price"]
        fig7.add_trace(go.Box(
            y=datos_tipo,
            name=tipo,
            marker_color=colores[i % len(colores)]
        ))
    fig7.update_layout(
        title="Distribución de precios por tipo de habitación",
        xaxis_title="Tipo de habitación",
        yaxis_title="Precio (ARS)",
        template=TEMPLATE,
        plot_bgcolor=COLORS["card"],
        paper_bgcolor=COLORS["card"],
        showlegend=False
    )

    # Tabla top 5
    top5_actual = calcular_score(dff)
    filas = []
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    for i, row in top5_actual.iterrows():
        filas.append(html.Div([
            html.Div(f"{medals[i]} {row['neighbourhood_cleansed']}",
                     style={"flex": "2", "color": COLORS["text"], "fontWeight": "bold", "fontSize": "15px"}),
            html.Div(f"${row['precio']:,.0f} ARS",
                     style={"flex": "1", "color": COLORS["accent"], "textAlign": "center"}),
            html.Div(f"{row['disponibilidad']:.0f} días/año",
                     style={"flex": "1", "color": "#74b9ff", "textAlign": "center"}),
            html.Div(f"{row['resenas']:.1f} reseñas",
                     style={"flex": "1", "color": "#a29bfe", "textAlign": "center"}),
            html.Div(f"⭐ {row['score']:.1f}/100",
                     style={"flex": "1", "color": COLORS["green"], "textAlign": "center", "fontWeight": "bold"}),
        ], style={"display": "flex", "padding": "15px 20px",
                  "backgroundColor": COLORS["card"] if i % 2 == 0 else "#1e2d4a",
                  "borderRadius": "8px", "marginBottom": "5px"}))

    encabezado = html.Div([
        html.Div("Barrio", style={"flex": "2", "color": COLORS["subtext"], "fontSize": "12px", "textTransform": "uppercase"}),
        html.Div("Precio promedio", style={"flex": "1", "color": COLORS["subtext"], "fontSize": "12px", "textTransform": "uppercase", "textAlign": "center"}),
        html.Div("Disponibilidad", style={"flex": "1", "color": COLORS["subtext"], "fontSize": "12px", "textTransform": "uppercase", "textAlign": "center"}),
        html.Div("Reseñas", style={"flex": "1", "color": COLORS["subtext"], "fontSize": "12px", "textTransform": "uppercase", "textAlign": "center"}),
        html.Div("Score inversión", style={"flex": "1", "color": COLORS["subtext"], "fontSize": "12px", "textTransform": "uppercase", "textAlign": "center"}),
    ], style={"display": "flex", "padding": "10px 20px", "marginBottom": "5px"})

    tabla = html.Div([encabezado] + filas,
                     style={"backgroundColor": "#0d1b2a", "borderRadius": "12px", "padding": "15px",
                            "boxShadow": "0 4px 15px rgba(0,0,0,0.4)"})

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, tabla

if __name__ == "__main__":
    app.run(debug=True)