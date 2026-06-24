from duckdb import DuckDBPyConnection, DuckDBPyRelation
import duckdb


def init_table(conn: DuckDBPyConnection) -> None:
    conn.sql(
        query="""
        CREATE TABLE IF NOT EXISTS tracks (
            track_name VARCHAR,
            duration UINTEGER,
            playcount UINTEGER,
            listeners UINTEGER,
            mbid VARCHAR,
            track_url VARCHAR,
            artist_name VARCHAR,
            artist_url VARCHAR,
            image_url_small VARCHAR
        )
        """
    )


# TODO: flatten json data, write required columns to db -- see scratch.txt for example
# def write_json_to_db(conn: DuckDBPyConnection, json_data):
