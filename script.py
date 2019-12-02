import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import random
import math
from operator import itemgetter


class City:

    def __init__(self, name, lat, lon):
        self.name = name
        self.latitude = lat
        self.longitude = lon
        self.possible_cities = {}
        self.cities_left = {}
        self.cities_before = []

    # Nie mozna w pythonie jawnie sortować po wartościach slownika, wiec w wyniku tej metody dostajemy krotke
    def get_closest_city_tuple(self):
        return sorted(self.cities_left.items(), key=lambda kv: kv[1])[0]

    def get_closest_city(self):
        return self.get_closest_city_tuple()[0]

    def get_closest_distance(self):
        return self.get_closest_city_tuple()[1]

    def get_distance_to_city(self, direct_city):
        return self.possible_cities[direct_city]

    def get_all_possible_distances(self):
        return list(self.possible_cities.values())

    def get_all_possible_cities(self):
        return list(self.possible_cities.keys())

    def count_distance(self, city_to_go):
        y1 = self.longitude
        x1 = self.latitude
        y2 = city_to_go.longitude
        x2 = city_to_go.latitude
        coefficient = 40075.704 / 360
        return math.sqrt(((x2 - x1) ** 2) + ((math.cos((x1 * math.pi) / 180) * (y2 - y1)) ** 2)) * coefficient

    def count_cost(self, city_to_go):
        return {self: self.count_distance(city_to_go)}

    def count_total_cost(self, city_to_go, city_start):
        return {self: self.count_distance(city_to_go) + city_to_go.count_distance(city_start)}

    def can_come_back(self, city_start):
        return city_start in self.possible_cities.keys()

    @staticmethod
    def find_by_name(city_name):
        for element in cities:
            if element.name == city_name:
                return element


# xml parser
root = ET.parse('sndlib-instances-xml/sndlib-instances-xml/polska/polska.xml').getroot()

nodes = {node for node in root.findall('./networkStructure/nodes/node')}
links = {link for link in root.findall('./networkStructure/links/link')}

cities = []
for node in nodes:
    name = node.attrib.get('id')
    x = node.find('./coordinates/x')
    y = node.find('./coordinates/y')
    cities.append(City(name, float(y.text), float(x.text)))

for link in links:
    source = link.find('./source').text
    target = link.find('./target').text
    for city in cities:
        if city.name == source:
            to_city = City.find_by_name(target)
            city.possible_cities.update({to_city: city.count_distance(to_city)})
        elif city.name == target:
            to_city = City.find_by_name(source)
            city.possible_cities.update({to_city: city.count_distance(to_city)})

print(len(cities))

# visualize points
polska = plt.imread("polska.jpg")
x = []
y = []
names = []
for city in cities:
    x.append(city.longitude)
    y.append(city.latitude)
    names.append(city.name)

plt.imshow(polska, extent=[14, 24, 48, 55])
plt.scatter(x, y)

for i, txt in enumerate(names):
    plt.annotate(txt, (x[i], y[i]))

cities = cities[0:len(cities)]
print(len(cities))


# Util functions
def cut_heuristic_function(best_with_heuristic, start_city):
    distance_without_heuristic = best_with_heuristic[-1] - City.find_by_name(best_with_heuristic[-2]).count_distance(
        start_city)
    best_without_heuristic = best_with_heuristic.copy()
    best_without_heuristic[-1] = distance_without_heuristic
    return best_without_heuristic


def algorithm():
    start_city = cities[random.randint(0, len(cities) - 1)]
    opened_states = []
    closed_states = []
    opened_states.append([start_city.name, 0])
    while len(opened_states) > 0:
        best_operator = cut_heuristic_function(opened_states[0], start_city)
        current_city = City.find_by_name(best_operator[-2])
        current_city.cities_left = {}
        # Stop condition:
        if len(best_operator) == len(cities) + 1 and current_city.can_come_back(start_city):
            return best_operator
        available_cities = set(current_city.possible_cities.keys()).copy()
        visited_cities = best_operator[0:len(best_operator) - 1]
        visited_cities_objects = {City.find_by_name(name) for name in visited_cities}
        p = list(available_cities - set(visited_cities_objects))
        for i in p:
            current_city.cities_left.update(i.count_total_cost(current_city, start_city))
        for i in current_city.cities_left:
            to_insert = visited_cities.copy()
            to_insert.append(i.name)
            to_insert.append(best_operator[-1] + current_city.cities_left[i])
            opened_states.append(to_insert)
        opened_states.sort(key=itemgetter(-1))
        closed_states.append(opened_states[0])
        opened_states.pop(0)


# algorithm run
winner = algorithm()
print(winner)

# add path to map
ordered_cities = []
for i in winner[:-1]:
    ordered_cities.append(City.find_by_name(i))
plt.scatter(ordered_cities[0].longitude, ordered_cities[0].latitude, color='red', marker="X", s=80)

for i in range(len(ordered_cities)):
    plt.plot([ordered_cities[i].longitude, ordered_cities[i-1].longitude],
             [ordered_cities[i].latitude, ordered_cities[i-1].latitude], 'k-', color='red')
plt.show()
