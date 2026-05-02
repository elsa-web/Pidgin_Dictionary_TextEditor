# import json
# from pathlib import Path

# JSON_DIR = Path(__file__).resolve().parent.parent / "json data"

# # Load grammar rules
# with (JSON_DIR / "grammar_rules.json").open("r", encoding="utf-8") as f:
#     GRAMMAR_RULES = json.load(f)

# # Load semantic mappings
# with (JSON_DIR / "semantic_map.json").open("r", encoding="utf-8") as f:
#     raw_semantics = json.load(f)

# # Load spell corrections
# with (JSON_DIR / "dictionary.json").open("r", encoding="utf-8") as f:
#     raw_spelling = json.load(f)

# # Convert to dicts for fast lookup
# SEMANTIC_MAP = {
#     entry["english"].lower(): entry
#     for entry in raw_semantics
#     if "english" in entry
# }

# SPELLING_MAP = {
#     entry["english"].lower(): entry
#     for entry in raw_spelling
#     if "english" in entry
# }


# class PidginParser:

#     def __init__(self, sentence: str, tokens: list):
#         self.sentence = sentence
#         self.tokens = tokens
#         self.errors = []
#         self.flagged_indices = set()

#     def parse(self) -> list:
#         self._check_syntax()
#         self._check_spelling()
#         self._check_semantics()
#         return self.errors

#     def _check_syntax(self):
#         lowered = self.sentence.lower()

#         for rule in GRAMMAR_RULES:
#             pattern_str = " ".join(rule["pattern"]).lower()
#             replacement_str = " ".join(rule["replacement"])

#             search_start = 0
#             while True:
#                 idx = lowered.find(pattern_str, search_start)
#                 if idx == -1:
#                     break

#                 end_idx = idx + len(pattern_str)

#                 self.errors.append({
#                     "type": "SYNTAX",
#                     "word": self.sentence[idx:end_idx],
#                     "start": idx,
#                     "end": end_idx,
#                     "message": rule.get("description", "Grammar pattern detected"),
#                     "suggestion": replacement_str,
#                     "all_suggestions": [replacement_str]
#                 })

#                 for i, tok in enumerate(self.tokens):
#                     if tok["start"] >= idx and tok["end"] <= end_idx:
#                         self.flagged_indices.add(i)

#                 search_start = end_idx

#     def _check_spelling(self):
#         for i, token in enumerate(self.tokens):
#             if i in self.flagged_indices:
#                 continue

#             lower = token["lower"]
#             if lower in SPELLING_MAP:
#                 entry = SPELLING_MAP[lower]
#                 correct = entry.get("pidgin", lower)
#                 self.errors.append({
#                     "type": "SPELLING",
#                     "word": token["raw"],
#                     "start": token["start"],
#                     "end": token["end"],
#                     "message": f'"{token["raw"]}" is misspelled. Did you mean "{correct}"?',
#                     "suggestion": correct,
#                     "all_suggestions": entry.get("suggestions", [correct])
#                 })
#                 self.flagged_indices.add(i)

#     def _check_semantics(self):
#         for i, token in enumerate(self.tokens):
#             if i in self.flagged_indices:
#                 continue

#             if token["type"] == "UNKNOWN":
#                 continue

#             lower = token["lower"]
#             if lower in SEMANTIC_MAP:
#                 info = SEMANTIC_MAP[lower]
#                 pidgin = info.get("pidgin_equivalent", "")

#                 if pidgin and pidgin.lower() != lower:
#                     self.errors.append({
#                         "type": "SEMANTIC",
#                         "word": token["raw"],
#                         "start": token["start"],
#                         "end": token["end"],
#                         "message": f'"{token["raw"]}" → Pidgin: "{pidgin}"',
#                         "suggestion": pidgin,
#                         "all_suggestions": info.get("suggestions", [pidgin])
#                     })


import json
from pathlib import Path

JSON_DIR = Path(__file__).resolve().parent.parent / "json data"

with (JSON_DIR / "lexicon.json").open("r", encoding="utf-8") as f:
    LEXICON = json.load(f)

WORD_VOCABULARY = LEXICON.get("word_vocabulary", {})
SPELLING_CORRECTION = LEXICON.get("spelling_correction", {})
SYNTAX_PATTERNS = LEXICON.get("syntax_patterns", {})
SEMANTIC_MAPPINGS = LEXICON.get("semantic_mappings", {})

SORTED_PATTERNS = sorted(SYNTAX_PATTERNS.keys(), key=len, reverse=True)


# ── Standalone helper functions ───────────────────────────────────────────────

def levenshtein(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def get_suggestions(word: str, vocabulary: dict, max_suggestions: int = 3) -> list:
    word = word.lower()
    candidates = []

    for vocab_word in vocabulary.keys():
        distance = levenshtein(word, vocab_word)
        if distance <= 2:
            candidates.append((vocab_word, distance))

    candidates.sort(key=lambda x: x[1])
    return [c[0] for c in candidates[:max_suggestions]]


# ── Parser class ──────────────────────────────────────────────────────────────

class PidginParser:

    def __init__(self, sentence: str, tokens: list):
        self.sentence = sentence
        self.tokens = tokens
        self.errors = []
        self.flagged_indices = set()

    def parse(self) -> list:
        self._check_syntax()
        self._check_spelling()
        self._check_semantics()
        self._check_unknown()
        return self.errors

    def _check_syntax(self):
        lowered = self.sentence.lower()

        for pattern in SORTED_PATTERNS:
            search_start = 0
            while True:
                idx = lowered.find(pattern, search_start)
                if idx == -1:
                    break

                end_idx = idx + len(pattern)
                pattern_info = SYNTAX_PATTERNS[pattern]

                self.errors.append({
                    "type": "SYNTAX",
                    "word": self.sentence[idx:end_idx],
                    "start": idx,
                    "end": end_idx,
                    "message": f'English grammar pattern "{pattern}" detected',
                    "suggestion": pattern_info.get("pidgin_equivalent", "—"),
                    "all_suggestions": pattern_info.get("suggestions", [])
                })

                for i, tok in enumerate(self.tokens):
                    if tok["start"] >= idx and tok["end"] <= end_idx:
                        self.flagged_indices.add(i)

                search_start = end_idx

    def _check_spelling(self):
        for i, token in enumerate(self.tokens):
            if i in self.flagged_indices:
                continue

            lower = token["lower"]
            if lower in SPELLING_CORRECTION:
                entry = SPELLING_CORRECTION[lower]
                correct = entry.get("pidgin", lower)
                self.errors.append({
                    "type": "SPELLING",
                    "word": token["raw"],
                    "start": token["start"],
                    "end": token["end"],
                    "message": f'"{token["raw"]}" is misspelled. Did you mean "{correct}"?',
                    "suggestion": correct,
                    "all_suggestions": entry.get("suggestions", [correct])
                })
                self.flagged_indices.add(i)

    def _check_semantics(self):
        for i, token in enumerate(self.tokens):
            if i in self.flagged_indices:
                continue

            if token["type"] == "UNKNOWN":
                continue

            lower = token["lower"]
            if lower in SEMANTIC_MAPPINGS:
                info = SEMANTIC_MAPPINGS[lower]
                pidgin = info.get("pidgin_equivalent", "")

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

    def _check_unknown(self):
        for i, token in enumerate(self.tokens):
            if i in self.flagged_indices:
                continue

            if token["type"] == "PUNCTUATION":
                continue

            lower = token["lower"]

            if lower in WORD_VOCABULARY:
                continue

            if lower in SEMANTIC_MAPPINGS:
                continue

            if lower in SPELLING_CORRECTION:
                continue

            # Skip proper nouns
            if token["raw"][0].isupper() and token["start"] > 0:
                continue

            suggestions = get_suggestions(lower, WORD_VOCABULARY)

            self.errors.append({
                "type": "SPELLING",
                "word": token["raw"],
                "start": token["start"],
                "end": token["end"],
                "message": f'"{token["raw"]}" not recognized — may be misspelled',
                "suggestion": suggestions[0] if suggestions else "—",
                "all_suggestions": suggestions
            })
            self.flagged_indices.add(i)