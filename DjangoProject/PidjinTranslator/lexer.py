import json
import re
from pathlib import Path


class PidginLexer:

    def __init__(self, lexicon_path=None):
        if lexicon_path is None:
            lexicon_path = Path(__file__).resolve().parent.parent / "json data" / "lexicon.json"
        else:
            lexicon_path = Path(lexicon_path)

        with open(str(lexicon_path), "r", encoding="utf-8") as lexicon_file:
            self.lexicon = json.load(lexicon_file)

        self.token_regex = re.compile(r"([a-zA-Z'\-]+|[^a-zA-Z\s])")
        self.punctuation_regex = re.compile(r"^[^a-zA-Z']+")

    def analyze(self, sentence):
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError("sentence field is required")

        tokens = []

        word_vocabulary = self.lexicon.get("word_vocabulary", {})

        for match in self.token_regex.finditer(sentence):
            token = match.group()
            start = match.start()
            end = match.end()

            if self.punctuation_regex.match(token):
                token_type = "PUNCTUATION"
            else:
                lower_token = token.lower()
                token_type = word_vocabulary.get(lower_token, {}).get("token_type", "UNKNOWN")

            tokens.append({
                "raw": token,
                "type": token_type,
                "lower": token.lower(),
                "start": start,
                "end": end
            })

        return {
            "sentence": sentence,
            "tokens": tokens,
            "summary": {
                "total_tokens": len(tokens),
                "status": "ok"
            }
        }