__author__ = 'alexandre cavalcante'

from os import listdir
from lxml import etree
from collections import OrderedDict
import time,re

my_path = '/home/alexandre/workspace/semantiweb/CORPUS_COMPLETO'

log = open('./BASE_TESTE/log_treat_XML.txt', 'w')

count_file = 1
resultat = open('./BASE_TESTE/RESULTADOS/resultat_1.txt', 'w')
user_list = open('./BASE_TESTE/user_list.txt', 'w')

# ler lista de profissoes
file_prof_list = open('/home/alexandre/python_projects/Semantic_Web/BASE_TESTE/lista_profissoes_regex.txt', 'r')


# creer liste de professions
list_professions = []
for i in file_prof_list:
    if not i in list_professions:
        list_professions.append(i)


# ler lista de adjetivos
file_adj_list = open('/home/alexandre/python_projects/Semantic_Web/BASE_TESTE/lista_adjetivos_regex.txt', 'r')

# cree list de adjetifs
list_adjecfis = []
for i in file_adj_list:
    if not i in list_adjecfis:
        list_adjecfis.append(i)

# creer sortier web

web_file = open('./BASE_TESTE/interventions_par_intervenants.html', 'w')
count_sortie_web = 0


# cette liste controle les noms qu`on déjà été vérifiés pour ecrire le fichier de noms
control_user_list = []

treated_user = []

sexe_user = OrderedDict()
sexe_user['f'] = 0
sexe_user['m'] = 0
sexe_user['?'] = 0

# lire dossier avec le fichier xml
xml_files = listdir(my_path)


# contar arquivos de resultado
ctrl_file = 1

# contar usuarios com comentarios
count_good_user = 0


# lista para controlar tipos de comentarios
count_type_comment = OrderedDict()

count_type_comment['sexe'] = 0
count_type_comment['csp'] = 0
count_type_comment['gout'] = 0
count_type_comment['age'] = 0
count_type_comment['TOUT'] = 0
count_type_comment['test_tout'] = 0
count_type_comment['type1'] = 0
count_type_comment['type2'] = 0
count_type_comment['type3'] = 0


# ****************************************************

# nous lisons ici les listes de noms qui nous utiliserons pour comparer avec les noms d`utilisateur

# lire list de noms femins
file_noms_feminins = open('/home/alexandre/python_projects/Semantic_Web/BASE_TESTE/list_noms_feminins.txt', 'r')
list_noms_feminins = []

# lire le fichier ligne a ligne
for nf in file_noms_feminins:
    # stocker les nom dans la liste de noms, et eliminer le \n avec strip()
    list_noms_feminins.append(nf.strip())


# lire list de noms masculins
file_noms_masculins = open('/home/alexandre/python_projects/Semantic_Web/BASE_TESTE/list_noms_masculins.txt', 'r')
list_noms_masculins = []

# lire le fichier ligne a ligne
for nm in file_noms_masculins:
    # stocker les nom dans la liste de noms, et eliminer le \n avec strip()
    list_noms_masculins.append(nm.strip())


# fermer fichier de noms
file_noms_feminins.close()
file_noms_masculins.close()

# lista para estocar nome do arqui e lista de usuario
index_file_users = OrderedDict()

# lire liste de fichiers
for file in xml_files:


    # verifier si le fichier n`est pas un fichier cache ou temporaire
    regex_file = re.compile('\w*\.xml~')
    regex_file2 = re.compile('\.\w*\.xml~?')

    if regex_file.match(file) or regex_file2.match(file):
        continue


    # #afficher message sur le flot de sortie standard
    # print('reading file ' + file + ' ' + time.strftime("%H:%M:%S") + '\t' + time.strftime("%d/%m/%Y"))
    #
    # # ecrire log
    # log.write('reading file ' + file + ' ' + time.strftime("%H:%M:%S") + '\t' + time.strftime("%d/%m/%Y"))

    index_file_users[file] = ''

    lista_user = ''

    try:
        # lire fichier xml
        tree = etree.parse(my_path + '/' + file)

        # obtenir liste d`utilisateur du fichier qu`on est train de traiter
        for user in tree.xpath('/thread/reponses/reponse/nom'):

            # extraire les id de l`utilisateur
            user_id = str(user.get('id'))

            if not user_id in control_user_list:

                control_user_list.append(user_id)
                user_list.write(user_id + '\n')
                lista_user += str(user_id + ' ')
        index_file_users[file]= lista_user

    except:
        pass

    try:
        # lire id d`utilisateur qui a pose la question
        question_user_id = tree.xpath('/thread/question/nom')[0].get('id')
        question = tree.xpath('/thread/question')

        if not question_user_id in control_user_list:
            control_user_list.append(question_user_id)
            user_list.write(question_user_id + '\n')
            index_file_users[file] = str(index_file_users[file] + ' ' + question_user_id)
    except:
        pass



# ***********************************************************************************#
#
#       deuxieme partie: lire user_list et chercher dans tous les fichiers
#       les constribuitions de l`utilisateur
#
#************************************************************************************

user_list.close()

# ouvrir fichier avec la liste d`utilisateurs
all_users = open('/home/alexandre/python_projects/Semantic_Web/BASE_TESTE/user_list.txt', 'r')


nb_utilisateurs = 0

# lire la liste ligne a ligne
for user2 in all_users:

    # eliminer le retour a ligne de l`id d`utilisateur
    user2 = user2.strip()

    # calculer les indices ou l`utilisateur femmes
    indices = OrderedDict()

    # exemple de contrib de l`utilisateur femmes
    exemple_contrbF = []

    # exemple de contrib de l`utilisateur hommes
    exemple_contrbM = []

    # stocker exemple de professions
    csp_professions = []
    csp_contributions = []

    # stocker exemple de gouts
    wish_list = []
    gout_contributions = []

    # liste pour stocker informations d`age
    set_age = []

    sexe_nom = ''

    # stocker indices de sexe
    indices['m'] = 0
    indices['f'] = 0

    # variables pour ecrire informations de noms
    nom = ''
    nom_min = ''

    # variable pour stocker le nombre de contributions de l'utilisateur
    nom_contr = 0

    # incrementer variables qui comptent les utilisateurs
    nb_utilisateurs += 1


    # lire tous les fichiers pour verifier s`il y a des contribuitions de l`utilisateur
    for file2 in index_file_users.keys():


        # verifier si le fichier n`est pas un fichier cache ou temporaire
        regex_file = re.compile('\w*\.xml~')
        regex_file2 = re.compile('\.\w*\.xml~?')

        if regex_file.match(file2) or regex_file2.match(file2):
            continue


        list_to_compare = index_file_users[file2]

        teste = False

        for i in list_to_compare.split():

            if i.strip() == user2:
                teste = True
                break

        if teste:

            try:
                # parse fichier xml
                tree2 = etree.parse(my_path + '/' + file2)
            except:
                continue

            new_user_list = []

            print(file2)

            try:
                # obtenir liste d`utilisateur du fichier qu`on est train de traiter
                for i in tree2.xpath('/thread/reponses/reponse/nom'):
                    # extraire les id de l`utilisateur
                    new_user_list.append(i.get('id').strip())

                # o valor vazio serve de base para fazer a inversao do xpath na fase de consulta do conteudo da pergunta
                question_user_id2 = ''

                if len(tree2.xpath('/thread/question/nom')) > 0:
                    # lire id d`utilisateur qui a pose la question
                    question_user_id2 = tree2.xpath('/thread/question/nom')[0].get('id')

                question2 = tree2.xpath('/thread/question')

                if not question_user_id2 in new_user_list:
                    new_user_list.append(question_user_id2)


                # verifier si l`utilisateur est dans la liste pour recuperer contribuition et essayer regex
                if user2 in new_user_list:

                    # increment le compteur de contributions
                    nom_contr += 1


                    #****************************************************************************************

                    # verifier le nom de l`utilisateur

                    #****************************************************************************************
                    # lire nom
                    if len(tree2.findall('//nom[@id="' + user2 + '"]')) > 0:

                        nom = tree2.findall('//nom[@id="' + user2 + '"]')[0].text
                    else:
                        continue

                    if nom == None:
                        continue

                    # verifier si le string n`est pas vide
                    if not nom == None:
                        # creer copie du nom en minuscule
                        nom_min = nom.lower()

                        # remplacer les noms diminutifs
                        nom_min.replace('inho', 'o')
                        nom_min.replace('inha', 'a')

                        print(' le nom min ehhhhhhh' + nom_min)

                        # prendre le premier nom des noms composes
                        while ' ' in nom_min or '-' in nom_min or '_' in nom_min or '*' in nom_min or '#' in nom_min or '&' in nom_min or '@' in nom_min or '!' in nom_min or '%' in nom_min or re.match(
                                '.*?(\d)', nom_min, flags=re.MULTILINE | re.IGNORECASE | re.UNICODE):

                            replace_symbol = re.compile('.*?(\s+|-+|_+|\*+|#+|&+|@+|!+|%+|\d+).*?')

                            symbol_temp = replace_symbol.match(nom_min)

                            if not symbol_temp == None:
                                symbol_to_replace = symbol_temp.group(1)
                                nom_min = nom_min.replace(symbol_to_replace, ' ')

                                # eliminer les espaces en blancs excedents
                                nom_min = ' '.join(nom_min.split()).strip()


                            # verifier si la regex trouve un substring
                            if re.match('(.*?)\s(.*?)\s?(.*?)', nom_min,
                                        flags=re.IGNORECASE | re.UNICODE | re.MULTILINE):

                                # capturer et remplacer symbole possibles symboles indesirables dans les nicknames
                                regex_premier_nom = re.search('(.*?)(\s+|-+|_+|\*)(\w*)', nom_min)
                                nom_min = regex_premier_nom.group(1)

                                # verifier si le nickname utilise des symbole avant le nom
                                if len(nom_min) == 1 or len(nom_min) == 2:
                                    nom_min = regex_premier_nom.group(3)

                        # verifier is le nom est dans la liste de noms feminins
                        if nom_min.lower() in list_noms_feminins:
                            sexe_nom = ' FEMINIM \n'

                            #incrementer le repertoire d`indice de l`utilisateur
                            indices['f'] += 1

                            # incrementer compteur pour les femme
                            sexe_user['f'] += 1
                        else:
                            # verifier is le nom est dans la liste de noms feminins
                            if nom_min.lower() in list_noms_masculins:
                                sexe_nom = ' MASCULIN \n'

                                #incrementer le repertoire d`indice de l`utilisateur
                                indices['m'] += 1

                                # incrementer compteur pour les homme
                                sexe_user['m'] += 1
                            else:
                                # incrementer compteur pour les indefinis
                                sexe_user['?'] += 1
                                sexe_nom = ' ??? - non-identifié \n\n'



                    #****************************************************************************************

                    # verifier le contribuition de l`utilisateur

                    #****************************************************************************************

                    if question_user_id2 == user2:
                        contri_temp = tree2.xpath('/thread/question')[0].text.strip()
                    else:
                        # extraire information de la contribuition
                        contri_temp = tree2.xpath('//nom[@id="' + user2 + '"]/following-sibling::constribution')[0].text.strip()

                    if contri_temp == None:
                        continue

                    log.write(' ok ' + file2 + ' lido\n')

                    # eliminiar espacos em excesso
                    contribution = ' '.join(contri_temp.replace('\n', ' ').split())

                    # regex - eu estou com quase \d\d anos
                    age = re.compile('.*?(eu)?\s*[e]?[s]?t[o|ô][u|w]?\s+[k|c][u|o]?[m|n]?\s+[q|k]?[u]?[a]?[s|z]?[e|i]?\s*(\d?\d?\d)\san[o|u]+s?',
                        flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # stocker age
                        new_age = age.match(contribution)
                        set_age.append(new_age.group(2))
                    # regex - eu estou no auge dos meus \d\d anos
                    age = re.compile(
                        '(.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*e?s?t[o|ô]?[u|w]?\s*[n]?[o|u]?\s*[a]?[u]?[g|j]?[e|i]?\s*d?[o|u]?s?\s*m?e?u?s?\s*q?u?a?[z|s]?[e|i]?\s+(\d?\d?\d)\s+an[o|u]+s?)',
                        flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # verifier si la phrase est negative
                        if age.match(contribution).group(3) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append(new_age.group(4))

                    # regex - eu tenho \d\d anos
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*tenh[o|u]\s?(\d?\d?\d)\s+an[o|u]+s?',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append(new_age.group(3))

                    # regex - minha idade eh \d\d anos
                    age = re.compile('.*?minha\s+ida+d[e|i]?\s+(é|e|eh)\s+(\d?\d?\d)\s+an[o|u]+s?',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)

                    if age.match(contribution):
                        # verifier si la phrase est negative
                        if not age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append(new_age.group(2))

                    # regex - eu fiz \d\d anos
                    age = re.compile('.*(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*fi[z|s]\s+(\d?\d?\d)\s+an[o|u]+s?',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)

                    if age.match(contribution):
                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append(new_age.group(3))

                    # regex - eu vou fazer \d\d anos
                    age = re.compile('.*(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*v[o|ô][u|w]?\s+fa[s|z][e|ê]r?\s+(\d?\d?\d)\s+an[o|u]+s?',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append(new_age.group(3))

                    # regex - eu vou fazer \d\d anos
                    age = re.compile('.*(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*a[c|k]abei\s+d[e|i]?\s+fa[s|z][e|ê]r?\s+(\d?\d?\d)\s+an[o|u]+s?',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)

                    if age.match(contribution):
                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append(new_age.group(3))

                    # regex - em MES eu faco \d\d anos
                    age = re.compile('.*?em\s+\w+\s+(eu)?\s*fa(c|ç|ss)[o|u]\s+(\d?\d?\d).?an[o|u]+s?',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # stocker age
                        new_age = age.match(contribution)
                        set_age.append(new_age.group(3))

                    # regex - eu farei \d\d anos
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*farei\s+(\d?\d?\d)\s+an[o|u]+s?', flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append(new_age.group(3))


                    # regex - eh o meu aniversario de \d\d anos
                    age = re.compile('.*?\s*(nao|ñ|não|naum|nãum|n)?\s*(é|eh)\s+o?\s*me[o|u]\s+a?ni+vers?[a|á]*r?i?[o|u]*\s+d[e|i]\s+(\d?\d?\d)\s+an[o|u]+s?',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        # verifier si la phrase est negative
                        if age.match(contribution).group(1) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append(new_age.group(3))


                    # regex - eu ja (nao) tenho (mais) \d\d anos
                    age = re.compile('.*?(eu)?\s*j?[a|á]?h?\s+(nao|ñ|não|naum|nãum|n)?\stenh[o|u]\s+(mais|\+)\s+(\d?\d?\d)\s+an[o|u]+s?',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append('<' + new_age.group(4))

                    # regex - eu estou com \d\d primaveras
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*[e]?[s]?t[o|ô][u|w]?\s+[k|c][u|o]?[m|n]?\s+(\d?\d?\d)\s+primaveras?',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append(new_age.group(3))

                    # regex - eu nao comletei \d\d primaveras
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*[c|k]ompletei\s*(\d?\d)\s*primaveras?',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            set_age.append(new_age.group(3))



                    #****************************************************************************************

                        # l`age doit etre calculee

                    #****************************************************************************************

                    # regex - eu nao nasci no dia 31 de abrial de 1919
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*nas?ci\s+n[o|u]\sdia\s+\d\d?\s+d[e|i]\s\w+\s+d[e|i]\s+(\d\d\d?\d?)',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)

                    # verifier le phrase n`est pas negative
                    if age.match(contribution):

                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)
                            year = new_age.group(3)

                            if len(year) == 4:

                                age_temp = int(time.strftime("%Y")) - int(year)
                                if age_temp > 0:
                                    set_age.append(str(age_temp))

                            if len(year) == 2:

                                age_temp = int('1' + time.strftime("%Y")[2:]) - int(year)
                                if age_temp > 0:
                                    set_age.append(str(age_temp))


                    # regex - eu nasci dia 30 de outubro de 1980
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*nas?ci\s*(em|n[o|u]\s*dia)?\s*\w*\s+d[e|i]\s+\w*\s*d?[e|i]?\s+(\d\d\d?\d?)',
                                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # verifier si la phrase est negative
                        if age.match(contribution).group(1) == None:

                            # stocker age
                            new_age = age.match(contribution)
                            year = new_age.group(4)

                            if len(year) == 4:

                                age_temp = int(time.strftime("%Y")) - int(year)
                                if age_temp > 0:
                                    set_age.append(str(age_temp))

                            if len(year) == 2:

                                age_temp = int('1' + time.strftime("%Y")[2:]) - int(year)
                                if age_temp > 0:
                                    set_age.append(str(age_temp))


                    #****************************************************************************************

                    #                                   idade por extenso

                    #****************************************************************************************

                    # regex - eu estou com (QUASE) TRINTA E TRES anos
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*[e]?[s]?t[o|ô][u|w]?\s+[k|c][u|o]?[m|n]?\s+(qua+[s|z][e|i])?\s*(vi+nt[e|i]+|tri+nta+\s*|[k|c]?q?u?are+nta+|[s|c]in[k|q]u?e+nta+|[s|c]e[s|c]s?e+nta+|[s|s]ete+nta+|oite+nta+|nove+nta)?\s*[e|i]?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*',
                        flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)

                    if age.match(contribution):
                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(4) == None:
                                age_string += new_age.group(4) + ' '

                            if not new_age.group(5) == None:
                                age_string += new_age.group(5)

                            if not new_age.group(6) == None:
                                age_string += new_age.group(6)

                            set_age.append(age_string.strip())


                    # regex - eu estou no(s) (auge) (dos) (meuss) (quase) TRINTA E TRES anos
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*e?s?t[o|ô]u?\s+n[o|u]s?\s*(au[g|j][e|i])?\s*(d[o|u]s)?\s*(meus)?\s*(qua[z|s][e|i])?\s*(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*',
                        flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)

                    if age.match(contribution):

                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:

                            # stocker age
                            new_age = age.match(contribution)

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(7) == None:
                                age_string += new_age.group(7) + ' '

                            if not new_age.group(8) == None:
                                age_string += new_age.group(8)

                            if not new_age.group(9) == None:
                                age_string += new_age.group(9)

                            set_age.append(age_string.strip())


                    #regex - eu tenho VINTE anos
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*tenh[o|u]\s+(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*',
                        flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        # verifier si la phrase est negative
                        if age.match(contribution).group(2) == None:
                            new_age = age.match(contribution)

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(3) == None:
                                age_string += new_age.group(3) + ' '

                            if not new_age.group(4) == None:
                                age_string += new_age.group(4)

                            if not new_age.group(5) == None:
                                age_string += new_age.group(5)

                            set_age.append(age_string.strip())

                    # regex - minha idade eh VINTA E SEIS anos
                    age = re.compile('.*?minha\s+ida+d[e|i]\s+(é|eh)\s+(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*',
                        flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # stocker age
                        new_age = age.match(contribution)

                        # contruire string ave l`age
                        age_string = ''

                        if not new_age.group(1) == None:
                            age_string += new_age.group(1) + ' '

                        if not new_age.group(2) == None:
                            age_string += new_age.group(2)

                        if not new_age.group(3) == None:
                            age_string += new_age.group(3)

                        set_age.append(age_string.strip())

                    # regex - eu fiz VINTE anos
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*fi[z|s]\s+(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*',
                        flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        if age.match(contribution).group(2) == None:

                            # stocker age
                            new_age = age.match(contribution)

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(3) == None:
                                age_string += new_age.group(3)

                            if not new_age.group(4) == None:
                                age_string += new_age.group(4)

                            if not new_age.group(5) == None:
                                age_string += new_age.group(5)

                            set_age.append(age_string.strip())


                    # regex - vou fazer QUARENTA anos
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*v[o|ô][u|w]?\s+fa[s|z][e|ê]r?\s+(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*', flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(3) == None:
                                age_string += new_age.group(3) + ' '

                            if not new_age.group(4) == None:
                                age_string += new_age.group(4)

                            if not new_age.group(5) == None:
                                age_string += new_age.group(5)

                            set_age.append(age_string.strip())

                    # regex - acabei de fazer VINTE anos
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s+a[c|k]abei\sd[e|i]\s+fa[s|z][e|ê]r?\s*(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*', flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(3) == None:
                                age_string += new_age.group(3) + ' '

                            if not new_age.group(4) == None:
                                age_string += new_age.group(4)

                            if not new_age.group(5) == None:
                                age_string += new_age.group(5)

                            set_age.append(age_string.strip())

                    # regex - eu faco VINTE anos
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*fa[c|ç][o|u]\s*(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*', flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # stocker age
                        new_age = age.match(contribution)

                        if age.match(contribution).group(2) == None:

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(3) == None:
                                age_string += new_age.group(3) + ' '

                            if not new_age.group(4) == None:
                                age_string += new_age.group(4)

                            if not new_age.group(5) == None:
                                age_string += new_age.group(5)

                            set_age.append(age_string.strip())

                    # regex - eu farei VINTE anos
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*farei\s*(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*', flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # stocker age
                        new_age = age.match(contribution)

                        if age.match(contribution).group(2) == None:

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(3) == None:
                                age_string += new_age.group(3) + ' '

                            if not new_age.group(4) == None:
                                age_string += new_age.group(4)

                            if not new_age.group(5) == None:
                                age_string += new_age.group(5)

                            set_age.append(age_string.strip())

                    # regex - eh o meu aniversario de VINTE anos
                    age = re.compile('.*?\s*(nao|ñ|não|naum|nãum|n)?\s*(é|eh)\s+?me[o|u]\s+a?ni+vers?[a|á]*r?i?[o|u]*\s*d[e|i]\s*(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*', flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # stocker age
                        new_age = age.match(contribution)

                        if age.match(contribution).group(1) == None:

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(3) == None:
                                age_string += new_age.group(3) + ' '

                            if not new_age.group(4) == None:
                                age_string += new_age.group(4)

                            if not new_age.group(5) == None:
                                age_string += new_age.group(5)

                            set_age.append(age_string.strip())


                    # regex - nao (ja) tenho mais VINTE anos
                    age = re.compile('.*?(eu)?\s*j?[a|á]?h?\s?(nao|ñ|não|naum|nãum|n)\stenh[o|u]\s[\+]?(mai?s|\+)\s*(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*', flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # stocker age
                        new_age = age.match(contribution)

                        # contruire string ave l`age
                        age_string = ''

                        if not new_age.group(4) == None:
                            age_string += new_age.group(4) + ' '

                        if not new_age.group(5) == None:
                            age_string += new_age.group(5)
                        if not new_age.group(6) == None:
                            age_string += new_age.group(6)

                        set_age.append(age_string.strip())

                    # regex - minha idade eh VINTE anos
                    age = re.compile('.*?minha\sidad[e|i]\s(é|eh)\s*(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*an[o|u]+[s|x]*', flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):
                        # stocker age
                        new_age = age.match(contribution)

                        # contruire string ave l`age
                        age_string = ''

                        if not new_age.group(2) == None:
                            age_string += new_age.group(2) + ' '

                        if not new_age.group(3) == None:
                            age_string += new_age.group(3)

                        if not new_age.group(4) == None:
                            age_string += new_age.group(4)

                        set_age.append(age_string.strip())

                    # regex - eu estou com VINTE primaveras
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*[e]?[s]?t[o|ô][u|w]?\s+[k|c][u|o]?[m|n]?\s*(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*primaveras?', flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        if age.match(contribution).group(2) == None:
                            # stocker age, flags = re.IGNORECASE | re.MULTILINE| re.UNICODE
                            new_age = age.match(contribution)

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(3) == None:
                                age_string += new_age.group(3) + ' '

                            if not new_age.group(4) == None:
                                age_string += new_age.group(4)

                            if not new_age.group(5) == None:
                                age_string += new_age.group(5)

                            set_age.append(age_string.strip())


                    # regex - eu nao completei VINTE Primaveras
                    age = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*[c|k]ompletei\s*(vi+nt[e|i]+\s*[e|i]?|tri+nta+\s*[e|i]?|[k|c]?q?u?are+nta+\s*[e|i]?|[s|c]in[k|q]u?e+nta+\s*[e|i]?|[s|c]e[s|c]s?e+nta+\s*[e|i]?|[s|s]ete+nta+\s*[e|i]?|oite+nta+\s*[e|i]?|nove+nta\s*[e|i]?)?\s*(u[n|m]+|doi[s|x]+|tr[ê|e]i?[z|s]+x*|[q|k]u?atr[o|u]+|[s|c]in[k|c][o|u]+|[s|c]ei[s|x]+|s[e|é]t[e|i]+|oit[o|u]+|nov[e|i]+|dei?[z|x]+)?\s*(on[z|s][e|i]+|dou?[s|z][e|i]+|tr[e|ê][s|z][e|i]+|[k|q]c?u?ator[z|s][e|i]+|[k|q]u?in[z|s][e|i]+|d[e|i][s|z]es?s?[c|z]?ei?[s|x]+|d[e|i][s|z]e[s|c]s?et[e|i]+|d[e|i][s|z]oit[o|u]+|d[e|i][z|s]enov[e|i]+)?\s*primaveras?', flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    if age.match(contribution):

                        if age.match(contribution).group(2) == None:
                            # stocker age
                            new_age = age.match(contribution)

                            # contruire string ave l`age
                            age_string = ''

                            if not new_age.group(3) == None:
                                age_string += new_age.group(3) + ' '

                            if not new_age.group(4) == None:
                                age_string += new_age.group(4)

                            if not new_age.group(5) == None:
                                age_string += new_age.group(5)

                            set_age.append(age_string.strip())

                    # todo incluir idade da loba, balsaquiana... etc.


                    #***************************************************************************************

                     #                   les regex ci-dessous fournissent age + sex

                    #***************************************************************************************


                    # regex - eu sou um SENHOR(A) de SETENTA anos
                    age_et_sexe = re.compile('.*?(eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*s[o|ô][u|w]?\s+u[m|n]a?\s+(s[e|i]nh[o|ô]r?|hom[i|e]m?|rapaz|m[i|e]nin[o|u]|moço)?(s[e|i]nhora?|mulh?[e|é]r?|m[i|e]nina|moça)?\s+d[e|i]\s+(\d\d?\d)\s+an[o|u]+[s|x]*', flags= re.MULTILINE| re.UNICODE | re.IGNORECASE)

                    if age_et_sexe.match(contribution):

                        if age_et_sexe.match(contribution).group(2) == None:

                            if not age_et_sexe.group(3)== None:

                                if not age_et_sexe.group(3) == None:
                                    #incrementer le repertoire d`indice de l`utilisateur
                                    indices['m'] += 1

                                if not age_et_sexe.group(4) == None:
                                    #incrementer le repertoire d`indice de l`utilisateur
                                    indices['m'] += 1

                        if not age_et_sexe.group(5) == None:
                            set_age.append(age_et_sexe.group(5))

                    #***************************************************************************************

                     #                   DECOUVRIR SEXE DE L`UTILISATEUR - FEMMES

                    #***************************************************************************************


                    # regex - minha cezariana
                    sexe = re.compile('.*?(minhas?\s*[s|c]e[s|z]ari[a|ã]nas?)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))

                    # regex - eu dei a luz de parto normal
                    sexe = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*d[e|ê]i\s*[a|à]\s+lu[s|z]\s+d[e|i]\s+part[o|u]\s+norma[l|u]?)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur

                        # verifier si la phrase est negative
                        if sexe.match(contribution).group(3) == None:
                            indices['f'] += 1
                            if not sexe.match(contribution).group(1) == None:
                                exemple_contrbF.append(sexe.match(contribution).group(1))

                    # regex - eu amamentei
                    sexe = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*amame+nt(o+|ei+|are+i+))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur

                        # verifier si la phrase est negative
                        if sexe.match(contribution).group(3) == None:

                            indices['f'] += 1
                            if not sexe.match(contribution).group(1) == None:
                                exemple_contrbF.append(sexe.match(contribution).group(1))

                    # regex - eu amamentava
                    sexe = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*\s+a+ma+me+nta+va+)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):

                        # verifier si la phrase est negative
                        if sexe.match(contribution).group(3) == None:

                            #incrementer le repertoire d`indice de l`utilisateur
                            indices['f'] += 1
                            if not sexe.match(contribution).group(1) == None:
                                exemple_contrbF.append(sexe.match(contribution).group(1))



                    # regex - minha primeira/ segunda ... gravides
                    sexe = re.compile('.*?(minha\s(primei?ra|segu+nda|tercei?ra|[q|c]u?arta|[q|k]u?inta|[s|c]ei?x?ta|s[é|e]tima|oitava|nona|d[e|é][s|c]ima)\s+gravid[e|ê][s|z])', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))

                    # regex - eu estou gravida
                    sexe = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*[i|e]?s?t[o|ô][u|w]?\sgr[a|á]+vi+da+)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if sexe.match(contribution).group(3) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))

                    # regex - eu estava gravida
                    sexe = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*[i|e]?s?tava\sgr[a|á]+vi+da+)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):

                        if sexe.match(contribution).group(3) == None:
                            #incrementer le repertoire d`indice de l`utilisateur
                            indices['f'] += 1
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    # regex - eu estou no meu  primeiro mes de gestacao
                    sexe = re.compile('.*?(eu\s+(est)?([o|ô]?[u|w]?|arei)\sn[o|u]s?\s*meus?\s+\w+\s*m[e|ê][s|z](es)?\sd[e|i]\s[g|j]esta[c|ç][a|ã][o|u])', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        exemple_contrbF.append(sexe.match(contribution).group(1))


                    # regex - eu estava nos meus pirmeiros meses de gestacao
                    sexe = re.compile('.*?(eu\s+(es)?tava\sn[o|u]s?\s*meus?\s+\w+\s*m[e|ê][s|z](es)?\sd[e|i]\s[g|j]esta[c|ç][a|ã][o|u])', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    # regex - eu estou de licenca maternindade
                    sexe = re.compile('.*?((eu)?\s?(es)?t[o|ô][u|w]?\s*d[e|i]\s*li[s|c]en[c|ç]+s?s?a\s*maternidad[e|i])', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    # regex - meus seios
                    sexe = re.compile('.*?(meus?\s+sei[o|u]+s?)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))

                    # regex - meus ovarios
                    sexe = re.compile('.*?(meus?\sov[a|á]ri[o|u]+s?)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    # regex - minha vagina
                    sexe = re.compile('.*?(minha\sva[g|j]i+na+)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    # regex - minha menstruacao
                    sexe = re.compile('.*?(minha\s?men?s?tr[u|o]a[c|ç][ã|a][o|u]+)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))

                    # regex - meu clitoris
                    sexe = re.compile('.*?(meu\s[c|k]l[í|i]t[o|ó]+ris)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    # regex - eu estou menstruada
                    sexe = re.compile('.*?((eu)?\s*(es)?t([o|ô][u|w]?|arei)\s(men?s?tr[u|o]ada+|na\smenon?pau[s|z]a))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))

                    # regex - ... eu estiver menstruada | menopausa
                    sexe = re.compile('.*?(eu\s+(es)?t(ava|aria|iv[e|é]r)\s(men?s?tr[u|o]ada+|na\smenon?pau[s|z]a))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    # regex - ... eu fiquei menstruada
                    sexe = re.compile('.*?((eu)?\s*(fi[q|k]u?ei|v[o|ô][w|u]\sfi[c|k]ar?)?\s(men?s?tr[u|o]ada+|na\smenon?pau[s|z]a))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    # regex - .. eu vou entrar na menopausa
                    sexe = re.compile('.*?((eu)?\s*v[o|ô][u|w]?\sentra+r?\s+(na)?\s*menon?pau[s|z]a)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))

                    # regex - meu utero
                    sexe = re.compile('.*?(me[o|u]\s+[u|ú]t[e|ê]r[o|u])', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    # regex - meu ginecologista
                    sexe = re.compile('.*?(me[o|u]\s[g|j]in[e|i][c|k][o|u]lo[g|j]ista)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    ##################################################################################

                    #                            NON-FISIOLOGIQUES - FEMMES

                    #################################################################################


                    # todo as duas regex seguintes seviram para definir status - casado, sou solteiro, etc...

                    sexe = re.compile('.*?(me[u|o]\s+marid[o|u]+)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))


                    sexe = re.compile('.*?(me[u|o]\s?[e|i]spo[s|z][o|u]+)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))




                    # regex - eu sou uma senhora|senhorinha
                    sexe = re.compile('.*?((eu)?\s?so[u|w]\s+u[m|n]a\s(s[e|i]nho+ra*|m[e|i]nina?|mo[ç|c]a?|mulh?[é|e]r?|garota?)(z?inha)?)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['f'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbF.append(sexe.match(contribution).group(1))




                    sexe = re.compile('.*?((eu)?\s?(so[u|w]|estou|tow|tô)\s+(\w+))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)


                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur

                        adjectif = sexe.match(contribution).group(4).strip()

                        for i in list_adjecfis:
                            i = i.strip()
                            if re.match(i, adjectif, flags=re.IGNORECASE|re.MULTILINE|re.UNICODE):

                                # regex para extrair morfema de genero


                                if adjectif[-1] == 'a':
                                    indices['f'] += 1
                                    exemple_contrbF.append(sexe.match(contribution).group(1))
                                    break

                                if adjectif[-1] =='o':
                                    indices['m'] += 1
                                    exemple_contrbM.append(sexe.match(contribution).group(1))
                                    break


                    #***************************************************************************************

                     #                   DECOUVRIR SEXE DE L`UTILISATEUR - HOMMES

                    #***************************************************************************************

                    # regex - meus testiculos
                    sexe = re.compile('.*?(me[u|o]s?\s+test[i|í]+[k|c][o|u]+l[o|u]+s?)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['m'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbM.append(sexe.match(contribution).group(1))

                    # regex - meu penis
                    sexe = re.compile('.*?(me[u|o]\s+p[e|ê]nis)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['m'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbM.append(sexe.match(contribution).group(1))



                    # regex - eu estou de pau duro    VULGAR DEMAIS, POREM....
                    sexe = re.compile('.*?((eu)?\s(es)?(t[o|ô][u|w]?|fiquei)\s+d[e|i]\spau\s+dur[o|u])', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['m'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbM.append(sexe.match(contribution).group(1))

                    # regex - meu urologista
                    sexe = re.compile('.*?(me[u|o]\s+[u|o]r[o|u]lo[g|j]ista)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['m'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbM.append(sexe.match(contribution).group(1))

                    # regex - eu sou um senhor  senhorzinho
                    sexe = re.compile('.*?((eu)?\s?so[u|w]\s*u?[m|n]?\s+(senh[o|ô]+r?|m[i|e]nin[o|u]?|garot[o|u]?|rapai?[z|s]|mos?s?ç[o|u]?|hom[e|i]m?)(z?inho)?)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['m'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbM.append(sexe.match(contribution).group(1))


                    # regex - eu sou muito macho
                    sexe = re.compile('.*?((eu)?\s?so[u|w]\s?(u?[m|n]?|mto|muit[o|u])\sma(ch|x)[o|u])', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['m'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbM.append(sexe.match(contribution).group(1))



                    # todo regex pour definir status social
                    sexe = re.compile('.*?(minh?a\s+[e|i]spo+[z|s]a+)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['m'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbM.append(sexe.match(contribution).group(1))

                    sexe = re.compile('.*?(minh?a\s+mulh?[e|é]+r?)', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if sexe.match(contribution):
                        #incrementer le repertoire d`indice de l`utilisateur
                        indices['m'] += 1
                        if not sexe.match(contribution).group(1) == None:
                            exemple_contrbM.append(sexe.match(contribution).group(1))



                    #**********************************************************************************

                    #                                       CSP

                    #**********************************************************************************

                    # regex eu trabalho COMO ENGENHEIRO
                    csp_temp = re.compile('.*?(eu\s*trabalh?[o|u]\s+([c-k]om[o|u]|d[e|i])\s+(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    csp = csp_temp.match(contribution)
                    if csp_temp.match(contribution):
                        if not csp.group(3) == None:
                            csp_professions.append(csp.group(3))
                        csp_contributions.append(csp.group(1))

                    # regex - eu tenho carteira assinada de PROFISSAO
                    csp_temp = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*tenh[o|u]\s+a?\s*[c|k]artei?ra\s*assinada\s*([c|k]om[o|u]|d[e|i])\s+(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    csp = csp_temp.match(contribution)
                    if csp_temp.match(contribution):
                        # verificar frase negativa
                        if csp_temp.match(contribution).group(3) == None:
                            if not csp.group(4) == None:
                                csp_professions.append(csp.group(4))
                            csp_contributions.append(csp.group(1))

                    # regex - eu atuo como PEDREIRO
                    csp_temp = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*atuo\s*[k|c]om[o|u]\s+(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    csp = csp_temp.match(contribution)
                    if csp_temp.match(contribution):
                        # verificar frase negativa
                        if csp_temp.match(contribution).group(3) == None:
                            if not csp.group(4) == None:
                                csp_professions.append(csp.group(4))
                            csp_contributions.append(csp.group(1))

                    # regex - eu teno cnpj de programador
                    csp_temp = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*tenh?[o|u]\scnpj\s*d[e|i]\s+(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    csp = csp_temp.match(contribution)
                    if csp_temp.match(contribution):
                        # verificar frase negativa
                        if csp_temp.match(contribution).group(3) == None:
                            if not csp.group(4) == None:
                                csp_professions.append(csp.group(4))
                                csp_contributions.append(csp.group(1))



                    # regex - eu comecei a trabalhar de PROFISSAO
                    csp_temp = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*[c|k][u|o]mecei\s+trabalhar?\s*d[e|i]\s+(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    csp = csp_temp.match(contribution)
                    if csp_temp.match(contribution):
                        # verificar frase negativa
                        if csp_temp.match(contribution).group(3) == None:
                            if not csp.group(4) == None:
                                csp_professions.append(csp.group(4))
                                csp_contributions.append(csp.group(1))


                    csp_temp = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*\s+sou\s*(uma?|o|a)?\s+(\w+\s*\w*\s*\w*\s*\w*\s*\w*\s*\w*\s*\w*))\.?\s?(numa|na|no|em|da|do)?')

                    csp = csp_temp.match(contribution)
                    if csp_temp.match(contribution):
                        # verificar frase negativa
                        if csp_temp.match(contribution).group(3) == None:
                            if not csp.group(5) == None:
                                # recuperar profissao
                                profissao = csp.group(5)
                                for prof in list_professions:
                                    prof = prof.strip()
                                    reg_to_text = str('('+ prof +').*')
                                    print(reg_to_text)
                                    reg_prof = re.compile(reg_to_text, flags= re.IGNORECASE)
                                    if reg_prof.match(profissao):
                                        # estocar resultado da regex profissoa
                                        csp_professions.append(reg_prof.match(profissao).group(1))
                                        # estocar frase inteira
                                        csp_contributions.append(csp.group(1))
                                        break


                #*********************************************************************************

                #                                APOSENTADOS

                #*********************************************************************************

                    # regex - eu sou aposentado
                    csp = re.compile('.*?((eu)?s*(nao|ñ|não|naum|nãum|n)?\s?(s[o|ô][w|u]|e?s?t[o|ô][w|u])\s*(aposentad(o|a)))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if csp.match(contribution):

                        sexe = csp.match(contribution)
                        if csp.match(contribution).group(3) == None:
                            if not sexe.group(5) == None and (sexe.group(5) == 'a' or sexe.group(5)== 'A'):
                                indices['f'] +=1
                                csp_professions.append(sexe.group(4))
                                exemple_contrbF.append(sexe.group(1))
                                csp_contributions.append(csp.match(contribution).group(1))
                            else:
                                indices['m'] +=1
                                csp_professions.append(sexe.group(4))
                                exemple_contrbM.append(sexe.group(1))
                                csp_contributions.append(csp.match(contribution).group(1))


                    # regex - eu me aposentei como PROFISSAO
                    csp_temp = re.compile('.*?((eu)?s*(nao|ñ|não|naum|nãum|n)?\s?m[e|i]\saposentei\s[c|k]om[o|u]\s+(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    csp = csp_temp.match(contribution)

                    if csp_temp.match(contribution):
                        if csp_temp.match(contribution).group(3) == None:
                            if not csp.group(1) == None:
                                csp_contributions.append(csp.group(1))
                                csp_professions.append('aposentado')

                    #*********************************************************************************

                    #                       PREFERENCE - GOUTS DE LA PERSONNE


                    #*********************************************************************************



                    #   TODO - TODAS AS REGEX DEVEM SER VERIFICADAS!!!! DEVO DECIDIR A ESTRUTURA DE ESPACOS E TESTA-LAS UMA A UMA

                    # regex - eu estou (adv) afim de de comprar (adv) um PRODUTO
                    gout_temp = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*e?s?t[o|ô][w|u]?\s*\w*\s*afi[n|m]\s*d[e|i]\s*[c|k]ompr[a|á]r?\s+\w*\s*(u[n|m]a?s?\s+|[o|a]s?\s+|ess[a|e]s?\s+|est[e|a]s?\s+|a[q|k]u?el[a|e]s?\s+)?(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)


                    if gout_temp.match(contribution):
                        # verificar se a frase e negativa
                        if gout_temp.match(contribution).group(3) == None:
                            gout = gout_temp.match(contribution)
                            if not gout.group(5) == None:
                                wish_list.append(gout.group(5))
                            gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())


                    # regex - se eu tivesse dinheiro, eu compraria (adv) um PRODUTO
                    gout_temp = re.compile('.*?(s[e|i]\s+eu\s+tivess?[e|i]\s*dinh?ei?r[o|u],?\s*e?u?\s*[c|k]ompr[a|á](va|ria)\s+\w*\s*(u[n|m]a?s?\s+|[o|a]s?\s+|ess[a|e]s?\s+|est[e|a]s?\s+|a[q|k]u?el[a|e]s?\s+)?(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        gout = gout_temp.match(contribution)
                        if not gout.group(4) == None:
                            wish_list.append(gout.group(4))
                        gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())


                    # regex - eu quero (adv) ter(adv) dinheiro para comprar (adv) um PRODUTO
                    gout_temp = re.compile('.*?(eu\s*(nao|ñ|não|naum|nãum|n)?\s*[k|q]u?er[o|u]?i?a?\s*\w*\s*t[e|ê]r?\s*\w*\s*dinh?ei?r[o|u]\s*pa?r?a?\s+[c|k]ompr[a|á]r?\s*\w*\s+(u[n|m]a?s?\s+|[o|a]s?\s+|ess[a|e]s?\s+|est[e|a]s?\s+|a[q|k]u?el[a|e]s?\s+)?(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        if gout_temp.match(contribution).group(2) == None:
                            gout = gout_temp.match(contribution)
                            if not gout.group(4) == None:
                                 wish_list.append(gout.group(4))
                            gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())

                    # regex - eu quero(adv) comprar(adv) (um) PRODUTO
                    gout_temp = re.compile('.*?(eu\s*(nao|ñ|não|naum|nãum|n)?\s*[k|q]u?er(o|u|ia)\s+\w*\s*[c|k]ompr[a|á]r?\s*\w*\s+(u[n|m]a?s?\s+|[o|a]s?\s+|ess[a|e]s?\s+|est[e|a]s?\s+|a[q|k]u?el[a|e]s?\s+)?(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        if gout_temp.match(contribution).group(2) == None:
                            gout = gout_temp.match(contribution)
                            if not gout.group(5) == None:
                                wish_list.append(gout.group(5))
                            gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())

                    # regex - se eu fosse(adv) rico, eu compraria(adv) um PRODUTO
                    gout_temp = re.compile('.*?(s[e|i]\s*eu\s+foss?[e|i]\s+\w*\s*ri[k|c][o|u],?\s*(eu)?\s*[c|k]ompr[a|á](va|ria)\s*\w*\s+(u[n|m]a?s?\s+|[o|a]s?\s+|ess[a|e]s?\s+|est[e|a]s?\s+|a[q|k]u?el[a|e]s?\s+)?(\w+\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        gout = gout_temp.match(contribution)
                        if not gout.group(5) == None:
                            wish_list.append(gout.group(5))
                        gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())

                    # regex - eu acho o PRODUTO (adv) melhor|lindo....
                        gout_temp = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*a(x|ch)[o|u]\s+(u[n|m]a?s?\s+|[o|a]s?\s+|ess[a|e]s?\s+|est[e|a]s?\s+|a[q|k]u?el[a|e]s?\s+)?(\w+\s*\w*\s*\w*\s*\w*\s*\w*)\s*\w*\s*(melhore?s?|fo+da+|lind[o|a]*u*s*|ira+d[o|a]*u*s*|bo[m|a]+s?|gosto+[s|z][o|a]*u*s*|ma+ra+vi+lho+[s|z][a|o]*u*s*|fo+f[o|a]*u*s*|pe+rfe+i+t[o|a]*u*s*|se+nsa+[s|c]i+o+na+[l|u]+i*[x|s]*|de+li+ci+o+[s|z][o|a]*u*s*|sa+bo+ro+[s|z][a|o]*u*s*|b[o|u]+ni+t[a|o]*u*[s|x]*|x?c?h?ei?ro[s|z][a|o]*u*s*|be+l[a|o]*u*s*|ga+t[a|o]*u*[s|x]*|\+?\s*m?a*i*[s|x]*\stop|the\s*be+st|confi[á|a]vel?i?s?))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        # VERIFICAR FRASE NEGATIVA
                        if gout_temp.match(contribution).group(3) == None:
                            gout = gout_temp.match(contribution)
                            if not gout.group(6) == None:
                                wish_list.append(gout.group(6))
                            gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())
                    #
                    # # regex - eu acho que o PRODUTO eh (adv)(adv) melhor|lindo....
                    # gout_temp = re.compile('.*?(e?u?\s*(nao|ñ|não|naum|nãum|n)?\s*a(x|ch)[o|u]\s+(q|ki|que|qui)\s*(u[n|m]a?s?\s+|[o|a]s?\s+|ess[a|e]s?\s+|est[e|a]s?\s+|a[q|k]u?el[a|e]s?\s+)?(\w+\s*\w*\s*\w*\s*\w*\s*\w*)\s*(é|eh|e|sao|são|saw)\s+\w*\s*(\+|mas|mais)?\s*(melhore?s?|fo+da+|lind[o|a]*u*s*|ira+d[o|a]*u*s*|bo[m|a]+s?|gosto+[s|z][o|a]*u*s*|ma+ra+vi+lho+[s|z][a|o]*u*s*|fo+f[o|a]*u*s*|pe+rfe+i+t[o|a]*u*s*|se+nsa+[s|c]i+o+na+[l|u]+i*[x|s]*|de+li+ci+o+[s|z][o|a]*u*s*|sa+bo+ro+[s|z][a|o]*u*s*|b[o|u]+ni+t[a|o]*u*[s|x]*|x?c?h?ei?ro[s|z][a|o]*u*s*|be+l[a|o]*u*s*|ga+t[a|o]*u*[s|x]*|\+?\s*m?a*i*[s|x]*\stop|the\s*be+st|confi[á|a]vel?i?s?))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)
                    #
                    # if gout_temp.match(contribution):
                    #     # VERIFICAR FRASE NEGATIVA
                    #     if gout_temp.match(contribution).group(2) == None:
                    #         gout = gout_temp.match(contribution)
                    #         if not gout.group(6) == None:
                    #             wish_list.append(gout.group(6))
                    #         gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())



                    # regex - eu gosto (adv) (daquele) PRODUTO
                    gout_temp = re.compile('.*?(eu\s+(nao|não|ñ|naum)?\s*gost[o|u]\s+\w*\s*(d[e|i]\s+|d[o|a]\s+|du|da[q|k]u?el[e|i]\s+|da[q|k]u?ela\s+|dess[e|i]\s+|dessa\s+)?s?(\w+\s*\w*\s*\w*\s*\w*\s*\w*))()?', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        # VERIFICAR FRASE NEGATIVA
                        if gout_temp.match(contribution).group(2) == None:
                            gout = gout_temp.match(contribution)
                            if gout.group(2) == None:

                                if not gout.group(4) == None:
                                    wish_list.append(gout.group(4))
                                gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())

                    # regex - para mim aquele PRODUTO eh um dos mais confiaveis
                    gout_temp = re.compile('.*?(pa?ra\s*mi[n|m],?\s*(u[n|m]a?s?\s+|[o|a]s?\s+|ess[a|e]s?\s+|est[e|a]s?\s+|a[q|k]u?el[a|e]s?\s+)?(\w+\s*\w*\s*\w*\s*\w*\s*\w*)\s+(eh+|e|é+|saw|sao|são|sau|som[o|u]s?)\s+(o+|a+|u[n|m]\s*d?o)?s?\s*(\+|mai[s|x])?\s*(melhore?s?|fo+da+|lind[o|a]*u*s*|ira+d[o|a]*u*s*|bo+[m|a]+s?|go+sto+[s|z][o|a]*u*s*|ma+ra+vi+lho+[s|z][a|o]*u*s*|fo+f[o|a]*u*s*|pe+rfe+i+t[o|a]*u*s*|se+nsa+[s|c]i+o+na+[l|u]+i*[x|s]*|de+li+ci+o+[s|z][o|a]*u*s*|sa+bo+ro+[s|z][a|o]*u*s*|b[o|u]+ni+t[a|o]*u*[s|x]*|x?c?h?ei?ro[s|z][a|o]*u*s*|be+l[a|o]*u*s*|ga+t[a|o]*u*[s|x]*|\+?\s*m?a*i*[s|x]*\stop|the\s*be+st|confi[á|a]vel?i?s?))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        gout = gout_temp.match(contribution)
                        if not gout.group(2) == None:
                            wish_list.append(gout.group(3))
                        gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())


                    # regex - eu soh compro PRODUTOMARCA
                    gout_temp = re.compile('.*?(eu\s*s[o|ó]h?\s*[k|c]ompr[o|u]\s*(d[o|a]s?)?\s*(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        gout = gout_temp.match(contribution)
                        if not gout.group(3) == None:
                            wish_list.append(gout.group(3))
                        gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())


                    # regex - eu (so) uso (do) PRODUTOMARCA
                    gout_temp = re.compile('.*?(eu\s+(s?[o|ó]h?)?\s*u[s|z][o|u]\s*(d[a|o]s)?\s*(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        gout = gout_temp.match(contribution)
                        if not gout.group(4) == None:
                            wish_list.append(gout.group(4))
                        gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())

                    # regex - eu sou (adv) fa daquele PESSOA|PRODUTO
                    gout_temp = re.compile('.*?((eu)?\s*(nao|ñ|não|naum|nãum|n)?\s*s[o|ô][u|w]\s+\w*\s*f[a|ã]+n?\s+(d(e|i|o|a)s?\s+|da[k|q]u?el[a|e]s\s+)?(\w+\s*\w*\s*\w*\s*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        if gout_temp.match(contribution).group(3) == None:
                            gout = gout_temp.match(contribution)
                            if not gout.group(3) == None:
                                wish_list.append(gout.group(3))
                            gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())


                    # regex - o meu (TIPO) preferido eh (PRODUTO|PESSOA)
                    gout_temp = re.compile('.*?((meu|minha)s?\s+(\w*\s*\w*\s*\w*)\s*(pre+f[e|i]+ri+d[o|a]?|favorit[a|o])u?s?\s+(eh+|é+|saw|sao|são|sau|som[o|u]s?)\s*(u[n|m]a?s?\s+|[o|a]s?\s+|ess[a|e]s?\s+|est[e|a]s?\s+|a[q|k]u?el[a|e]s?\s+)?(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        gout = gout_temp.match(contribution)

                        # objeto
                        if not gout.group(3) == None:
                            phrase = gout.group(3)

                        if not gout.group(6) == None:
                            phrase += gout.group(6)

                        wish_list.append(phrase)
                        gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())

                    # regex - quanto custa|ta|ta saindo... um PRODUTO
                    gout_temp = re.compile('.*?(nao|ñ|não|naum|nãum|n)?\s*(quant[o|u]\s+([c|k]ust(a|ão|am)\s+|(es)?t[á|a]h?\s+|(es)?t[á|a]h?\s+[c|k]ustand[o|u]\s+|(es)?t[á|a]h?\s+saind[o|u]\s+)(u[n|m]a?s?\s+|[o|a]s?\s+|ess[a|e]s?\s+|est[e|a]s?\s+|a[q|k]u?el[a|e]s?\s+)(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        if gout_temp.match(contribution).group(1) == None:
                            gout = gout_temp.match(contribution)
                            if not gout.group(9) == None:
                                wish_list.append(gout.group(9))
                            gout_contributions.append(gout.group(2))


                    # regex - qual o preco de um PRODUTO
                    gout_temp = re.compile('.*?(qua[l|u]\s+[o|u]\s+pre[c|ç][o|u]\s+(du[m|n]\s+|d[e|i]\s+u[n|m]a?s?\s+|d[o|a]s?\s+|dess[a|e]s?\s+|dest[e|a]s?\s+|da[q|k]u?el[a|e]s?\s+)?(\w+\s*\w*\s*\w*\s*\w*\s*\w*))', flags= re.MULTILINE | re.UNICODE | re.IGNORECASE)

                    if gout_temp.match(contribution):
                        gout = gout_temp.match(contribution)
                        if not gout.group(2) == None:
                            wish_list.append(gout.group(2))
                        gout_contributions.append(gout.group(1) + ' ---> QUESTION ' + question2[0].text.replace('\n', '').strip())


                    #*************************************************************************************

                    #                   CREER SORTIE WEB

                    #*************************************************************************************

                    count_sortie_web +=1

                    if count_sortie_web < 100000:

                        web_file.write('<tr>\n<td>'+ nom.strip() + '</td>\n<td class="td2">' + contribution.strip() + '</td>\n</tr>' )
                    else:
                        web_file.close()

            except etree.XMLSyntaxError:
                pass

    #*************************************************************************************

    #                   ECRIRE SORTIE POUR les utilisateur

    #*************************************************************************************

    # ECRIRE INFORMATIONS SUR LE SEXE


    # verifier si les informations de GOUT, CSP, ou SEXE ont été trouvées

    if len(gout_contributions) > 0 or len(csp_professions) > 0 or len(exemple_contrbF) > 0 or len(exemple_contrbM) > 0:
        count_good_user +=1
        ctrl_file +=1
        if ctrl_file == 1000 :
            resultat.close()
            ctrl_file = 0
            count_file +=1
            resultat = open('./BASE_TESTE/RESULTADOS/resultat_' + str(count_file) + '.txt', 'w')


        resultat.write('##############################################################################' + '\n' + '\n')

        if not nom == None:
            # ecrire nom complet, dans le fichier de resultas
            resultat.write('- NICKNAME COMPLET : ' + nom + ' \n')
            # ecrire nom nettoye dans le fichier de resultat
            resultat.write('- NOM APRES DE NETTOYAGE : ' + nom_min + '\n')
        else:
            # ecrire nom complet, dans le fichier de resultas
            resultat.write('- NICKNAME COMPLET : inconnue \n')
            resultat.write('- NOM APRES DE NETTOYAGE : inconnue \n')

        resultat.write('- LE NOM EST IDENTIFIE COMME : \n' + sexe_nom)
        resultat.write('NOMBRE DE CONTRIBUTIONs : ' + str(nom_contr) + '\n\n')

        resultat.write(' ÂGEs DECLARÉs : \n')

        if len(set_age)> 1:
            count_type_comment['age'] +=1
            count_type_comment['test_tout'] +=1
            resultat.write('cet utilisateur a déclaré ' + str(len(set_age)) + ' différents.' + '\n')

        for t in set_age:

            # todo criar metodo para converter idade por extenso em int!!!!
            resultat.write('- ' + t + '\n')

        resultat.write('\n')

        resultat.write('** SOMMAIRE : ** \n\n      - SEXE - \n')

        pourcentage1 = 0
        pourcentage2 = 0

        total = indices['f']+indices['m']
        if indices['f'] > 0:
            resultat.write(str( (indices['f'] / total) * 100) + '% des indices indiquent que l`utilisateur est une FEMME' + '\n')
            # inserir informacao tipo encontrado
            pourcentage2 =  (indices['f'] / total) * 100

        if indices['m'] > 0:
            resultat.write(str( (indices['m'] / total) * 100) + '% des indices indiquent que l`utilisateur est un HOMME' + '\n\n')
            pourcentage1 = (indices['m'] / total) * 100

        if indices['f'] > 0:

            if len(exemple_contrbF) > 0:
                resultat.write('Exemples de contributions où l`utilisateur écrit comme une femme: \n')

                for i in exemple_contrbF:
                    resultat.write('"'+ i + '"  ')

        if indices['m'] > 0:

            if len(exemple_contrbM) > 0:
                resultat.write('Exemples de contributions où l`utilisateur écrit comme un homme: \n')

                for i in exemple_contrbM:
                    resultat.write('"'+ i + '"')

        resultat.write('\n')


        if pourcentage1 > 90 or pourcentage2 > 90:
            count_type_comment['sexe'] +=1
            count_type_comment['test_tout'] +=1


        # ECRIRE INFORMATIONS SUR LA CSP

        resultat.write('\n\n      - CSP - \n')

        if len(csp_professions) > 0:
            resultat.write('Profsseion déclarées par l`utilisateur : \n')
            for i in csp_professions:
                resultat.write(i + '\n')

        if len(csp_contributions) > 0:
            resultat.write('Exemples de contribution avec contenu CSP: \n')
            for p in csp_contributions:
                resultat.write('"' + p + '"')
                count_type_comment['csp'] +=1
                count_type_comment['test_tout'] +=1
            resultat.write('\n')
        else:
            resultat.write('aucune information de CSP trouvée \n\n')


        # ECRIRE INFORMATIONS SUR lE GOUT
        resultat.write('\n      - GOUTS & WISH List - \n\n')

        if len(wish_list) > 0:
            resultat.write('L`utilisateur semble avoir envie de posseder les itens ci-dessous : \n')
            count_type_comment['gout'] +=1
            count_type_comment['test_tout'] +=1

            for i in wish_list:
                resultat.write(' - ' + i + '\n')

            resultat.write('Exemples de contribution avec contenu GOUT: \n')
            for p in gout_contributions:
                resultat.write('"' + p + '"')
            resultat.write('\n')

        else:
            resultat.write('Aucune information de gout trouvee. \n\n\n\n')

        # verificar resultat da contagem do tipo de comentario econtrado
        if count_type_comment['test_tout'] == 1:
            count_type_comment['type1'] +=1

        if count_type_comment['test_tout'] == 2:
            count_type_comment['type2'] +=1

        if count_type_comment['test_tout'] == 3:
            count_type_comment['type2'] +=1

        if count_type_comment['test_tout'] == 4:
            count_type_comment['TOUT'] +=1

        # zerar variavel para recommecar contagem
        count_type_comment['test_tout'] = 0

resultat.write("******************************************************************************************")
resultat.write('\n')
resultat.write('numero total de usuário :' + str(nb_utilisateurs))
resultat.write('\n')
resultat.write('numero de usuario com comentarios :'+ str(count_good_user))

resultat.write('\n')


resultat.write('-------> EM RELACAO AO TODO  < --------------------')
resultat.write('\n')
if sexe_user['f'] > 0 and nb_utilisateurs > 0:
    resultat.write('a media de mulheres : ' + str(sexe_user['f'] / nb_utilisateurs))
resultat.write('\n')
if sexe_user['m'] > 0 and nb_utilisateurs > 0:
    resultat.write('a media de homens : ' + str(sexe_user['m'] / nb_utilisateurs))
resultat.write('\n')
if sexe_user['?'] > 0 and nb_utilisateurs > 0:
    resultat.write('a media de nao-ident : ' + str(sexe_user['?'] / nb_utilisateurs))
resultat.write('\n')
if nb_utilisateurs > 0:
    if count_type_comment['TOUT'] > 0:
        resultat.write('porcentagem de usuario com comentario nas 4 categorias: ' + str((count_type_comment['TOUT']/ nb_utilisateurs)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['type3'] > 0:
        resultat.write('porcentagem de usuario com comentario em 3 categorias: ' + str((count_type_comment['type3']/ nb_utilisateurs)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['type2'] > 0:
        resultat.write('porcentagem de usuario com comentario em 2 categorias: ' + str((count_type_comment['type2']/ nb_utilisateurs)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['type1'] > 0:
        resultat.write('porcentagem de usuario com comentario em 1 categoria: ' + str((count_type_comment['type1']/ nb_utilisateurs)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['sexe'] > 0:
        resultat.write('porcentagem de usuario que nos conhecemos o sexo : ' + str((count_type_comment['sexe']/ nb_utilisateurs)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['age'] > 0:
        resultat.write('porcentagem de usuario que nos conhecemos a idade : ' + str((count_type_comment['age']/ nb_utilisateurs)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['csp'] > 0:
        resultat.write('porcentagem de usuario que nos conhecemos a csp: ' + str((count_type_comment['csp']/ nb_utilisateurs)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['gout'] > 0:
        resultat.write('porcentagem de usuario que nos conhecemos algo sobre o gout: ' + str((count_type_comment['gout']/ nb_utilisateurs)*100) + ' %')

resultat.write('\n')
resultat.write('-------> EM RELACAO AOS USUARIO COM DADOS   < --------------------')


if count_good_user > 0:
    resultat.write('\n')
    if sexe_user['f'] > 0:
        resultat.write('a media de mulheres : ' + str(sexe_user['f'] / count_good_user))
    resultat.write('\n')
    if sexe_user['m'] > 0:
        resultat.write('a media de homens : ' + str(sexe_user['m'] / count_good_user))
    resultat.write('\n')
    if sexe_user['?'] > 0:
        resultat.write('a media de nao-ident : ' + str(sexe_user['?'] / count_good_user))
    resultat.write('\n')
    if count_type_comment['TOUT'] > 0:
        resultat.write('porcentagem de usuario com comentario nas 4 categorias: ' + str((count_type_comment['TOUT']/ count_good_user)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['type3'] > 0:
        resultat.write('porcentagem de usuario com comentario em 3 categorias: ' + str((count_type_comment['type3']/ count_good_user)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['type2'] > 0:
        resultat.write('porcentagem de usuario com comentario em 2 categorias: ' + str((count_type_comment['type2']/ count_good_user)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['type1'] > 0:
        resultat.write('porcentagem de usuario com comentario em 1 categoria: ' + str((count_type_comment['type1']/ count_good_user)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['sexe'] > 0:
        resultat.write('porcentagem de usuario que nos conhecemos o sexo : ' + str((count_type_comment['sexe']/ count_good_user)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['age'] > 0:
        resultat.write('porcentagem de usuario que nos conhecemos a idade : ' + str((count_type_comment['age']/ count_good_user)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['csp'] > 0:
        resultat.write('porcentagem de usuario que nos conhecemos a csp: ' + str((count_type_comment['csp']/ count_good_user)*100) + ' %')
        resultat.write('\n')
    if count_type_comment['gout'] > 0:
        resultat.write('porcentagem de usuario que nos conhecemos algo sobre o gout: ' + str((count_type_comment['gout']/ count_good_user)*100) + ' %')

# continuer traitement avec des regex
resultat.close()
log.close()
