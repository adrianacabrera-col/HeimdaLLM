from pathlib import Path

from lark import Lark

from heimdallm.bifrosts.sql.bifrost import Bifrost as _SQLBifrost

from .. import presets

_THIS_DIR = Path(__file__).parent
_GRAMMAR_PATH = _THIS_DIR / "grammar.lark"


class Bifrost(_SQLBifrost):
    """
    A Bifrost for MySQL ``SELECT`` queries

    :param llm: The LLM integration to use.
    :param prompt_envelope: The prompt envelope used to wrap the untrusted human input
        and unwrap the untrusted LLM output.
    :param constraint_validators: A sequence of constraint validators that will be used
        to validate the parse tree returned by the ``tree_producer``. Only one validator
        needs to succeed for validation to pass.
    """

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

    @classmethod
    def reserved_keywords(self) -> set[str]:
        return presets.reserved_keywords