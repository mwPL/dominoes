# Write your code here
import random


# function for splitting dominoes between players
def split(number):
    selection = []
    for i in range(number):
        selection.append(dom.pop(random.randint(0, len(dom) - 1)))
    return selection


# function for finding snakes in lists. returns max snake, or -1 if no snake
def findsnake(selection):
    snakes = []
    for element in selection:
        if element[0] == element[1]:
            snakes.append(element)
    if len(snakes) < 1:
        return [-1, -1]
    else:
        return max(snakes)


def starts(p, c):
    if p == [-1, -1] and c == [-1, -1]:
        print('No snake')
        exit()
    elif p > c:
        return player.pop(player.index(p))
    else:
        return comp.pop(comp.index(c))


def resultcheck():
    if len(player) == 0:
        print('Status: The game is over. You won!')
        return True
    if len(comp) == 0:
        print('Status: The game is over. The computer won!')
        return True
    if draw():
        print("Status: The game is over. It's a draw!")
        return True
    return False


# checking for draw
def draw():
    check = 0  # checking number of times end number appears
    if snake[0][0] == snake[-1][1]:
        for element in snake:
            check = check + element.count(snake[0][0])
    if check == 8:
        return True
    else:
        return False


# action - 0 draw from stock, negative number insert to the left, positive number append to the right
def action(user, choice):
    if int(choice) == 0:
        if len(stock) > 0:
            # print('0 option, should append to stock')
            user.append(stock.pop(random.randint(0, len(stock)-1)))
            return True
        #else:
            #print('Stock is empty')
    if int(choice) < 0:
        piece = user[abs(int(choice))-1]
        if snake[0][0] == piece[1]:
            # print('no swap left insert')
            snake.insert(0, user.pop(abs(int(choice))-1))
            return True
        elif snake[0][0] == piece[0]:
            piece[0], piece[1] = piece[1], piece[0]
            # print('swap left insert')
            snake.insert(0, user.pop(abs(int(choice))-1))
            return True
        else:
            return False
    elif int(choice) > 0:
        piece = user[int(choice)-1]
        if snake[-1][1] == piece[0]:
            # print('no swap right append')
            snake.append(user.pop(int(choice)-1))
            return True
        elif snake[-1][1] == piece[1]:
            piece[0], piece[1] = piece[1], piece[0]
            # print('swap right append')
            snake.append(user.pop(int(choice)-1))
            return True
        else:
            return False


# computer move
def compmove():
    pd = {x:0 for x in range(7)} #initiating pieces dictionary
    for i in range(len(pd)):
        for j in range(len(comp)):
            pd[i] = pd[i] + comp[j].count(i)
    for i in range(len(pd)):
        for j in range(len(snake)):
            pd[i] = pd[i] + snake[j].count(i)
    # priority list descending in format: [value, [piece]]
    prioritylist = []
    for x in comp:
        prioritylist.append([pd[x[0]] + pd[x[1]], x])
    prioritylist.sort(reverse=True)
    #for x in prioritylist:
        #print(x)

    for no in range(len(prioritylist)):
        #print(f'Checking: {prioritylist[no]} index: {comp.index(prioritylist[no][1])} dest:{comp[comp.index(prioritylist[no][1])]} figure:{(comp.index(prioritylist[no][1]))+1}')
        #print(f'positive if: figure{(comp.index(prioritylist[no][1]))+1}')
        if action(comp, (comp.index(prioritylist[no][1]))+1):
            return True
        #print(f'negative if: figure{-(comp.index(prioritylist[no][1])+1)}')
        if action(comp, -(comp.index(prioritylist[no][1])+1)):
            return True
    action(comp, 0)
    return True


# check if string is numeric (to account for -)
def num(input):
    if len(input) == 0:
        return False
    if input[0] not in '-0123456789':
        return False
    for el in input[1:]:
        if el not in '0123456789':
            return False
    return True


# printing snake as a string
def printsnake():
    if len(snake) < 7:
        printout = ''
        for el in snake:
            printout = printout + str(el)
        print(printout)
    else:
        ls = str(snake[0]) + str(snake[1]) + str(snake[2])
        mid = '...'
        rs = str(snake[-3]) + str(snake[-2]) + str(snake[-1])
        print(ls+mid+rs)



# creating 28 domino pieces
dom = []
for i in range(7):
    for j in range(i, 7):
        dom.append([i, j])

comp = split(7)
player = split(7)
stock = dom

startingpiece = [starts(findsnake(player), findsnake(comp))]
status = "player" if len(player) > len(comp) else "computer"
snake = startingpiece

while True:
    print(70 * '=')
    print(f'Stock size: {len(stock)}')
    print(f'Computer pieces: {len(comp)}\n')
    printsnake()
    print('\nYour pieces:')
    for i in range(len(player)):
        print(f'{i + 1}: {player[i]}')
    if resultcheck():
        exit()
    statusmsg = "It's your turn to make a move. Enter your command." if status == "player" \
        else "Computer is about to make a move. Press Enter to continue..."
    print(f'\nStatus: {statusmsg}')
    entry = input()
    if status == "computer":
       # snake.append(comp.pop(random.randint(0, len(comp) - 1)))
        compmove()
    else:
        while not num(entry) or abs(int(entry)) not in range(len(player) + 1):
            print('Invalid input. Please try again.')
            entry = input()
        while not action(player, entry):
            print('Illegal move. Please try again.')
            entry = input()
            while not num(entry) or abs(int(entry)) not in range(len(player) + 1):
                print('Invalid input. Please try again.')
                entry = input()
    if status == "computer":
        status = "player"
    else:
        status = "computer"