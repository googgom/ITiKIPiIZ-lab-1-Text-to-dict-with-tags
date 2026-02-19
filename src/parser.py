import xml.etree.ElementTree as xp
import rules

#tree = xp.parse('dict.opcorpora.xml')
#root = tree.getroot()


# Основная задача получить из .xml lemmata и grammemes
def extractor( filepath ):
    print("EILE:1")
    tree = xp.parse(filepath)
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




# Должен создать структуру подобную map<string, vector < string > >, что бы хранить варианты
# Ёж: NOUN,habib; NOUN,ibrab;
# В том числе для форм(l->f)
# Позволит решать противоречия(потом?)
'''
def _exper_getLList( L ):
    data: dict[str, list[str]] = {}

    for la in L: # список лемм
        for wf in la: # список слов\форм?
            for c in wf: # список ?
'''