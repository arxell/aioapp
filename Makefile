pip:
	pip install -U pip setuptools pip-tools
	pip-compile requirements/base.in
	pip-sync -i https://pip.ostrovok.in/simple/ requirements/base.txt
	pip install -r requirements/dev.txt

rm-pyc:
	find . -name '*.pyc' -delete
	find . -name '*__pycache__' -delete


isort:
	./code_checks/checks/make_isort.sh

black:
	./code_checks/checks/make_black.sh

vulture:
	./code_checks/checks/make_vulture.sh

format: rm-pyc isort black

run:
	gunicorn --reload --config etc/gunicorn/guni.py app.main:app

test: rm-pyc
	py.test app/ --reuse-db --tb=short --verbose -s

docker-build:
	docker-compose build

docker-run:
	docker-compose run

docker-build-and-run: docker-build docker-run
