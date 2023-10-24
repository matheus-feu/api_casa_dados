from bs4 import BeautifulSoup


def convert_state_abbreviation_to_name(state):
    states = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins'
    }
    return states[state]


list_of_states = [
    'Acre',
    'Alagoas',
    'Amapá',
    'Amazonas',
    'Bahia',
    'Ceará',
    'Distrito Federal',
    'Espírito Santo',
    'Goiás',
    'Maranhão',
    'Mato Grosso',
    'Mato Grosso do Sul',
    'Minas Gerais',
    'Pará',
    'Paraíba',
    'Paraná',
    'Pernambuco',
    'Piauí',
    'Rio de Janeiro',
    'Rio Grande do Norte',
    'Rio Grande do Sul',
    'Rondônia',
    'Roraima',
    'Santa Catarina',
    'São Paulo',
    'Sergipe',
    'Tocantins'
]


def parse_quadro_societario(quadro_societario_element) -> list:
    """
    Faz o parse do quadro societário e retorna uma lista com os dados.
    :param quadro_societario_element:
    :return: Lista com os dados do quadro societário
    """
    quadro_societario = []

    quadro_societario_html = quadro_societario_element.get_attribute('outerHTML')
    soup_qsa = BeautifulSoup(quadro_societario_html, 'html.parser')
    qsa_elements = soup_qsa.find_all('p', {'data-v-81897e2b': True})

    for qsa_element in qsa_elements:
        texto = qsa_element.get_text().strip()
        partes = texto.split(' - ')

        if len(partes) == 2:
            nome_socio, cargo = partes
            quadro_societario.append(f'{nome_socio} - {cargo}')

    return quadro_societario


def parse_other_elements(soup) -> dict:
    """
    Localiza os elementos que não estão dentro de uma div com a classe 'column is-narrow'
    e retorna um dicionário com os dados.
    :param soup: Elemento BeautifulSoup
    :return: Dicionário com os dados
    """
    result = {}
    elements = soup.find_all('div', {'class': 'column is-narrow', 'data-v-81897e2b': True})

    for element in elements:
        p_elements = element.find_all('p', {'data-v-81897e2b': True})

        if len(p_elements) == 2:
            key = p_elements[0].get_text()
            value = p_elements[1].get_text()
            result[key] = value

    return result
