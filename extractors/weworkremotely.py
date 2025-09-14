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

    jobs = soup.find("div", id="search-results").find_all(
        "li", class_="new-listing-container")

    for job in jobs:
        title = job.find("h3", class_="new-listing__header__title")
        company = job.find("p", class_="new-listing__company-name")
        # skills = None
        url_tag = job.find("a", recursive=False)
        url = url_tag["href"]

        job_data = {
            "title": title.text,
            "company": company.text,
            "url": f"https://weworkremotely.com/{url}",
            # "skills": skills
        }
        all_jobs.append(job_data)


def extract_weworkremotely_jobs(keyword):
    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}"
    scrape_page(url)
    return all_jobs   

extract_weworkremotely_jobs('python')
print(all_jobs)