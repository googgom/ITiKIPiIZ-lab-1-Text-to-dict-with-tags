import parser
import rules
import sys
import os

INPUT_FILENAME = "input.txt"
OUTPUT_FILENAME = "output.txt"
OUTPUT_MODE = "N"


if "--help" in sys.argv:
    print("Usage: ./qup --help|--mode=short|--mode=long\n")
    print("\tDefault mode:\tСтала{стал=VERB}")
    print("\tShort mode:\tСтала{стал=ГЛ}")
    print("\tLong mode:\tСтала{стал=глагол (личная форма)}")
    print("\n\n")
    print(f"If file {INPUT_FILENAME} is found in directory, it will be used for input")
    print("Otherwise terminal input will be asked")
    print(f"File {INPUT_FILENAME} supports endline, unlike terminal input")
    sys.exit(0)
elif "--mode=long" in sys.argv:
    OUTPUT_MODE = "L"
elif "--mode=short" in sys.argv:
    OUTPUT_MODE = "S"


text = ""
if not os.path.exists(INPUT_FILENAME):
    print("Введите текст без переводов строки: ")
    text = input()
else:
    with open(INPUT_FILENAME, 'r') as f:
        text = f.read()
        print(text)

text = rules.rule1(text) # Убирает спецсимволы

new_text = ""
sentences = text.split('\n')

data, basic, serus, lerus = parser.fastParser("dict.opcorpora.xml")

for sentence in sentences:
    words = sentence.split(' ')
    new_sentence = ""
    for word in words:
        new_word = rules.noyo(word.lower()) # Ё не пройдёт! КАПС НЕ ПРОЙДЁТ!
        value = data.get(new_word, "?")
        if OUTPUT_MODE == "L":
            value = lerus.get(value, "?")
        elif OUTPUT_MODE == "S":
            value = serus.get(value, "?")
        new_sentence += word + '{' + basic.get(new_word, "нераспознано") + '=' + value + '}' + ' '
    new_text += new_sentence + '\n'

print(new_text)
