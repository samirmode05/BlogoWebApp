#Importing app from the folder
from website import create_app

#Running the Flask app
if __name__ == "__main__":
    app = create_app()
    app.run(debug = True)    