import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import random
import math


class City:

    def __init__(self, name, lat, lon):
        self.name = name
        self.latitude = lat
        self.longitude = lon
        self.possible_cities = {}

    # Nie mozna w pythonie jawnie sortować po wartościach slownika, wiec w wyniku tej metody dostajemy krotke
    def get_closest_city_tuple(self):
        return sorted(self.possible_cities.items(), key=lambda kv: kv[1])[0]

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

    def count_distance_heuristic(self, to_city):
        y1 = self.longitude
        x1 = self.latitude
        y2 = to_city.longitude
        x2 = to_city.latitude
        coefficient = 40075.704 / 360
        return math.sqrt(((x2 - x1) ** 2) + ((math.cos((x1 * math.pi)/180) * (y2 - y1)) ** 2)) * coefficient

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
    setupCost = link.find('./setupCost').text
    for city in cities:
        if city.name == source:
            city.possible_cities.update({City.find_by_name(target): float(setupCost)})
        elif city.name == target:
            city.possible_cities.update({City.find_by_name(source): float(setupCost)})


print(len(cities))

index = 7
test_city = City.find_by_name('Gdansk')
print('xml parser check: ')
print('Selected city: ', test_city.name)
print('Number of admissible cities to visit', len(test_city.possible_cities))
for j in test_city.possible_cities:
    print('admissible city: ', j.name, ', and the setup cost is: ', test_city.possible_cities[j])

print('Distance to closest city from city from ', test_city.name, ' is: ', test_city.get_closest_distance(),
      ' and this city is: ', test_city.get_closest_city().name)
print('Distance to another city from city from ', test_city.name, ' is: ', test_city.get_all_possible_distances()[1],
      ' and this city is: ', test_city.get_all_possible_cities()[1].name)

# visualize points
polska = plt.imread("polska.jpg")
x = []
y = []
names = []
for city in cities:
    x.append(city.longitude)
    y.append(city.latitude)
    names.append(city.name)
print(x, '::', y)

plt.imshow(polska, extent=[14, 24, 48, 55])
plt.scatter(x, y)

for i, txt in enumerate(names):
    plt.annotate(txt, (x[i], y[i]))

plt.show()

# algorithm starts
visited_cities = []
first_city = cities[random.randint(0, len(cities) - 1)]
print(len(first_city.possible_cities))



# Util functions