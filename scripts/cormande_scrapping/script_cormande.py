import xml.etree.ElementTree as ET
import bisect
import re

path = r'cormande/data_xml/'
files = [
    'aimer.xml',
    'aller.xml',
    'alors.xml',
    'au.xml',
    'autre.xml',
    'avec.xml',
    'avoir.xml',
    'bien.xml',
    'ce.xml',
    'cela.xml',
    'celui.xml',
    'chose.xml',
    'comme.xml',
    'croire.xml',
    'dans.xml',
    'de.xml', # 39981
    'deux.xml',
    'devoir.xml',
    'dire.xml',
    'donner.xml',
    'du.xml',
    'elle.xml',
    'en.xml',
    'est.xml',
    'et.xml',
    'faire.xml',
    'falloir.xml',
    'femme.xml',
    'grand.xml',
    'homme.xml',
    'il.xml',
    'jamais.xml',
    'je.xml', # 5893
    'jour.xml',
    'le.xml', # 57762
    'leur.xml',
    'lui.xml',
    'main.xml',
    'mais.xml',
    'me.xml',
    'mettre.xml',
    'moi.xml',
    'mon.xml',
    'n.xml',
    'ne.xml',
    'non.xml',
    'notre.xml',
    'nous.xml',
    'on.xml',
    'ou.xml',
    'par.xml',
    'parler.xml',
    'pas.xml',
    'passer.xml',
    'plus.xml',
    'pour.xml',
    'pouvoir.xml',
    'prendre.xml',
    'puis.xml',
    'qu.xml',
    'quand.xml',
    'que.xml',
    'qui.xml',
    'regarder.xml',
    'sans.xml',
    'savoir.xml',
    'se.xml',
    'si.xml',
    'son.xml',
    'sous.xml',
    'sur.xml',
    'te.xml',
    'temps.xml',
    'ton.xml',
    'toujours.xml',
    'tout.xml',
    'trouver.xml',
    'tu.xml',
    'un.xml',
    'venir.xml',
    'vie.xml',
    'voir.xml',
    'votre.xml',
    'vouloir.xml',
    'vous.xml',
    'y.xml',
    'yeux.xml',
]

pairs = set()
pairs_l = []
nb_rest = 0
nb_concern = 0

################################################################################

def print_direct_childs(root) :
    for elem in root:
        print(child.tag, child.attrib)

def print_all_tree(root) :
    for elem in root.iter() :
        print(elem.tag)


def create_alignement(root) :

    global pairs
    global pairs_l

    tag_fr = '[FR_COR]'
    tag_bam = '[BAM_COR]'
    for parallel_lines in root.iter('parallel_lines') :
        pair = tag_fr
        for parline in parallel_lines :
            phrase = ''
            for balise in parline :
                if balise.tag == 'ref' :
                    continue
                if balise.text is not None :
                    phrase += balise.text
            phrase = phrase.replace('\n',' ')
            phrase = " ".join(phrase.split())
            pair += phrase + tag_bam
        pair = pair[:-len(tag_bam)]
        pairs_l.append(pair)
        pairs.add(pair)

    return pairs,pairs_l

def remove_balises(s) :
    s = re.sub('<[^>]+>','',s)
    return s

def find_number(s) :
    match = re.findall(r"\d+\s*\)", s)
    return match

def ends_with_period(string):
    pattern = r"\.\s*$"
    return bool(re.search(pattern, string))

def similar_size(fr,bam) :
    size_fr = len(fr.split())
    size_bam = len(bam.split())
    return (min([size_fr,size_bam]) / max([size_fr,size_bam])) > 0.5


def select_first_sentence(s,lang) :


    s = s.replace(lang,'')
    s += '<!'
    pattern = r"([^.!?:]*[.!?:])"
    sentences = re.findall(pattern, s)
    # tri des phrases par longueur

    if not len(sentences) :
        s = s.replace('<!','')
        return lang+s

    sorted_sentences = sorted(sentences, key=len, reverse=True)
    # récupération de la première phrase, qui est la plus longue
    longest_sentence = sorted_sentences[0]
    longest_sentence = longest_sentence.replace('<!','')
    return lang+longest_sentence

def preprocess_number(fr,bam) :

    fr = fr.replace('[FR_COR]','')
    bam = bam.replace('[BAM_COR]','')
    numbers_par_fr = find_number(fr)
    numbers_par_fr = ['-1'] + numbers_par_fr
    numbers_par_bam = find_number(bam)
    numbers_par_bam = ['-1'] + numbers_par_bam


    if len(numbers_par_fr) == 1 or len(numbers_par_bam) == 1 :
        return '[FR_COR]'+fr,'[BAM_COR]'+bam

    # Les deux sont strictement supérieurs à 1
    split_fr = re.split(r"\d+\s*\)",fr)
    fr_dict = { key : val for key,val in zip(numbers_par_fr,split_fr)}

    split_bam = re.split(r"\d+\s*\)",bam)
    bam_dict = { key : val for key,val in zip(numbers_par_bam,split_bam)}

    for k,v in fr_dict.items() :
        if k == '-1' : continue
        v2 = bam_dict.get(k,None)
        if v2 is None : continue
        fr = '[FR_COR]'+v
        bam = '[BAM_COR]'+v2
        return fr,bam

    # Si il y a des patterns XXXX ) dans fr et bam, mais qu'aucun ne matchent.
    return None,None

def filter() :

    global pairs
    global pairs_l
    global nb_rest
    global nb_concern

    file_fr = open(f"cormande/FR_COR_processed.txt", "w")
    file_bam = open(f"cormande/BAM_COR_processed.txt", "w")

    print_freq = 10000
    for pair in pairs :

        fr = pair.split('[BAM_COR]')[0]
        bam = '[BAM_COR]'+pair.split('[BAM_COR]')[1]

        # if not "pour un python" in fr :
        #     continue

        if nb_concern % print_freq == 0 :
            print('+--------------------------------------------+')
            print("Exemple de processing :")
            print("",fr)
            print("",bam)
            print("\n")

        fr = remove_balises(fr)
        bam = remove_balises(bam)

        if nb_concern % print_freq == 0 :
            print("\tSupprimer les '<balises>' :")
            print("\t",fr)
            print("\t",bam)
            print("\n")

        fr,bam = preprocess_number(fr,bam)

        if nb_concern % print_freq == 0 :
            print("\t\tTraiter les pattern 'XXXX )' :")
            print("\t\t",fr)
            print("\t\t",bam)
            print("\n")

        if fr is None and bam is None :
            pass
        else :
            fr = select_first_sentence(fr,'[FR_COR]')
            bam = select_first_sentence(bam,'[BAM_COR]')
            if nb_concern % print_freq == 0 :
                print("\t\t\tGarder la phrase la plus longue :")
                print("\t\t\t",fr)
                print("\t\t\t",bam)
                print("\n")
            if not similar_size(fr,bam) :
                fr = None
                bam = None

        if nb_concern % print_freq == 0 :
            print("\t\t\t\tSupprimer la paire si la différence de taille est siginicative :")
            print("\t\t\t\t",fr)
            print("\t\t\t\t",bam)
            print("\n")

        nb_concern += 1
        if fr is not None and bam is not None :
            nb_rest += 1
            file_fr.write(fr+"\n")
            file_bam.write(bam+"\n")

    assert(nb_concern == len(pairs))
    print("Paires scrappées (overlap possible)",len(pairs_l),"\nPaires uniques",len(pairs),"\nPaires restantes après processing",nb_rest)
    file_fr.close()
    file_bam.close()

def save_as_file() :
    global pairs
    with open(f"cormande/FR_BAM_COR.txt", "w") as file :
        for pair in pairs :
            file.write(pair+"\n")

################################################################################

if __name__ == '__main__':

    for file in files :
        file = path+file
        tree = ET.parse(file)
        root = tree.getroot()
        create_alignement(root)

    save_as_file()
    filter()
