class Sector:
    list = None

    __processors = ()

    a = [[None, None], [None, None]]
    b = [[None, None], [None, None]]
    c = [[None, None], [None, None]]
    d = [[None, None], [None, None]]

    __pattern = -1

    def __init__(self, sector_list):

        self.__processors = (self.process_0, self.process_1, self.process_2, self.process_3, self.process_4,
                             self.process_5)

        s = sector_list
        a = [[s[0][0], s[0][1]], [s[1][0], s[1][1]]]
        b = [[s[0][2], s[0][3]], [s[1][2], s[1][3]]]
        c = [[s[2][0], s[2][1]], [s[3][0], s[3][1]]]
        d = [[s[2][2], s[2][3]], [s[3][2], s[3][3]]]

        self.list = sector_list

        self.a = a
        self.b = b
        self.c = c
        self.d = d


    def process_0(self):
        return "<Пусто>"

    def process_1(self):
        s = self.list

        a = self.A()
        b = self.B()
        c = self.C()
        d = self.D()

        info = ""

        tp = ""

        if (a == b and a == c and d == b and d == c) or (a == b and a != c and d != b and d == c):
            tp = "А"
            info = "   * " + self.L(1, 4)
            info = info.replace("2 нед", "\n   * 2 нед")
        elif a != b and a == c and d != b and d == c or (a != b and a != c and d != b and d != c):
            tp = "Б1"
            info_1 = "   1-я подгруппа:\n      * " + a + c
            info_2 = "   2-я подгруппа:\n      * " + b + d
            info = info_1 + "\n" + info_2
        elif a == b and a != c and d != b and d != c:
            if " нед" in a+b+c+d:
                tp = "В1"

                info += "   {}\n".format(a)

                info += "   2 нед.\n"
                info += "      * 1-я подгруппа - {}\n".format(c)
                info += "      * 2-я подгруппа - {}\n".format(d)
            else:
                tp = "В2 (Б1)"
                info_1 = "   1-я подгруппа:\n      * " + a + c
                info_2 = "   2-я подгруппа:\n      * " + b + d
                info = info_1 + "\n" + info_2
        elif a != b and a != c and d != b and d == c:
            tp = "Д"

            info += "   1-я неделя\n"
            info += "      * 1-я подгруппа - {}\n".format(a)
            info += "      * 2-я подгруппа - {}\n".format(b)

            info += "   {}\n".format(c)

        print("Type {}".format(tp))

        return info

    def process_2(self):
        a = self.A()
        b = self.B()

        info = ""
        tp = ""

        if a == b:
            tp = "А"
            info = "   * " + self.L(1, 2)
        else:
            tp = "В"
            info_1 = "   1-я подгруппа:\n      * " + a
            info_2 = "   2-я подгруппа:\n      * " + b
            info = info_1 + "\n" + info_2

        print("Type {}".format(tp))
        return info

    def process_3(self):
        c = self.C()
        d = self.D()

        info = ""
        tp = ""

        if c == d:
            tp = "А"
            info = "   * " + self.L(3, 4)
        else:
            tp = "В"
            info_1 = "   1-я подгруппа:\n      * " + c
            info_2 = "   2-я подгруппа:\n      * " + d
            info = info_1 + "\n" + info_2

        print("Type {}".format(tp))
        return info

    def process_4(self):
        a = self.A()
        c = self.C()

        info = ""
        tp = ""

        if c == a:
            tp = "А"
            info = "   1-я подгруппа:\n"
            info = "      * {}".format(a)
        else:
            tp = "B"
            info = "   1-я подгруппа:\n"
            info = "      * {}\n".format(a)
            info = "      * {}".format(c)

        print("Type {}".format(tp))
        return info

    def process_5(self):
        s = self.list

        b = self.A()
        d = self.C()

        info = ""
        tp = ""

        if b == d:
            tp = "А"
            info += "   2-я подгруппа:\n"
            info += "      * {}".format(b)
        else:
            tp = "B"
            info += "   2-я подгруппа:\n"
            info += "      * {}\n".format(b)
            info += "      * {}".format(d)

        print("Type {}".format(tp))
        return info

    def process_6(self):
        a = self.A()
        c = self.C()
        d = self.D()

        info = ""

        if a != c and c == d:
            info += "   1 нед.\n"
            info += "      * 1-я подгруппа - {}\n".format(a)

            info += "   2 нед.\n"
            info += "      * {}\n".format(c)

        elif a == c and c != d:
            info_1 = "   1-я подгруппа:\n      * {}\n".format(a)
            info_2 = "   2-я подгруппа:\n      * {}".format(d)
            info = info_1 + "\n" + info_2

        else:
            info += "   1 нед.\n"
            info += "      * 1-я подгруппа - {}\n".format(a)

            info += "   2 нед.\n"
            info += "      * 1-я подгруппа - {}\n".format(c)
            info += "      * 2-я подгруппа - {}\n".format(d)

        return info

    def process_7(self):
        b = self.B()
        c = self.C()
        d = self.D()

        info = ""

        if b != d and c == d:
            info += "   1 нед.\n"
            info += "      * 2-я подгруппа - {}\n".format(b)

            info += "   2 нед.\n"
            info += "      * {}\n".format(c)

        elif b == d and c != d:
            info_1 = "   1-я подгруппа:\n      * {}\n".format(c)
            info_2 = "   2-я подгруппа:\n      * {}".format(b)
            info = info_1 + "\n" + info_2

        else:
            info += "   1 нед.\n"
            info += "      * 2-я подгруппа - {}\n".format(b)

            info += "   2 нед.\n"
            info += "      * 1-я подгруппа - {}\n".format(c)
            info += "      * 2-я подгруппа - {}\n".format(d)

        return info

    def process_8(self):
        a = self.A()
        b = self.B()
        d = self.D()

        info = ""

        if a == b and b != d:
            info += "   1 нед.\n"
            info += "      * {}\n".format(a)

            info += "   2 нед.\n"
            info += "      * 2-я подгруппа - {}\n".format(d)

        elif a != b and b == d:
            info_1 = "   1-я подгруппа:\n      * {}\n".format(a)
            info_2 = "   2-я подгруппа:\n      * {}".format(b)
            info = info_1 + "\n" + info_2

        else:

            info += "   1 нед.\n"
            info += "      * 1-я подгруппа - {}\n".format(a)
            info += "      * 2-я подгруппа - {}\n".format(b)

            info += "   2 нед.\n"
            info += "      * 2-я подгруппа - {}\n".format(d)

        return info

    def process_9(self):
        a = self.A()
        b = self.B()
        c = self.C()

        info = ""

        if a == b and a != c:
            info += "   1 нед.\n"
            info += "      * {}\n".format(a)

            info += "   2 нед.\n"
            info += "      * 1-я подгруппа - {}\n".format(c)

        elif a != b and a == c:
            info_1 = "   1-я подгруппа:\n      * {}\n".format(a)
            info_2 = "   2-я подгруппа:\n      * {}".format(b)
            info = info_1 + "\n" + info_2
            
        else:
            info += "   1 нед.\n"
            info += "      * 1-я подгруппа - {}\n".format(a)
            info += "      * 2-я подгруппа - {}\n".format(b)

            info += "   2 нед.\n"
            info += "      * 1-я подгруппа - {}\n".format(c)

        return info

    def process_10(self):
        a = self.A()

        info = "   1-я подгруппа:\n"
        info = "      * {}".format(a)

        return info

    def process_11(self):
        b = self.B()

        info = "   2-я подгруппа:\n"
        info = "      * {}".format(b)

        return info

    def process_12(self):
        c = self.C()

        info = "   1-я подгруппа:\n"
        info = "      * {}".format(c)

        return info

    def process_13(self):
        d = self.D()

        info = "   2-я подгруппа:\n"
        info = "      * {}".format(d)

        return info

    def process_14(self):
        a = self.A()
        d = self.D()

        info = ""

        info_1 = "   1-я подгруппа:\n      * " + a
        info_2 = "   2-я подгруппа:\n      * " + d
        info = info_1 + "\n" + info_2

        return info

    def process_15(self):
        b = self.B()
        c = self.C()

        info = ""

        info_1 = "   1-я подгруппа:\n      * " + b
        info_2 = "   2-я подгруппа:\n      * " + c
        info = info_1 + "\n" + info_2

        return info

    def unisum(self, list):
        unique_list = []

        for line in list:
            for el in line:
                if el not in unique_list:
                    if el != "_":
                        unique_list.append(el)

        unique_str = ""
        for item in unique_list:
            unique_str += str(item) + " "

        return unique_str

    def process(self):
        pattern = self.pattern

        return self.__processors[pattern]()

    @property
    def pattern(self):
        pattern = -1

        a = self.A()
        b = self.B()
        c = self.C()
        d = self.D()

        yes = self.bln
        def no(x): return not yes(x)

        if no(a) and no(b) and no(c) and no(d):
            pattern = 0

        elif yes(a) and yes(b) and yes(c) and yes(d):
            pattern = 1

        elif yes(a) and yes(b) and no(c) and no(d):
            pattern = 2

        elif no(a) and no(b) and yes(c) and yes(d):
            pattern = 3

        elif yes(a) and no(b) and yes(c) and no (d):
            pattern = 4

        elif no(a) and yes(b) and no(c) and yes(d):
            pattern = 5

        elif yes(a) and no(b) and yes(c) and yes(d):
            pattern = 6

        elif no(a) and yes(b) and yes(c) and yes(d):
            pattern = 7

        elif yes(a) and yes(b) and no(c) and yes(d):
            pattern = 8

        elif yes(a) and yes(b) and yes(c) and no(d):
            pattern = 9

        elif yes(a) and no(b) and no(c) and no(d):
            pattern = 10

        elif no(a) and yes(b) and no(c) and no(d):
            pattern = 11

        elif no(a) and no(b) and yes(c) and no(d):
            pattern = 12

        elif no(a) and no(b) and no(c) and yes(d):
            pattern = 13

        elif yes(a) and no(b) and no(c) and yes(d):
            pattern = 14

        elif no(a) and yes(b) and yes(c) and no(d):
            pattern = 15

        else:
            pattern = -1

        return pattern

    def bln(self, x):
        if x == "":
            return False
        else:
            return True

    def S(self, num):
        return self.unisum([self.list[num-1]])

    def L(self, start, end):
        lst = []
        for i in range(start, end + 1):
            lst.append([self.S(i)])

        return self.unisum(lst)

    def A(self):
        return self.unisum(self.a)

    def B(self):
        return self.unisum(self.b)

    def C(self):
        return self.unisum(self.c)

    def D(self):
        return self.unisum(self.d)


if __name__ == "__main__":
    lstf = [['ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский '], ['ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский '], ['ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский '], ['ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский ', 'ф и з и ч е с к а я к у л ь т у р а Ольшевский ']]
    lstd = [['1 нед. физика', '1 нед. физика', '1 нед. физика', '1 нед. физика'], ['Блинкова 312 к 12', 'Блинкова 312 к 12', 'Блинкова 312 к 12', 'Блинкова 312 к 12'], ['9.55 2 нед. Психология труда', '9.55 2 нед. Психология труда', '9.55 2 нед. Психология труда', '9.55 2 нед. Психология труда'], ['д.Вержибок Г.В.424 к 1', 'д.Вержибок Г.В.424 к 1', 'д.Вержибок Г.В.424 к 1', 'д.Вержибок Г.В.424 к 1']]

    lst1 = [[' английский ', ' английский ', ' английский ', ' английский '], [' язык', ' язык', ' язык', ' язык'],
     ['411.0', 'к 18', '430.0', 'к 18'], ['Васильева ', 'Васильева ', 'Левитская ', 'Левитская ']]
    lst0 = [['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '_']]

    lst2 = [['1', '_', '_', '_'], ['_', '_', '3', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '_']]

    lst3 = [['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '3', '_4'], ['_', '2', '_', '_']]

    lst4 = [['2', '_', '_', '_'], ['_', '2', '_', '_'], ['_', '_', '_', '_'], ['2', '_', '_', '_']]

    lst5 = [['_', '_', '_', '5'], ['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '5', '_']]

    lst6 = [['_3', '_', '_', '_'], ['_3', '_', '_', '_'], ['3', '_', '3', '_'], ['3', '_', '_', '5']]

    lst7 = [['_', '_', '6', '_'], ['_', '_', '7', '_'], ['`1`', '_', '8', '_'], ['2', '_', '_', '_']]

    lst8 = [['2', '_', '_', '2'], ['_', '2', '2', '_'], ['_', '_', '4', '_'], ['_', '_', '_', '4']]

    lst9 = [['_', '5', '_', '_'], ['5', '_', '_', '5'], ['_', '5', '_', '_'], ['5', '_', '_', '_']]

    lst10 = [['1', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '_']]

    lst11 = [['_', '_', '_', '_'], ['_', '_', '_', '3'], ['_', '_', '_', '_'], ['_', '_', '_', '_']]

    lst12 = [['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '4', '_', '_'], ['_', '_', '_', '_']]

    lst13 = [['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '5']]

    lst14 = [['2', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '2']]

    lst15 = [['_', '_', '_', '4'], ['_', '_', '_', '_'], ['_', '_', '_', '_'], ['4', '_', '_', '_']]

    lst16 = [['_', '_', '_', '4'], ['_', '3_', '_', '_3'], ['_', '23', '_', '_'], ['4', '3', '_', '_']]

    lsd = [['1 нед', '_', '1 нед', '_'], ['1', '_', '3', '_'], ['2 нед', '3', '2 нед', '_'], ['_', '1', '1', '_']]

    lsdd = [['1 нед', 'в', '1 нед', 'в'], ['_', '_', '_', '_'], ['2 нед', 'а', '2 нед', 'и'], ['_', '_', '_', '_']]

    l1 = [['Технология конструкционных ', 'Технология конструкционных ', 'Информатика', 'Информатика'], ['материалов', 'материалов', '_', '_'], ['11.0', 'к 7', '402.0', 'к 8'], ['Миньков ', 'Миньков ', 'Бабак', 'Бабак']]
    l2 = [['1 нед. Основы психологии и педагогики ', '1 нед. Основы психологии и педагогики ', '1 нед. Основы психологии и педагогики ', '1 нед. Основы психологии и педагогики '], ['ст.пр.Леонтьева Т.Г. 438 к 1', 'ст.пр.Леонтьева Т.Г. 438 к 1', 'ст.пр.Леонтьева Т.Г. 438 к 1', 'ст.пр.Леонтьева Т.Г. 438 к 1'], ['2 нед.История науки и техники ', '2 нед.История науки и техники ', '2 нед.История науки и техники ', '2 нед.История науки и техники '], [' ст.пр.Карбалевич Н.И. 438 к 1 ', ' ст.пр.Карбалевич Н.И. 438 к 1 ', ' ст.пр.Карбалевич Н.И. 438 к 1 ', ' ст.пр.Карбалевич Н.И. 438 к 1 ']]
    l3 = [['Метрология', 'Метрология', 'Информационные ', 'Информационные '], ['и стандартизация', 'и стандартизация', 'технологии', 'технологии'], ['305.0', 'к 2 ', '208.0', 'к 3'], ['Ахремчук', 'Ахремчук', 'Горностай ', 'Горностай ']]
    l4 = [['_', '_', '_', '_'], ['_', '_', '_', '_'], ['2 нед Механика материалов', '2 нед Механика материалов', '2 нед Механика материалов', '2 нед Механика материалов'], ['Дикан Ж.Г. 207 к 18', 'Дикан Ж.Г. 207 к 18', 'Дикан Ж.Г. 207 к 18', 'Дикан Ж.Г. 207 к 18']]
    l5 = [['1 нед. Философия.', '1 нед. Философия.', '1 нед. Философия.', '1 нед. Философия.'], ['ст.пр.Волнистый А.Г. 221 к 6 ', 'ст.пр.Волнистый А.Г. 221 к 6 ', 'ст.пр.Волнистый А.Г. 221 к 6 ', 'ст.пр.Волнистый А.Г. 221 к 6 '], ['_', '_', '_', '_'], ['_', '_', '_', '_']]

    l6 = [['9.55 Прикладная ', '9.55 Прикладная ', '_', '_'], ['механика', 'механика', '_', '_'], ['455.0', 'к 1', '_', '_'], ['Хрущев ', 'Хрущев ', '_', '_']]

    s = Sector(l6)

    print(s.A() == s.B())
    print(s.A() == s.C())
    print(s.D() == s.C())
    print(s.D() == s.B())

    #print(s.A())
    #print(s.B())
    #print(s.C())
    #print(s.D())



    print("Pattern =", s.pattern)
    print(s.process())
