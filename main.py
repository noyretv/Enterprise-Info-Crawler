import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

FILENAME = os.environ.get("FILENAME", "统一社会信用代码.xlsx")
SEARCH_URL = "https://www.qcc.com/web/search"

HEADERS = {
    'upgrade-insecure-requests': '0',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Cookie': 'your_cookie_here'
}


def get_data_from_file():
    df = pd.read_excel(FILENAME)
    return tuple(df.iloc[:, 0])


def parse_table_data(details_soup):
    table = details_soup.find("table", {"class": "ntable"})
    tds = table.find_all('td')
    json_data = {}
    for i in range(len(tds) // 2):
        tds_key = tds[i * 2].text.strip()
        tds_value = tds[i * 2 + 1].text.strip().replace('\n', '').replace(' ', '')
        if tds_key == '经营者':
            tds_value = tds_value[1:tds_value.rfind('关联')]
        if tds_key == '经营场所':
            tds_value = tds_value.replace('附近企业', '')
        json_data[tds_key] = tds_value
    return json_data


def get_company_info(credit_code):
    my_ip = get_my_ip()

    params = {"key": credit_code}
    response = requests.get(SEARCH_URL, params=params, headers=HEADERS)

    if response.status_code != 200:
        print(f"查询失败，状态码：{response.status_code},请求ip:{my_ip}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    company_url = soup.find("a", href=re.compile("https://www.qcc.com/firm/"))

    if not company_url:
        print(f"未找到 {credit_code} 对应的企业详细信息,请求ip:{my_ip}")
        return None

    details_url = company_url['href']
    details_response = requests.get(details_url, headers=HEADERS)

    if details_response.status_code != 200:
        print(f"查询详细信息失败，状态码：{details_response.status_code},请求ip:{my_ip}")
        return None

    details_soup = BeautifulSoup(details_response.text, "html.parser")
    json_data = parse_table_data(details_soup)

    print(f"已爬取并处理 {credit_code} 的企业工商信息,请求ip:{my_ip}")
    return json_data

def get_my_ip(url="https://api.ipify.org"):
    response = requests.get(url)
    return response.text


def main():
    credit_codes = get_data_from_file()
    json_list = [get_company_info(code) for code in credit_codes]
    json_list = [data for data in json_list if data]

    if json_list:
        file_name = '企业工商信息.xlsx'
        if os.path.exists(file_name):
            df = pd.read_excel(file_name)
            new_data = pd.DataFrame(json_list)
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = pd.DataFrame(json_list)

        df.to_excel(file_name, index=False)
        print("数据已写入企业工商信息.xlsx")

if __name__ == "__main__":
    main()