"""
Pidgin lexer error categories:
- SPELLING: misspelled words with correction guidance.
- SYNTAX: English sentence structures that should be converted to Pidgin forms.
- SEMANTIC: English words where a Pidgin equivalent is expected.
"""

import json
import re
from pathlib import Path

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


LEXICON_PATH = Path(__file__).resolve().parent.parent / "json data" / "lexicon.json"
with LEXICON_PATH.open("r", encoding="utf-8") as lexicon_file:
	LEXICON = json.load(lexicon_file)


TOKEN_REGEX = re.compile(r"([a-zA-Z'\-]+|[^a-zA-Z\s])")
PUNCTUATION_REGEX = re.compile(r"^[^a-zA-Z']+")


def _get_syntax_suggestion(pattern_value):
	pidgin_equivalent = pattern_value.get("pidgin_equivalent", "")
	suggestions = pattern_value.get("suggestions", [])
	if pidgin_equivalent:
		return pidgin_equivalent
	if isinstance(suggestions, list) and suggestions:
		return suggestions[0]
	if isinstance(suggestions, str) and suggestions:
		return suggestions
	return "—"


@csrf_exempt
def analyze(request):
	"""Analyze a JSON sentence input and return tokens, errors, and summary metadata."""
	if request.method != "POST":
		return JsonResponse({"error": "Method not allowed"}, status=405)

	try:
		body = json.loads(request.body)
	except json.JSONDecodeError:
		return JsonResponse({"error": "Invalid JSON"}, status=400)

	sentence = body.get("sentence")
	if not isinstance(sentence, str) or not sentence.strip():
		return JsonResponse({"error": "sentence field is required"}, status=400)

	try:
		tokens = []
		errors = []

		lowered_sentence = sentence.lower()
		syntax_patterns = LEXICON.get("syntax_patterns", {})
		sorted_patterns = sorted(syntax_patterns.keys(), key=len, reverse=True)
		for pattern in sorted_patterns:
			if pattern in lowered_sentence:
				pattern_value = syntax_patterns.get(pattern, {})
				errors.append(
					{
						"type": "SYNTAX",
						"word": sentence,
						"message": "English grammar pattern detected",
						"suggestion": _get_syntax_suggestion(pattern_value),
					}
				)

		word_vocabulary = LEXICON.get("word_vocabulary", {})
		spell_correction = LEXICON.get("spell_correction", {})
		semantic_mappings = LEXICON.get("semantic_mappings", {})

		for token in TOKEN_REGEX.findall(sentence):
			if PUNCTUATION_REGEX.match(token):
				continue

			lower_token = token.lower()

			if lower_token in word_vocabulary:
				token_type = word_vocabulary[lower_token].get("token_type", "UNKNOWN")
				tokens.append({"raw": token, "type": token_type, "lower": lower_token})

				semantic_info = semantic_mappings.get(lower_token)
				if semantic_info:
					pidgin_equivalent = semantic_info.get("pidgin_equivalent", "")
					if pidgin_equivalent and pidgin_equivalent.lower() != lower_token:
						errors.append(
							{
								"type": "SEMANTIC",
								"word": token,
								"message": f'English word "{token}" — Pidgin equivalent is "{pidgin_equivalent}"',
								"suggestion": pidgin_equivalent,
							}
						)
				continue

			if lower_token in spell_correction:
				correction_info = spell_correction[lower_token]
				correct = correction_info.get("correct", lower_token)
				pidgin_equivalent = correction_info.get("pidgin_equivalent", correct)
				tokens.append({"raw": token, "type": "UNKNOWN", "lower": lower_token})
				errors.append(
					{
						"type": "SPELLING",
						"word": token,
						"message": (
							f'Misspelled word "{token}". Correct form is "{correct}" '
							f'and Pidgin equivalent is "{pidgin_equivalent}"'
						),
						"suggestion": pidgin_equivalent,
					}
				)
				continue

			if lower_token in semantic_mappings:
				semantic_info = semantic_mappings[lower_token]
				pidgin_equivalent = semantic_info.get("pidgin_equivalent", "—")
				tokens.append({"raw": token, "type": "WORD", "lower": lower_token})
				errors.append(
					{
						"type": "SEMANTIC",
						"word": token,
						"message": f'English word "{token}" — Pidgin equivalent is "{pidgin_equivalent}"',
						"suggestion": pidgin_equivalent,
					}
				)
				continue

			tokens.append({"raw": token, "type": "UNKNOWN", "lower": lower_token})
			errors.append(
				{
					"type": "UNKNOWN",
					"word": token,
					"message": f'Word "{token}" not found in lexicon',
					"suggestion": "—",
				}
			)

		error_types = list(dict.fromkeys(error["type"] for error in errors))
		response = {
			"sentence": sentence,
			"tokens": tokens,
			"errors": errors,
			"summary": {
				"total_tokens": len(tokens),
				"total_errors": len(errors),
				"error_types": error_types,
				"status": "errors_found" if errors else "ok",
			},
		}

		return JsonResponse(response, status=200)
	except Exception as e:
		return JsonResponse({"error": "Internal lexer error", "detail": str(e)}, status=500)
