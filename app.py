# Version 1.0
# Created by Aaron Su 16 Dec 2019

from src import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
