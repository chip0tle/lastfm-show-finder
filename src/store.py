from duckdb import DuckDBPyConnection, DuckDBPyRelation
import duckdb


def init_table(conn: DuckDBPyConnection) -> None:
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


# TODO: flatten & store (add position column)
def write_json_to_tracks_db(conn: DuckDBPyConnection, json_data) -> None:
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


# TODO: temp table & logic for PoP updates
# TODO: cleanup func for dropping _temp tables
