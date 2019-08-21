from collections import OrderedDict

def odd_numbers():
    lst = [1, 5, 6, 12, 19, 7, 8, 44, 27]
    total = 0
    for i in lst:
        if i % 2 == 1:
            total += i
    print(total)


def sum_elements():
    lst = [1, 5, 6, 12, 19, 7, 8, 44, 27]
    total = sum(lst)
    print(total)


def reverse_string(word):
    rword = ''
    index = len(word)
    while index > 0:
        rword += word[index - 1]
        index -= 1
    return rword


def remove_repeat(word):
    return "".join(OrderedDict.fromkeys(word))


def fizzbuzz():
    numbers = [45, 22, 14, 65, 97, 72]
    for i in range(len(numbers)):
        if i % 3 == 0 and i % 5 == 0:
            numbers[i] = 'fizzbuzz'
        elif i % 3 == 0:
            numbers[i] = 'fizz'
        elif i % 5 == 0:
            numbers[i] = 'buzz'
    return numbers


def pyramid(height):
    for i in range(1, height+1, 2):
        print(' ' * height + i * 'x')
        height -= 1
  




if __name__ == '__main__':
    pyramid(3)
    
