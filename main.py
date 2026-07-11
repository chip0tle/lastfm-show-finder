import os
import duckdb
from src.fetch import get_as_json
from src.store import init_table, write_json_to_tracks_db, cleanup
from dotenv import load_dotenv

load_dotenv()

LASTFM_KEY: str | None = os.getenv(key="LASTFM_API_KEY")
LASTFM_CHART_URL: str = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={LASTFM_KEY}&format=json"
# LASTFM_TOPTRACKS_URL: str = f"http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country=us&api_key={LASTFM_KEY}&format=json"
DATABASE_PATH: str = "data/db.duckdb"


def main():
    # Init database
    with duckdb.connect(database=DATABASE_PATH) as conn:
        # Init tracks_flattened if not exists
        init_table(conn)

        # Check if tracks_flattened has data from today
        latest_pull_date = conn.sql(
            query="SELECT MAX(date_pulled) FROM tracks_flattened GROUP BY date_pulled"
        ).fetchall()
        today_date = conn.sql(query="SELECT CAST((CURRENT_DATE) AS DATE)").fetchall()
        if not latest_pull_date == today_date:
            # Request chart data from Last.fm
            chart_data = get_as_json(api_key=LASTFM_KEY, url=LASTFM_CHART_URL)
            chart_tracklist = chart_data["tracks"]["track"]
            # Flatten & store API data
            write_json_to_tracks_db(conn, json_data=chart_tracklist)

        # TODO: PoP update & position calcs logic
        # conn.sql(query="DESCRIBE tracks_temp").show()
        # conn.sql(query="DESCRIBE tracks_flattened").show()

        # Drop any _temp tables, close db connection
        cleanup(conn)
        conn.close()


if __name__ == "__main__":
    main()
