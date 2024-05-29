from fractions import Fraction
from math import gcd, floor
import numpy as np


class LiniarFunction:
    class Line:
        def __init__(self, x1, y1, x2, y2):
            self.x1, self.x2 = x1, x2
            self.y1, self.y2 = y1, y2
        
        def calc(self, number):
            x = np.linspace(self.x1, self.x2, number)
            k = (self.y2 - self.y1) / (self.x2 - self.x1)
            b = self.y1 - self.x1*k
            y = x*k + b
            return x, y
    
    def __init__(self, slopecoef, freecoef, precision):
        self.precision = precision
        self.slopecoef_rat = Fraction(slopecoef)
        self.freecoef_rat = Fraction(freecoef)
        self.slopecoef_2adic = self.fractionTo2adic(self.slopecoef_rat)
        self.freecoef_2adic = self.fractionTo2adic(self.freecoef_rat)
        return
    
    def fractionTo2adic(self, rational):
        result = 0b00000000
        numer = rational.numerator
        denom = rational.denominator
        i = 0
        numbers = dict()

        tmp = (numer - denom)/2
        if tmp % 1 == 0:
            result += 1 << i
            numer = tmp
        else: 
            numer /= 2
        i+=1

        while int(numer) not in numbers.keys():
            numbers[int(numer)] = i
            tmp = (numer - denom)/2
            if tmp % 1 == 0:
                result += 1 << i
                numer = tmp
            else: 
                numer /= 2
            i+=1
        cycle = result >> numbers[int(numer)]
        return bin(result^(cycle << numbers[int(numer)]))[2:], bin(cycle)[2:], i - numbers[int(numer)], numbers[int(numer)]
    
    def multiplicativeOrder(self, A, N) :
        if (gcd(A, N) != 1) :
            return 1
        # result store power of A that raised 
        # to the power N-1
        result = 1
        k = 1
        while (k <= N):
            # modular arithmetic
            result = (result * A) % N 
            # return smallest + ve integer
            if (result == 1) :
                return k
            # increment power
            k = k + 1
        return 1

    def cablenum(self):
        e = gcd(self.freecoef_rat.denominator, self.slopecoef_rat.denominator)
        return self.multiplicativeOrder(2, int(self.freecoef_rat.denominator/e))
    
    def info(self):
        format = lambda s: f"...({(s[2] - len(s[1]))*'0'}{s[1]}){(s[3] - len(s[0]))*'0'}{s[0]}"
        numbers_info = f"{self.freecoef_rat} = {format(self.freecoef_2adic)}\
                        \n{self.slopecoef_rat} = {format(self.slopecoef_2adic)}"
        cable_info = f"number of cables: {self.cablenum()}" #cable turns around the inner circle: {}"
        return f"{numbers_info}\n{cable_info}"
    
    def divideonlines(self, freecoef_rat):
        freecoef = float(freecoef_rat)
        slopecoef = float(self.slopecoef_rat)

        if slopecoef != 0:
            vecround = lambda a, pres: (round(a[0], pres), round(a[1], pres))

            y_prev =  0
            x_prev = round(-freecoef/slopecoef, 5)
            points = [vecround((x_prev, y_prev), 5)]

            direction = 1
            step_y = 1
            if slopecoef<0:
                step_y = -1
                direction = -1
            step_x = 1

            compare = lambda a, b : round(a[0]%1, 5) == round(b[0]%1, 5) \
                                    and round(a[1]%1, 5) == round(b[1]%1, 5)
            dist = lambda a, b: ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

            start_x, start_y = floor(x_prev), y_prev
            prev = points[0]

            cur_x = vecround((start_x + step_x,
                                freecoef + slopecoef*(start_x + step_x)), 5)
            cur_y = vecround(((start_y + step_y - freecoef)/slopecoef,
                            start_y + step_y), 5)

            if dist(cur_x, prev) < dist(cur_y, prev):
                prev = cur_x
                step_x += 1
            elif dist(cur_x, prev) > dist(cur_y, prev):
                prev = cur_y
                step_y += direction
            else:
                prev = cur_x
                step_x += 1
                step_y += direction

            while not compare(points[0], prev):
                points.append(prev)
                cur_x = vecround((start_x + step_x,
                                freecoef + slopecoef*(start_x + step_x)), 5)
                cur_y = vecround(((start_y + step_y - freecoef)/slopecoef,
                                start_y + step_y), 5)
                if dist(cur_x, prev) < dist(cur_y, prev):
                    prev = cur_x
                    step_x += 1
                elif dist(cur_x, prev) > dist(cur_y, prev):
                    prev = cur_y
                    step_y += direction
                else:
                    prev = cur_x
                    step_x += 1
                    step_y += direction
            points.append(prev)
            
            mod1 = lambda val: val%1 if val%1 != 0 else 1
            lines = []
            for i in range(1, len(points)):
                if points[i-1][1] > points[i][1]:
                    start_y = mod1(points[i-1][1])
                    end_y = points[i][1]%1
                else:
                    end_y = mod1(points[i][1])
                    start_y = points[i-1][1]%1
                start_x = points[i-1][0]%1
                end_x = mod1(points[i][0])
                line = LiniarFunction.Line(start_x, start_y, end_x, end_y)
                lines.append(line.calc(self.precision))
        else:
            line = LiniarFunction.Line(0, freecoef%1, 1, freecoef%1)
            lines = [line.calc(self.precision)]
        return lines
    
    def divideoncables(self):
        cables = []
        self.freecoefs = []
        for i in range(self.cablenum()):
            self.freecoefs.append((-self.freecoef_rat*2**i)%1)
            cables.append(self.divideonlines(self.freecoefs[i]))  
        return cables