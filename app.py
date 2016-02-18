from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Worl"

@app.route("/health")
    return 0

if __name__ == "__main__":
    app.run()
