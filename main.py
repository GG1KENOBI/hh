import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json
from scrapy import Selector

def get_links(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f'https://hh.ru/search/resume?area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=true&from=employer_index_header&text={text}&page=1',
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        page_count = int(
            soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find(
                "span").text)
    except:
        return
    for page in range(page_count + 1):
        try:
            data = requests.get(
                url=f'https://hh.ru/search/resume?area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=true&from=employer_index_header&text={text}&page={page}',
                headers={"user-agent": ua.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, 'lxml')
            for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                yield f'https://hh.ru{a.attrs["href"].split("?")[0]}'
        except Exception as e:
            print(f"{e}")


def get_resume(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        name = soup.find(attrs={"class":"resume-block__title-text"}).text
    except:
        name = ''
    try:
        salary = soup.find(attrs={"class":"resume-block__salary"}).text.replace('\u2009', ' ').replace('\xa0', ' ')
    except:
        salary = ''
    try:
        tags_skills = [tag.text for tag in soup.find(attrs={"class":"bloko-tag-list"}).find_all(attrs={'class':'bloko-tag__section_text'})]
    except:
        tags_skills = []
    try:
        sel = Selector(text=data.text)
        info = [' '.join(sel.css('#a11y-main-content > div.resume-header-title > p > span:nth-child(1)::text').extract()),
                ' '.join(sel.css('#a11y-main-content > div.resume-header-title > p > span:nth-child(2) > span::text').extract()).replace('\xa0', ''),
                ' '.join(sel.css('.resume-header-title > p:nth-child(3) > span:nth-child(3) > span:nth-child(1)::text').extract()).replace('\xa0', ' '),]
    except:
        info = []
    try:
        personal_address = sel.css('.bloko-translate-guard > p:nth-child(1) > span:nth-child(1)::text').extract()
    except:
        personal_address = []
    try:
        experience = ' '.join(sel.css('.resume-wrapper > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h2:nth-child(1) > span:nth-child(1) > span:nth-child(1)::text').extract()).replace('\xa0', ' ')
    except:
        experience = []
    # try:
    #     work1 = [
    #         ' '.join(sel.css('#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content.main-content_broad-spacing > div > div:nth-child(2) > div > div > div.resume-wrapper > div > div > div.bloko-gap.bloko-gap_top > div:nth-child(2) > div.resume-block-item-gap > div > div:nth-child(1) > div > div.bloko-column.bloko-column_xs-4.bloko-column_s-2.bloko-column_m-2.bloko-column_l-2::text').extract()).replace('\xa0', ' '),
    #         ' '.join(sel.css('#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content.main-content_broad-spacing > div > div:nth-child(2) > div > div > div.resume-wrapper > div > div > div.bloko-gap.bloko-gap_top > div:nth-child(2) > div.resume-block-item-gap > div > div:nth-child(1) > div > div.bloko-column.bloko-column_xs-4.bloko-column_s-2.bloko-column_m-2.bloko-column_l-2 > div > span:nth-child(1)::text').extract()).replace('\xa0', ' '),
    #         ' '.join(sel.css('#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content.main-content_broad-spacing > div > div:nth-child(2) > div > div > div.resume-wrapper > div > div > div.bloko-gap.bloko-gap_top > div:nth-child(2) > div.resume-block-item-gap > div > div:nth-child(1) > div > div.bloko-column.bloko-column_xs-4.bloko-column_s-2.bloko-column_m-2.bloko-column_l-2 > div > span:nth-child(2)::text').extract()).replace('\xa0', ' '),
    #         ' '.join(sel.css('#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content.main-content_broad-spacing > div > div:nth-child(2) > div > div > div.resume-wrapper > div > div > div.bloko-gap.bloko-gap_top > div:nth-child(2) > div.resume-block-item-gap > div > div:nth-child(1) > div > div.bloko-column.bloko-column_xs-4.bloko-column_s-6.bloko-column_m-7.bloko-column_l-10 > div > div:nth-child(1) > a::text').extract()).replace('\xa0', ' '),
    #         ' '.join(sel.css('#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content.main-content_broad-spacing > div > div:nth-child(2) > div > div > div.resume-wrapper > div > div > div.bloko-gap.bloko-gap_top > div:nth-child(2) > div.resume-block-item-gap > div > div:nth-child(1) > div > div.bloko-column.bloko-column_xs-4.bloko-column_s-6.bloko-column_m-7.bloko-column_l-10 > div > p::text').extract()).replace('\xa0', ' '),
    #         ' '.join(sel.css('#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > div.main-content.main-content_broad-spacing > div > div:nth-child(2) > div > div > div.resume-wrapper > div > div > div.bloko-gap.bloko-gap_top > div:nth-child(2) > div.resume-block-item-gap > div > div:nth-child(1) > div > div.bloko-column.bloko-column_xs-4.bloko-column_s-6.bloko-column_m-7.bloko-column_l-10 > div > div:nth-child(4)::text').extract()).replace('\xa0', ' '),
    #     ]
    # except:
    #     work1 = []
    try:
        about_me = [tag.text for tag in soup.find(attrs={"data-qa":"resume-block-skills"})]
    except:
        about_me = []
    try:
        edu = [tag.text for tag in soup.find(attrs={"data-qa":"resume-block-education"}).find_all(attrs={'data-qa':'resume-block-education-item'})]
    except:
        edu = []
    try:
        languages = [tag.text for tag in soup.find(attrs={"data-qa":"resume-block-languages"}).find_all(attrs={'data-qa':'resume-block-language-item'})]
    except:
        languages = []
    try:
        nationality = [tag.text for tag in soup.find(attrs={"data-qa":"resume-block-additional"})]
    except:
        nationality = []
    try:
        exp = [tag.text.replace('\n', ' ').replace('\xa0',' ') for tag in soup.find(attrs={"data-qa":"resume-block-experience"}).find_all(attrs={'class':'resume-block-item-gap'})]
    except:
        exp = []
    try:
        add_edu = [tag.text.replace('\n', ' ').replace('\xa0',' ') for tag in soup.find(attrs={"data-qa":"resume-block-additional-education"}).find_all(attrs={'class':'resume-block-item-gap'})]
    except:
        add_edu = []
    resume = {
        "name": name,
        "info": info,
        "edu": edu,
        "add_edu": add_edu,
        "salary": salary,
        "personal_address": personal_address,
        "experience": experience,
        "exp": exp,
        "about_me": about_me,
        "tags_skills": tags_skills,
        "languages": languages,
        "nationality": nationality,
        "url": link,
    }
    return resume

if __name__ == '__main__':
    data = []
    for a in get_links("python"):
        data.append(get_resume(a))
        with open('hh_data_new.json', "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

