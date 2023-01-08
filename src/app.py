#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return '''
     <form action="/carbon-emission-report" method="POST">
         <input name="user_input">
         <input type="submit" value="Enter the resource (ie. VM, Storage, etc.) to get Carbon Emission Report">
     </form>
     '''

@app.route("/carbon-emission-report", methods=["POST"])
def getCarbonEmissionReport():
    input_text = request.form.get("user_input", "")
    if not input_text:
        return "Please enter a resource to get Carbon Emission Report"
    return "Carbon Emission report is current not available for the resource: " + input_text
