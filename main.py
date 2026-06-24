import os
import duckdb
from src.fetch import get_as_json
from src.store import init_table
from dotenv import load_dotenv

load_dotenv()

LASTFM_KEY: str | None = os.getenv(key="LASTFM_API_KEY")
LASTFM_CHART_URL: str = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={LASTFM_KEY}&format=json"
DATABASE_PATH: str = "data/db.duckdb"


def main():
    # Request chart data from Last.fm
    chart_data = get_as_json(api_key=LASTFM_KEY, url=LASTFM_CHART_URL)
    print(chart_data)

    # Init database
    with duckdb.connect(database=DATABASE_PATH) as conn:
        # Write json to database
        init_table(conn)


if __name__ == "__main__":
    main()
