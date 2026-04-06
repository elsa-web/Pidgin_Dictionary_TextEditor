import json
import re
from pathlib import Path

# ─── Load the lexicon once at startup ────────────────────────────────────────
LEXICON_PATH = Path(__file__).resolve().parent.parent / "json data" / "lexicon.json"
with LEXICON_PATH.open("r", encoding="utf-8") as f:
    LEXICON = json.load(f)

syntax_patterns = LEXICON.get("syntax_patterns", {})
semantic_mappings = LEXICON.get("semantic_mappings", {})

# Sort patterns longest-first so "I am going to" is checked before "I am going"
SORTED_PATTERNS = sorted(syntax_patterns.keys(), key=len, reverse=True)


# ─── The Parser class ─────────────────────────────────────────────────────────
class PidginParser:
    """
    Receives the token list produced by the lexer and detects:
    - SYNTAX errors: sequences of tokens matching known bad grammar patterns
    - SEMANTIC errors: individual tokens that have a more natural Pidgin form
    
    Returns a list of error objects with exact character positions.
    """

    def __init__(self, sentence: str, tokens: list):
        """
        sentence : the original raw text the user typed
        tokens   : list of token dicts from the lexer, each must have
                   {"raw": ..., "lower": ..., "start": ..., "end": ...}
        """
        self.sentence = sentence
        self.tokens = tokens
        self.errors = []

        # Keep track of which token indices have already been flagged
        # so we don't double-report the same word for both SYNTAX and SEMANTIC
        self.flagged_indices = set()

    def parse(self) -> list:
        """Run all checks and return the combined error list."""
        self._check_syntax()
        self._check_semantics()
        return self.errors

    # ── SYNTAX CHECK ──────────────────────────────────────────────────────────
    def _check_syntax(self):
        """
        Slide a window over the lowercased sentence and look for known
        syntax patterns (e.g. "I am going", "they are eating").
        When found, record the start/end positions so the UI knows
        exactly where to draw the BLUE underline.
        """
        lowered = self.sentence.lower()

        for pattern in SORTED_PATTERNS:
            search_start = 0
            # A pattern can appear multiple times in a sentence
            while True:
                idx = lowered.find(pattern, search_start)
                if idx == -1:
                    break  # pattern not found, move on

                end_idx = idx + len(pattern)
                pattern_info = syntax_patterns[pattern]

                self.errors.append({
                    "type": "SYNTAX",
                    "word": self.sentence[idx:end_idx],  # exact original casing
                    "start": idx,
                    "end": end_idx,
                    "message": f'English grammar pattern "{pattern}" detected',
                    "suggestion": pattern_info.get("pidgin_equivalent", "—"),
                    "all_suggestions": pattern_info.get("suggestions", [])
                })

                # Mark every token that falls inside this matched region
                for i, tok in enumerate(self.tokens):
                    if tok["start"] >= idx and tok["end"] <= end_idx:
                        self.flagged_indices.add(i)

                search_start = end_idx  # continue searching after this match

    # ── SEMANTIC CHECK ────────────────────────────────────────────────────────
    def _check_semantics(self):
        """
        For each token NOT already flagged by a syntax rule,
        check whether it has a more natural Pidgin equivalent
        in semantic_mappings.
        """
        for i, token in enumerate(self.tokens):
            if i in self.flagged_indices:
                continue  # already covered by a syntax error, skip

            lower = token["lower"]
            if lower in semantic_mappings:
                info = semantic_mappings[lower]
                pidgin = info.get("pidgin_equivalent", "")

                # Only flag if the pidgin form is actually different from English
                if pidgin and pidgin.lower() != lower:
                    self.errors.append({
                        "type": "SEMANTIC",
                        "word": token["raw"],
                        "start": token["start"],
                        "end": token["end"],
                        "message": f'"{token["raw"]}" → Pidgin: "{pidgin}"',
                        "suggestion": pidgin,
                        "all_suggestions": info.get("suggestions", [pidgin])
                    })