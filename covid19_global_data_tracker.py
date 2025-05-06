import pandas as pd
import plotly.express as px
from typing import List

# 1. Fetch WHO global CSV data
def fetch_who_global_data(url: str) -> pd.DataFrame:
    """
    Fetch global COVID-19 data from WHO CSV endpoint.

    Returns a DataFrame with columns:
      - Date_reported
      - Country
      - New_cases
      - Cumulative_cases
    Falls back to sample data if download fails.
    """
    try:
        df = pd.read_csv(url)
        # select only the columns we need
        df = df[['Date_reported', 'Country', 'New_cases', 'Cumulative_cases']]
    except Exception as e:
        print(f"⚠️ Could not fetch WHO data ({e}), using fallback sample.")
        sample = {
            'Date_reported': pd.date_range('2020-01-01', periods=7).tolist() * 2,
            'Country': ['CountryA']*7 + ['CountryB']*7,
            'New_cases': [1,2,3,4,5,6,7] + [2,3,1,0,4,5,3],
            'Cumulative_cases': [1,3,6,10,15,21,28] + [2,5,6,6,10,15,18]
        }
        df = pd.DataFrame(sample)
    print(f"Loaded {len(df)} total records.")
    display(df.head())
    return df

# 2. Clean & index the data
def clean_global_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse dates, drop invalids, set index, drop duplicates, and sort.
    """
    df = df.copy()
    df['Date_reported'] = pd.to_datetime(df['Date_reported'], errors='coerce')
    df = df.dropna(subset=['Date_reported'])
    df = df.set_index('Date_reported').sort_index().drop_duplicates()
    print("After cleaning:")
    display(df.tail())
    return df

# 3. Aggregate global daily new cases & compute rolling average
def compute_global_rolling(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """
    Sum New_cases across all countries by date, then add 7-day avg.
    """
    daily = df.groupby(df.index).agg({'New_cases': 'sum'}).rename(columns={'New_cases': 'Total_new_cases'})
    daily['7day_avg'] = daily['Total_new_cases'].rolling(window, min_periods=1).mean()
    print("Global daily and 7‑day average head:")
    display(daily.head(10))
    return daily

# 4. Plot global 7-day rolling average
def plot_global_rolling(daily_df: pd.DataFrame) -> None:
    fig = px.line(
        daily_df,
        y='7day_avg',
        title='Global COVID-19: 7‑Day Rolling Average of New Cases',
        labels={'7day_avg': 'New Cases (7‑day avg)'}
    )
    fig.update_layout(xaxis_title='Date', yaxis_title='New Cases (7‑day avg)')
    fig.show()

# 5. Plot rolling average for selected countries
def plot_countries_rolling(
    df: pd.DataFrame,
    countries: List[str],
    metric: str = 'New_cases',
    window: int = 7
) -> None:
    """
    For each country in `countries`, compute and plot a rolling average of `metric`.
    """
    subset = df[df['Country'].isin(countries)].copy()
    # compute rolling per country
    subset[f'{metric}_{window}d_avg'] = (
        subset.groupby('Country')[metric]
              .rolling(window, min_periods=1)
              .mean()
              .reset_index(level=0, drop=True)
    )
    print(f"Plotting rolling average for: {', '.join(countries)}")
    fig = px.line(
        subset,
        x=subset.index,
        y=f'{metric}_{window}d_avg',
        color='Country',
        title=f'7‑Day Rolling Average of {metric.replace("_"," ").title()} by Country',
        labels={f'{metric}_{window}d_avg': f'{metric.replace("_"," ").title()} (7‑day avg)'}
    )
    fig.update_layout(xaxis_title='Date', yaxis_title=f'{metric.replace("_"," ").title()} (7‑day avg)')
    fig.show()

# === Main execution ===

if __name__ == "__main__":
    WHO_URL = "https://covid19.who.int/WHO-COVID-19-global-data.csv"

    # Fetch & clean
    raw_global = fetch_who_global_data(WHO_URL)
    clean_global = clean_global_data(raw_global)

    # Global rolling plot
    global_daily = compute_global_rolling(clean_global)
    plot_global_rolling(global_daily)

    # Compare a few large countries
    compare_list = ["United States", "India", "Brazil"]
    plot_countries_rolling(clean_global, compare_list)
