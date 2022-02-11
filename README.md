# labamale (an anagram for the romanian `balamale`)
Calculating dual link positions for wall mounted beds

## Finding all solutions for dual-linked wall-bed mechanism

`labamale.py` produces all possible combinations of a dual link mechanism given the sizes of the bed frame, bed mount and the bed frame's vertical and horizontal positions. I takes no arguments, all tuning needs to be performed inside the script:

- `poz_oriz` the rectangle of the bed frame in horizontal position
- `poz_vert` " vertical position
- `zona_pivoti_montant` the area of the bed mount where the links can be attached to

`labamale.py` implements backtracking to find all possible beams of the dual link bed mechanism using the circle ecuation starting from given horizontal and vertical bed frame positions

### Running

```
 # ./labamale.py
```

### Sample Output

```
h1_x,h1_y,p1_x,p1_y,v1_x,v1_y,h2_x,h2_y,p2_x,p2_y,v2_x,v2_y
7,32,20,21,33,9,11,36,20,29,29,13
7,32,20,21,33,9,27,38,20,29,27,29
7,32,20,21,33,9,35,39,20,29,26,37
7,32,20,21,33,9,43,40,20,29,25,45
19,33,20,21,32,21,11,36,20,29,29,13
19,33,20,21,32,21,27,38,20,29,27,29
19,33,20,21,32,21,35,39,20,29,26,37
```

Each line contains 6 coordinates, as follows:
- (h1_x, h1_y) coordinates of mech's beam 1 on the bed frame when in horizontal position
- (p1_x, p1_y) coordinates of mech's beam 1 pivot on the bed mount
- (v1_x, v1_y) coordinates of mech's beam 1 on the bed frame when in vertical position
- (h2_x, h2_y) coordinates of mech's beam 2 on the bed frame when in horizontal position
- (p2_x, p2_y) coordinates of mech's beam 2 pivot on the bed mount
- (v2_x, v2_y) coordinates of mech's beam 2 on the bed frame when in vertical position

### Solution visualization

`viz.html` uses JavaScript to draw the bed mechanism on a HTML5 canvas. Enter one line from `labamale`'s output inside the editbox and press `Baga` to get a display for that specific link configuration 

## Pivot and strut mount position calculator for wall-beds

`viz_struts.html` takes the pivot position in regards to the bed pillar and the distance between the pivot, the lower strut mount in regards to the mattress and the lenght of the extended strut and computes the height of the upper strut mount to the bed pillar
