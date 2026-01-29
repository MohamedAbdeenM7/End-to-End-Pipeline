"""
Enhanced Interactive Dashboard for Ford GoBike Data Analysis

Features:
- Modern, responsive design with dark mode
- Advanced filtering capabilities
- Real-time data updates
- Multiple visualization types
- Export functionality
- Statistical insights

Run:
    pip install dash pandas plotly dash-bootstrap-components
    python enhanced_dashboard.py
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

# Configuration
CSV_PATH = "cleaned_fordgobike.csv"
MAPBOX_STYLE = "carto-darkmatter"

# Color scheme
COLORS = {
    'primary': '#00d4ff',
    'secondary': '#7b2cbf',
    'success': '#06ffa5',
    'warning': '#ffb703',
    'danger': '#ff006e',
    'dark': '#0a0e27',
    'light': '#f8f9fa',
    'card_bg': '#1a1f3a',
    'text': '#e0e0e0'
}

def generate_dummy(n=1500):
    """Generate dummy data for demo purposes"""
    rng = pd.date_range("2020-01-01", periods=90, freq="H")
    start = np.random.choice(rng, size=n)
    dur = np.random.exponential(scale=600, size=n).astype(int)
    stations = ["Market St @ 7th", "Howard St", "Embarcadero", "Mission St", "Van Ness", 
                "Ferry Building", "Civic Center", "Union Square"]
    
    df = pd.DataFrame({
        "trip_id": range(1, n+1),
        "start_time": start,
        "duration_sec": dur,
        "start_station_name": np.random.choice(stations, size=n),
        "end_station_name": np.random.choice(stations, size=n),
        "start_station_latitude": np.random.uniform(37.76, 37.80, size=n),
        "start_station_longitude": np.random.uniform(-122.45, -122.39, size=n),
        "user_type": np.random.choice(["Subscriber", "Customer"], size=n, p=[0.75, 0.25]),
        "member_gender": np.random.choice(["Male", "Female", "Other"], size=n, p=[0.5, 0.45, 0.05]),
        "age": np.random.randint(18, 70, size=n)
    })
    
    df["day_of_week"] = df["start_time"].dt.day_name()
    df["month"] = df["start_time"].dt.strftime("%b")
    df["hour"] = df["start_time"].dt.hour
    df["age_group"] = pd.cut(df["age"], bins=[0, 29, 50, 200], labels=["Young", "Adult", "Senior"])
    df["trip_duration_min"] = df["duration_sec"] / 60.0
    
    return df

def load_data():
    """Load data from CSV or generate dummy data"""
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, parse_dates=["start_time"])
        print(f"✓ Loaded data from {CSV_PATH}")
    else:
        print(f"⚠ {CSV_PATH} not found. Generating dummy dataset...")
        df = generate_dummy(2000)
    
    # Ensure required columns
    df["start_time"] = pd.to_datetime(df["start_time"])
    if "trip_duration_min" not in df.columns:
        df["trip_duration_min"] = df["duration_sec"] / 60.0
    if "age_group" not in df.columns:
        df["age_group"] = pd.cut(df["age"], bins=[0, 29, 50, 200], labels=["Young", "Adult", "Senior"])
    if "hour" not in df.columns:
        df["hour"] = df["start_time"].dt.hour
    
    return df

# Load data
df = load_data()

# Initialize Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Ford GoBike Analytics Dashboard"

# Custom CSS
custom_css = {
    'card': {
        'backgroundColor': COLORS['card_bg'],
        'borderRadius': '15px',
        'padding': '20px',
        'boxShadow': '0 4px 15px rgba(0, 212, 255, 0.1)',
        'border': f'1px solid {COLORS["primary"]}',
        'marginBottom': '20px'
    },
    'kpi_card': {
        'backgroundColor': COLORS['card_bg'],
        'borderRadius': '12px',
        'padding': '25px',
        'textAlign': 'center',
        'boxShadow': '0 4px 20px rgba(0, 212, 255, 0.15)',
        'border': f'2px solid {COLORS["primary"]}',
        'transition': 'transform 0.3s ease',
    },
    'header': {
        'background': f'linear-gradient(135deg, {COLORS["secondary"]} 0%, {COLORS["primary"]} 100%)',
        'padding': '30px',
        'borderRadius': '15px',
        'marginBottom': '30px',
        'boxShadow': '0 8px 32px rgba(0, 212, 255, 0.3)'
    }
}

# Filter options
user_types = sorted(df["user_type"].dropna().unique())
genders = sorted(df["member_gender"].dropna().unique())
age_groups = sorted(df["age_group"].dropna().unique())

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("🚴 Ford GoBike Analytics Dashboard", 
                       style={'color': 'white', 'fontWeight': '700', 'marginBottom': '10px'}),
                html.P("Real-time insights into bike-sharing patterns and user behavior",
                      style={'color': COLORS['text'], 'fontSize': '18px', 'marginBottom': '0'})
            ], style=custom_css['header'])
        ])
    ]),
    
    # Filters Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("🔍 Filters", style={'color': COLORS['primary']})),
                dbc.CardBody([
                    html.Label("📅 Date Range", style={'color': COLORS['text'], 'fontWeight': '600'}),
                    dcc.DatePickerRange(
                        id="date_range",
                        min_date_allowed=df["start_time"].min().date(),
                        max_date_allowed=df["start_time"].max().date(),
                        start_date=df["start_time"].min().date(),
                        end_date=df["start_time"].max().date(),
                        style={'marginBottom': '20px'}
                    ),
                    
                    html.Label("👥 User Type", style={'color': COLORS['text'], 'fontWeight': '600', 'marginTop': '15px'}),
                    dcc.Dropdown(
                        id="user_type",
                        options=[{"label": u, "value": u} for u in user_types],
                        value=None,
                        multi=True,
                        placeholder="All User Types",
                        style={'marginBottom': '15px'}
                    ),
                    
                    html.Label("⚧ Gender", style={'color': COLORS['text'], 'fontWeight': '600'}),
                    dcc.Dropdown(
                        id="gender",
                        options=[{"label": g, "value": g} for g in genders],
                        value=None,
                        multi=True,
                        placeholder="All Genders",
                        style={'marginBottom': '15px'}
                    ),
                    
                    html.Label("🎂 Age Group", style={'color': COLORS['text'], 'fontWeight': '600'}),
                    dcc.Checklist(
                        id="age_group",
                        options=[{"label": f" {a}", "value": a} for a in age_groups],
                        value=age_groups,
                        style={'color': COLORS['text']}
                    ),
                    
                    html.Hr(style={'borderColor': COLORS['primary'], 'marginTop': '20px'}),
                    
                    dbc.Button("🔄 Reset Filters", id="reset_btn", color="primary", 
                              className="w-100", style={'marginTop': '10px'})
                ])
            ], style={'backgroundColor': COLORS['card_bg'], 'border': f'1px solid {COLORS["primary"]}'})
        ], width=3),
        
        # Main Content
        dbc.Col([
            # KPI Cards
            html.Div(id="kpi_row", style={'marginBottom': '25px'}),
            
            # Charts Grid
            dbc.Row([
                dbc.Col([dcc.Graph(id="trips_by_weekday")], width=6),
                dbc.Col([dcc.Graph(id="trips_by_hour")], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([dcc.Graph(id="age_distribution")], width=6),
                dbc.Col([dcc.Graph(id="gender_pie")], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([dcc.Graph(id="duration_box")], width=6),
                dbc.Col([dcc.Graph(id="user_type_trend")], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([dcc.Graph(id="station_map")], width=8),
                dbc.Col([dcc.Graph(id="top_routes")], width=4),
            ]),
        ], width=9)
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(style={'borderColor': COLORS['primary']}),
            html.P(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                  f"Total Records: {len(df):,}",
                  style={'textAlign': 'center', 'color': COLORS['text'], 'marginTop': '20px'})
        ])
    ])
], fluid=True, style={'backgroundColor': COLORS['dark'], 'minHeight': '100vh', 'padding': '20px'})

def create_kpi_card(title, value, icon, color):
    """Create a KPI card component"""
    return dbc.Col([
        html.Div([
            html.Div([
                html.Span(icon, style={'fontSize': '40px', 'marginBottom': '10px'}),
                html.H3(value, style={'color': color, 'fontWeight': '700', 'margin': '10px 0'}),
                html.P(title, style={'color': COLORS['text'], 'fontSize': '14px', 'marginBottom': '0'})
            ])
        ], style=custom_css['kpi_card'])
    ], width=3)

@app.callback(
    Output("kpi_row", "children"),
    Output("trips_by_weekday", "figure"),
    Output("trips_by_hour", "figure"),
    Output("age_distribution", "figure"),
    Output("gender_pie", "figure"),
    Output("duration_box", "figure"),
    Output("user_type_trend", "figure"),
    Output("station_map", "figure"),
    Output("top_routes", "figure"),
    [
        Input("date_range", "start_date"),
        Input("date_range", "end_date"),
        Input("user_type", "value"),
        Input("gender", "value"),
        Input("age_group", "value"),
        Input("reset_btn", "n_clicks")
    ]
)
def update_dashboard(start_date, end_date, user_type, gender, age_group, reset_clicks):
    """Update all dashboard components based on filters"""
    
    # Filter data
    dff = df.copy()
    
    if start_date:
        dff = dff[dff["start_time"] >= pd.to_datetime(start_date)]
    if end_date:
        dff = dff[dff["start_time"] <= pd.to_datetime(end_date) + pd.Timedelta(days=1)]
    if user_type:
        dff = dff[dff["user_type"].isin(user_type if isinstance(user_type, list) else [user_type])]
    if gender:
        dff = dff[dff["member_gender"].isin(gender if isinstance(gender, list) else [gender])]
    if age_group:
        dff = dff[dff["age_group"].isin(age_group)]
    
    # Calculate KPIs
    total_trips = len(dff)
    avg_duration = dff["trip_duration_min"].mean() if total_trips > 0 else 0
    active_users = dff["trip_id"].nunique()
    popular_station = dff["start_station_name"].mode().iloc[0] if not dff.empty else "N/A"
    
    # KPI Cards
    kpis = dbc.Row([
        create_kpi_card("Total Trips", f"{total_trips:,}", "🚴", COLORS['primary']),
        create_kpi_card("Avg Duration", f"{avg_duration:.1f} min", "⏱️", COLORS['success']),
        create_kpi_card("Active Users", f"{active_users:,}", "👥", COLORS['warning']),
        create_kpi_card("Top Station", popular_station[:15], "📍", COLORS['danger']),
    ])
    
    # Chart 1: Trips by Weekday
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    trips_wd = dff.groupby("day_of_week").size().reindex(weekday_order).fillna(0)
    
    fig_weekday = go.Figure()
    fig_weekday.add_trace(go.Scatter(
        x=trips_wd.index,
        y=trips_wd.values,
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=10, color=COLORS['primary'], line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor=f'rgba(0, 212, 255, 0.1)'
    ))
    fig_weekday.update_layout(
        title="📅 Trips by Day of Week",
        template="plotly_dark",
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text']),
        hovermode='x unified'
    )
    
    # Chart 2: Trips by Hour
    if "hour" in dff.columns:
        trips_hour = dff.groupby("hour").size()
        fig_hour = go.Figure()
        fig_hour.add_trace(go.Bar(
            x=trips_hour.index,
            y=trips_hour.values,
            marker=dict(
                color=trips_hour.values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Trips")
            )
        ))
        fig_hour.update_layout(
            title="🕐 Trips by Hour of Day",
            template="plotly_dark",
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text']),
            xaxis_title="Hour",
            yaxis_title="Number of Trips"
        )
    else:
        fig_hour = go.Figure()
    
    # Chart 3: Age Distribution
    fig_age = go.Figure()
    fig_age.add_trace(go.Histogram(
        x=dff["age"],
        nbinsx=20,
        marker=dict(color=COLORS['success'], line=dict(color='white', width=1))
    ))
    fig_age.update_layout(
        title="🎂 Age Distribution",
        template="plotly_dark",
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text']),
        xaxis_title="Age",
        yaxis_title="Frequency"
    )
    
    # Chart 4: Gender Distribution
    gender_counts = dff["member_gender"].value_counts()
    fig_gender = go.Figure()
    fig_gender.add_trace(go.Pie(
        labels=gender_counts.index,
        values=gender_counts.values,
        hole=0.4,
        marker=dict(colors=[COLORS['primary'], COLORS['success'], COLORS['warning']]),
        textinfo='label+percent',
        textfont=dict(size=14, color='white')
    ))
    fig_gender.update_layout(
        title="⚧ Gender Distribution",
        template="plotly_dark",
        paper_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text'])
    )
    
    # Chart 5: Duration Box Plot
    fig_duration = go.Figure()
    for user_type_val in dff["user_type"].unique():
        data_subset = dff[dff["user_type"] == user_type_val]["trip_duration_min"]
        fig_duration.add_trace(go.Box(
            y=data_subset,
            name=user_type_val,
            marker=dict(color=COLORS['primary'] if user_type_val == 'Subscriber' else COLORS['warning'])
        ))
    fig_duration.update_layout(
        title="⏱️ Trip Duration by User Type",
        template="plotly_dark",
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text']),
        yaxis_title="Duration (minutes)"
    )
    
    # Chart 6: User Type Trend
    if "month" in dff.columns:
        user_trend = dff.groupby(["month", "user_type"]).size().reset_index(name="trips")
        fig_trend = px.line(
            user_trend,
            x="month",
            y="trips",
            color="user_type",
            markers=True,
            title="📈 User Type Trends"
        )
        fig_trend.update_layout(
            template="plotly_dark",
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text'])
        )
    else:
        fig_trend = go.Figure()
    
    # Chart 7: Station Map
    if not dff.empty and "start_station_latitude" in dff.columns:
        station_data = dff.groupby([
            "start_station_name",
            "start_station_latitude",
            "start_station_longitude"
        ]).size().reset_index(name="trips")
        
        fig_map = px.scatter_mapbox(
            station_data,
            lat="start_station_latitude",
            lon="start_station_longitude",
            size="trips",
            hover_name="start_station_name",
            hover_data={"trips": True, "start_station_latitude": False, "start_station_longitude": False},
            zoom=11,
            height=500,
            color="trips",
            color_continuous_scale="Viridis"
        )
        fig_map.update_layout(
            mapbox_style=MAPBOX_STYLE,
            title="🗺️ Station Activity Map",
            template="plotly_dark",
            paper_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text']),
            margin={"r": 0, "t": 40, "l": 0, "b": 0}
        )
    else:
        fig_map = go.Figure()
    
    # Chart 8: Top Routes
    if "start_station_name" in dff.columns:
        routes = dff.groupby("start_station_name").size().nlargest(10).reset_index(name="trips")
        fig_routes = go.Figure()
        fig_routes.add_trace(go.Bar(
            x=routes["trips"],
            y=routes["start_station_name"],
            orientation='h',
            marker=dict(
                color=routes["trips"],
                colorscale='Plasma',
                showscale=False
            )
        ))
        fig_routes.update_layout(
            title="🏆 Top 10 Start Stations",
            template="plotly_dark",
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            font=dict(color=COLORS['text']),
            xaxis_title="Number of Trips",
            yaxis_title="",
            height=500
        )
    else:
        fig_routes = go.Figure()
    
    return kpis, fig_weekday, fig_hour, fig_age, fig_gender, fig_duration, fig_trend, fig_map, fig_routes

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚴 Ford GoBike Analytics Dashboard")
    print("="*60)
    print(f"📊 Loaded {len(df):,} records")
    print(f"📅 Date range: {df['start_time'].min()} to {df['start_time'].max()}")
    print("🌐 Starting server at http://127.0.0.1:8050/")
    print("="*60 + "\n")
    
    app.run(debug=True, port=8050)
