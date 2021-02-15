
class Dreptunghi:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def gen_puncte(self, margine):
        for x in range(self.x +  margine, self.x + self.w - margine):
            for y in range(self.y + margine, self.y + self.h - margine):
                yield x, y
    def contine(self, x, y):
        return self.x <= x and self.x + self.w >= x and self.y <= y and self.y + self.h >= y

class Cerc:
    def __init__(self, x, y, sq_r):
        self.x = x
        self.y = y
        self.sq_r = sq_r

    def contine(self, x, y):
        return self.sq_r == round((self.x - x) ** 2 + (self.y - y) ** 2)

def sq_d(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

min_dist = 7
sq_min_dist = min_dist ** 2

def pivot_valid(pivot_x, pivot_y, planeta_x, planeta_y):
    """
    pivotul e pe montant, iar planetele pe cadrul patului
    """
    sq_r = (pivot_x - planeta_x) ** 2 + (pivot_y - planeta_y) ** 2
    if sq_r < 100:
        return False, 0, 0
    pivot = Cerc(pivot_x, pivot_x, sq_r)

    # pozitie fata de coltul st jos
    dx = planeta_x - poz_oriz.x
    dy = planeta_y - poz_oriz.y
    assert(dx > 0 and dy > 0)

    # gasim punctul pe dreptunghiul vertical (transpus)
    tx = poz_vert.x + poz_vert.w - dy
    ty = poz_vert.y + dx

    assert(poz_vert.contine(tx, ty))
    return pivot.contine(tx, ty), tx, ty

poz_oriz = Dreptunghi(3, 25, 50, 20)
poz_vert = Dreptunghi(20, 5, 20, 50)

zona_pivoti_montant = Dreptunghi(20, 20, 20, 20)

print("h1_x,h1_y,p1_x,p1_y,v1_x,v1_y,h2_x,h2_y,p2_x,p2_y,v2_x,v2_y")

for p1_x, p1_y in zona_pivoti_montant.gen_puncte(0):
    for p2_x, p2_y in zona_pivoti_montant.gen_puncte(0):
        if p2_x < p1_x or ( p2_x == p1_x and p2_y < p1_y ):
            continue
        if sq_d(p1_x, p1_y, p2_x, p2_y) < sq_min_dist:
            continue

        for h1_x, h1_y in poz_oriz.gen_puncte(3):
            contine1, v1_x, v1_y = pivot_valid(p1_x, p1_y, h1_x, h1_y)
            if contine1:
                for h2_x, h2_y in poz_oriz.gen_puncte(3):
                    contine2, v2_x, v2_y = pivot_valid(p2_x, p2_y, h2_x, h2_y)
                    if contine2:
                        print(f"{h1_x},{h1_y},{p1_x},{p1_y},{v1_x},{v1_y},{h2_x},{h2_y},{p2_x},{p2_y},{v2_x},{v2_y}")


