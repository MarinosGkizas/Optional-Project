import xlrd
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
import urllib.error
import re
import mysql.connector
import urllib
import csv
import numpy as np
from pandas import DataFrame
import operator



aftouristwn_2011_12 = 'https://www.statistics.gr/en/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113885&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=en'
aftouristwn_2013_14 = 'https://www.statistics.gr/en/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113926&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=en'
#Συνολικές αφίξεις τουριστών στην Ελλάδα για την τετραετία 2011-2015

#Ανάκτηση δεδομένων από την ιστοσελίδα και μεταονομασία και πρόβλεψη λαθών
try:
    req = urllib.request.urlretrieve(aftouristwn_2011_12, "2012.xls") 
       
except urllib.error.HTTPError as e:
	print('Σφάλμα HTTP: ',e.code)
except urllib.error.URLError as e:
	print('Αποτυχία σύνδεσης στο διαδίκτυο')
	print('Αιτία: ',e.reason)

try:
    req = urllib.request.urlretrieve(aftouristwn_2013_14, "2014.xls")
    
except urllib.error.HTTPError as e:
	print('Σφάλμα HTTP: ',e.code)
except urllib.error.URLError as e:
	print('Αποτυχία σύνδεσης στο διαδίκτυο')
	print('Αιτία: ',e.reason)

book = xlrd.open_workbook("2012.xls") #Άνοιγμα του κατεβασμένου αρχειου excel
worksheet = book.sheet_by_index(11) #Επιλογή πίνακα που θέλουμε να δουλέψουμε
arrivals2011 = int(worksheet.cell(138, 2).value) #Επιλογή και μετατροπή σε ακέραιο της τιμής στην γραμμη 138 και στήλη 2
arrivals2012 = int(worksheet.cell(138, 3).value) #Επιλογή και μετατροπή σε ακέραιο της τιμής στην γραμμη 138 και στήλη 3




book = xlrd.open_workbook("2014.xls") #Άνοιγμα του κατεβασμένου αρχειου excel
worksheet = book.sheet_by_index(11) #Επιλογή πίνακα που θέλουμε να δουλέψουμε
arrivals2013 = int(worksheet.cell(137, 2).value) #Επιλογή και μετατροπή σε ακέραιο της τιμής στην γραμμη 137 και στήλη 2
arrivals2014 = int(worksheet.cell(137, 3).value) #Επιλογή και μετατροπή σε ακέραιο της τιμής στην γραμμη 137 και στήλη 3

    
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "51ffa881d4",
    port = '3306',
    database = "mydatabase"
    )                           #Δημιουργία βάσης δεδομένων
cursor = db.cursor()
#Δημιουργία table για συνολικές αφίξεις τουριστών για 2011-2014
cursor.execute("CREATE TABLE synolo_touristwn(Etos INT, Synolo INT)") #Δημιουργία table
sql = "INSERT INTO synolo_touristwn(Etos,Synolo) VALUES(%s,%s)" #Εισαγωγή δεδομένων στο table
val = [ ('2011', arrivals2011),
        ('2012', arrivals2012),        
        ('2013', arrivals2013),
        ('2014', arrivals2014) ]
cursor.executemany(sql,val)
db.commit()
#Δημιουργία csv αρχείου
with open('touristes_file', mode='w') as touristes_file:
    touristes_writer = csv.writer(touristes_file,delimiter = '-',quotechar = '|',quoting = csv.QUOTE_ALL)
    touristes_writer.writerow   (   ['Etos','Synolo']   )
    touristes_writer.writerow   (   ['2011',arrivals2011]   )
    touristes_writer.writerow   (   ['2012',arrivals2012]   )
    touristes_writer.writerow   (   ['2013',arrivals2013]   )
    touristes_writer.writerow   (   ['2014',arrivals2014]   )
#Δημιουργία γραφήματος
plt.bar (   [2011]  , [arrivals2011], label = "2011", color = 'red')
plt.bar (   [2012]  , [arrivals2012], label = "2012", color = 'yellow')
plt.bar (   [2013]  , [arrivals2013], label = "2013", color = 'b')
plt.bar (   [2014]  , [arrivals2014], label = "2014", color = 'g')
plt.legend()
plt.xlabel('Χρονολογίες')
plt.ylabel('Τουρίστες(*10.000.000)')

plt.title('Διάγραμμα τουριστών/χρονολογία')

plt.show()


#Αφίξεις τουριστών στην Ελλάδα ανά τρίμηνο το 2011-2014
book = xlrd.open_workbook("2012.xls") #Άνοιγμα του κατεβασμένου αρχειου excel
worksheet = book.sheet_by_index(0) #Επιλογή πίνακα που θέλουμε να δουλέψουμε
arrivals_jan_2011 = int(worksheet.cell(66, 2).value) 
arrivals_jan_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(1)
arrivals_feb_2011 = int(worksheet.cell(66, 2).value)
arrivals_feb_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(2)
arrivals_mar_2011 = int(worksheet.cell(66, 2).value)
arrivals_mar_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(3)
arrivals_apr_2011 = int(worksheet.cell(66, 2).value)
arrivals_apr_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(4)
arrivals_may_2011 = int(worksheet.cell(66, 2).value)
arrivals_may_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(5)
arrivals_jun_2011 = int(worksheet.cell(66, 2).value)
arrivals_jun_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(6)
arrivals_jul_2011 = int(worksheet.cell(66, 2).value)
arrivals_jul_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(7)
arrivals_aug_2011 = int(worksheet.cell(66, 2).value)
arrivals_aug_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(8)
arrivals_sep_2011 = int(worksheet.cell(66, 2).value)
arrivals_sep_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(9)
arrivals_oct_2011 = int(worksheet.cell(66, 2).value)
arrivals_oct_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(10)
arrivals_nov_2011 = int(worksheet.cell(66, 2).value)
arrivals_nov_2012 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(11)
arrivals_dec_2011 = int(worksheet.cell(66, 2).value)
arrivals_dec_2012 = int(worksheet.cell(66, 3).value)
 
book = xlrd.open_workbook("2014.xls") #Άνοιγμα του κατεβασμένου αρχειου excel
worksheet = book.sheet_by_index(0)
arrivals_jan_2013 = int(worksheet.cell(66, 2).value) 
arrivals_jan_2014 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(1)
arrivals_feb_2013 = int(worksheet.cell(66, 2).value) 
arrivals_feb_2014 = int(worksheet.cell(66, 3).value) 

worksheet = book.sheet_by_index(2)
arrivals_mar_2013 = int(worksheet.cell(66, 2).value)
arrivals_mar_2014 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(3)
arrivals_apr_2013 = int(worksheet.cell(66, 2).value)
arrivals_apr_2014 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(4)
arrivals_may_2013 = int(worksheet.cell(66, 2).value)
arrivals_may_2014 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(5)
arrivals_jun_2013 = int(worksheet.cell(66, 2).value)
arrivals_jun_2014 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(6)
arrivals_jul_2013 = int(worksheet.cell(66, 2).value)
arrivals_jul_2014 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(7)
arrivals_aug_2013 = int(worksheet.cell(66, 2).value)
arrivals_aug_2014 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(8)
arrivals_sep_2013 = int(worksheet.cell(66, 2).value)
arrivals_sep_2014 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(9)
arrivals_oct_2013 = int(worksheet.cell(66, 2).value)
arrivals_oct_2014 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(10)
arrivals_nov_2013 = int(worksheet.cell(66, 2).value)
arrivals_nov_2014 = int(worksheet.cell(66, 3).value)

worksheet = book.sheet_by_index(11)
arrivals_dec_2013 = int(worksheet.cell(66, 2).value)
arrivals_dec_2014 = int(worksheet.cell(66, 3).value)
 
arrivals_jan_mar_2011 = int(arrivals_jan_2011) + int(arrivals_feb_2011) + int(arrivals_mar_2011)
arrivals_apr_jun_2011 = int(arrivals_apr_2011) + int(arrivals_may_2011) + int(arrivals_jun_2011)
arrivals_jul_sep_2011 = int(arrivals_jul_2011) + int(arrivals_aug_2011) + int(arrivals_sep_2011)
arrivals_oct_dec_2011 = int(arrivals_oct_2011) + int(arrivals_nov_2011) + int(arrivals_dec_2011)

arrivals_jan_mar_2012 = int(arrivals_jan_2012) + int(arrivals_feb_2012) + int(arrivals_mar_2012)
arrivals_apr_jun_2012 = int(arrivals_apr_2012) + int(arrivals_may_2012) + int(arrivals_jun_2012)
arrivals_jul_sep_2012 = int(arrivals_jul_2012) + int(arrivals_aug_2012) + int(arrivals_sep_2012)
arrivals_oct_dec_2012 = int(arrivals_oct_2012) + int(arrivals_nov_2012) + int(arrivals_dec_2012)

arrivals_jan_mar_2013 = int(arrivals_jan_2013) + int(arrivals_feb_2013) + int(arrivals_mar_2013)
arrivals_apr_jun_2013 = int(arrivals_apr_2013) + int(arrivals_may_2013) + int(arrivals_jun_2013)
arrivals_jul_sep_2013 = int(arrivals_jul_2013) + int(arrivals_aug_2013) + int(arrivals_sep_2013)
arrivals_oct_dec_2013 = int(arrivals_oct_2013) + int(arrivals_nov_2013) + int(arrivals_dec_2013)

arrivals_jan_mar_2014 = int(arrivals_jan_2014) + int(arrivals_feb_2014) + int(arrivals_mar_2014)
arrivals_apr_jun_2014 = int(arrivals_apr_2014) + int(arrivals_may_2014) + int(arrivals_jun_2014)
arrivals_jul_sep_2014 = int(arrivals_jul_2014) + int(arrivals_aug_2014) + int(arrivals_sep_2014)
arrivals_oct_dec_2014 = int(arrivals_oct_2014) + int(arrivals_nov_2014) + int(arrivals_dec_2014)

cursor.execute("CREATE TABLE afikseis_ana_trimhno(Trimhno VARCHAR(255), Afikseis INT)")
sql = "INSERT INTO afikseis_ana_trimhno(Trimhno , Afikseis) VALUES (%s,%s)"
val = [ ('Jan-Mar-2011' , arrivals_jan_mar_2011),
		('Apr-Jun-2011' , arrivals_apr_jun_2011),
		('Jul-Sep-2011' , arrivals_jul_sep_2011),
		('Oct-Dec-2011' , arrivals_oct_dec_2011),
		('Jan-Mar-2012' , arrivals_jan_mar_2012),
		('Apr-Jun-2012' , arrivals_apr_jun_2012),
		('Jul-Sep-2012' , arrivals_jul_sep_2012),
		('Oct-Dec-2012' , arrivals_oct_dec_2012),
		('Jan-Mar-2013' , arrivals_jan_mar_2013),
		('Apr-Jun-2013' , arrivals_apr_jun_2013),
		('Jul-Sep-2013' , arrivals_jul_sep_2013),
		('Oct-Dec-2013' , arrivals_oct_dec_2013),
		('Jan-Mar-2014' , arrivals_jan_mar_2014),
		('Apr-Jun-2014' , arrivals_apr_jun_2014),
		('Jul-Sep-2014' , arrivals_jul_sep_2014),
		('Oct-Dec-2014' , arrivals_oct_dec_2014) ]
cursor.executemany(sql,val)
db.commit()

#Δημιουργία csv αρχείου
with open('touristes_ana_trimhno', mode = 'w') as touristes_ana_trimhno:
			touristes_writer = csv.writer(touristes_ana_trimhno, delimiter = '-', quotechar = '|' , quoting = csv.QUOTE_ALL)
			touristes_writer.writerow   (   ['Trimhno' , 'Afikseis'  ]   )
			touristes_writer.writerow   (   ['Jan-Mar-2011', arrivals_jan_mar_2011]   )
			touristes_writer.writerow   (   ['Apr-Jun-2011', arrivals_apr_jun_2011]   )
			touristes_writer.writerow   (   ['Jul-Sep-2011', arrivals_jul_sep_2011]   )
			touristes_writer.writerow   (	['Oct-Dec-2011', arrivals_oct_dec_2011]   )
			touristes_writer.writerow   (	['Jan-Mar-2012', arrivals_jan_mar_2012]   )
			touristes_writer.writerow   (	['Apr-Jun-2012', arrivals_apr_jun_2012]   )
			touristes_writer.writerow   (	['Jul-Sep-2012', arrivals_jul_sep_2012]   )
			touristes_writer.writerow   (	['Oct-Dec-2012', arrivals_oct_dec_2012]   )	
			touristes_writer.writerow   (	['Jan-Mar-2013', arrivals_jan_mar_2013]   )
			touristes_writer.writerow   (	['Apr-Jun-2013', arrivals_apr_jun_2013]   )
			touristes_writer.writerow   (	['Jul-Sep-2013', arrivals_jul_sep_2013]   )
			touristes_writer.writerow   (	['Oct-Dec-2013', arrivals_oct_dec_2013]   )
			touristes_writer.writerow   (	['Jan-Mar-2014', arrivals_jan_mar_2014]   )
			touristes_writer.writerow   (	['Apr-Jun-2014', arrivals_apr_jun_2014]   )
			touristes_writer.writerow   (	['Jul-Sep-2014', arrivals_jul_sep_2014]   )
			touristes_writer.writerow   (	['Oct-Dec-2014', arrivals_oct_dec_2014]   )
			
#Δημιουργία γραφήματος
plt.bar([0,4,8,12], [arrivals_jan_mar_2011, arrivals_jan_mar_2012, arrivals_jan_mar_2013 , arrivals_jan_mar_2014], label= "Jan-Mar", color = 'b' )
plt.bar([1,5,9,13], [arrivals_apr_jun_2011, arrivals_apr_jun_2012, arrivals_apr_jun_2013 , arrivals_apr_jun_2014], label= "Apr-Jun", color = 'g' )
plt.bar([2,6,10,14], [arrivals_jul_sep_2011, arrivals_jul_sep_2012, arrivals_jul_sep_2013 , arrivals_jul_sep_2014], label= "Jul-Sep", color = 'y' )
plt.bar([3,7,11,15], [arrivals_jan_mar_2011, arrivals_jan_mar_2012, arrivals_jan_mar_2013 , arrivals_jan_mar_2014], label= "Jan-Mar", color = 'purple')
plt.legend()
plt.xlabel('Τρίμηνα')
plt.ylabel('Αφίξεις(*10.000.000)')

locs, labels = plt.xticks()
plt.xticks(range(16),('2011', '2011', '2011', '2011','2012', '2012', '2012', '2012','2013', '2013', '2013', '2013','2014', '2014', '2014', '2014'))
plt.xticks(rotation=45)
plt.xticks(fontsize=9)
plt.yticks(range(0, 14000000,2000000))

plt.yticks(fontsize=9)

plt.title('Αφίξεις/Τρίμηνο')
plt.show()



#Aφίξεις τουριστών στην Ελλάδα ανά μέσο μεταφοράς για 2011-2014

af_ana_meso_2011 = 'https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113865&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el'
af_ana_meso_2012 = 'https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113886&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el'
af_ana_meso_2013 = 'https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113905&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el'
af_ana_meso_2014 = 'https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113925&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el'

try:
    req = urllib.request.urlretrieve(af_ana_meso_2011, "af_ana_meso_2011.xls") 
       
except urllib.error.HTTPError as e:
	print('Σφάλμα HTTP: ',e.code)
except urllib.error.URLError as e:
	print('Αποτυχία σύνδεσης στο διαδίκτυο')
	print('Αιτία: ',e.reason)

try:
    req = urllib.request.urlretrieve(af_ana_meso_2012, "af_ana_meso_2012.xls")
    
except urllib.error.HTTPError as e:
	print('Σφάλμα HTTP: ',e.code)
except urllib.error.URLError as e:
	print('Αποτυχία σύνδεσης στο διαδίκτυο')
	print('Αιτία: ',e.reason)

try:
    req = urllib.request.urlretrieve(af_ana_meso_2013, "af_ana_meso_2013.xls") 
       
except urllib.error.HTTPError as e:
	print('Σφάλμα HTTP: ',e.code)
except urllib.error.URLError as e:
	print('Αποτυχία σύνδεσης στο διαδίκτυο')
	print('Αιτία: ',e.reason)

try:
    req = urllib.request.urlretrieve(af_ana_meso_2014, "af_ana_meso_2014.xls")
    
except urllib.error.HTTPError as e:
	print('Σφάλμα HTTP: ',e.code)
except urllib.error.URLError as e:
	print('Αποτυχία σύνδεσης στο διαδίκτυο')
	print('Αιτία: ',e.reason)


book = xlrd.open_workbook("af_ana_meso_2011.xls") #Άνοιγμα του κατεβασμένου αρχειου excel
worksheet = book.sheet_by_index(11) #Επιλογή πίνακα που θέλουμε να δουλέψουμε
aer_2011 = int(worksheet.cell(134, 2).value) 
sid_2011 = int(worksheet.cell(134, 3).value)
thal_2011 = int(worksheet.cell(134, 4).value) 
odikws_2011 = int(worksheet.cell(134, 5).value)

book = xlrd.open_workbook("af_ana_meso_2012.xls") #Άνοιγμα του κατεβασμένου αρχειου excel
worksheet = book.sheet_by_index(11) #Επιλογή πίνακα που θέλουμε να δουλέψουμε
aer_2012 = int(worksheet.cell(136, 2).value) 
sid_2012 = int(worksheet.cell(136, 3).value)
thal_2012 = int(worksheet.cell(136, 4).value) 
odikws_2012 = int(worksheet.cell(136, 5).value)

book = xlrd.open_workbook("af_ana_meso_2013.xls") #Άνοιγμα του κατεβασμένου αρχειου excel
worksheet = book.sheet_by_index(11) #Επιλογή πίνακα που θέλουμε να δουλέψουμε
aer_2013 = int(worksheet.cell(136, 2).value) 
sid_2013 = int(worksheet.cell(136, 3).value)
thal_2013 = int(worksheet.cell(136, 4).value) 
odikws_2013 = int(worksheet.cell(136, 5).value)

book = xlrd.open_workbook("af_ana_meso_2014.xls") #Άνοιγμα του κατεβασμένου αρχειου excel
worksheet = book.sheet_by_index(11) #Επιλογή πίνακα που θέλουμε να δουλέψουμε
aer_2014 = int(worksheet.cell(136, 2).value) 
sid_2014 = int(worksheet.cell(136, 3).value)
thal_2014 = int(worksheet.cell(136, 4).value) 
odikws_2014 = int(worksheet.cell(136, 5).value)


cursor.execute("CREATE TABLE touristes_af_ana_meso(etos INT, aeroporikws INT, sidhrodromikws INT, thalassiws INT, odikws INT)") #Δημιουργία table
sql = "INSERT INTO touristes_af_ana_meso(etos, aeroporikws, sidhrodromikws, thalassiws, odikws) VALUES(%s,%s,%s,%s,%s)" #Εισαγωγή δεδομένων στο table
val = [ ('2011', aer_2011, sid_2011, thal_2011, odikws_2011),
        ('2012', aer_2012, sid_2012, thal_2012, odikws_2012),        
        ('2013', aer_2013, sid_2013, thal_2013, odikws_2013),
        ('2014', aer_2014, sid_2014, thal_2014, odikws_2014) ]
cursor.executemany(sql,val)
db.commit()

#Δημιουργία csv αρχειου
with open('touristes_af_ana_meso', mode='w') as touristes_af_ana_meso:
    touristes_writer = csv.writer(touristes_af_ana_meso,delimiter = '-',quotechar = '|',quoting = csv.QUOTE_ALL)
    touristes_writer.writerow(['Etos','Aeroporikws', 'Sidhrodromikws', 'Thalassiws', 'Odikws'])
    touristes_writer.writerow  (   ['2011', aer_2011, sid_2011, thal_2011, odikws_2011]  )
    touristes_writer.writerow  (   ['2012', aer_2012, sid_2012, thal_2012, odikws_2012]  )
    touristes_writer.writerow  (   ['2013', aer_2013, sid_2013, thal_2013, odikws_2013]  )
    touristes_writer.writerow  (   ['2014', aer_2014, sid_2014, thal_2014, odikws_2014]  )

#Δημιουργία γραφήματος
plt.bar([0,4,8,12], [aer_2011, aer_2012, aer_2013, aer_2014], label= "Αεροπορικώς", color = 'r' )
plt.bar([1,5,9,13], [sid_2011, sid_2012, sid_2013, sid_2014 ], label= "Σιδηροδρομικώς", color = 'teal' )
plt.bar([2,6,10,14], [thal_2011, thal_2012, thal_2013, thal_2014], label= "Θαλασσίως", color = 'chocolate' )
plt.bar([3,7,11,15], [odikws_2011, odikws_2012, odikws_2013, odikws_2014], label= "Οδικώς", color = 'royalblue')
plt.legend()
plt.xlabel('Μέσο Μεταφοράς')
plt.ylabel('Αφίξεις(*100.00.000)')

locs, labels = plt.xticks()
plt.xticks(range(16),('Αεροπορικώς_2011', 'Σιδηροδρομικώς_2011', 'Θαλασσίως_2011', 'Οδικώς_2011', 'Αεροπορικώς_2012', 'Σιδηροδρομικώς_2012', 'Θαλασσίως_2012', 'Οδικώς_2012', 'Αεροπορικώς_2013', 'Σιδηροδρομικώς_2013', 'Θαλασσίως_2013', 'Οδικώς_2013', 'Αεροπορικώς_2014', 'Σιδηροδρομικώς_2014', 'Θαλασσίως_2014', 'Οδικώς_2014' ))
plt.xticks(rotation=20)
plt.xticks(fontsize=7)
plt.yticks(range(0, 14000000,2000000))

plt.yticks(fontsize=9)

plt.title('Αφίξεις/Μέσο Μεταφοράς')
plt.show()

#Χώρες καταγωγής με το μεγαλύτερο μερίδιο στις αφίξεις τουριστών στην Ελλάδα για το 2011-2014
book = xlrd.open_workbook("2012.xls")
sheet = book.sheet_by_index(11)


g2011= int(max(sheet.col_values(2,start_rowx = 79, end_rowx = 111)))
germany = str(sheet.cell(83,1))

u2011 = int(sheet.cell(86,2).value)
united_kingdom = str(sheet.cell(86, 1))

f2011 = int(sheet.cell(82,2).value)
france = str(sheet.cell(82,1))

i2011 = int(sheet.cell(89, 2).value)
italy = str(sheet.cell(89, 1))

g2012= int(max(sheet.col_values(3,start_rowx =79 ,end_rowx = 111)))

u2012 = int(sheet.cell(86, 3).value)
            
f2012 = int(sheet.cell(82,3).value)

r2012 = int(sheet.cell(109, 2).value)
russia = str(sheet.cell(109, 1))

book = xlrd.open_workbook("2014.xls")
sheet = book.sheet_by_index(11)


g2013= int(max(sheet.col_values(2,start_rowx = 78, end_rowx = 110)))
germany1 = str(sheet.cell(83,1))

u2013 = int(sheet.cell(85,2).value)
united_kingdom1 = str(sheet.cell(85, 1))

r2013 = int(sheet.cell(109, 2).value)
russia1 = str(sheet.cell(109 ,1))

f2013 = int(sheet.cell(82, 2).value)
france1 = str(sheet.cell(82, 1))


g2014= int(max(sheet.col_values(3,start_rowx =78 ,end_rowx = 110)))

u2014 = int(sheet.cell(85, 3).value)

b2014 = int(sheet.cell(80, 2).value)
bulgaria1 = str(sheet.cell(80, 1))

f2014 = int(sheet.cell(81, 3).value)



cursor.execute("CREATE TABLE max_touristes(etos INT, xwra VARCHAR(255), afikseis INT)") #Δημιουργία table
sql = "INSERT INTO max_touristes(etos,xwra, afikseis) VALUES(%s,%s,%s)" #Εισαγωγή δεδομένων στο table
val = [ ('2011', germany, g2011),
        ('2011', united_kingdom, u2011),
        ('2011', france, f2011),
        ('2011', italy, i2011),
        ('2012', germany, g2012),
        ('2012', united_kingdom, u2012),
        ('2012', france, f2012),
        ('2012', russia, r2012),
        ('2013', germany1 , g2013),
        ('2013', united_kingdom1 ,u2013),
        ('2013', russia1, r2013),
        ('2013', france1, f2013),
        ('2014', germany1 , g2014),
        ('2014', united_kingdom1 ,u2014),
        ('2014', bulgaria1, b2014),
        ('2014', france1, f2014)]
cursor.executemany(sql,val)
db.commit()

#Δημιουργία csv αρχειου
with open('max_touristes', mode='w') as max_touristes:
    touristes_writer = csv.writer(max_touristes,delimiter = '-',quotechar = '|',quoting = csv.QUOTE_ALL)
    touristes_writer.writerow  (  ['Etos','Xwra','Afikseis'] )
    touristes_writer.writerow  (  ['2011', 'germany', g2011] )
    touristes_writer.writerow  (  ['2011', 'united_kingdom', u2011] )
    touristes_writer.writerow  (  ['2011', 'france' ,f2011]  )
    touristes_writer.writerow  (  ['2011', 'italy', i2011]  )
    touristes_writer.writerow  (  ['2012', 'germany', g2012] )
    touristes_writer.writerow  (  ['2012', 'united_kingdom', u2012] )
    touristes_writer.writerow  (  ['2012', 'france', f2012]  )
    touristes_writer.writerow  (  ['2012', 'russia', r2012]  )
    touristes_writer.writerow  (  ['2013', 'germany', g2013] )
    touristes_writer.writerow  (  ['2013', 'united_kingdom', u2013] )
    touristes_writer.writerow  (  ['2013', 'russia' ,r2013]  )
    touristes_writer.writerow  (  ['2013', 'france', f2013]  )
    touristes_writer.writerow  (  ['2014', 'germany', g2014] )
    touristes_writer.writerow  (  ['2014', 'united_kingdom', u2014] )
    touristes_writer.writerow  (  ['2014', 'bulgaria', b2014]  )
    touristes_writer.writerow  (  ['2014', 'france', f2014]  )

#Δημιουργία γραφήματος1
plt.bar([0], [g2011], label= "Γερμανία 2011", color = 'black')
plt.bar([2], [u2011],label = "Ηνωμένο Βασίλειο 2011",color = 'red')
plt.bar([4],[f2011],label = "Γαλλία 2011", color = 'blue')
plt.bar([6], [i2011],label = "Ιταλία 2011", color ='green')
plt.legend()
plt.ylabel('Αφίξεις(*10.000.000)')


plt.title('Αφίξεις το 2011')
plt.show()

#Δημιουργία γραφήματος2
plt.bar([0], [g2012], label= "Γερμανία 2012", color = 'black')
plt.bar([2], [u2012],label = "Ηνωμένο Βασίλειο 2012",color = 'red')
plt.bar([4],[f2012],label = "Γαλλία 2012", color = 'blue')
plt.bar([6], [r2012],label = "Ρωσία 2012", color ='green')
plt.legend()
plt.ylabel('Αφίξεις(*10.000.000)')


plt.title('Αφίξεις το 2012')
plt.show()

#Δημιουργία γραφήματος3
plt.bar([0], [g2013], label= "Γερμανία 2013", color = 'black')
plt.bar([2], [u2013],label = "Ηνωμένο Βασίλειο 2013",color = 'red')
plt.bar([4],[r2013],label = "Ρωσία 2013", color = 'green')
plt.bar([6], [f2013],label = "Γαλλία 2013", color ='blue')
plt.legend()
plt.ylabel('Αφίξεις(*10.000.000)')


plt.title('Αφίξεις το 2013')
plt.show()
#Δημιουργία γραφήματος4
plt.bar([0], [g2014], label= "Γερμανία 2014", color = 'black')
plt.bar([2], [u2014],label = "Ηνωμένο Βασίλειο 2014",color = 'red')
plt.bar([4],[b2014],label = "Βουλργαρία 2014", color = 'green')
plt.bar([6], [f2014],label = "Γαλλία 2014", color ='blue')
plt.legend()
plt.ylabel('Αφίξεις(*10.000.000)')


plt.title('Αφίξεις το 2014')
plt.show()


    
