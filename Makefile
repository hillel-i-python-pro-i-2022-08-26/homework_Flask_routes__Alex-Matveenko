.PHONY: flask-i-run
# run flask server
flask-i-run:
		@python3 -m pip install --upgrade pip
		@pip install --requirement requirements.txt
		@python main.py
