from flask import Flask, render_template, request
from extractors.web3 import extract_web3_jobs
from extractors.berlinstartupjobs import extract_berlinstartupjobs_jobs
from extractors.weworkremotely import extract_weworkremotely_jobs

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html", name="Juno")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword in db:
        jobs = db[keyword]
    else:
        web3 = extract_web3_jobs(keyword)
        berlinstartupjobs = extract_berlinstartupjobs_jobs(keyword)
        weworkremotely = extract_weworkremotely_jobs(keyword)
        jobs = berlinstartupjobs + web3
        jobs = jobs + weworkremotely
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)



app.run("0.0.0.0")

