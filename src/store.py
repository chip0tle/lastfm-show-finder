from duckdb import DuckDBPyConnection, DuckDBPyRelation
import duckdb


def init_table(conn: DuckDBPyConnection) -> None:
    """
    Initialize main tracks_flattened table.
    """
    conn.sql(
        query="""
        CREATE TABLE IF NOT EXISTS tracks_flattened (
            position INTEGER,
            track_name VARCHAR,
            duration INTEGER,
            playcount BIGINT,
            listeners BIGINT,
            track_mbid VARCHAR,
            track_url VARCHAR,
            artist_name VARCHAR,
            artist_mbid VARCHAR,
            artist_url VARCHAR,
            streamable_text VARCHAR,
            streamable_fulltrack VARCHAR,
            image_url_small VARCHAR,
            date_pulled DATE
        )
        """
    )


def write_json_to_tracks_db(conn: DuckDBPyConnection, json_data) -> None:
    """
    Flatten & store json-structured python dict into persistent duckdb.
    """
    # Bring python dict (json) into duckdb
    conn.execute(
        query="""
            CREATE OR REPLACE TABLE tracks_temp AS
            SELECT x.*
            FROM (SELECT unnest($1) AS x)
        """,
        parameters=[json_data],
    )
    # Flatten schema, add position & date pulled, store in tracks_flattened
    conn.execute(
        query="""
            INSERT INTO tracks_flattened
            SELECT
                ROW_NUMBER() OVER () AS position,
                name AS track_name,
                duration::INT AS duration,
                playcount::BIGINT AS playcount,
                listeners::BIGINT AS listeners,
                mbid AS track_mbid,
                url AS track_url,
                artist.name AS artist_name,
                artist.mbid AS artist_mbid,
                artist.url AS artist_url,
                streamable['#text'] AS streamable_text,
                streamable.fulltrack AS streamable_fulltrack,
                image[1]['#text'] AS image_url_small,
                CURRENT_DATE AS date_pulled
            FROM tracks_temp
            """
    )


def cleanup_temp_tables(conn: DuckDBPyConnection) -> None:
    """
    Drop tables matching '%_temp' pattern
    """
    pattern: str = "%_temp"
    tables_to_drop = conn.execute(
        query="SELECT table_name FROM duckdb_tables WHERE table_name LIKE ?",
        parameters=(pattern,),
    ).fetchall()
    for (table_name,) in tables_to_drop:
        drop_query = f'DROP TABLE IF EXISTS "{table_name}" RESTRICT'
        conn.execute(query=drop_query)
        print(f"Dropped: {table_name}")


def date_check(conn: DuckDBPyConnection) -> bool:
    """
    Returns true if max(date_pulled) in tracks_flattened = today
    """
    latest_pull_date = conn.sql(
        query="SELECT MAX(date_pulled) FROM tracks_flattened"
    ).fetchall()
    today_date = conn.sql(query="SELECT CAST((CURRENT_DATE) AS DATE)").fetchall()
    # print(
    #     f"Latest pull in tracks_flattened: {latest_pull_date} \nCurrent date: {today_date}"
    # )
    return latest_pull_date == today_date


def cleanup_hist_data(conn: DuckDBPyConnection) -> None:
    # TODO: cleanup should drop rows where date_pulled > 14 days ago
    pass


def cleanup_all(conn: DuckDBPyConnection) -> None:
    cleanup_hist_data(conn)
    cleanup_temp_tables(conn)
    print("DB cleanup completed!")


# TODO: temp table & view(?) logic for PoP updates
