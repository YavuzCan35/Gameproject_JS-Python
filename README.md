# Gameproject_JS-HTML-CSS-PythonFlask
World map splitted in to countries. Each player will lead a country create buildings and units to compete and fight with each other.


	python-flask will be the serverside computing center and html , js & css for user side interactions and visuals.


	Every country will have certain amount of main cities to build and borders for each of these cities.

	Cities will have certain buildings to produce units.

	Units needs to move on the map and coordinates must be updated frequently.

	Leaflet map can be tweaked for visual side. Shout out to leaflet team for their amazing work.

	HTML page is gonna be used for a browser side.



1) geoptry.py creates turkey_map.html 


		with 5 city plotted on the map 
	
		with build, produce unit and cancel options

2)app.py runs as flask server and listens send-data node for interaction such as build

example message recived on flask side app.py

	127.0.0.1 - - [23/Feb/2024 12:51:42] "POST /send-data HTTP/1.1" 200 -
	{'cityName': 'Ankara', 'info': 'build'}
	Received data from the client
	127.0.0.1 - - [23/Feb/2024 12:51:43] "OPTIONS /send-data HTTP/1.1" 200 -
	127.0.0.1 - - [23/Feb/2024 12:51:43] "POST /send-data HTTP/1.1" 200 -
	{'cityName': 'Ankara', 'info': 'produce'}
	Received data from the client
	127.0.0.1 - - [23/Feb/2024 12:51:43] "OPTIONS /send-data HTTP/1.1" 200 -
	127.0.0.1 - - [23/Feb/2024 12:51:43] "POST /send-data HTTP/1.1" 200 -
	{'cityName': 'Ankara', 'info': 'cancel'}
	Received data from the client
 

returned confirmation to html site console:

	turkey_map.html:48 Fetch finished loading: POST "http://127.0.0.1:5000/send-data".
	onClickButton @ turkey_map.html:48
	onclick @ turkey_map.html:227
	turkey_map.html:57 Data sent successfully: {message: 'Data received successfully'}

3)maindata.py ( creates all_players_data.pickle and players_map.html)

	cities_info.csv contains info for cities and countries location and name
	gets information from csv file for countries and ciry loactiions (filename is parameter to locate data)
	creates buildings and costs in the city.building array
	creates players by assigning countries to them(1 country per player usually):
		assigning number to the player
			then for each country:
				get cities:
					calculate city id(unique 1 to 872 ish, all cities ) index in the csv
					gets the city name,latitude,longitude and city_score(not yet used, future mechanics)
					assigns to an array : buildings and productable units as name_building,cost_building,unit_type and unit_cost
						building if not in construction 0(otherwise 1)
						building level (1 as initial building level)
					finilize the city with City(name,lat,long)
					append citty to cities
		append country to player
		append cities to player(cities are appended to player directly because when another city acquired from another player, then city will change ownership of players)
		player is appended to all players
	return all players
	
	limits maxed zoomed out view and over extended iterations to sides
	creates the map with a layer

	plots player on map
		popup containers
			for cities of players
				city_names, building information, upgrade costs with new upgrade costs
			unit info like cost etc ( building costs should change when level has changed.but units is static for now)

	CSS make up for buttons and boxes

	custom_js adds the dynamic events to communicate with flask when button clicked(sends button label and additional info but this info can stay on only server side and changed with the command from server instead of being sent from player to server to prevent cheating)

map.get_name() for exact map element name or map._name map._id and marker.get_name()
