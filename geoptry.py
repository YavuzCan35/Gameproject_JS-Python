import folium
import requests
import pandas as pd
# Dummy data for example purposes
data = {
    'City': ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya'],
    'Latitude': [41.0082, 39.9334, 38.4192, 40.1826, 36.8969],
    'Longitude': [28.9784, 32.8597, 27.1287, 29.0669, 30.7133],
}

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)

# Create a folium map centered around Turkey
turkey_map = folium.Map(location=[39.9208, 32.8541], zoom_start=6)


# Function to handle button click
def on_button_click(event, info):
    city_name = event.target.value
    # Here, you can add your code to send the city_name and info to the server
    url = 'http://127.0.0.1:5000/send-data'
    payload = {'cityName': city_name, 'info': info}
    response = requests.post(url, json=payload)
    print(response.json())


# Add markers with buttons for the cities
for index, row in df.iterrows():
    # Create a button HTML element for each info
    button_html_info1 = f'<button type="button" value="{row["City"]}" onclick="onClickButton(event, \'build\')">Build</button>'
    button_html_info2 = f'<button type="button" value="{row["City"]}" onclick="onClickButton(event, \'produce\')">Produce unit</button>'
    button_html_info3 = f'<button type="button" value="{row["City"]}" onclick="onClickButton(event, \'cancel\')">Cancel</button>'

    # Create a marker with popup containing the buttons
    popup_content = f"{row['City']}<br>{button_html_info1}{button_html_info2}{button_html_info3}"
    marker = folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_content,
        icon=folium.Icon(color='blue')
    )
    marker.add_to(turkey_map)

# Create a custom JavaScript function for button click event
custom_js = """
<script>
function onClickButton(event, info) {
    // Get the value (city name) from the button
    var cityName = event.target.value;

    // Send the cityName and info to the Flask server
    fetch('http://127.0.0.1:5000/send-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'cityName': cityName, 'info': info })
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
turkey_map.get_root().html.add_child(folium.Element(custom_js))

# Display the map
turkey_map.save('turkey_map.html')  # Save the interactive map to an HTML file
