install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

run:
	python app/main.py

push:
	git add .
	git commit -a -m=${m}
	git push

format:
	black app/*.py app/*/*.py app/*/*/*.py app/database/models/*.py

lint:
	pylint --disable=R,C app/*.py app/*/*.py app/*/*/*.py app/database/models/*.py

test:
	pytest --cov=app app/tests/

deploy:
	#deploy code

all: install lint test deploy
