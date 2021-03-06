
class Variables:
    """
    This class stores different variables related with the crawlers and news
    stored from arquivo.pt.
    """

    arquivo_start_year = 1996

    newspaper_site = {
        'publico': 'http://www.publico.pt',
        'expresso': 'http://expresso.pt/',
        'diario_noticias': 'http://www.dn.pt/',
        'correio_manha': 'http://www.cmjornal.pt/',
        'sol': 'http://sol.sapo.pt/',
        'sol2': 'http://www.sol.pt/',
        'visao': 'https://visao.sapo.pt/',
        'jornal_noticias': 'https://www.jn.pt/'
    }

    newspaper_list = ['publico',
                      'expresso',
                      'diario_noticias',
                      'correio_manha',
                      'sol',
                      'sol2',
                      'visao',
                      'jornal_noticias'
                      ]

    keywords = [
                'violencia domestica',
                'violação',
                'feminicidio',
                'feminicidios',
                'femicidio',
                'femicidios',
                'violações',
                'assassinada',
                'assassinadas',
                'mulher assassinada',
                'mulheres assassinadas',
                'assassina mulher',
                'assassinam mulher',
                'assassina mulheres',
                'assassinam mulheres',
                'assassina companheira',
                'assassina esposa',
                'assassinam companheira',
                'assassinam esposa',
                'mata mulher',
                'matam mulher',
                'mata mulheres',
                'matam mulheres',
                'mata namorada',
                'matam namorada',
                'mata esposa',
                'matam esposa',
                'mata companheira',
                'matam companheira',
                'namorado mata',
                'marido mata',
                'companheiro mata',
                'namorado assassina',
                'marido assassina',
                'companheiro assassina',
                'filho mata mae',
                'filhos matam mae',
                'mata sogra',
                'filho assassina mae',
                'filhos assassinam mae',
                'assassina sogra',
                'assassinou mulher',
                'assassinaram mulher',
                'assassinou mulheres',
                'assassinaram mulheres',
                'assassinou companheira',
                'assassinou esposa',
                'assassinaram companheira',
                'assassinaram esposa',
                'matou mulher',
                'mataram mulher',
                'matou mulheres',
                'mataram mulheres',
                'matou namorada',
                'mataram namorada',
                'matou esposa',
                'mataram esposa',
                'matou companheira',
                'mataram companheira',
                'namorado matou',
                'marido matou',
                'companheiro matou',
                'namorado assassinou',
                'marido assassinou',
                'companheiro assassinou',
                'filho matou mae',
                'filhos mataram mae',
                'matou sogra',
                'filho assassinou mae',
                'filhos assassinaram mae',
                'assassinou sogra',
                'matou mae',
                'mataram mae',
                'mata mae',
                'matam mae',
                'mulher',
                'mulheres'
                ]

    keyword_categories = ['feminicidio','violencia_domestica','violencia_sexual','assedio_sexual','mulheres_assassinadas']

    keyword_type = {
        'feminicidio': 'feminicidio',
        'feminicidios': 'feminicidio',
        'femicidio': 'feminicidio',
        'femicidios': 'feminicidio',
        'violencia domestica': 'violencia_domestica',
        'violação': 'violencia_sexual',
        'violações': 'violencia_sexual',
        'assédio sexual': 'assedio_sexual',
        'assassinada': 'mulheres_assassinadas',
        'assassinadas': 'mulheres_assassinadas',
        'mulher assassinada': 'mulheres_assassinadas',
        'mulheres assassinadas': 'mulheres_assassinadas',
        'assassina mulher': 'mulheres_assassinadas',
        'assassinam mulher': 'mulheres_assassinadas',
        'assassina mulheres': 'mulheres_assassinadas',
        'assassinam mulheres': 'mulheres_assassinadas',
        'assassina companheira': 'mulheres_assassinadas',
        'assassina esposa': 'mulheres_assassinadas',
        'assassinam companheira': 'mulheres_assassinadas',
        'assassinam esposa': 'mulheres_assassinadas',
        'mata mulher': 'mulheres_assassinadas',
        'matam mulher': 'mulheres_assassinadas',
        'mata mulheres': 'mulheres_assassinadas',
        'matam mulheres': 'mulheres_assassinadas',
        'mata namorada': 'mulheres_assassinadas',
        'matam namorada': 'mulheres_assassinadas',
        'mata esposa': 'mulheres_assassinadas',
        'matam esposa': 'mulheres_assassinadas',
        'mata companheira': 'mulheres_assassinadas',
        'matam companheira': 'mulheres_assassinadas',
        'namorado mata': 'mulheres_assassinadas',
        'marido mata': 'mulheres_assassinadas',
        'companheiro mata': 'mulheres_assassinadas',
        'namorado assassina': 'mulheres_assassinadas',
        'marido assassina': 'mulheres_assassinadas',
        'companheiro assassina': 'mulheres_assassinadas',
        'filho mata mae': 'mulheres_assassinadas',
        'filhos matam mae': 'mulheres_assassinadas',
        'mata sogra': 'mulheres_assassinadas',
        'filho assassina mae': 'mulheres_assassinadas',
        'filhos assassinam mae': 'mulheres_assassinadas',
        'assassina sogra': 'mulheres_assassinadas',
        'assassinou mulher': 'mulheres_assassinadas',
        'assassinaram mulher': 'mulheres_assassinadas',
        'assassinou mulheres': 'mulheres_assassinadas',
        'assassinaram mulheres': 'mulheres_assassinadas',
        'assassinou companheira': 'mulheres_assassinadas',
        'assassinou esposa': 'mulheres_assassinadas',
        'assassinaram companheira': 'mulheres_assassinadas',
        'assassinaram esposa': 'mulheres_assassinadas',
        'matou mulher': 'mulheres_assassinadas',
        'mataram mulher': 'mulheres_assassinadas',
        'matou mulheres': 'mulheres_assassinadas',
        'mataram mulheres': 'mulheres_assassinadas',
        'matou namorada': 'mulheres_assassinadas',
        'mataram namorada': 'mulheres_assassinadas',
        'matou esposa': 'mulheres_assassinadas',
        'mataram esposa': 'mulheres_assassinadas',
        'matou companheira': 'mulheres_assassinadas',
        'mataram companheira': 'mulheres_assassinadas',
        'namorado matou': 'mulheres_assassinadas',
        'marido matou': 'mulheres_assassinadas',
        'companheiro matou': 'mulheres_assassinadas',
        'namorado assassinou': 'mulheres_assassinadas',
        'marido assassinou': 'mulheres_assassinadas',
        'companheiro assassinou': 'mulheres_assassinadas',
        'filho matou mae': 'mulheres_assassinadas',
        'filhos mataram mae': 'mulheres_assassinadas',
        'matou sogra': 'mulheres_assassinadas',
        'filho assassinou mae': 'mulheres_assassinadas',
        'filhos assassinaram mae': 'mulheres_assassinadas',
        'assassinou sogra': 'mulheres_assassinadas',
        'matou mae': 'mulheres_assassinadas',
        'mataram mae': 'mulheres_assassinadas',
        'mata mae': 'mulheres_assassinadas',
        'matam mae': 'mulheres_assassinadas'
    }

    @classmethod
    def get_keywords_from_category(self, category):
        keyword_list = []
        # Iterate over all the items in dictionary and filter items which has even keys
        for (key, value) in Variables.keyword_type.items():
            # Check if key is even then add pair to new dictionary
            if value == category:
                keyword_list.append(key)
        return keyword_list
