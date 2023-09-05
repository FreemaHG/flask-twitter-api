############### virtualenv
-include .env

venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d venv || python3 -m venv venv
	touch venv/touchfile

############### install

.PHONY: install
install: venv install-pre-commit
	. venv/bin/activate; make install-deps

.PHONY: install-pre-commit
install-pre-commit:
	mkdir -p .git/hooks
	echo "#!/bin/bash\nmake lint" > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

.PHONY: install-deps
install-deps:
	pip install -r app/requirements/development.txt

############### tests

.PHONY: test
test: venv
	. venv/bin/activate; pytest ./tests/

.PHONY: test-coverage
test-coverage: venv
	. venv/bin/activate; pytest \
		--cov-config=.coveragerc \
		--cov-report=term \
		--cov-report=html \
		--cov-report=xml \
		--no-cov-on-fail \
		--cov=. \
		./tests/

############### other

.PHONY: clean
clean:
	rm -rf venv
	find . -iname "*.pyc" -delete

############### codestyle

.PHONY: format
format: venv
	. venv/bin/activate; make format-ruff; make format-black

.PHONY: format-black
format-black: venv
	python3 -m black . --exclude 'venv/|\.local/|\.cache/|\.git/'

.PHONY: format-ruff
format-ruff: venv
	python3 -m ruff . --fix

############### lint

.PHONY: lint
lint: venv
	. venv/bin/activate; make lint-ruff; make lint-black

.PHONY: lint-black
lint-black: venv
	. venv/bin/activate; python3 -m black . --diff --check --exclude 'venv/|\.local/|\.cache/|\.git/'

.PHONY: lint-ruff
lint-ruff: venv
	. venv/bin/activate; python3 -m ruff .

############### migrate

.PHONY: migrate
migrate: venv
	. venv/bin/activate; alembic upgrade head

.PHONY: create-migration
create-migration:
	. venv/bin/activate; alembic revision --autogenerate -m "$(shell date +%s)"
	make format
	git add migrations
