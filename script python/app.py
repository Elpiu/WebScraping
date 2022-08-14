
#    Documents by author
#    Citations
#    h-index

"""Lettura dei link degli autori da file, il file deve terminare con un \n

Keyword arguments:
argument -- description
Return: list of links
"""
def prendiLink():
    #Lettura del file degli autori e link
    lines = []
    #RICERCADOCENTI.txt
    with open("dati/RICERCADOCENTI.txt","r") as txt_file:
        #Skip frist line
        txt_file.readline()
        lines = txt_file.readlines()

    #Presa dei link
    links = []
    for l in lines:
        links.append(l[l.find("http"):])
    
    return links


"""Core dell'applicazione, simula il browser con un driver, carica il DOM
   di pagina (con uan richesta request.get() non viene caricata tutta la
   pagina ma solo il suo codice sorgente), attraverso il driver è possibile
   caricare il DOM come se si stesse facendo 'inspect' da browser, la ricerca
   dei dati viene fatta semplicamente con una find e stringcutting

    Documents by author
    Citations
    h-index

Keyword arguments: pagina html
argument -- page
Return: Autore e metricsOverview 
"""
def prendiMetriche(page):
    from selenium import webdriver
    import time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    #Path di gecko driver
    path = "geckodriver\\geckodriver.exe"

    driver=webdriver.Firefox(executable_path=path)
    
    driver.get(page)
    #driver.set_page_load_timeout(5000)
    delay=5

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'authorProfileForm')))
    except TimeoutException:
        #close browser
        driver.close()
        driver.quit()
        raise TimeoutException
    
    
    
    html = driver.page_source

    #import io
    #fname = "out.html"
    #with io.open(fname, "w", encoding="utf-8") as f:
    #    f.write(html)

    patternName='<h2 class="AuthorHeader-module__syvlN margin-size-4-t">'
    position = html.find(patternName)
    subString = html[position:len(patternName)+position+30]
    titleName=  subString[subString.find('>')+1:subString.find('</')]
    

    pattern='<els-typography tag="h3" variant="tertiary-header" class="hydrated">'
    s1=html.find(pattern)
    sString1=html[s1:s1+len(pattern)+10]
    #Sposta avanti
    html = html[s1+len(pattern)+10:]
    s2=html.find(pattern)
    sString2=html[s2:s2+len(pattern)+10]
    #Sposta avanti
    html = html[s2+len(pattern)+10:]
    s3=html.find(pattern)
    sString3=html[s3:s3+len(pattern)+10]

    data= []
    x1,x2 = titleName.split(',')
    data.append(x1)
    data.append(x2[1:])

    data.append(sString1[sString1.find('>')+1:sString1.find('</')])
    data.append(sString2[sString2.find('>')+1:sString2.find('</')])
    data.append(sString3[sString3.find('>')+1:sString3.find('</')])

    
    #close browser
    driver.close()
    driver.quit()

    return data



from selenium.common.exceptions import TimeoutException
links = prendiLink()

#Prepara file csv

#Debug
currentPosition=1

import io
fname = "out.csv"
with io.open(fname, "w") as f:
    f.write("Cognome,Nome,Documents by author,Citations,h-index"+ "\n")

#Per ogni link prendi i dati degli autori
    for link in links:
        #Se ci sono errori di caricamento Riprova (ATTENZIONE LOOP!)
        while True:
            try:
                data = prendiMetriche(link)
            except (TimeoutException,ValueError):
                continue
            break
        
        #Debug
        print(link + f"     -->Count {currentPosition}")
        print(f"{data[0]},{data[1]},{data[2]},{data[3]},{data[4]}"+ "\n")
        f.write(f"{data[0]},{data[1]},{data[2]},{data[3]},{data[4]}"+ "\n")
        f.flush()
        currentPosition+=1


#Alcune pagine non vengono caricate e rimangono appese in memoria
    #bisogna uccidere il processo dopo 10secondi tipo
#Se ci sono dai deati con nome,cognome,,, riprova un numero di volte

#Se accade uno dei due eventi sopra citati scrivere il su un file di 
# log che a quel link non è stato possibile ricavare i dati (VAI AVANTI)





