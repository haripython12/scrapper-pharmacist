import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import csv
import os
import re

SEARCH_URL = "https://idbop.mylicense.com/verification/Search.aspx"
SEARCH_RESULTS_URL = "https://idbop.mylicense.com/verification/SearchResults.aspx"
USER_DETAILS_URL = "https://idbop.mylicense.com/verification/"


# -------------- Main Starts Here ------------- #
'''
STEPS:
	1. Start a session by requesting to search page
	2. Request with form data to search page get results
	3. Create a list of all available pages (pagination)
	4. Loop over all pages
	5. Save all user's data to csv
'''

#################################################################
# Request to SEARCH_URL to start session
session = requests.session()
response = session.post(SEARCH_URL)

#################################################################
# Request with form_data to get results for query & create a list
# of pagination

input_value_last_name = "L"
payload = {
	"__EVENTTARGET": "",
	"__EVENTARGUMENT": "",
	"__LASTFOCUS": "",
	"__VIEWSTATE": "/wEPDwUJNzM2NTgwNzkyD2QWAgIBD2QWAmYPZBYCAgEPZBYCAgEPZBYCAgEPZBYGAgQPZBYCAgEPZBYCZg8QZGQWAWZkAgcPZBYCAgMPZBYCZg8QZGQWAWZkAggPZBYCAgEPZBYCZg8QZGQWAWZkZJ5q3J0dw03/5HffG5EFxOMrDBg2WFHCzJt+mz3mmQ6J",
	"__VIEWSTATEGENERATOR": "85FE3531",
	"__EVENTVALIDATION": "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",
	"t_web_lookup__first_name": "",
	"t_web_lookup__license_type_name": "",
	"t_web_lookup__last_name": input_value_last_name,
	"t_web_lookup__addr_city": "",
	"t_web_lookup__license_no": "",
	"t_web_lookup__addr_state": "",
	"t_web_lookup__license_status_name": "",
	"t_web_lookup__addr_county": "",
	"t_web_lookup__addr_zipcode": "",
	"sch_button": "Search"
}
response = session.post(SEARCH_URL, data=payload, cookies=session.cookies)
first_search_results_html = BeautifulSoup(response.text, 'html.parser')
href_tags = [data['href'] for data in first_search_results_html.select("font a")]
pagination_list = [re.search(r"(datagrid_results\$.*,)", link).group()[:-2] for link in href_tags if"__doPostBack('datagrid_results" in link]

all_users_info = []



#################################################################
# Extract user's required information from detail page

def extract_user_info(detail_page_url, payload, cookie):
	# Required_info
	required_user_info = {'ctl1_first_name', 'ctl1_m_name', 'ctl1_last_name', 'ctl1_license_no', 'ctl1_license_type','ctl1_status', 'ctl1_issue_date', 'ctl1_expiry', 'ctl1_last_ren'}

	def filter_required_data(all_available_data):
		user_info = {}
		for data in all_available_data:
			try:
				split_id_name = data['id'].split('__')
				if split_id_name[1] in required_user_info:
					user_info[split_id_name[1]] = data.get_text()
			except Exception as e:
				pass
		return user_info

	# Request to detail page
	response = session.post(detail_page_url, data=payload, cookies=cookie)
	detail_page = BeautifulSoup(response.text, 'html.parser')
	all_available_data = detail_page.find_all("span")

	return filter_required_data(all_available_data)



#################################################################
# Write all data for all users from all pages to csv

def write_to_csv(data):
	with open('result.csv', 'w+') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(
			['first_name', 'm_name', 'last_name', 'license_no', 'license_type', 'status', 'issue_date', 'expiry',
			 'last_ren'])
		try:
			for user_dict in tqdm(data):
				writer.writerow([user_dict['ctl1_first_name'], user_dict['ctl1_m_name'], user_dict['ctl1_last_name'],
								 user_dict['ctl1_license_no'], user_dict['ctl1_license_type'], user_dict['ctl1_status'],
								 user_dict['ctl1_issue_date'], user_dict['ctl1_expiry'], user_dict['ctl1_last_ren']])
		except Exception as e:
			print '[ERROR: write_to_csv()]' + str(e)

#################################################################
# Loop over all pages

for index, page in enumerate(pagination_list):

	if index == 0:
		search_results_html = first_search_results_html
	else:
		payload = {
			"__EVENTTARGET": page,
			"__VIEWSTATE": "/wEPDwUJNzM2NTgwNzkyD2QWAgIBD2QWAmYPZBYCAgEPZBYCAgEPZBYCAgEPZBYCAgIPZBYCZg9kFgJmDxQrAAsPFhgeE0F1dG9HZW5lcmF0ZUNvbHVtbnNoHghQYWdlU2l6ZQIoHhNVc2VBY2Nlc3NpYmxlSGVhZGVyZx4HQ2FwdGlvbgUHUmVzdWx0cx4LXyFJdGVtQ291bnQCKB4IRGF0YUtleXMWAB4Jc29ydF9uYW1lBQRERVNDHhBDdXJyZW50U29ydE9yZGVyBQ1zb3J0X25hbWUgQVNDHhVfIURhdGFTb3VyY2VJdGVtQ291bnQC8w4eCVBhZ2VDb3VudAIwHgxBbGxvd1NvcnRpbmdnHgtBbGxvd1BhZ2luZ2dkZBYMHghQb3NpdGlvbgsqJ1N5c3RlbS5XZWIuVUkuV2ViQ29udHJvbHMuUGFnZXJQb3NpdGlvbgAeBE1vZGULKiNTeXN0ZW0uV2ViLlVJLldlYkNvbnRyb2xzLlBhZ2VyTW9kZQEeD1BhZ2VCdXR0b25Db3VudAIoHglCYWNrQ29sb3IJdVNK/x4JRm9yZUNvbG9yCqQBHgRfIVNCAoyAoAYWBB8PCXVTSv8fEQIIZGRkZGRkZGRkRtCXKFxPronD0XkiQqXXsmmpZHeTGqpZpV/OO7K9lvI=",
			"__VIEWSTATEGENERATOR": "3731BCAC",
			"__EVENTVALIDATION": "/wEdACvKrYBRANOgvJYF3bBCOVu7Qwjb7dpaSQmPwtIuHjurAHFMAHrsd5b8+Xvbgnxy7bXrXDnHS0qGT9msBN4gT1V60Jzo/EEl4DFlyzKmMrEoR5Sm395/bdx8igU/gNBvIfUu45Lveq2EnNqnozsqglkUblEmKU1BKZPW+G8orkM5bdDYhLLV4KBEYuAGQBDfY5bwwUXmNmGpr9Ix904e+N1uIwhRQKnqgU1jLPrSapDyZ2PVXEivPaVLQfxbUmFX6rEJbrTCKjebiUFO0WdsgTwLsL34jqdPZTqZjvdGJAPz7Y6gaHZjH0Tvm4QMeb65GF6J9kZ6h9Wm572E4APoh7A/1DYAunntbhXkvN7xllPdv9fVEH7f+9ltxA+428xQPHJeeysypqiYU/RNIfOJg09+xGYEqVrwP6Kyy/RlmZciKWa+2lU/E+KshBy6yVIeghUf07sMwRuOyYyCFY/JnH2nLWxWFBrG3aZy2pLZjFoQxL/iGm/HWmI1c/NVUJnoVzTd5pLXBEscHCT/IzcFDRVq3qQyP9SmVtDzqHv/41rjcjsvbk4CAAHUzmH9SFobXS+ggKZl8oHo9IPPciqq4wN/MCiC37pyM1+DFD56R9nYCwpKJN2SOjX40iHG1dR6gWmnyCiTyh+Tf0m/Prt29wXgG2mYRHKiPoSgZOT1xmxFshoyPmrlHWBpTYYZeOq7KG0rdZc35j901BsuCjzDNOx0M3M3KMBGwXS4Jyuc3ix4APxwzcEgtof+34QjfptoeFgvtLEy1vWDNH8HUXPW4PP9uLBzNI+0oFKNgk2sIQ3whCoy+kM7WQQ6xvAA+FqGEZJQ+hvcXtjc8eA2SSjBjpDw9LeKN9xPxVQmBk8YXWckVDo8Z1R0dtEvPbZq37B8Xv/8QXpMlCMTD1IpCvsW9UKZ6fp/2SWA8Vwt+eylN4UaBADlI14y6TfPayrJ35tw4T8="
		}
		response = session.post(SEARCH_RESULTS_URL, data=payload, cookies=session.cookies)
		search_results_html = BeautifulSoup(response.text, 'html.parser')

	href_tags = [data['href'] for data in search_results_html.select("td a")]
	users_detail_pages = [str(USER_DETAILS_URL + link) for link in href_tags if "Details.aspx?result=" in link]

	for detail_page_url in tqdm(users_detail_pages):
		user_info = extract_user_info(detail_page_url, payload, session.cookies)
		all_users_info.append(user_info)

#################################################################
# Write all data to csv now
write_to_csv(all_users_info)


