class Sector:
    list = None

    __processors = []

    a = [[None, None], [None, None]]
    b = [[None, None], [None, None]]
    c = [[None, None], [None, None]]
    d = [[None, None], [None, None]]

    __pattern = -1

    mode = ""

    def __init__(self, sector_list, mode="default"):
        self.__processors = [self.process_0, self.process_1, self.process_2, self.process_3, self.process_4,
                             self.process_5, self.process_6, self.process_7, self.process_8, self.process_9,
                             self.process_10, self.process_11, self.process_12, self.process_13, self.process_14,
                             self.process_15, self.process_error]

        w = len(sector_list[0])
        h = len(sector_list)

        if w == 4 and h == 4:
            pass
        elif w == 2 and h == 4:
            sector_list = self.reformat_2x4(sector_list)
        elif w == 1 and h == 4:
            sector_list = self.reformat_1x4(sector_list)
        else:
            self.list = None
            return

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

    @staticmethod
    def reformat_2x4(sector_list):
        s = sector_list
        new_list = [[s[0][0], s[0][0], s[0][1], s[0][1]],
                    [s[1][0], s[1][0], s[1][1], s[1][1]],
                    [s[2][0], s[2][0], s[2][1], s[2][1]],
                    [s[3][0], s[3][0], s[3][1], s[3][1]]]
        return new_list

    @staticmethod
    def reformat_2x2(sector_list):
        s = sector_list
        new_list = [[s[0][0], s[0][0], s[0][1], s[0][1]],
                    [s[0][0], s[0][0], s[0][1], s[0][1]],
                    [s[2][0], s[2][0], s[2][1], s[2][1]],
                    [s[2][0], s[2][0], s[2][1], s[2][1]]]
        return new_list

    @staticmethod
    def reformat_1x4(sector_list):
        s = sector_list
        new_list = [[s[0][0], s[0][0], s[0][0], s[0][0]],
                    [s[1][0], s[1][0], s[1][0], s[1][0]],
                    [s[2][0], s[2][0], s[2][0], s[2][0]],
                    [s[3][0], s[3][0], s[3][0], s[3][0]]]
        return new_list


    def init2x4(self, sector_list):
        s = sector_list
        a = [[s[0][0]], [s[1][0]]]
        b = [[s[0][1]], [s[1][1]]]
        c = [[s[2][0]], [s[3][0]]]
        d = [[s[2][1]], [s[3][1]]]

        self.list = sector_list

        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def remove_weeks(self, txt: str):
        txt = txt.replace("1 нед.", "1 нед")
        txt = txt.replace("1 нед", "")

        txt = txt.replace("2 нед.", "2 нед")
        txt = txt.replace("2 нед", "")

        return txt

    def has_nums(self, txt: str):
        txt = txt.replace("СГМ 1", "СГМ_1")
        txt = txt.replace("СГМ 2", "СГМ_2")
        txt = txt.replace("СГМ 3", "СГМ_3")

        txt = txt.replace("1 нед.", "1 нед")
        txt = txt.replace("1 нед", "")

        txt = txt.replace("2 нед.", "2 нед")
        txt = txt.replace("2 нед", "")

        for i in range(0, 4):
            try:
                txt = txt.replace(".", ". ")
            except:
                pass


        words = txt.split()
        # print(words)

        for word in words:
            if word.isdigit() or (word[-1] in ('а', 'б', 'в', 'a') and word[:-1].isdigit()):
                return True

        return False

    def are_brothers(self, x: str, y: str):
        return (not self.has_nums(x) and self.has_nums(y)) or (x == y)

    def sum_if_not_equal(self, x: str, y: str):
        if x == y:
            return x
        else:
            return x+y
    def binary_sector(self):
        binary_sector = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        for i in range(0, 4):
            for j in range(0, 4):
                if self.list[i][j] != '_':
                    binary_sector[i][j] = 1
                else:
                    binary_sector[i][j] = 0

        return binary_sector

    def is_time(txt: str):
        if len(txt) == 5:
            return txt[0].isdigit() and txt[1].isdigit() and (txt[2] == "." or txt[2] == ":") \
                and txt[3].isdigit() and txt[4].isdigit()

        elif len(txt) == 4:
            return txt[0].isdigit() and (txt[1] == "." or txt[1] == ":") and txt[2].isdigit() and txt[3].isdigit()

        else:
            return False


    def process_0(self):
        return "<Пусто>"

    def process_1(self):
        eq = self.are_brothers

        a = self.A()
        b = self.B()
        c = self.C()
        d = self.D()

        eq_ac = eq(a, c)
        eq_bd = eq(b, d)

        a1 = a.lower()

        l1 = self.list[0][0]
        l2 = self.list[1][0]
        l3 = self.list[2][0]
        l4 = self.list[3][0]

        info = ""

        # 1.1
        if (a == b and c == d and eq_ac and eq_bd) or (
                l1 == l2 and l2 == l3 and l3 != l4) or "физическая культура" in a1:
            info += "\n      •  " + self.L(1, 4)

        # 1.2
        elif a != b and c != d and not eq_ac and not eq_bd:
            r21 = self.list[1][0]
            r22 = self.list[1][2]
            r41 = self.list[3][0]
            r42 = self.list[3][2]

            if (self.has_nums(r21) and not self.has_nums(r22)) or (self.has_nums(r22) and not self.has_nums(r21)):
                r1 = ""
                r2 = ""

                if r21 == r22:
                    r1 = r21
                else:
                    r1 = r21 + r22

                if r41 == r42:
                    r2 = r41
                else:
                    r2 = r41 + r42

                info += "\n      •  " + "1-я неделя — " + a + r1
                info += "\n      •  " + "2-я неделя — " + c + r2
            else:
                info += "\n   1-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + a
                info += "\n      •  " + "2-я подгруппа — " + b

                info += "\n   2-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + c
                info += "\n      •  " + "2-я подгруппа — " + d


        # 1.3
        elif a == b and c == d and not eq_ac and not eq_bd:
            info += "\n      •  " + "1-я неделя — " + a
            info += "\n      •  " + "2-я неделя — " + c

        # 1.4
        elif a != b and c != d and eq_ac and eq_bd:
            info += "\n   1-я подгруппа:"
            info += "\n      •  " + self.sum_if_not_equal(a, c)

            info += "\n   2-я подгруппа:"
            info += "\n      •  " + self.sum_if_not_equal(b, d)

        # 1.5
        elif a == b and c == d and not eq_ac and not eq_bd:
            info += "\n   1-я неделя:"
            info += "\n      •  " + "1-я подгруппа — " + a
            info += "\n      •  " + "2-я подгруппа — " + b

            info += "\n   2-я неделя:"
            info += "\n      •  " + c

        # 1.6
        elif a == b and c != d and not eq_ac and not eq_bd:
            info += "\n   1-я неделя:"
            info += "\n      •  " + a

            info += "\n   2-я неделя:"
            info += "\n      •  " + "1-я подгруппа — " + c
            info += "\n      •  " + "2-я подгруппа — " + d

        # 1.7
        elif a != b and c != d and eq_ac and not eq_bd:
            info += "\n   1-я подгруппа:"
            info += "\n      •  " + self.sum_if_not_equal(a, c)

            info += "\n   2-я подгруппа:"
            info += "\n      •  " + "1-я неделя — " + b
            info += "\n      •  " + "2-я неделя — " + d

        # 1.8
        elif a != b and c != d and not eq_ac and eq_bd:
            info += "\n   1-я подгруппа:"
            info += "\n      •  " + "1-я неделя — " + a
            info += "\n      •  " + "2-я неделя — " + c

            info += "\n   2-я подгруппа:"
            info += "\n      •  " + self.sum_if_not_equal(b, d)

        # 1.0
        else:
            info = "\n      •  " + self.L(1, 4)
            pass

        return info

    def process_2(self):
        a = self.A()
        b = self.B()

        info = ""

        if "физическая" in a.lower() + b.lower() or "курсовое" in a.lower() + b.lower():
            info += "\n      • "

            c = self.C()
            d = self.D()

            if a != b:
                info += a + b
            else:
                info += a

            if a != c:
                if c != d:
                    info += c + d
                else:
                    info += c

        else:
            if a != b:
                info += "\n   1-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + a
                info += "\n      •  " + "2-я подгруппа — " + b
            else:
                info += "\n   1-я неделя:"
                info += "\n      •  " + a
        return info

    def process_3(self):
        c = self.C()
        d = self.D()

        info = ""

        if c != d:
            info += "\n   2-я неделя:"
            info += "\n      •  " + "1-я подгруппа — " + c
            info += "\n      •  " + "2-я подгруппа — " + d
        else:
            info += "\n   2-я неделя:"
            info += "\n      •  " + c

        return info

    def process_4(self):
        a = self.A()
        c = self.C()

        info = ""

        if self.are_brothers(a, c):
            info += "\n   1-я подгруппа:"
            info += "\n      •  " + self.sum_if_not_equal(a, c)
        else:
            info += "\n   1-я подгруппа:"
            info += "\n      •  " + "1-я неделя — " + a
            info += "\n      •  " + "2-я неделя — " + c

        return info

    def process_5(self):
        s = self.list

        b = self.B()
        d = self.D()

        info = ""

        if self.are_brothers(b, d):
            info += "\n   2-я подгруппа:"
            info += "\n      •  " + self.sum_if_not_equal(b, d)
        else:
            info += "\n   2-я подгруппа:"
            info += "\n      •  " + "1-я неделя — " + b
            info += "\n      •  " + "2-я неделя — " + d

        return info

    def process_6(self):
        a = self.A()
        c = self.C()
        d = self.D()

        eq = self.are_brothers(a, c)

        info = ""

        if eq:
            info += "\n   1-я подгруппа:"
            info += "\n      •  " + self.sum_if_not_equal(a, c)

            info += "\n   2-я подгруппа:"
            info += "\n      •  " + "2-я неделя — " + d
        else:
            if c == d:
                info += "\n   1-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + a

                info += "\n   2-я неделя:"
                info += "\n      •  " + c

            else:
                info += "\n   1-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + a

                info += "\n   2-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + c
                info += "\n      •  " + "2-я подгруппа — " + d

        return info

    def process_7(self):
        b = self.B()
        c = self.C()
        d = self.D()

        eq = self.are_brothers(b, d)

        info = ""

        if eq:
            info += "\n   1-я подгруппа:"
            info += "\n      •  " + "2-я неделя — " + c

            info += "\n   2-я подгруппа:"
            info += "\n      •  " + self.sum_if_not_equal(b, d)
        else:
            if c == d:
                info += "\n   1-я неделя:"
                info += "\n      •  " + "2-я подгруппа — " + b

                info += "\n   2-я неделя:"
                info += "\n      •  " + c

            else:
                info += "\n   1-я неделя:"
                info += "\n      •  " + "2-я подгруппа — " + b

                info += "\n   2-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + c
                info += "\n      •  " + "2-я подгруппа — " + d

        return info

    def process_8(self):
        a = self.A()
        b = self.B()
        d = self.D()

        eq = self.are_brothers(b, d)

        info = ""

        if eq:
            info += "\n   1-я подгруппа:"
            info += "\n      •  " + "1-я неделя — " + a

            info += "\n   2-я подгруппа:"
            info += "\n      •  " + self.sum_if_not_equal(b, d)
        else:
            if a == b:
                info += "\n   1-я неделя:"
                info += "\n      •  " + a

                info += "\n   2-я неделя:"
                info += "\n      •  " + "2-я подгруппа — " + d

            else:
                info += "\n   1-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + a
                info += "\n      •  " + "2-я подгруппа — " + b

                info += "\n   2-я неделя:"
                info += "\n      •  " + "2-я подгруппа — " + d

        return info

    def process_9(self):
        a = self.A()
        b = self.B()
        c = self.C()

        eq = self.are_brothers(a, c)

        info = ""

        if eq:
            info += "\n   1-я подгруппа:"
            info += "\n      •  " + self.sum_if_not_equal(a, c)

            info += "\n   2-я подгруппа:"
            info += "\n      •  " + "2-я неделя — " + b
        else:
            if a == b:
                info += "\n   1-я неделя:"
                info += "\n      •  " + a

                info += "\n   2-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + c

            else:
                info += "\n   1-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + a
                info += "\n      •  " + "2-я подгруппа — " + b

                info += "\n   2-я неделя:"
                info += "\n      •  " + "1-я подгруппа — " + c

        return info

    def process_10(self):
        a = self.A()

        info = ""

        info += "\n   1-я неделя:"
        info += "\n      •  " + "1-я подгруппа — " + a

        return info

    def process_11(self):
        b = self.B()

        info = ""

        info += "\n   1-я неделя:"
        info += "\n      •  " + "2-я подгруппа — " + b

        return info

    def process_12(self):
        c = self.C()

        info = ""

        info += "\n   2-я неделя:"
        info += "\n      •  " + "1-я подгруппа — " + c

        return info

    def process_13(self):
        d = self.D()

        info = ""

        info += "\n   2-я неделя:"
        info += "\n      •  " + "2-я подгруппа — " + d

        return info

    def process_14(self):
        a = self.A()
        d = self.D()

        info = ""

        info += "\n   1-я неделя:"
        info += "\n      •  " + "1-я подгруппа — " + a

        info += "\n   2-я неделя:"
        info += "\n      •  " + "2-я подгруппа — " + d

        return info

    def process_15(self):
        b = self.B()
        c = self.C()

        info = ""

        info += "\n   1-я неделя:"
        info += "\n      •  " + "2-я подгруппа — " + b

        info += "\n   2-я неделя:"
        info += "\n      •  " + "1-я подгруппа — " + c

        return info

    def process_error(self):
        return "Ошибка!"

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
        if self.list is None:
            return self.process_0()

        pattern = self.pattern

        if pattern in range(0, 16):
            return self.__processors[pattern]() + " (#{})".format(pattern)
            #return self.__processors[pattern]()
        else:
            return self.process_error()

    @property
    def pattern(self):
        pattern = -1

        a = self.A()
        b = self.B()
        c = self.C()
        d = self.D()

        yes = self.bln

        def no(x):
            return not yes(x)

        if no(a) and no(b) and no(c) and no(d):
            pattern = 0

        elif yes(a) and yes(b) and yes(c) and yes(d):
            pattern = 1

        elif yes(a) and yes(b) and no(c) and no(d):
            pattern = 2

        elif no(a) and no(b) and yes(c) and yes(d):
            pattern = 3

        elif yes(a) and no(b) and yes(c) and no(d):
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
        return self.unisum([self.list[num - 1]])

    def L(self, start, end):
        lst = []
        for i in range(start, end + 1):
            lst.append([self.S(i)])

        return self.unisum(lst)

    def A(self):
        a = self.unisum(self.a)
        return self.remove_weeks(a)

    def B(self):
        b = self.unisum(self.b)
        return self.remove_weeks(b)

    def C(self):
        c = self.unisum(self.c)
        return self.remove_weeks(c)

    def D(self):
        d = self.unisum(self.d)
        return self.remove_weeks(d)


if __name__ == "__main__":
    s = Sector([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    print(s.has_nums("a 1"))

    print()
    pass
