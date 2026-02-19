import parser
import rules

print("Введите текст: ")

#text = input()
text = "Стала стабильнее экономическая и политическая обстановка, предприятия вывели из тени зарплаты сотрудников. Все Гришины одноклассники уже побывали за границей, он был чуть ли не единственным, кого не вывозили никуда дальше Красной Пахры."
text = rules.rule1(text) # Убирает спецсимволы

new_text = ""
sentences = text.split('\n')

data, basic = parser.fastParser("dict.opcorpora.xml")

'''
print("MILE:1")
L, G = parser.extractor("dict.opcorpora.xml")
print("MILE:2")
data, basic = parser.getLList(L)
print("MILE:3")
'''
for sentence in sentences:
    words = sentence.split(' ')
    new_sentence = ""
    for word in words:
        new_word = rules.noyo(word.lower()) # Ё не пройдёт! КАПС НЕ ПРОЙДЁТ!
        new_sentence += word + '{' + basic.get(new_word, "нераспознано") + '=' + data.get(new_word, "?") + '}' + ' '
    new_text += new_sentence + '\n'

print(new_text)
