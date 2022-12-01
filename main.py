THETA = "\u03B8"
BRAILLE = [" ", "\u2840", "\u28C0", "\u28E0", "\u28E4", "\u28E6", "\u28F6", "\u28FE", "\u28FF"]


class Draw:
    @classmethod
    def braille(cls, derive):
        braille_string = ""
        if 0 <= derive < 8:
            braille_string += BRAILLE[derive]
        elif derive < 8**2:
            braille_string += BRAILLE[derive // 8] + BRAILLE[derive % 8]
        else:
            braille_string += BRAILLE[derive // 8**2] + BRAILLE[(derive // 8) % 8] + BRAILLE[derive % 8]
        return braille_string

class Theta:
    def __init__(self, derive, exponant=1):
        self.exponant = exponant
        self.derive = derive

    def str(self):
        return (f'{Draw.braille(self.derive):>3}{" " if self.exponant == 1 else self.exponant}',
                f'{THETA:^4}')

    def dt(self):
        if self.exponant == 1:
            return [Theta(self.derive + 1, self.exponant)], 1
        else:
            newsTheta = [Theta(self.derive + 1, 1), Theta(self.derive, self.exponant - 1)]
            nombre = self.exponant
            return newsTheta, nombre

    def __eq__(self, other):
        if isinstance(other, Theta):
            return self.derive == other.derive and self.exponant == other.exponant
        else:
            return False

    def copy(self):
        return Theta(self.derive, self.exponant)

class Elt:
    def __init__(self):
        self.rpoint = 0
        self.theta: list[Theta] = []
        self.nombre = 1

    def str(self):
        l1 = f"  {Draw.braille(self.rpoint)} "
        if self.nombre == 1:
            l2 = "  r "
        elif self.nombre == -1:
            l2 = " -r "
        else:
            l2 = f"{self.nombre:>2}r "
        for t in self.theta:
            l1 += t.str()[0]
            l2 += t.str()[1]
        return l1 + f" ", l2 + f" "

    def dt(self):
        # newEq = Eq("tmp")
        # newElt = Elt()
        # newElt.rpoint = self.rpoint + 1
        # newElt.theta = self.theta.copy()
        # newElt.nombre = self.nombre
        # newEq.elt.append(newElt)
        # for i in range(len(self.theta)):
        #     newElt = Elt()
        #     print(self.theta[i].str())
        #     Tderive = self.theta[i].derive()
        #     if Tderive[1] != -1:
        #         newElt.nombre = self.nombre
        #         newElt.rpoint = self.rpoint
        #         newElt.theta = Tderive[0]
        #         newEq.elt.append(newElt)
        #     else:
        #         for t in Tderive[0]:
        #             newElt.nombre = self.nombre
        #             newElt.rpoint = self.rpoint
        #             newElt.theta = t
        #             newEq.elt.append(newElt)
        # return newEq
        newEq = Eq("tmp")
        newElt = Elt()
        # R'
        newElt.rpoint = self.rpoint + 1
        newElt.theta = self.theta.copy()
        newElt.nombre = self.nombre
        newEq.elt.append(newElt)
        # Theta'
        for i in range(len(self.theta)):
            newElt = Elt()
            Tderive = self.theta[i].dt()
            Tcopy = self.theta.copy()
            Tcopy.pop(i)
            Tcopy.extend(Tderive[0])
            newElt.rpoint = self.rpoint
            newElt.theta = Tcopy
            newElt.nombre = self.nombre * Tderive[1]
            newEq.elt.append(newElt)
        return newEq

    def copy(self):
        newElt = Elt()
        newElt.rpoint = self.rpoint
        newElt.theta = self.theta.copy()
        newElt.nombre = self.nombre
        return newElt

    def theta_join(self):
        newtheta = []
        for i in self.theta:
            if i not in newtheta:
                newtheta.append(i.copy())
            else:
                newtheta[newtheta.index(i)].exponant += i.exponant
        self.theta = newtheta


class Eq:
    def __init__(self, arg, elt=None):
        self.arg: str = arg
        self.elt: list[Elt] = [] if elt is None else elt

    def str(self):
        return ("(" + "   ".join([e.str()[0] for e in self.elt]) + ") ->"), (
                "(" + " + ".join([e.str()[1] for e in self.elt]) + f") {self.arg}")

    def dt(self):
        newEq = Eq(self.arg)
        for e in self.elt:
            newEq.elt.extend(e.dt().elt)
        return newEq

    def th(self):
        newEq = Eq(self.arg)
        for e in self.elt:
            newElt = Elt()
            newElt.rpoint = e.rpoint
            theta = e.theta.copy()
            theta.append(Theta(1, 1))
            newElt.theta = theta
            newElt.nombre = e.nombre
            newEq.elt.append(newElt)
        return newEq

    def neg(self):
        for e in range(len(self.elt)):
            self.elt[e].nombre *= -1

    def eq_join(self):   # TODO TOFIX
        newEq = Eq(self.arg)
        for e in self.elt:
            for ne in newEq.elt:
                if e.rpoint == ne.rpoint and e.theta == ne.theta:
                    ne.nombre += e.nombre
                    break
            else:
                newEq.elt.append(e.copy())
        return newEq


    def eq_rm_zero(self):
        newEq = Eq(self.arg)
        for e in self.elt:
            if e.nombre != 0:
                newEq.elt.append(e.copy())
        return newEq

def draw(UR, UT, pow):
    print(f"d^{pow}OM   " + UR.str()[0])
    print(f"dt^{pow}  = " + UR.str()[1])
    print("        " + UT.str()[0])
    print("  +     " + UT.str()[1])
    print("")

def ALLdraw(E):
    print(E.str()[0])
    print(E.str()[1])
    print("")


if __name__ == "__main__":
    # Final Test
    # First iteration OM = rUR
    # Second iteration dOM = r'UR + rT'UT
    UR = Eq("UR")
    elt = Elt()
    elt.rpoint = 1
    UR.elt.append(elt)
    UT = Eq("UT")
    elt = Elt()
    elt.rpoint = 0
    elt.theta.append(Theta(1, 1))
    UT.elt.append(elt)

    for i in range(1, 20):
        # newUR = derive(UR) + theta(UT)
        # newUT = derive(UT) - theta(UR)
        # UR = join(UR)
        # UT = join(UT)


        draw(UR, UT, i)
        URdt = UR.dt()


        UTdt = UT.dt()


        URth = UR.th()


        UTth = UT.th()
        UTth.neg()

        UR = Eq("UR")
        UR.elt.extend(URdt.elt)
        UR.elt.extend(UTth.elt)
        UT = Eq("UT")
        UT.elt.extend(UTdt.elt)
        UT.elt.extend(URth.elt)



        for e in UR.elt:
            e.theta_join()
        for e in UT.elt:
            e.theta_join()

        UR = UR.eq_join()
        UT = UT.eq_join()

        UR = UR.eq_rm_zero()
        UT = UT.eq_rm_zero()
        print("")



    print("Final")
    draw(UR, UT, 4)