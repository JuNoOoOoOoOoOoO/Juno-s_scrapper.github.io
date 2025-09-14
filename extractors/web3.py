import requests
from bs4 import BeautifulSoup

all_jobs = []


def scrape_page(url):
    print(f"Scraping {url}")
    response = requests.get(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        })

    soup = BeautifulSoup(response.content, "html.parser")

    jobs = soup.find("tbody", class_="tbody").find_all("tr")

    for job in jobs:
        title = job.find("td", scope="row").find("a")
        company = job.find("td", class_="job-location-mobile").find("a")
        skills_tag = job.find(
            "td",
            style=
            "display: block !important; margin-left: 10px; margin-top: -60px; margin-bottom: 10px"
        ).find_all("span")
        url = title["href"]

        skills_text = [tag.text.strip() for tag in skills_tag]

        job_data = {
            "title": title.text,
            "company": company.text,
            "url": "https://web3.career" + url,
            "skills": skills_text
        }
        all_jobs.append(job_data)


def extract_web3_jobs(keyword):
    url = f"https://web3.career/{keyword}-jobs"
    scrape_page(url)
    return all_jobs    