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

    jobs = soup.find("ul", class_="jobs-list-items").find_all("li")

    for job in jobs:
        title = job.find("h4", class_="bjs-jlid__h").find("a")
        company = job.find("a", class_="bjs-jlid__b")
        skills_tag = job.find("div", class_="links-box").find_all("a")
        description = job.find("div", class_="bjs-jlid__description")
        url = title['href']

        skills_text = [tag.text.strip() for tag in skills_tag]

        job_data = {
            "title": title.text,
            "company": company.text,
            "url": url,
            "skills": skills_text
        }
        all_jobs.append(job_data)


def extract_berlinstartupjobs_jobs(keyword):
    url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"
    scrape_page(url)
    return all_jobs
