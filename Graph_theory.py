import time, os, csv, pprint

city = input("City:\n").lower()
folder = city + "metro"
#input can be taipei, sfran or futuretaipei

#Loads statistics about the city, currently only capacity and line length
stats = {}
with open(city+"_stats.csv", "r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.split(",")
        stats[line[0]] = float(line[1].rstrip("\n"))

# Loads each line individually
metrolines = {}
for metrofile in os.listdir(folder):
    linename = metrofile.split("_")[0]
    metrolines[linename] = []
    with open(folder + "/" + metrofile) as file:    
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            metrolines[linename].append(row[0])
for line in metrolines:
    metrolines[line] = [station.lower().rstrip() for station in metrolines[line]]

#finds the number of vertices
stations = []
for line in metrolines:
    stations.extend(metrolines[line])
with open(city + "stationlist.txt", "w") as file:
    for x in sorted(set(stations)):
        file.write(x + "\n")
vertices = len(set(stations))
print(f"Vertices: {vertices}")

edgepairs = []

#Finds the number of edges using alphabetized pairs
for line in metrolines:
    for index in range((len(metrolines[line])-1)):
        pair = sorted([metrolines[line][index], metrolines[line][index+1]])
        edgepairs.append(",".join(pair))
edges = len(set(edgepairs))
print(f"Edges: {edges}")

#finds number of subgraphs
linkages = {}
trstations = []
for line in metrolines:
    otherlines = list(metrolines.keys())
    otherlines.remove(line)
    linkages[line] = []
    for otherline in otherlines:
        trs = set(metrolines[line]).intersection(set(metrolines[otherline]))
        if bool(trs):
            linkages[line].append(otherline)
            trstations.extend(trs)
trstations = set(trstations)
subgraphs = {}
sgcount = 0
for line in linkages:
    dissolved = [line]
    dissolved.extend(linkages[line])
    subgraphs[sgcount] = dissolved
    sgcount += 1

changes = True
while changes:
    subgcount = len(subgraphs)
    for idx1 in subgraphs:
        others = list(subgraphs.keys())
        others.remove(idx1)
        for idx2 in others:
            intersect = set(subgraphs[idx1]).intersection(set(subgraphs[idx2]))
            if bool(intersect):
                subgraphs[idx1].extend(subgraphs[idx2])
                subgraphs[idx2] = []
    if not bool(subgraphs[idx2]):
        subgraphs.pop(idx2)
    if subgcount == len(subgraphs):
        changes = False
for s in list(subgraphs):
    if not bool(subgraphs[s]):
        subgraphs.pop(s)
subgraphs = len(subgraphs)
print(f"Subgraphs: {subgraphs}")

#print("α = (e-v+p)/(2v-5)")
alpha = (edges - vertices + subgraphs) / ((2 * vertices)-5)
print(f"α = {round(alpha, 3)}")

#print("β = e/v")
beta = edges / vertices
print(f"β = {round(beta,3)}")

#print("γ = e/3(v-2)")
gamma = edges / (3 * (vertices-2))
print(f"γ = {round(gamma,3)}")

#print("η = (L(G))/e")
eta = stats["length"]/edges
print(f"η = {round(eta,3)}")

#print("θ = Q(G)/v")
theta = stats["load"] / vertices
print(f"θ = {round(theta,3)}")
