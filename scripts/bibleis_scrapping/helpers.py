# Créer un seul fichier par langue contenant tous les livres

from os import walk

files = []
books = []
for (dirpath, dirnames, filenames) in walk('.'):
    files.extend(filenames)
    break

for file in files :
  if file.split('_')[1] == 'BAMLSB.txt' :
    books.append(file.split('_')[0])

for book in books :
  with open(f'{book}_BAMLSB.txt','r') as f1 :
    verses = f1.readlines()
  with open(f'00_bambara.txt','a+') as f2 :
    f2.writelines(verses)
  with open(f'{book}_FRABIB.txt','r') as f3 :
    verses2 = f3.readlines()
  with open(f'00_francais.txt','a+') as f4 :
    f4.writelines(verses2)

###############################################################

# Vérifier l'alignement 

def check_final_alignment() :
  with open(f'00_bambara.txt','r') as f :
    verses = f.readlines()
    verses1 = verses
  with open(f'00_francais.txt','r') as f :
    verses = f.readlines()
    verses2 = verses
  k = 0
  for verse1, verse2 in zip(verses1,verses2) :
    k+=1
    x1 = int(verse1.split('[VERSE_ID]')[1][1:3])
    x2 = int(verse2.split('[VERSE_ID]')[1][1:3])
    if x1 != x2 :
      print(verse1)
      print(verse2)
      return
    else :
      print(k,'ligne alignée ok')

def check_alignment(book) :
  with open(f'{book}_FRABIB.txt','r') as f :
    verses = f.readlines()
    verses1 = verses
  with open(f'{book}_BAMLSB.txt','r') as f :
    verses = f.readlines()
    verses2 = verses
  for verse1, verse2 in zip(verses1,verses2) :
    x1 = int(verse1.split('[VERSE_ID]')[1][1:3])
    x2 = int(verse2.split('[VERSE_ID]')[1][1:3])
    if x1 != x2 :
      print(verse1)
      print(verse2)
      return
    else :
      print('ok')
