import pickle
import csv
import time

import folium
import requests
class City:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.score = 0
        self.buildings = []
        self.owner_country = None
class Unit:
    def __init__(self, unit_type, level, health, attack, defense, view_range):
        self.unitnumber=None
        self.unit_type = unit_type
        self.level = level
        self.health = health
        self.attack = attack
        self.defense = defense
        self.view_range = view_range
        self.location = None
        self.target_location = None
        self.moving_info = None
class Building:
    def __init__(self, name, in_construction, level, required_resources,
                 producing_unit, productable_unit_types, required_unit_resources):
        self.name = name
        self.in_construction = in_construction
        self.level = level
        self.required_resources = required_resources
        self.producing_unit = producing_unit
        self.productable_unit_types = productable_unit_types
        self.required_unit_resources = required_unit_resources
        self.target_production_complete_time = None
class Player:
    def __init__(self, id, country_name):
        self.id = id
        self.country_name = country_name
        self.supplies = 0
        self.components = 0
        self.electronics = 0
        self.rare_materials = 0
        self.population = 0
        self.money = 0
        self.units = []
        self.technology = None
        self.possessed_cities = []  # List to store City objects
    def assign_country(self, country):
        self.country_name = country
    @property
    def general_score(self):
        return sum(city.score for city in self.possessed_cities)
    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
# Read city information from the CSV file
def read_city_info_from_csv(filename):
    cities = {}
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            city_id = int(row[0])
            country_name = row[1]
            city_name = row[2]
            latitude = float(row[3])
            longitude = float(row[4])
            cities[city_id] = (country_name, city_name, latitude, longitude)
    return cities
def create_players_and_countries_from_csv(num_players, num_countries_per_player, num_cities_per_country, city_info):
    players = []
    for i in range(num_players):
        player = Player(f"{i + 1}", "")
        for j in range(num_countries_per_player):
            cities = []
            country_name = city_info[(i + 1) * (num_countries_per_player * num_cities_per_country)][0]
            for k in range(num_cities_per_country):
                city_id = i * (num_countries_per_player * num_cities_per_country) + j * num_cities_per_country + k + 1
                city_name = city_info[city_id][1]
                latitude = city_info[city_id][2]
                longitude = city_info[city_id][3]
                city_score = 100 + (10 * k) + (20 * j)
                buildings = [Building(f"Building", 0, 1, {"Supplies": 100,"Components":50}, 1, ["Infantry"], {"Supplies": 50})]
                city = City(city_name, latitude, longitude)
                city.buildings = buildings
                cities.append(city)
            player.assign_country(country_name)
            player.possessed_cities = cities
        players.append(player)
    return players
# Function to calculate building upgrade cost
def get_building_upgrade_cost(building):
    # Assuming upgrade cost increases by 50% for each level
    upgrade_cost_multiplier = 1.5
    current_level = building.level
    upgrade_cost = {resource: int(cost * (upgrade_cost_multiplier ** current_level)) for resource, cost in building.required_resources.items()}
    return upgrade_cost
# Function to create a folium map and plot player coordinates with different colored markers
def plot_players_on_map(players):
    global my_map,custom_js,colors
    # Define colors for markers, one for each player
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
              'lightred']

    # Set the southwest and northeast corners of the map
    southwest = (-8, -180)  # Latitude, Longitude
    northeast = (8, 180)  # Latitude, Longitude
    # Create a folium map centered around a certain location
    my_map = folium.Map(location=[39.9208, 32.8541], zoom_start=2, tiles='OpenStreetMap', min_zoom=2.5 , max_zoom=8, max_bounds=True)
    # Define the bounds for the map
    my_map.fit_bounds([southwest, northeast])
    my_map_name=my_map.get_name()
    print(my_map_name)

    # Plot the players' cities on the map with different colored markers for each player
    for player_idx, player in enumerate(players):
        for city in player.possessed_cities:
            # Here, customize the button labels and onclick functions based on your requirements
            popup_html = f"<div class='popup-container'>"
            popup_html += f"<h3>Player {player_idx}<br>"
            popup_html += f"<b>{city.name}</b> ({player.country_name})</div></h3>"

            # Wrapper for "Building info" and "Unit info" sections
            popup_html += f"<div class='info-wrapper'>"
            popup_html += "<div class='building-info'>"
            for building in city.buildings:
                upgrade_cost = get_building_upgrade_cost(building)
                popup_html += f"<b>{building.name}</b> (Level: {building.level})<br>"
                popup_html += "<b>Upgrade Cost:</b><br>"
                for resource, cost in upgrade_cost.items():
                    popup_html += f"| {resource}: {cost}<br>"
                popup_html += f"<button class='action-btn' onclick='onButtonClicked(event, \"{player.id}\", \"1\", \"{city.latitude}\", \"{city.longitude}\", \"{building.name}\", {building.level})'>Upgrade building</button><br>"
                popup_html += f"<button class='action-btn' onclick='onButtonClicked(event, \"{player.id}\", \"2\", \"{city.latitude}\", \"{city.longitude}\", \"{building.name}\", {building.level})'>Cancel construction</button><br>"
            popup_html += "</div>"

            popup_html += "<div class='unit-info'>"
            popup_html += f"<b>Infantry</b>"
            popup_html += f"</b>(Level: 1)<br>"
            popup_html += "<b>Production Cost:</b><br>"
            popup_html += "| Supplies: 50<br>"
            popup_html += f"<button class='action-btn' onclick='onButtonClicked(event, \"{player.id}\", \"3\", \"{city.latitude}\", \"{city.longitude}\", \"{building.name}\", {building.level})'>Produce Unit</button><br>"
            popup_html += f"<button class='action-btn' onclick='onButtonClicked(event, \"{player.id}\", \"4\", \"{city.latitude}\", \"{city.longitude}\", \"{building.name}\", {building.level})'>Cancel Production</button><br>"
            popup_html += "</div></div></div>"
            player_color = colors[player_idx % len ( colors )]
            marker=folium.Marker(location=[city.latitude, city.longitude], popup=popup_html,
                          icon=folium.Icon(color=player_color)).add_to(my_map)
            print(marker.get_name())

    # Create a custom CSS style for the popup
    custom_css = """
    <style>
    .popup-container {
        font-family: Arial, sans-serif;
        font-size: 8px;
        width: 150px; /* Adjust the width as needed */
        display: flex;
        flex-direction: column;
    }
    .player-city-info {
        font-size: 11px;
        height: 10px; /* Adjust the width as needed */
        margin-bottom: 5px;
    }    
    .info-wrapper {
        display: flex;
        flex-direction: row; /* Arrange Building info and Unit info side by side */
    }
    .building-info, .unit-info {
        display: flex;
        flex-direction: column;
        align-items: flex-start;        
        flex: 1; /* Allow both sections to take equal width */
   
    }
    .building-info button, .unit-info button {
        width: 90%;
    }
    .action-btn {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 12px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 12px;
        margin: 2px;
        cursor: pointer;
        border-radius: 4px;
    }
    </style>
    """

    # Add the custom CSS to the map
    my_map.get_root().html.add_child(folium.Element(custom_css))

    # Create a custom JavaScript function to handle button clicks
    custom_js = """
      <script>
      function onButtonClicked(event,playerId, buttonLabel, cityLatitude, cityLongitude, buildingName, buildingLevel) {
          // Send the city and building information to the Flask server
          fetch('http://127.0.0.1:5000/send-data', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                    'playerId': playerId,
                  'buttonLabel': buttonLabel,
                  'cityLatitude': cityLatitude,
                  'cityLongitude': cityLongitude,
                  'buildingName': buildingName,
                  'buildingLevel': buildingLevel
              })
          })
          .then(response => response.json())
          .then(data => {
              console.log('Data sent successfully:', data);
              // You can add additional code here to handle the server response if needed
          })
          .catch(error => {
              console.error('Error sending data:', error);
          });
      }
      </script>
      """
    # Add the custom JavaScript to the map
    my_map.get_root().html.add_child(folium.Element(custom_js))
    # Save the map to an HTML file
    my_map.save("players_map.html")
# Function to print player information
def print_player_info(player):
    print(f"Player: {player.id}")
    print("Country:", player.country_name)
    print("Cities:")
    for city in player.possessed_cities:
        print(f" - {city.name} (Lat: {city.latitude}, Long: {city.longitude})")
        for building in city.buildings:
            upgrade_cost = get_building_upgrade_cost(building)
            print(f"    - {building.name} (Level: {building.level})")
            print("      Upgrade Cost:")
            for resource, cost in upgrade_cost.items():
                print(f"      - {resource}: {cost}")
    print(f"General Score: {player.general_score}")
    print("-" * 30)
# Path to the CSV file containing city information
csv_filename = "cities_info.csv"
# Read city information from CSV
city_info = read_city_info_from_csv(csv_filename)
if __name__ == "__main__":
    # Create 10 players with 1 country each and 5 cities per country using city_info from CSV

    players = create_players_and_countries_from_csv(num_players=20, num_countries_per_player=1,
                                                  num_cities_per_country=5, city_info=city_info)
    # Call the function to plot the players on the map
    plot_players_on_map(players)
    # Print player information
    for player in players:
        print_player_info(player)
    # Save all player data to a file
    with open("all_players_data.pickle", 'wb') as f:
        pickle.dump(players, f)
    print("All players data saved to all_players_data.pickle")
    # Example of loading all players data from the file
    with open("all_players_data.pickle", 'rb') as f:
        loaded_players = pickle.load(f)
    # Accessing City and Building information
    print(loaded_players[0].possessed_cities[0].buildings[0].name)


    ################################################ experimental zone ####################################
    time.sleep(15)
    # Add a new city for the first player (index 0)
    new_city = City ( "NewCity", 40.0, -80.0 )  # Provide the desired latitude and longitude
    new_building = Building ( "NewBuilding", 0, 1, {"Supplies": 50, "Components": 25}, 1, ["Infantry"],
                              {"Supplies": 25} )
    new_city.buildings = [new_building]
    players[0].possessed_cities.append ( new_city )
    city=new_city
    player_idx = 0
    player = players[0]
    # Here, customize the button labels and onclick functions based on your requirements
    popup_html = f"<div class='popup-container'>"
    popup_html += f"<h3>Player {player_idx}<br>"
    popup_html += f"<b>{city.name}</b> ({player.country_name})</div></h3>"

    # Wrapper for "Building info" and "Unit info" sections
    popup_html += f"<div class='info-wrapper'>"
    popup_html += "<div class='building-info'>"
    for building in city.buildings:
        upgrade_cost = get_building_upgrade_cost ( building )
        popup_html += f"<b>{building.name}</b> (Level: {building.level})<br>"
        popup_html += "<b>Upgrade Cost:</b><br>"
        for resource, cost in upgrade_cost.items ( ):
            popup_html += f"| {resource}: {cost}<br>"
        popup_html += f"<button class='action-btn' onclick='onButtonClicked(event, \"{player.id}\", \"1\", \"{city.latitude}\", \"{city.longitude}\", \"{building.name}\", {building.level})'>Upgrade building</button><br>"
        popup_html += f"<button class='action-btn' onclick='onButtonClicked(event, \"{player.id}\", \"2\", \"{city.latitude}\", \"{city.longitude}\", \"{building.name}\", {building.level})'>Cancel construction</button><br>"
    popup_html += "</div>"

    popup_html += "<div class='unit-info'>"
    popup_html += f"<b>Infantry</b>"
    popup_html += f"</b>(Level: 1)<br>"
    popup_html += "<b>Production Cost:</b><br>"
    popup_html += "| Supplies: 50<br>"
    popup_html += f"<button class='action-btn' onclick='onButtonClicked(event, \"{player.id}\", \"3\", \"{city.latitude}\", \"{city.longitude}\", \"{building.name}\", {building.level})'>Produce Unit</button><br>"
    popup_html += f"<button class='action-btn' onclick='onButtonClicked(event, \"{player.id}\", \"4\", \"{city.latitude}\", \"{city.longitude}\", \"{building.name}\", {building.level})'>Cancel Production</button><br>"
    popup_html += "</div></div></div>"
    player_color = colors[player_idx % len ( colors )]
    marker = folium.Marker ( location=[city.latitude, city.longitude], popup=popup_html,
                             icon=folium.Icon ( color=player_color ) ).add_to ( my_map )
    print ( marker.get_name ( ) )

    my_map.save("players_map.html")
    custom_js = """
        <script>
   
            // Function to update the marker's position
            function updateMarker(lat, lng) {
                marker_name.setLatLng([lat, lng]);
            }
            // Function to get marker position from Flask every 5 seconds
            function getMarkerPosition() {
                fetch('http://127.0.0.1:5000/get_marker_position')
                .then(response => response.json())
                .then(data => {
                    updateMarker(data.lat, data.lng);
                })
                .catch(error => {
                    console.error('Error fetching marker position:', error);
                })
                .finally(() => {
                    setTimeout(getMarkerPosition, 1000); // Call the function again after 5 seconds
                });
            }
        
            // Start getting marker position
            getMarkerPosition();
        </script>
        """

    custom_js = custom_js.replace ( "my_map_name", my_map.get_name ( ) )

    custom_js = custom_js.replace ( "marker_name", marker.get_name ( ) )
    print ( my_map.get_name ( ) )
    my_map.get_root ( ).html.add_child ( folium.Element ( custom_js ) , index=1)

    my_map.save ( "players_map.html" )
    print (     my_map.__getstate__() )
    # Call the function to plot the players on the map
    #plot_players_on_map(players)

