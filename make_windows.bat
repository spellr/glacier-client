python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

fbs freeze
fbs installer