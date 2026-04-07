# import json
# import re
# from pathlib import Path


# class PidginLexer:

# 	def __init__(self, lexicon_path=None):
		
# 		if lexicon_path is None:
# 			lexicon_path = Path(__file__).resolve().parent.parent / "json data" / "lexicon.json"
# 		else:
# 			lexicon_path = Path(lexicon_path)
		
# 		with open(str(lexicon_path), "r", encoding="utf-8") as lexicon_file:
# 			self.lexicon = json.load(lexicon_file)
		
# 		self.token_regex = re.compile(r"([a-zA-Z'\-]+|[^a-zA-Z\s])")
# 		self.punctuation_regex = re.compile(r"^[^a-zA-Z']+")

# 	def analyze(self, sentence):
		
# 		if not isinstance(sentence, str) or not sentence.strip():
# 			raise ValueError("sentence field is required")

# 		tokens = []
# 		errors = []

# 		# Check for syntax patterns
# 		lowered_sentence = sentence.lower()
# 		syntax_patterns = self.lexicon.get("syntax_patterns", {})
# 		sorted_patterns = sorted(syntax_patterns.keys(), key=len, reverse=True)
		
# 		for pattern in sorted_patterns:
# 			if pattern in lowered_sentence:
# 				pattern_value = syntax_patterns.get(pattern, {})
# 				errors.append({
# 					"type": "SYNTAX",
# 					"word": sentence,
# 					"message": "English grammar pattern detected",
# 					"suggestion": self._get_syntax_suggestion(pattern_value),
# 				})

# 		# Tokenize and analyze
# 		word_vocabulary = self.lexicon.get("word_vocabulary", {})
# 		spell_correction = self.lexicon.get("spell_correction", {})
# 		semantic_mappings = self.lexicon.get("semantic_mappings", {})

# 		for match in self.token_regex.finditer(sentence):
# 			token = match.group()
# 			start = match.start()
# 			end = match.end()

# 			if self.punctuation_regex.match(token):
# 				continue

# 			lower_token = token.lower()

# 			# Token in vocabulary
# 			if lower_token in word_vocabulary:
# 				token_type = word_vocabulary[lower_token].get("token_type", "UNKNOWN")
# 				tokens.append({
# 					"raw": token,
# 					"type": token_type,
# 					"lower": lower_token,
# 					"start": start,
# 					"end": end
# 				})

# 				semantic_info = semantic_mappings.get(lower_token)
# 				if semantic_info:
# 					pidgin_equivalent = semantic_info.get("pidgin_equivalent", "")
# 					if pidgin_equivalent and pidgin_equivalent.lower() != lower_token:
# 						errors.append({
# 							"type": "SEMANTIC",
# 							"word": token,
# 							"message": f'English word "{token}" — Pidgin equivalent is "{pidgin_equivalent}"',
# 							"suggestion": pidgin_equivalent,
# 						})
# 				continue

# 			# Spelling correction
# 			if lower_token in spell_correction:
# 				correction_info = spell_correction[lower_token]
# 				correct = correction_info.get("correct", lower_token)
# 				pidgin_equivalent = correction_info.get("pidgin_equivalent", correct)
# 				tokens.append({
# 					"raw": token,
# 					"type": "UNKNOWN",
# 					"lower": lower_token,
# 					"start": start,
# 					"end": end
# 				})
# 				errors.append({
# 					"type": "SPELLING",
# 					"word": token,
# 					"message": (
# 						f'Misspelled word "{token}". Correct form is "{correct}" '
# 						f'and Pidgin equivalent is "{pidgin_equivalent}"'
# 					),
# 					"suggestion": pidgin_equivalent,
# 				})
# 				continue

# 			# Semantic mapping (word exists but needs Pidgin equivalent)
# 			if lower_token in semantic_mappings:
# 				semantic_info = semantic_mappings[lower_token]
# 				pidgin_equivalent = semantic_info.get("pidgin_equivalent", "—")
# 				tokens.append({
# 					"raw": token,
# 					"type": "WORD",
# 					"lower": lower_token,
# 					"start": start,
# 					"end": end
# 				})
# 				errors.append({
# 					"type": "SEMANTIC",
# 					"word": token,
# 					"message": f'English word "{token}" — Pidgin equivalent is "{pidgin_equivalent}"',
# 					"suggestion": pidgin_equivalent,
# 				})
# 				continue

# 			# Unknown token
# 			tokens.append({
# 				"raw": token,
# 				"type": "UNKNOWN",
# 				"lower": lower_token,
# 				"start": start,
# 				"end": end
# 			})
# 			errors.append({
# 				"type": "UNKNOWN",
# 				"word": token,
# 				"message": f'Word "{token}" not found in lexicon',
# 				"suggestion": "—",
# 			})

# 		# Build response
# 		error_types = list(dict.fromkeys(error["type"] for error in errors))
# 		return {
# 			"sentence": sentence,
# 			"tokens": tokens,
# 			"errors": errors,
# 			"summary": {
# 				"total_tokens": len(tokens),
# 				"total_errors": len(errors),
# 				"error_types": error_types,
# 				"status": "errors_found" if errors else "ok",
# 			},
# 		}

# 	@staticmethod
# 	def _get_syntax_suggestion(pattern_value):
	
# 		pidgin_equivalent = pattern_value.get("pidgin_equivalent", "")
# 		suggestions = pattern_value.get("suggestions", [])
		
# 		if pidgin_equivalent:
# 			return pidgin_equivalent
# 		if isinstance(suggestions, list) and suggestions:
# 			return suggestions[0]
# 		if isinstance(suggestions, str) and suggestions:
# 			return suggestions
# 		return "—"








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