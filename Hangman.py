#!/usr/bin/python
# -*- coding: utf-8 -*-

# Это игра - Висилица
from re import search
from re import finditer
from os import get_terminal_size
from os import system
from os import name as nameOS
from sys import stdout
from time import sleep
import urllib.request


# Очистка экрана консоли
def clear_screen():
  if nameOS == 'nt':
    system('cls')
  else:
    system('clear')


# Медленный побуквенный вывод
def sprint(str, ending='\n'):
  for i in str:
    if i == ' ':
      print(' ', end='')
      continue
    sleep(0.1)
    stdout.write(i)
    stdout.flush()
  print(end=ending)


# Генерация нового слова с сайта
def new_word():
  url = "http://free-generator.ru/generator.php?action=word&type=1"
  fp = urllib.request.urlopen(url)

  mystr = fp.read().decode('unicode_escape')
  fp.close()

  pattern = r'word":"\D+",'
  return search(pattern, mystr)[0][7:-2]


# Проверка повтора символа
def is_repeated(char):
  if char in all_chars:
    return True
  else:
    return False


# Вывод опробованных букв
def print_used_chars():
  print("Буквы, которые вы пробовали: ", end=' ')

  if len(all_chars) != 0:
    for char in all_chars:
      _str = "'{}'".format(char)
      print(_str, end=' ')

  if input_char.isalpha() and \
     len(input_char) == 1 and \
     not is_repeated(input_char):
    print("'{}'".format(input_char))
  else:
    print()


# Вывод отгадываемого слова в зашифрованном виде
def print_word():
  print('Наше слово: ', end="")
  for i in range(len(input_word)):
    if i in indexes.keys():
      print(indexes[i], end="")
    else:
      print('-', end="")
  print()


# Вывод всей информации в одной команде
def info():
  print()
  print_word()
  print_used_chars()
  print('Попыток осталось: ' + str(attempts))
  print()


clear_screen()
# Получаем размер консольного окна
term_size = get_terminal_size().columns

sprint('Виселица!'.center(term_size))
for i in range(term_size):
  print('-', end='')
print()

sprint('Кол-во попыток:', ' ')
attempts = input()
while not attempts.isdigit():
  print('Введите число!')
  attempts = input()
attempts = int(attempts)
input_word = new_word()
clear_screen()

print("Наше слово: ", end='')
for i in range(len(input_word)):
  print("-", end="")
print()

indexes = {}
all_chars = []
# Условие проигрыша
while attempts != 0:
  is_empty = True

  input_char = input('Введите букву: ').lower()
  clear_screen()

  if len(input_char) != 1 or not input_char.isalpha():
    print('Нужно ввести 1 букву!')
    info()
    continue

  result = finditer(input_char, input_word)

  for match in result:
    is_empty = False
    indexes[match.start()] = input_char

  if is_empty:
    if is_repeated(input_char):
      print('Ты уже пробовал эту букву!')
      print('Выбери другую')
      info()
      continue
    attempts -= 1
    print('Такой буквы в слове нет!')
  else:
    if is_repeated(input_char):
      print('Ты уже пробовал эту букву!')
      print('Выбери другую')
      info()
      continue

    if len(indexes) == len(input_word):
      print("Вы угадали слово '{}'!".format(input_word))
      input('Нажмите Enter, чтобы выйти\n')
      break
    print('Ты угадал!')
  info()
  all_chars.append(input_char)
else:
  print('Вы проиграли!')
  print('Слово, котороые мы загадали: ' + input_word)
  input('Нажмите Enter, чтобы выйти\n')
