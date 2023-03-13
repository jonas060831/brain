from dotenv import load_dotenv, find_dotenv
from application import app
import os
from waitress import serve

#load the .env file
load_dotenv(find_dotenv())

if __name__ == "__main__":
    if os.getenv('PYTHON_ENV') != 'DEVELOPMENT': #WHEN on production use this
        print(f"Server is now up and Running on port {os.getenv('PORT')}")
        serve(app, host="0.0.0.0", port=os.getenv('PORT'))
    else:
        app.run(port=8000, debug=True)
