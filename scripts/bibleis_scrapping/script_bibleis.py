import os

def clear() :
	os.system('clear')
	return

clear()

url_patterns = [
	# 'https://live.bible.is/bible/BAMLSB/MAT/',
	# 'https://live.bible.is/bible/FRABIB/MAT/',
	# 'https://live.bible.is/bible/BAMLSB/MRK/',
	# 'https://live.bible.is/bible/FRABIB/MRK/',
	# 'https://live.bible.is/bible/BAMLSB/LUK/',
	# 'https://live.bible.is/bible/FRABIB/LUK/',
	# 'https://live.bible.is/bible/BAMLSB/JHN/',
	# 'https://live.bible.is/bible/FRABIB/JHN/',
	# 'https://live.bible.is/bible/BAMLSB/ACT/',
	# 'https://live.bible.is/bible/FRABIB/ACT/',
	# 'https://live.bible.is/bible/BAMLSB/ROM/',
	# 'https://live.bible.is/bible/FRABIB/ROM/',
	# 'https://live.bible.is/bible/BAMLSB/1CO/',
	# 'https://live.bible.is/bible/FRABIB/1CO/',
	# 'https://live.bible.is/bible/BAMLSB/2CO/',
	# 'https://live.bible.is/bible/FRABIB/2CO/',
	# 'https://live.bible.is/bible/BAMLSB/GAL/',
	# 'https://live.bible.is/bible/FRABIB/GAL/',
	# 'https://live.bible.is/bible/BAMLSB/EPH/',
	# 'https://live.bible.is/bible/FRABIB/EPH/',
	# 'https://live.bible.is/bible/BAMLSB/PHP/',
	# 'https://live.bible.is/bible/FRABIB/PHP/',
	# 'https://live.bible.is/bible/BAMLSB/COL/',
	# 'https://live.bible.is/bible/FRABIB/COL/',
	# 'https://live.bible.is/bible/BAMLSB/1TH/',
	# 'https://live.bible.is/bible/FRABIB/1TH/',
	# 'https://live.bible.is/bible/BAMLSB/2TH/',
	# 'https://live.bible.is/bible/FRABIB/2TH/',
	# 'https://live.bible.is/bible/BAMLSB/1TI/',
	# 'https://live.bible.is/bible/FRABIB/1TI/',
	# 'https://live.bible.is/bible/BAMLSB/2TI/',
	# 'https://live.bible.is/bible/FRABIB/2TI/',
	# 'https://live.bible.is/bible/BAMLSB/TIT/',
	# 'https://live.bible.is/bible/FRABIB/TIT/',
	# 'https://live.bible.is/bible/BAMLSB/PHM/',
	# 'https://live.bible.is/bible/FRABIB/PHM/',
	# 'https://live.bible.is/bible/BAMLSB/HEB/',
	# 'https://live.bible.is/bible/FRABIB/HEB/',
	# 'https://live.bible.is/bible/BAMLSB/JAS/',
	# 'https://live.bible.is/bible/FRABIB/JAS/',
	# 'https://live.bible.is/bible/BAMLSB/1PE/',
	# 'https://live.bible.is/bible/FRABIB/1PE/',
	'https://live.bible.is/bible/BAMLSB/2PE/',
	'https://live.bible.is/bible/FRABIB/2PE/',
	'https://live.bible.is/bible/BAMLSB/1JN/',
	'https://live.bible.is/bible/FRABIB/1JN/',
	'https://live.bible.is/bible/BAMLSB/2JN/',
	'https://live.bible.is/bible/FRABIB/2JN/',
	'https://live.bible.is/bible/BAMLSB/3JN/',
	'https://live.bible.is/bible/FRABIB/3JN/',
	'https://live.bible.is/bible/BAMLSB/JUD/',
	'https://live.bible.is/bible/FRABIB/JUD/',
	'https://live.bible.is/bible/BAMLSB/REV/',
	'https://live.bible.is/bible/FRABIB/REV/',
	]

nb_chapters = [
#28,28,
#16,16,
#24,24,
#21,21,
#28,28,
#16,16,
#16,16,
#13,13,
#6,6,
#6,6,
# 4,4,
# 4,4,
# 5,5,
# 3,3,
# 6,6,
# 4,4,
# 3,3,
# 1,1, #PHM
#13,13,
#5,5,
#5,5,
3,3,
5,5,
1,1,
1,1,
1,1,
22,22,
]


#url_patterns = ['https://live.bible.is/bible/BAMLSB/MAT/',	'https://live.bible.is/bible/FRABIB/MAT/']
#nb_chapters = [3,3]

assert len(nb_chapters) == len(url_patterns)

start_urls = []
for url_pattern,nb_chapter in zip(url_patterns,nb_chapters) :
  for i in range(1,nb_chapter+1,1) :
    start_urls.append(url_pattern+str(i))

#response.__dict__.keys()

k = 0
for url in start_urls :
	k+=1
	print(url)
	fetch(url)
	xp0 = 'div.main-wrapper div.chapter'
	for sub_block in response.css(xp0) : # page web / chapitre
		xp1 = 'span.drop-caps::text'
		sub_sub_block = sub_block.css(xp1)
		chapter = sub_sub_block.extract_first()
		#print("Chapter",chapter)
		xp1 = 'span.align-left span'
		sub_sub_block = sub_block.css(xp1)
		for sub_sub_sub_block in sub_sub_block :
		  xp2 = 'span::attr(data-verseid)'
		  verseid = sub_sub_sub_block.css(xp2).extract_first()
		  #print("VerseID",verseid)
		  xp2 = 'span::text'
		  verse = sub_sub_sub_block.css(xp2).extract_first()
		  #print(verse)
		  verse = verse.replace('\n',' ')
		  verse = " ".join(verse.split())
		  #data = {'book' : response.__dict__['_url'].split('/')[-2], 'chapter' : chapter, 'VerseID' : verseid, 'lang' : response.__dict__['_url'].split('/')[-3], 'verse':verse}
		  tmp = response.__dict__['_url'].split('/')
		  lang = tmp[-3]
		  book = tmp[-2]
		  data = f"[BOOK] {book} [CHAPTER] {chapter} [VERSE_ID] {verseid} [LANG] {lang} [VERSE] {verse}"
		  with open(f"{lang}_{book}.txt", "a+") as file :
			  file.write(data+"\n")
