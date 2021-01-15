#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request

import csv

app = Flask(__name__)


@app.route("/")
def homepage():
    """
    Renders homepage of site.
    """
    return render_template("index.html")


@app.route("/showname")
def showname():
    """
    Renders page with username from request displayed on it.
    """
    uname = request.args.get("username")
    return render_template("name.html", name=uname)


@app.route("/formtest", methods=["GET", "POST"])
def formtest():
    """
    Renders page with a form to take a user name. If they enter a name and
    click submit it renders the name page.
    """
    if request.method == "POST":
        formdata = request.form
        if formdata["name"] is not None and formdata["name"] != "":
            name = formdata["name"]
            return render_template("name.html", name=name)
        else:
            return render_template("formtest.html")
    else:
        return render_template("formtest.html")


@app.route("/allegiances")
def allegiances_json():
    """
    Returns json of allegiances csv file.
    """
    csvfile = open("/opt/allegiance.csv", "r")
    reader = csv.reader(csvfile)
    keys = ["Name", "Affiliation", "Allegiance"]
    allegiances = []
    i = 0
    for row in reader:
        if i != 0:
            dict = {}
            for key, value in zip(keys, row):
                dict[key] = value
            allegiances.append(dict)
        else:
            i += 1
    return jsonify(allegiances)


@app.route("/allegiancedashboard")
def allegiances_html():
    """
    Renders dashboard of allegiances from allegiances csv file returned from
    /allegiances.
    """
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run()
