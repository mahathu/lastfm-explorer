from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def main():
    with open("mahathu.csv", "r") as f:
        lines = [l.strip() for l in f.readlines()]

    colnames = ["artist", "album", "title", "time"]
    tracks = [dict(zip(colnames, line.split(","))) for line in lines[::-1]]

    # naive:
    # group tracks by day and calculate how often artist was played. hashmap?
    # for each day, get the favourite artist from the past 7 days.
    # if it's different to the one before, start a new object.

    return render_template("timeline.html", tracks=tracks)
