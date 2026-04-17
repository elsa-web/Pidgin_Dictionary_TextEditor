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
		#lex_errors = lexer_result["errors"]

		# Phase 2: Parser - detect syntax and semantic errors
		parser = PidginParser(sentence, tokens)
		parser_errors = parser.parse()

		# Build response
		error_types = list(dict.fromkeys(error["type"] for error in parser_errors))
		response = {
			"sentence": sentence,
			"tokens": tokens,
			"errors": parser_errors,
			"summary": {
				"total_tokens": len(tokens),
				"total_errors": len(parser_errors),
				"error_types": error_types,
				"status": "errors_found" if parser_errors else "ok",
			},
		}

		return JsonResponse(response, status=200)

	except Exception as e:
		return JsonResponse({
			"error": "Internal analysis error",
			"detail": str(e)
		}, status=500)