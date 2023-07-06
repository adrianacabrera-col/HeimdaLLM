import sqlite3
from pathlib import Path

from lark import Lark

from heimdallm.bifrosts.sql.bifrost import Bifrost as _SQLBifrost

_THIS_DIR = Path(__file__).parent
_GRAMMAR_PATH = _THIS_DIR / "sqlite.lark"


class Bifrost(_SQLBifrost):
    @staticmethod
    def build_grammar() -> Lark:
        """
        Returns a limited ``SELECT`` grammar

        noteworthy:
            - no outer joins
            - no subqueries

        Theoretically, subqueries could be allowed, but it would be more work, and
        I'm not yet convinced that an LLM produces subqueries often enough to make
        it worth it.

        Outer joins are unsafe because the join constraint is not applied to the
        rows that would be considered "outer."
        """
        with open(_GRAMMAR_PATH, "r") as h:
            grammar = Lark(
                ambiguity="explicit",
                maybe_placeholders=False,
                grammar=h,
            )
        return grammar


def get_schema(conn: sqlite3.Connection):
    """a convenience function to get the schema of a sqlite database. you
    probably want to write your own function to do this, one that doesn't
    include tables and columns that you care about sending to the LLM"""
    schema = []
    for line in conn.iterdump():
        if "CREATE TABLE" in line:
            schema.append(line)
    return "\n".join(schema)
