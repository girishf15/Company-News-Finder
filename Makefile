# used CHATGPT to generate this script

.PHONY: run test

run:
	uvicorn app.main:app --reload

test:
	pytest tests/
