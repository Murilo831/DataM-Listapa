from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import csv
import time
from math import ceil

inicio = time.time()

# Caso queira mudar o tempo de cada click
timeSleep = 2.5

# NÃO MEXER NESSE
t = csv.writer(open('test', 'w'))
t.writerow(['urls'])

# ALTERAR ESSE
f = csv.writer(open('Natal - Doce.csv', 'w'))
f.writerow(['Phone'])

html = ['https://listapa.com.br/busca/q=Doce&cid=Natal%2CRN&p=1']

allUrls = []


# Pega os Links de todas as outras paginas
def todasUrls(html):
    cont = 1

    restoDivi1 = 37
    contando1 = 0

    voltas = 0
    quebra = 0
    div10 = 0

    urls = []

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(0.5)
    driver.get(html)
    while True:
        contando1 += 1
        try:

            test = driver.find_element_by_xpath('//div[@id="boxTotalEnco"]/strong')

            source_code = test.get_attribute("outerHTML")
            soup = BeautifulSoup(source_code, 'html.parser')
            break
        except NoSuchElementException:
            if contando1 == 1:
                print('A pagina ainda não carregou.\nAguarde alguns segundos... ')
            continue

    for quant in soup:
        for num in quant:
            print(num)

            div10 = int(num)

            quebra = div10 / 10

            voltas = ceil(quebra)
            print(voltas)

    for i in range(voltas):

        restoDivi = 37
        contando = 0
        if i == 0:
            sleep(timeSleep)

            test = driver.find_element_by_xpath("//*")

            source_code = test.get_attribute("outerHTML")

            soup = BeautifulSoup(source_code, 'html.parser')

        else:
            # Botão para o próxima pagina
            driver.find_element_by_xpath('//i[@class="fa fa-chevron-right"]').click()

            sleep(timeSleep)
            contando = 0
            # Carrega a pagina
            while True:
                contando1 += 1
                try:
                    # elemento
                    e = driver.find_element_by_xpath("//ul[@class='pagination']")

                    # Pega as dimensões do site
                    location = e.location
                    size = e.size
                    w, h = size['width'], size['height']
                    # Desce o scroll até a posição do elemento
                    driver.execute_script(f"window.scrollTo(0,{h})")
                    #print(location)
                    #print(size)
                    #print(w, h)

                    # volta e sempre um a +
                    if i < voltas-1:
                        test = driver.click = driver.find_element_by_xpath('//i[@class="fa fa-chevron-right"]')

                        source_code = test.get_attribute("outerHTML")
                        BeautifulSoup(source_code, 'html.parser')
                    else:
                        # Pega a posição do ultimo elemento
                        test = driver.click = driver.find_element_by_xpath(f'//ul[@class="pagination"]//li[@class="active"]')

                        source_code = test.get_attribute("outerHTML")
                        BeautifulSoup(source_code, 'html.parser')
                    break
                except NoSuchElementException:
                    if contando1 == 1:
                        print('A pagina ainda não carregou.\nAguarde alguns segundos...1 ')
                    continue

            # Pega os dados já carregados
            while True:

                contando += 1
                try:
                    test = driver.find_element_by_xpath("//*")

                    source_code = test.get_attribute("outerHTML")

                    soup = BeautifulSoup(source_code, 'html.parser')
                    break

                except NoSuchElementException:
                    if contando == 1:
                        print('A pagina ainda não carregou.\nAguarde alguns segundos...2 ')
                    else:
                        break
                    continue
                except ElementClickInterceptedException:
                    if contando == 1:
                        print('Botão para clicar ainda não apareceu ')
                    else:
                        break
                    continue

        contentLinks = soup.find(id='content')

        url = []

        # Pega os links
        def takeLinks(content):
            lista = []
            links = content.find_all('div', class_='panel-body')

            for link in links:
                dados = link.find_all('h5')
                for dado in dados:
                    data = dado.find_all('a')
                    for values in data:
                        value = values.get('href')
                        lista.append(value)
            # print(lista)
            return lista

        url = takeLinks(contentLinks)
        print(url)

        urls += url

        txt = urls
        t.writerow([txt])

        print(f'------------{cont} de {voltas}')
        cont += 1

    driver.close()
    return urls


for i in range(len(html)):
    vetAllLinks = todasUrls(html[i])

allUrls += vetAllLinks

print(allUrls)


# Pega o numero do estabelecimento
def takeNumber(dados):
    numeros = []
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(2.5)
    for i in range(len(dados)):
        url = dados[i]
        try:
            driver.get(url)
        except WebDriverException:
            continue
        volNum = 0
        contErro = 0
        while True:
            contErro += 1
            volNum += 1
            try:
                name = driver.find_element_by_class_name('listaTitulo')
                name.click()

                sleep(2.5)

                break
            except TimeoutException:
                if volNum == 1:
                    print('O site ainda não carregou\nAguarde uns segundos...1')
                continue
            except NoSuchElementException:
                print('carregando...')
                if contErro == 3:
                    break
                else:
                    continue
            except ElementClickInterceptedException:
                print('Botão para clicar ainda não apareceu ')
                continue
            except WebDriverException:
                continue

        try:
            name = driver.find_element_by_class_name('listaTitulo')
            name.click()

            sleep(2.5)

            valor = driver.find_element_by_id('pTele2')
            valor.click()

            sleep(2.5)
            page = valor.get_attribute('innerHTML')

            soup2 = BeautifulSoup(page, 'html.parser')

            numeros += soup2
            print(f'{i} - numeros')
        except NoSuchElementException:
            numeros += '-'
            print('Não tem')
            continue
        except TimeoutException:
            if volNum == 1:
                print('O site ainda não carregou\nAguarde uns segundos...')
            continue
        except ElementClickInterceptedException:
            continue
        except WebDriverException:
            continue

    return numeros


number = []

number = takeNumber(allUrls)

print(number)

# Add CSV

for i in range(len(number)):
    f.writerow([number[i]])

fim = time.time()
duration = int(fim - inicio)
print(f'durou: {duration} seg')
print(f'FINALIZOU A COLETA DE LINKS')
