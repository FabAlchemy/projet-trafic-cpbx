cross_coords = [(1355, 1552), (1139, 984), (1608, 914), (1687, 1168), (1289, 1395), (1038, 1465), (930, 1503), (644, 1692),
 (622, 1752), (608, 1391), (541, 1080), (579, 2112), (746, 2128), (858, 1820), (1092, 1862), (941, 2134),
  (1278, 2186), (1355, 1950), (1359, 1826), (1510, 1833), (1525, 1534), (1817, 1534), (1910, 1743), (1788, 1764),
   (1764, 2053), (2065, 2101), (3002, 1815), (2653, 1651), (3422, 1608), (3319, 968), (2238, 743), (2373, 346),
    (1932, 289), (1764, 575), (1431, 377), (1359, 555), (1314, 366), (1186, 617), (1089, 804), (1101, 341)]
# Nb of crosses = 40

generator_cross_coords = [(0, 1110), (292, 1667), (716, 2440), (2253, 2440), (3824, 1667), (2193, 0), (1103, 0)]
# Nb of generator crosses = 7

l = len(cross_coords) -1
roads = [(l+1,10),(10,1),(1,38),(38,39),(39,36),(36,37),(37,38),(37,35),(35,34),(34,33),(39,l+7),(l+6,32),(32,33),(33,2),
(32,31),(31,30),(2,30),(30,29),(29,28),(28,l+5),(28,26),(26,25),(l+4,25),(26,27),(22,27),(22,25),(21,22),(3,21),(2,3),(1,2),
(1,5),(5,4),(4,3),(4,0),(0,20),(20,21),(20,19),(0,18),(18,17),(19,23),(23,22),(23,24),(24,25),(17,24),(17,16),(15,16),(14,15),
(14,17),(13,14),(12,15),(12,l+3),(12,13),(11,12),(11,8),(8,13),(8,l+2),(7,8),(7,9),(6,7),(6,9),(5,6),(5,13),(9,10),
(34,36),(18,19)]
# Nb of roads = 66

priority_axis = [(33,37),(2,30),(13,28),(27,28),(31,33),(30,61),(60,58),(58,56),(55,54),(57,62),(0,1),None,(51,50),(51,61),
(48,47),(46,49),None,(47,43),(37,38),(39,64),(34,35),(27,26),(26,25),(39,40),(42,43),(25,22),(20,23),None,(18,19),None,
(16,17),None,(11,12),(12,13),(63,9),None,(4,63),(6,7),(2,3),(3,10)]

# def maximum(liste):
#     maxx,maxy = 0,0
#     for x in liste:
#         if x[0]> maxx:
#             maxx = x[0]
#         if x[1] > maxy:
#             maxy = x[1]
#     return maxx,maxy
#
# print(maximum(cross_coords))
# print(maximum(generator_cross_coords))

# def modify(liste):
#     for x in liste:
#         if x != None:
#             if x[0] >=48 and <

print(roads[50])
