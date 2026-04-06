"""
API Views for the Pidgin Translator
"""

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .lexer import PidginLexer
from .parser import PidginParser


# Initialize lexer once
lexer = PidginLexer()


@csrf_exempt
@require_http_methods(["POST"])
def analyze(request):
	"""Analyze a sentence using lexical and syntactic analysis.
	
	POST endpoint that accepts a JSON payload with a 'sentence' field.
	Performs two-phase analysis:
	  1. Lexer: tokenization, spelling detection, word vocabulary lookup
	  2. Parser: syntax pattern detection, semantic equivalence checking
	
	Returns combined tokens and errors from both phases.
	
	Request body:
		{
			"sentence": "text to analyze"
		}
	
	Response (200 OK):
		{
			"sentence": "...",
			"tokens": [...],
			"errors": [...],
			"summary": {...}
		}
	"""
	try:
		body = json.loads(request.body)
	except json.JSONDecodeError:
		return JsonResponse({"error": "Invalid JSON"}, status=400)

	sentence = body.get("sentence")
	if not isinstance(sentence, str) or not sentence.strip():
		return JsonResponse({"error": "sentence field is required"}, status=400)

	try:
		# Phase 1: Lexer - tokenize and detect spelling errors
		lexer_result = lexer.analyze(sentence)
		tokens = lexer_result["tokens"]
		lex_errors = lexer_result["errors"]

		# Phase 2: Parser - detect syntax and semantic errors
		parser = PidginParser(sentence, tokens)
		parser_errors = parser.parse()

		# Merge errors from both phases
		all_errors = lex_errors + parser_errors
		
		# Remove duplicates while preserving order
		seen = set()
		unique_errors = []
		for error in all_errors:
			error_key = (error["type"], error["word"], error.get("start", error["word"]))
			if error_key not in seen:
				seen.add(error_key)
				unique_errors.append(error)

		# Build response
		error_types = list(dict.fromkeys(error["type"] for error in unique_errors))
		response = {
			"sentence": sentence,
			"tokens": tokens,
			"errors": unique_errors,
			"summary": {
				"total_tokens": len(tokens),
				"total_errors": len(unique_errors),
				"error_types": error_types,
				"status": "errors_found" if unique_errors else "ok",
			},
		}

		return JsonResponse(response, status=200)

	except Exception as e:
		return JsonResponse({
			"error": "Internal analysis error",
			"detail": str(e)
		}, status=500)