import xml.etree.ElementTree as xp
import rules
import pickle
import os

CACHE_FILE = "vocabulary-cache.pkl"


#tree = xp.parse('dict.opcorpora.xml')
#root = tree.getroot()


# Основная задача получить из .xml lemmata и grammemes
def extractor( filepath ):
    
    print("EILE:1")
    if os.path.exists(filepath):
        tree = xp.parse(filepath)
    else:
        print(f"Vocabulary {filepath} not found... Downloading from net...")
        os.system("./download-vocabulary.sh")
        tree = xp.parse(filepath)
    '''
    print("EILE:1")
    try:
        tree = xp.parse(filepath)
    except FileNotFoundError:
        print(f"Vocabulary {filepath} not found... Downloading from net...")
    '''
    root = tree.getroot()
    L = None
    G = None
    for child in root:
        if child.tag == "lemmata":
            L = child
        elif child.tag == "grammemes":
            G = child
    
    if L == None or G == None:
        print("ERROR: lemmata or grammemes is None")
        exit()
    else:
        return L, G

#L, G = extractor('dict.opcorpora.xml')


# Только сопоставление с [BIGL] большебуквенными формами, но с под-формами
# еж: NOUN
# ежи: NOUN
def getLList( L ):
    __repeats_cnt = 0
    __null_keys = 0
    __rewrites = 0
    data: dict[str, str] = {}
    basic: dict[str, str] = {}

    for word in L:
        # список лемм
        texts = []
        cur_key = ""
        base = word[0].attrib['t']
        for forms in word:
            # список слов\форм?
            texts.append(rules.noyo(forms.attrib['t'])) # Ё не нужны!
            basic[forms.attrib['t']] = base
            for c in forms:
                # список ?
                cur_val = c.attrib['v']
                if cur_val.isupper() == True:
                    cur_key = cur_val

        #print("LILE:2")
        for text in texts:
            if cur_key == None:
                __null_keys += 1
            if text in data and cur_key == data[text]:
                __repeats_cnt += 1
            if text in data and cur_key != data[text]:
                __rewrites += 1
            data[text] = cur_key
        
    print("Неопределённых частей речи в словаре:", __null_keys)
    print("Повторных заполнений в словаре:", __repeats_cnt)
    print("Конфликтных определений в словаре:", __rewrites)
    return data, basic
# Не решены внутренние копии



# Объединение извлечения поддеревьев и генерации data, basic
def unitedParser( filepath ):
    __repeats_cnt = 0
    __null_keys = 0
    __rewrites = 0
    data: dict[str, str] = {}
    basic: dict[str, str] = {}
    serus: dict[str, str] = {}
    lerus: dict[str, str] = {}
    # !erus - альтернативная форма записи части речи
    # ShortEditRus, LongEditRus

    print("UnitedParserStep:1")
    if not os.path.exists(filepath):
        print(f"Vocabulary {filepath} not found... Downloading from net...")
        os.system("./download-vocabulary.sh")
    
    context = xp.iterparse(filepath, events=('end',))

    for __e_t, word in context:
        if word.tag == "grammeme":
            serus[word[0].text] = word[1].text
            lerus[word[0].text] = word[2].text
        elif word.tag == "lemma":
            texts = []
            cur_key = None
            base = word[0].attrib['t']

            for forms in word:
                texts.append(rules.noyo(forms.attrib['t'])) # Ё не нужны!
                basic[forms.attrib['t']] = base

                for c in forms:
                    cur_val = c.attrib['v']
                    if cur_val.isupper() == True:
                        cur_key = cur_val

            for text in texts:
                if cur_key == None:
                    __null_keys += 1
                if text in data and cur_key == data[text]:
                    __repeats_cnt += 1
                if text in data and cur_key != data[text]:
                    __rewrites += 1
                data[text] = cur_key
            
            word.clear()

    print("Неопределённых частей речи в словаре:", __null_keys)
    print("Повторных заполнений в словаре:", __repeats_cnt)
    print("Конфликтных определений в словаре:", __rewrites)
    return data, basic, serus, lerus



# Для ускорения работы можно записать результат парсера в бинарный файл
def fastParser( filepath ):
    if os.path.exists(CACHE_FILE):
        print("fastParser:Загрузка Кэша")
        with open(CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        print("fastParser:Кэш не найден, первый запуск будет дольше")

        data, basic, serus, lerus = unitedParser(filepath)

        print("fastParser:Сохранение Кэша")
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump((data, basic, serus, lerus), f, protocol=pickle.HIGHEST_PROTOCOL)
        return data, basic, serus, lerus
    print("fastParser:Каким то образом механизм проверки Кэша был проигнорирован")
    return unitedParser(filepath)
