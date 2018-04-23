#PURPOSE: SCRAPES ABRAHAM LINCOLN BRIGADES
#AUTHOR: SHOM MAZUMDER
#DATE FIRST CREATED: 04/23/2018
#DATE LAST UPDATED: 04/23/2018
#################################################################

#IMPORT PACKAGES
from selenium import webdriver #webscraping
from selenium.webdriver.common.keys import Keys
import pandas as pd #for dataframe creation
import numpy as np
import time #pausing between queries
import string


#INIT VARS
lincoln_url_main = "http://www.alba-valb.org/volunteers/browse/?b_start:int=0&-C=" #url for website that hosts BLM protest data info
cols = ['name','bio','url']
df = pd.DataFrame(columns = cols)


#INIT CHROMEBROWSER
browser = webdriver.Chrome() #initialize browser
browser.implicitly_wait(10) #wait until data on page loads
#browser.maximize_window() #expand broswer
browser.get(lincoln_url_main) #go to lincoln brigades site

pages = 134 #number of pages to iterate over

#function to get the name and bio for a given person on a given page
def get_name(index):
	xpath_person_name = '//*[@id="main_container"]/div[3]/div/div/div/div[3]/table/tbody/tr[' + str(index) + ']/td[2]/table/tbody/tr[1]/td[1]'
	person_name = browser.find_element_by_xpath(xpath_person_name).text
	return person_name

def get_bio(index):

	#start by finding the link and storing it
	xpath_person_link = '//*[@id="main_container"]/div[3]/div/div/div/div[3]/table/tbody/tr[' + str(index) + ']/td[2]/table/tbody/tr[1]/td[1]/strong/a'
	person_link = browser.find_elements_by_xpath(xpath_person_link)
	person_link_url = person_link[0].get_attribute('href')

	#now navigate to the link and grab the bio
	browser.get(person_link_url)
	#browser.implicitly_wait(10) #wait a bit for the data to populate

	#now get the bio (check to see if there's an image or not)
	if len(browser.find_elements_by_xpath('//*[@id="main_container"]/div[3]/div/div/div/div[3]/div[2]/p[2]')[0].text) >0:
		bio_element = browser.find_elements_by_xpath('//*[@id="main_container"]/div[3]/div/div/div/div[3]/div[2]/p[2]')
	else:
		bio_element = browser.find_elements_by_xpath('//*[@id="main_container"]/div[3]/div/div/div/div[3]/div[2]/p[4]')
	bio = bio_element[0].text

	return [bio,person_link_url]

#scrape
lincoln_base_url = "http://www.alba-valb.org/volunteers/browse/?b_start:int="
lincoln_end_url = "&-C="
for j in range(pages):
	lincoln_url = lincoln_base_url + str(j*20) + lincoln_end_url
	browser.get(lincoln_url)

	#get number of rows on page
	tot_row_count = len(browser.find_elements_by_xpath('//*[@id="main_container"]/div[3]/div/div/div/div[3]/table/tbody/tr'))
	num_rows_w_bio = tot_row_count - 2

	for i in range(num_rows_w_bio):
		row_num = i + 2
		name = get_name(row_num)
		bio = get_bio(row_num)

		name = name.encode('utf-8')
		biography = bio[0].encode('utf-8')
		#biography = bio[0].encode('utf-8').translate(None, string.punctuation)

		url = bio[1].encode('utf-8')

		# store features in a temporary dataframe
		temp_df = pd.DataFrame([{cols[0]: name,
			cols[1]: biography,
			cols[2]: url}], index=[0])

		#append data from this page to dataframe
		df = df.append(temp_df)

		#go back
		browser.back()
		time.sleep(5)


df.to_csv(path_or_buf = "~/Dropbox/ideas/lincoln-brigade/raw-brigades-data.csv", encoding = 'utf-8',index = False)


#browser.execute_script("window.history.go(-1)")

#get the link to click on for the person
#person_link = browser.find_elements_by_xpath('//*[@id="main_container"]/div[3]/div/div/div/div[3]/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[1]/strong/a')
#person_link_href = person_link[0].get_attribute('href')
#print(person_link_href)

#find name of person
#name = browser.find_element_by_xpath('//*[@id="main_container"]/div[3]/div/div/div/div[3]/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[1]')
#print(name.text)

#click on person
#browser.get(person_link_href)
#browser.implicitly_wait(10)

#now get the bio
#bio_element = browser.find_elements_by_xpath('//*[@id="main_container"]/div[3]/div/div/div/div[3]/div[2]/p[2]')
#print(bio_element[0].text)

#go back
#browser.execute_script("window.history.go(-1)")

#do the following for each page i
#for i in range(73):

	#grab relevant features from the data on the page
#	locations = pd.Series(get_feature(cols[0]))
#	dates = pd.Series(get_feature(cols[1]))
#	subjects = pd.Series(get_feature(cols[2]))
#	participants = pd.Series(get_feature(cols[3]))
#	times = pd.Series(get_feature(cols[4]))
#	descriptions = pd.Series(get_feature(cols[5]))
#	urls = pd.Series(get_feature(cols[6]))

	# store features in a temporary dataframe
#	temp_df = pd.DataFrame({cols[0]: locations,
#		cols[1]: dates,
#		cols[2]: subjects,
#		cols[3]: participants,
#		cols[4]: times,
#		cols[5]: descriptions,
#		cols[6]: urls})

	#append data from this page to dataframe
#	df = df.append(temp_df)

	#click to go to next page
#	browser.find_element_by_xpath("//*[@id=\"blm-results\"]/div[1]/ul/li[4]").click()

	#wait 10 seconds
#	time.sleep(5)

#close chrome browser
browser.quit()

#output data to csv
#df.to_csv(path_or_buf = "~/Dropbox/policing_protest/BLM_scraper/BLM_raw_out.csv", encoding = 'utf-8')

