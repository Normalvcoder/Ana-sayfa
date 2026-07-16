from flask import Flask

app = Flask(__name__) # Initialize the app

@app.route("/") # Define the URL route
def hello_world(): # Define the view function
    return "<p>Hello, World!</p>" # The response