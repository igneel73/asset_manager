from flask import Flask

# setup
app = Flask(__name__)

# execution
if __name__ == '__main__':
    app.run(debug=True)
