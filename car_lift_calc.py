import math
import numpy as np
import turtle as t
import copy

class GVec:
    def __init__(self, x, y):
        self.x = float(0)
        self.y = float(0)
        self.add2(x, y)

    def add2(self, vx, vy):
        self.x += vx
        self.y += vy
        self.len = math.sqrt(self.x * self.x + self.y * self.y)

        return self

    def add(self, v):
        self.add2(v.x, v.y)

        return self

    def elongate(self, dl):
        crt_angle = self.get_crt_angle()
        self.len += dl

        self.x = self.len * math.cos(crt_angle)
        self.y = self.len * math.sin(crt_angle)

        return self

    def len(self):
        return self.len

    def get_crt_angle(self):
        if self.len > 0:
            try:
                tmp = self.y / self.x
            except ZeroDivisionError:
                tmp = float('inf') if self.y > 0 else float('-inf')
            crt_angle = math.atan(tmp)

            return crt_angle
        return 0


    def rotate(self, angle):
        if self.len > 0:
            crt_angle = self.get_crt_angle()
            angle += crt_angle
	
            self.x = self.len * math.cos(angle)
            self.y = self.len * math.sin(angle)
        return self

    def __str__(self):
        return "cart ({:.2f}, {:.2f}) / angular ({:.2f}, {:.2f})".format(self.x, self.y, self.len, self.get_crt_angle() * 180 / math.pi)

class GLine:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def fromGVecs(v1, v2):
        return GLine.fromPoints(v1.x, v1.y, v2.x, v2.y)

    @staticmethod
    def fromPoints(x1, y1, x2, y2):
        assert not (x1 == x2 and y1 == y2)

        if x1 != x2 and y1 != y2:
            a = 1 / (x2 - x1)
            b = - 1 / (y2 - y1)
            c = y1 / (y2 - y1) - x1 / (x2 - x1)
        elif x1 == x2:
            b = 0
            a = 1
            c = -x1
        elif y1 == y2:
            a = 0
            b = 1
            c = -y1

        return GLine(a, b, c)

    def hasPoint(self, x, y):
        return self.a * x + self.b * y + self.c == 0

    def distToPoint(self, x, y):
        return abs(self.a * x + self.b * y + self.c) / math.sqrt(self.a * self.a + self.b * self.b)

    def intersectPoint(self, l):
        A = np.array([ [ self.a, self.b ], [l.a, l.b] ])
        B = np.array([ -self.c, -l.c ])
        X = np.linalg.inv(A).dot(B)
        return GVec(X[0], X[1])


class ClearanceCalc:

    def __init__(self, amp: float = 285.1, rh:float = 13.6, dh: float = 20.0, rl: float = 495, mc: float = 2):
        self.amp = amp
        self.rh = rh
        self.dh = dh
        self.rl = rl
        self.mc = mc

        car_angle = math.asin(dh / amp)

        print("Valori intrare (cm):")
        print("  ampatament: {:.1f}".format(amp))
        print("  garda sol: {:.1f}".format(rh))
        print("  dif nivel lift: {:.1f}".format(dh))
        print("  min clearance: {:.1f}".format(mc))


        self.vec_rear = GVec(self.amp, 0).rotate(car_angle)
        self.rh_vec_front = GVec(0, self.rh).rotate(car_angle)
        self.rh_vec_rear = GVec(self.amp, 0).rotate(car_angle).add(self.rh_vec_front)

        self.rh_line = GLine.fromGVecs(self.rh_vec_front, self.rh_vec_rear)
        self.lift_line = GLine.fromGVecs(GVec(0, dh), GVec(1, dh))

        self.rh_lift_intersect = self.rh_line.intersectPoint(self.lift_line)
        self.lift_end = copy.deepcopy(self.rh_lift_intersect).add(GVec(self.rl, 0))

        car_angle_check = math.asin((self.rh_vec_rear.y - self.rh_vec_front.y) / (self.rh_vec_rear.x - self.rh_vec_front.x))

        self.cl_vec_front = GVec(0, -mc).rotate(car_angle).add(self.rh_vec_front)
        self.cl_vec_rear = copy.deepcopy(self.cl_vec_front).add(self.vec_rear)

        self.cl_line = GLine.fromGVecs(self.cl_vec_front, self.cl_vec_rear)

        self.min_cl_point = self.cl_line.intersectPoint(self.lift_line)

        print("{:.2f}".format(car_angle_check * 180 / math.pi))

        print("Valori calculate (cm,grade):")
        print("  unghi masina: {:.2f}".format(car_angle * 180 / math.pi))
        print("  punct atingere masina: " + str(self.rh_lift_intersect))
        print("  lungime rampa: {:.2f}".format(self.min_cl_point.len))
        print("  unghi rampa: {:.2f}".format(self.min_cl_point.get_crt_angle() * 180 / math.pi))
        print("  lungime proiectie  rampa: {:.2f}".format(self.min_cl_point.x))

    def draw(self):
        c = Canvas()

        c.set_color('blue')

        c.draw_line(GVec(0, 0), self.rh_vec_front)
        c.draw_line(self.rh_vec_front, self.rh_vec_rear)
        c.draw_line(self.vec_rear, self.rh_vec_rear)

        c.set_color('red')

        c.draw_line(self.rh_lift_intersect, self.lift_end)
        
        c.draw_grid([self.rh_lift_intersect.x], [self.rh_lift_intersect.y])

        c.center_y = -100
        c.set_color('blue')

        c.draw_line(GVec(0, 0), self.rh_vec_front)
        c.draw_line(self.rh_vec_front, self.rh_vec_rear)
        c.draw_line(self.vec_rear, self.rh_vec_rear)
        c.set_color('red')
        c.draw_line(self.min_cl_point, self.lift_end)
        c.set_color('green')
        c.draw_line(self.cl_vec_rear, self.cl_vec_front)
        c.set_color('red')
        c.draw_line(self.min_cl_point, GVec(0,0))
        c.draw_grid([self.min_cl_point.x], [self.min_cl_point.y])


class Canvas:
    def __init__(self):
        self.center_x = -140
        self.center_y = 0
        self.scale = 3

    def set_color(self, c):
        t.color(c)

    def draw_line(self, v1, v2):
        t.penup()

        t.setpos(self.scale * (v1.x + self.center_x), self.scale * (v1.y + self.center_y))
        t.pendown()

        t.setpos(self.scale * (v2.x + self.center_x), self.scale * (v2.y + self.center_y))
        t.penup()

    def set_pos(self, x, y):
        t.setpos(self.scale * (x + self.center_x), self.scale * (y + self.center_y))

    def draw_h_grid_line(self, x, label):
        gl_len = 15
        font_h = 20

        self.draw_line(GVec(x, 0), GVec(x, -gl_len))
        self.set_pos(x + 2, -gl_len)
        t.write(label, font=('Arial', 24, 'normal'))

    def draw_v_grid_line(self, y, label):
        gl_len = 15
        font_h = 20

        self.draw_line(GVec(0, y), GVec(-gl_len, y))
        self.set_pos(-gl_len, y + 2)
        t.write(label, font=('Arial', 24, 'normal'))

    def draw_grid(self, xpoints, ypoints):

        t.color('grey')

        # 0x
        self.draw_line(GVec(0, 0), GVec(200, 0))
        self.draw_h_grid_line(0, "0cm")
        for p in xpoints:
            self.draw_h_grid_line(p, "{:.1f}".format(p))

        # 0y
        self.draw_line(GVec(0, 0), GVec(0, 40))
        self.draw_v_grid_line(0, "0")
        for p in ypoints:
            self.draw_v_grid_line(p, "{:.1f}".format(p))


def test_rot():
    v = GVec(1, 0)
    print(v)

    v.rotate(math.pi / 2)
    print(v)

    v.rotate(math.pi / 2)
    print(v)
    
    v.rotate(-math.pi)
    print(v)

    v.rotate(math.pi)
    print(v)

    v.rotate(-math.pi / 4)
    print(v)

    v.elongate(1.41)

def test_line():
    l = GLine.fromPoints(0, 1, 1, 1)
    print(l.hasPoint(2, 1))
    print(l.hasPoint(2, 2))
    print(l.distToPoint(9, 9))

    l = GLine.fromPoints(7, 1, 7, 2)
    print(l.hasPoint(7, 8))
    print(l.hasPoint(8, 7))

    print(l.distToPoint(9, 9))

    l = GLine.fromPoints(1, 1, 7, 7)
    print(l.hasPoint(2, 2))
    print(l.hasPoint(2, 2.1))

    print(l.distToPoint(0, 1))

    l1 = GLine.fromPoints(0, 0, 1, 1)
    l2 = GLine.fromPoints(0, 1, 1, 0)

    print(l1.intersectPoint(l2))

if __name__ == "__main__":
    x = ClearanceCalc()
    x.draw()
    while True:
        pass
