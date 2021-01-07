from flask import Flask, render_template

app = Flask(__name__)

# Root HOMEPAGE
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html", page_title="Home")

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port='5000',
            debug=True)