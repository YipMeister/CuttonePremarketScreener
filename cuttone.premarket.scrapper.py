import requests
from bs4 import BeautifulSoup
import time
import re
import numpy as np
import pandas as pd
from datetime import date

def main():
	today = date.today()
	newpage = ''
	def link_grab(site):
		page =  requests.get(site)
		soup = BeautifulSoup(page.text, 'html.parser')
		maintext = soup.find('div', "site-content")
		cuttone = maintext.find('a', text = 'Cuttone Morning Market Overview and Recap – CUTN/SUPR')
		if cuttone == None:
			return link_grab('http://10.10.90.208/tip/page/2/')
		else:
			newpage = str(cuttone.get('href'))
			return newpage

	def Tickers_today(MorningReportSite):
		page = requests.get(MorningReportSite)
		soup = BeautifulSoup(page.text, 'html.parser')
		companynamepattern = re.compile('.+?(?=[ ][(])')
		tickerpattern = re.compile('\((.*?)\)')
		analystratingpattern = re.compile('(?<=\) )(.*)(?= at)')
		analystcompanypattern = re.compile('(?<=at )(.*)(?=;)')
		pricetargetpattern = re.compile('(?<=\$)(.*)')
		companyname_list = []
		tickername_list = []
		analyst_rating_list = []
		analyst_company_list = []
		price_target_list = []
		maintext = soup.find_all('ul', type = 'disc')
		return maintext

	def Scraper(raw_text):
		companynamepattern = re.compile('.+?(?=[ ][(])')
		tickerpattern = re.compile('\((.*?)\)')
		analystratingpattern = re.compile('(?<=\) )(.*)(?= at)')
		analystcompanypattern = re.compile('(?<=at )(.*)(?=;)')
		analystcompanypattern_noPT = re.compile('(?<=at )(\w+)$')
		analystcompanypattern_noPT_2 = re.compile('(?<=at )(\w+)( )(\w+)$')
		pricetargetpattern = re.compile('(?<=\$)(.*)')
		companyname_list = []
		tickername_list = []
		analyst_rating_list = []
		analyst_company_list = []
		price_target_list = []	
						
		for lines in raw_text:
			liner_li = lines.find_all('li', class_= 'MsoNormal')
			for inside in liner_li:
				insidetext = inside.text
				print(insidetext)
				if 'Annual general meeting' in insidetext:
					continue
				if 'Other events:' in insidetext:
					continue
				if 'Sales results:' in insidetext:
					continue
				if 'Other/M&A:' in insidetext:
					continue
				if 'Earnings Calls:' in insidetext:
					continue
				companyname = str(companynamepattern.findall(insidetext))
				companyname = companyname.replace("[' ", '')
				companyname = companyname.replace("']", '')
				tickername = str(tickerpattern.findall(insidetext))
				tickername = tickername.replace("['", '')
				tickername = tickername.replace("']", '')
				tickername = tickername.replace(' CN','') # replacing CN in canada
				analyst_rating = str(analystratingpattern.findall(insidetext))
				analyst_rating = analyst_rating.replace("['", '')
				analyst_rating = analyst_rating.replace("']", '')
				analyst_rating = analyst_rating.replace("rated ", '')
				analyst_company = str(analystcompanypattern.findall(insidetext))
				analyst_company = analyst_company.replace("['", '')
				analyst_company = analyst_company.replace("']", '')
				
				if str(analystcompanypattern.findall(insidetext)):
					if len(str(analystcompanypattern.findall(insidetext))) == 2:
						if len(str(analystcompanypattern_noPT.findall(insidetext))) > 2:
							analyst_company = str(analystcompanypattern_noPT.findall(insidetext))	
						else:
							analyst_company = str(analystcompanypattern_noPT_2.findall(insidetext))
							analyst_company = analyst_company.replace("[('", "")
							analyst_company = analyst_company.replace("', ' ', '", "")
							analyst_company = analyst_company.replace("')]", "")
						analyst_company = analyst_company.replace("['", '')
						analyst_company = analyst_company.replace("']", '')
					else:
						print(len(str(analystcompanypattern.findall(insidetext))))
						analyst_company = str(analystcompanypattern.findall(insidetext))
						analyst_company = analyst_company.replace("['", '')
						analyst_company = analyst_company.replace("']", '')
						print(analyst_company)
				price_target = str(pricetargetpattern.findall(insidetext))
				price_target = price_target.replace("['", '')
				price_target = price_target.replace("']", '')
				
				companyname_list.append(companyname)
				tickername_list.append(tickername)
				analyst_rating_list.append(analyst_rating)
				analyst_company_list.append(analyst_company)
				price_target_list.append(price_target)
		print(companyname_list, tickername_list, analyst_rating_list, analyst_company_list, price_target_list)
		
		return_dict = {'Company Name': companyname_list,
		'Ticker Name': tickername_list,
		'Analyst Rating': analyst_rating_list,
		'Rating Company': analyst_company_list,
		'Price Target': price_target_list}

		return return_dict


	def premarketpricer(ticker_symbol):
		hi_price = []
		lo_price = []
		premarketvolume = []
		for singlesymbol in ticker_symbol:
			print(singlesymbol)
			try:
				pm2_page = 'http://old.nasdaq.com/symbol/'+ singlesymbol +'/premarket'
				pm2_pagereq = requests.get(pm2_page)
				pm2_soup = BeautifulSoup(pm2_pagereq.text, 'html.parser')   
				pm2_hiprice = pm2_soup.find('span', id='quotes_content_left_lblHighprice')
				pm2_loprice = pm2_soup.find('span', id='quotes_content_left_lblLowprice')
				pm2_premarketvol = pm2_soup.find('span', id='quotes_content_left_lblVolume')
				pm2_hiprice = (pm2_hiprice.text).replace('$ ','')
				pm2_loprice = (pm2_loprice.text).replace('$ ','')
				pm2_premarketvol = (pm2_premarketvol.text).replace(',','')
				
				print(pm2_hiprice)
				print(pm2_loprice)
				print(pm2_premarketvol)

				hi_price.append(pm2_hiprice)
				lo_price.append(pm2_loprice)
				premarketvolume.append(pm2_premarketvol)

			except AttributeError:
				hi_price.append('')
				lo_price.append('')
				premarketvolume.append('')
				continue
			print(hi_price,lo_price,premarketvolume)
			return_dict_premarket = {'Premarket High': hi_price,
			'Premarket Low': lo_price,
			'Premarket Volume': premarketvolume}

		return (return_dict_premarket)

								
	webpage = "http://10.10.90.208/tip/"
	newpage = link_grab(webpage)
	maintextscraped = Tickers_today(newpage)
	scrapped_dict = Scraper(maintextscraped)
	print(scrapped_dict)
	prepared_tickers = scrapped_dict['Ticker Name']
	premarket_info = premarketpricer(prepared_tickers)
	print(premarket_info)
	combined_dict = {**scrapped_dict, **premarket_info}
	
	df = pd.DataFrame(combined_dict, columns = ['Company Name', 'Ticker Name', 'Analyst Rating', 'Rating Company','Price Target','Premarket High','Premarket Low','Premarket Volume'])
	print(df)
	df.to_excel(str(today)+'cuttonereport.xlsx', sheet_name ='sheet1', index = False)

	
if __name__=='__main__':
	main()


'''


'''
