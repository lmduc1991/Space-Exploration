from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re

# list to contain information
# ## link to every project
# detail_link=[]
 ## Organization detail
org_detail = []
## Location detail
location_detail=[]
## Date detail
date_detail = []
## project detail
project_detail = []
##rocket status
rocket_status_detail=[]
##Price detail
price_detail =[]
##Mission status
mission_status_detail=[]

# date_loc=[]
# n=10
# url_r = 'https://nextspaceflight.com'
# page = f'/launches/past/?page={n}&search='
# # homepage
# response = requests.get(url_r + page)
# web_res = response.text
# # Make soup
# soup = BeautifulSoup(web_res, 'html.parser')
# date_locations = soup.find(name='div', class_='mdl-card__supporting-text')
# p = date_locations.getText().strip().splitlines()
# print(p)
# m=0
# for i,item in enumerate(p):
#     item = item.strip()
#     p[i] = item
#     if item != '':
#         p[m] = item
#         m += 1
# print(p)

def get_data(n):
    detail_link=[]
    url_r = 'https://nextspaceflight.com'
    page = f'/launches/past/?page={n}&search='
    # homepage
    response = requests.get(url_r + page)
    web_res = response.text
    # Make soup
    soup = BeautifulSoup(web_res, 'html.parser')
    ## Find project detail
    project_title = soup.find_all(name='h5', class_='header-style')
    for project in project_title:
        project = project.get_text(strip=' ')
        project_detail.append(project)
    ##Find location and date
    date_locations = soup.find_all(name='div', class_='mdl-card__supporting-text')
    for dl in date_locations:
        m = 0
        dl_list = dl.getText().strip().splitlines()
        for i, item in enumerate(dl_list):
            item = item.strip()
            dl_list[i] = item
            if item != '':
                dl_list[m] = item
                m +=1
        date_inf = dl_list[0]
        loc_inf = dl_list[1]
        date_detail.append(date_inf)
        location_detail.append(loc_inf)
    ##Create link to every card
    button = soup.find_all(name='button', class_='mdc-button')
    for b in button:
        if b.get_text(strip=' ') == 'Details':
            access_path = b.get('onclick').split('=')[1]
            access_link = access_path.strip(' ').replace("'", "")
            detail_link.append(url_r + access_link)
        else:
            pass
    # access every link
    for l in detail_link:
        side_response = requests.get(l)
        side_res = side_response.text
        side_soup = BeautifulSoup(side_res, 'html.parser')
        # get the mission status
        mission_info = side_soup.find(name='h6', class_='status')
        mission_status = mission_info.get_text(strip=' ')
        mission_status_detail.append(mission_status)

        ##find the second card on website contain information about price, organisation and status
        all_card = side_soup.find_all(class_='mdl-card__supporting-text')
        #
        # ## get the Date information
        # date_inf = all_card[0].find(id='localized')
        # date_launch = date_inf.get_text(strip=' ')
        # date_detail.append(date_launch)
        #
        # ##get the location information
        # location_inf = all_card[4].find(name='h4', class_='mdl-card__title-text')
        # location_launch = location_inf.get_text(strip=' ')
        # location_detail.append(location_launch)

        ##get organization data, rocket status and price
        second_card = all_card[1].find_all(class_='mdl-cell')
        ###Get the organisation data
        organ_name = second_card[0].getText()
        org_detail.append(organ_name)
        ###Get the price
        e = second_card[2].getText()
        if "Price" in e:
            price_raw_inf = e.split(':')[1].strip(" ")
            price_num_inf = price_raw_inf.split(" ")[0].strip(' ')
            price_num_inf=price_num_inf.replace('$','')
            price_detail.append(price_num_inf)
        else:
            price_detail.append('na')
        ### get the rocket status
        for r in second_card:
            if "Status" in r.getText():
                status_inf = r.getText().split(':')[1].strip(" ")
                rocket_status_detail.append(status_inf)

for n in range(201,222):
    get_data(n)


# # print(detail_link)
# # print(len(detail_link))
print(org_detail)
print(len(org_detail))
print(location_detail)
print(len(location_detail))
print(date_detail)
print(len(date_detail))
print(project_detail)
print(len(project_detail))
print(rocket_status_detail)
print(len(rocket_status_detail))
print(price_detail)
print(len(price_detail))
print(mission_status_detail)
print(len(mission_status_detail))

dict= {'Organisation': org_detail,'Location': location_detail,
       'Date': date_detail, 'Detail': project_detail,
       'Rocket_status': rocket_status_detail,
       'Price': price_detail,
       'Mission_status': mission_status_detail}
#convert to dataframe
df = pd.DataFrame(dict)
df.index = np.arange(1, len(df)+1)
#convert to csv
csv = df.to_csv('mission_launch(201-221).csv')
