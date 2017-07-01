def  a_name():
    over_25 = 100
    over_string = ''
    if over_25 > 0:
        over_string += "\n OVER 25\n" + "{}  |  {}  |  {}  |  {}".format('time', 'home',
                                          'away', over_25)
    return  over_string
a_name()
print(a_name())
