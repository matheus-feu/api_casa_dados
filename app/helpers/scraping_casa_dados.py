import re
import time

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from unidecode import unidecode

from app.helpers.utils import convert_state_abbreviation_to_name, list_of_states, parse_other_elements, parse_quadro_societario


class CasaDadosScraper:
    def __init__(self):
        self.driver = None
        self.url_base = 'https://casadosdados.com.br/solucao/cnpj?q='
        self.url_advanced = 'https://casadosdados.com.br/solucao/cnpj/pesquisa-avancada'

    def initialize_selenium(self):
        options = uc.ChromeOptions()
        options.headless = False
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-gpu')
        options.add_argument("--start-minimized")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        self.driver = uc.Chrome(options=options, use_subprocess=False)
        self.driver.delete_all_cookies()

        return self.driver

    @classmethod
    def transform_date(cls, date):
        try:
            return date.strftime("%d/%m/%Y")
        except AttributeError:
            return None

    def fill_input_field(self, xpath, value):
        input_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, xpath)
            )
        )

        if value in list_of_states:
            input_element.send_keys(value)

            try:
                time.sleep(2)
                dropdown_options = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="__nuxt"]/div/div[2]/section/div[3]/div[2]/div/div/div/div/div[2]/div')))

                if dropdown_options:
                    dropdown_options.click()
            except Exception:
                pass
        else:
            input_element.send_keys(value)

    def select_option_by_value(self, xpath, value):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)
            )
        )
        select = Select(element)
        try:
            select.select_by_value(value)
        except NoSuchElementException:
            return None

    def click_button(self, xpath):
        button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, xpath)
            )
        )
        if button:
            button.click()

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def exclude_pop_up(self):
        self.driver.execute_script(
            "const elements = document.getElementsByClassName('adsbygoogle adsbygoogle-noablate'); while (elements.length > 0) elements[0].remove()")

    def get_num_results_and_num_pages(self):
        num_results = None

        try:
            time.sleep(5)

            result = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__nuxt"]/div/div[2]/section/div[9]/div[1]/div/div/div/div/p'))
            )
        except Exception:
            return None

        try:
            qnt_pages_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__nuxt"]/div/div[2]/section/div[8]/div/nav/ul/li[4]/a'))
            )
            num_pages = int(qnt_pages_element.text)
        except NoSuchElementException:
            return None

        if "Nenhum resultado para sua pesquisa" in result.text:
            return num_results

        if "Encontrado" in result.text:
            found_index = result.text.find("Encontrado")
            if found_index != -1:
                found_text = result.text[found_index:]
                match = re.search(r'[0-9.]+', found_text)
                if match:
                    num_results = match.group()

        return num_results, num_pages

    def scrape_pagination(self, qnt_pages: int) -> list:
        result = []

        for page in range(1, qnt_pages + 1):
            try:
                time.sleep(2)

                elements = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located(
                        (By.XPATH, '//*[@id="__nuxt"]/div/div[2]/section/div[9]/div[1]/div/div/div/div'))
                )

                for element in elements:
                    html = element.get_attribute('outerHTML')
                    soup = BeautifulSoup(html, 'html.parser')

                    box_divs = soup.find_all('div', class_='box')

                    for box_div in box_divs:
                        strong_elements = box_div.find_all('strong')

                        if len(strong_elements) < 2:
                            continue

                        cnpj = strong_elements[0].get_text()
                        name = strong_elements[1].get_text()

                        situation = box_div.find('small').get_text()
                        address_small = box_div.find('small', text=lambda text: "|" in text)
                        address = address_small.get_text() if address_small else None

                        link_element = box_div.find('a', {'target': '_blank'})
                        partial_link = link_element['href'] if link_element else None

                        info_dict = {
                            'cnpj': cnpj,
                            'name': name,
                            'status': situation,
                            'address': address,
                            'partial_link': partial_link
                        }

                        if all(info is not None for info in [cnpj, name, situation, partial_link]):
                            result.append(info_dict)

                if page < qnt_pages:
                    self.scroll_to_bottom()
                    self.click_button('//*[@id="__nuxt"]/div/div[2]/section/div[10]/div/nav/a[2]')

            except Exception as e:
                raise e

        return result

    def input_fields(self, **kwargs):
        for field, value in kwargs.items():
            if value:
                if field == "social_reason":
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[2]/div[1]/section/div/div/div/div/div/div[1]/input',
                        value)

                elif field == "cnae":
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[2]/div[2]/section/div/div/div/div/div[1]/input',
                        value)

                elif field == "legal_nature":
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[2]/div[3]/section/div/div/div/div/div[1]/input',
                        value)

                elif field == "situation":
                    self.select_option_by_value(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[3]/div[1]/div/div/select',
                        value.upper())

                elif field == "state":
                    state = value
                    if len(value) == 2:
                        state = convert_state_abbreviation_to_name(state)
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[3]/div[2]/div/div/div/div/div[1]/input',
                        state)

                if field == "city":
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[3]/div[3]/div/div/div/div/div[1]/input',
                        unidecode(value).upper())

                elif field == "neighborhood":
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[3]/div[4]/div/div/div/div/div[1]/input',
                        value)

                elif field == "cep":
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[3]/div[5]/div/div/div/div/div[1]/input',
                        value)

                elif field == "ddd":
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[4]/div[1]/div/div/div/div/div[1]/input',
                        value)

                elif field == "date_to":
                    date_format = self.transform_date(value)
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[4]/div[2]/div/div[1]/div/div/div/div[1]/div/input',
                        date_format)

                elif field == "date_from":
                    date_format = self.transform_date(value)
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[4]/div[2]/div/div[2]/div/div/div/div[1]/div/input',
                        date_format)

                elif field == "share_capital_to":
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[4]/div[3]/section/div/div/input', value)

                elif field == "share_capital_from":
                    self.fill_input_field(
                        '//*[@id="__nuxt"]/div/div[2]/section/div[4]/div[4]/div/div/input', value)

    def basic_scraping_casa_dados(self, cnpj) -> dict:
        try:
            self.initialize_selenium()
            self.driver.get(url=f'{self.url_base}{cnpj}')
            self.scroll_to_bottom()

            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__nuxt"]/div/div[2]/section/div[2]/div[2]/div/article/div/div/p/a/span/i'))
            )
            time.sleep(3)
            element.click()

            self.exclude_pop_up()
            element.click()

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            result = {}

            quadro_societario_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__nuxt"]/div/div[2]/section[1]/div/div/div[4]/div[1]/div[4]')
                )
            )

            if quadro_societario_element:
                # Criar uma chave no result e realizar o parse do quadro societário
                result['Quadro Societário'] = parse_quadro_societario(quadro_societario_element)

            # Atualizar o dicionário result com os dados do QSA
            result.update(parse_other_elements(soup))

            return result

        except TimeoutException as e:
            raise e
        finally:
            self.driver.quit()

    def advanced_scraping_casa_dados(self, **kwargs) -> tuple:
        try:
            self.initialize_selenium()
            self.driver.get(self.url_advanced)
            self.exclude_pop_up()

            self.input_fields(**kwargs)

            self.scroll_to_bottom()
            self.click_button('//*[@id="__nuxt"]/div/div[2]/section/div[6]/div/div/a[1]')

            num_results, qnt_pages = self.get_num_results_and_num_pages()

            if num_results and qnt_pages is not None:
                if "qnt_pages" in kwargs and kwargs["qnt_pages"] is not None:
                    qnt_pages_requested = kwargs["qnt_pages"]
                    qnt_pages = min(qnt_pages, qnt_pages_requested)

                result = self.scrape_pagination(qnt_pages)
                if result:
                    return result, num_results, qnt_pages

        except Exception:
            return None, None
        except NoSuchElementException:
            return None, None
        finally:
            self.driver.quit()


scraper = CasaDadosScraper()
