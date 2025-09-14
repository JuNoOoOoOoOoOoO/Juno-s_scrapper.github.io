'''
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://www.wanted.co.kr/")

time.sleep(1)

page.click("button.Aside_searchButton__Ib5Dn") # 돋보기 버튼 클릭

time.sleep(1)

page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter") # 플레이스홀더 입력

time.sleep(1)

page.keyboard.down("Enter") # 엔터

time.sleep(3)

page.click("a#search_tab_position") # 앵커에 있는 포지션 id 클릭

time.sleep(3)

for i in range(3):  # 스크롤 세번 내리기
    page.keyboard.down("End")
    time.sleep(1)

time.sleep(1)

content = page.content()

p.stop()

soup =BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__zQcZs")

jobs_db = []

for job in jobs:
    link = f"https://www.wanted.co.kr/{job.find('a')['href']}"    # href="/wd/308756"
    title = job.find("strong", class_="JobCard_title___kfvj").text
    company = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu wds-nkj4w6").text
    experience = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l wds-nkj4w6").text
    reward = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l wds-nkj4w6").text

    job = {
        "title": title,
        "company": company,
        "experience": experience,
        "reward": reward,
        "link": link
    }
    jobs_db.append(job)

file = open("jobs.csv", "w")    # 파일이 없으면 만듦
writer = csv.writer(file)      
writer.writerow(
    [
        "title",
        "company",
        "experience",
        "reward",
        "link"
    ]
)

for job in jobs_db:
    writer.writerow(job.values())
'''
#====================================================

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
