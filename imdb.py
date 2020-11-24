from bs4 import BeautifulSoup
import urllib.request
import csv
import time

urlpage="https://www.imdb.com/chart/top/?sort=ir,desc&mode=simple&page=1"

# query the website and return the html to the variable 'page'
page = urllib.request.urlopen(urlpage)
# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')
# find results within table
table = soup.find('tbody', attrs={'class': 'lister-list'})
results = table.find_all('tr')
print('Number of results', len(results))

rows = [] 
rows.append(['Titre','titre original','date','note IMDB','note rottentomatoes 1','note rottentomatoes 2'])
print(rows)

for result in results:
	film=[]
	titre=result.find('td',attrs={'class':'titleColumn'}).find('a').getText()
	film.append(titre)
	url=result.find('td',attrs={'class':'titleColumn'}).find('a')['href']
	
	

	pageDetail= urllib.request.urlopen('https://www.imdb.com/'+url)
	soupDetail = BeautifulSoup(pageDetail, 'html.parser')
	originalTitle=''

	try :
		originalTitle=soupDetail.find('div', attrs={'class':'originalTitle'}).getText() 
		originalTitle=originalTitle.replace(' (original title)','')
	except :
		originalTitle=titre
		
	film.append(originalTitle)
	date=result.find('td',attrs={'class':'titleColumn'}).find('span',attrs={'class':'secondaryInfo'}).getText()
	date=date.replace('(','')
	date=date.replace(')','')
	film.append(date)

	note=result.find('td',attrs={'class':'ratingColumn imdbRating'}).getText()
	note=note.replace('\n','')
	film.append(note)

	try:
		urlRT='\nhttps://www.rottentomatoes.com/m/'+originalTitle.replace(' ','_').replace(':','').replace(',','').replace("'",'')
		print(urlRT)
		pageRT=urllib.request.urlopen(urlRT)
		soupRT=BeautifulSoup(pageRT, 'html.parser')
		noteRT=soupRT.find_all('span',attrs={'class':'mop-ratings-wrap__percentage'})
		noteRT1=noteRT[0].getText()
		noteRT1=noteRT1.replace('\n','').replace(' ','').replace('%','')
		noteRT2=noteRT[1].getText()
		noteRT2=noteRT2.replace('\n','').replace(' ','').replace('%','')

	except Exception as e:
		print(e)
		print('\n')
		noteRT1=0
		noteRT2=0
	

	film.append(noteRT1)
	film.append(noteRT2)
	print(film)
	rows.append(film)
	time.sleep(1)


# Create csv and write rows to output file
with open('filmratings.csv','w', newline='') as f_output:
	csv_output = csv.writer(f_output)
	csv_output.writerows(rows)