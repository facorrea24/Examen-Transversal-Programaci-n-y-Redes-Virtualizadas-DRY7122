import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "b844056c-60c8-41a7-b7d6-d1073ae6f6c7"

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    if json_status == 200:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        new_loc = name
        if state:
            new_loc += ", " + state
        if country:
            new_loc += ", " + country

        print(f"Geocoding API URL for {new_loc} (Location Type: {value})\n{url}")

    else:
        lat = "null"
        lng = "null"
        new_loc = location
    
    return json_status, lat, lng, new_loc

while True:
    loc1 = input("Ciudad de inicio: ")
    if loc1.lower() in ["salir", "s"]:
        break
    
    orig = geocoding(loc1, key)
    print(orig)
    
    loc2 = input("Ciudad de destino: ")
    if loc2.lower() in ["salir", "s"]:
        break
    
    dest = geocoding(loc2, key)

    print("=================================================")
    print("Seleccione el medio de transporte:")
    print("1. Auto")
    print("2. Bus")
    print("3. Avión")
    transport_option = input("Ingrese una opción: ")

    transport_dict = {
        "1": "car",
        "2": "bus",
        "3": "airplane"
    }
    
    vehicle_type = transport_dict.get(transport_option, "car")

    print("=================================================")
    
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        vehicle = "&vehicle=" + vehicle_type
        paths_url = route_url + urllib.parse.urlencode({"key": key}) + op + dp + vehicle
        paths_response = requests.get(paths_url)
        paths_status = paths_response.status_code
        paths_data = paths_response.json()
        
        print(f"Routing API Status: {paths_status}\nRouting API URL:\n{paths_url}")
        print("=================================================")
        print(f"Direcciones de {orig[3]} a {dest[3]}")
        print("=================================================")
        
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print(f"Distancia Recorrida: {miles:.1f} miles / {km:.1f} km")
            print(f"Duracion del viaje: {hr:02d}:{min:02d}:{sec:02d}")
            print("=================================================")
        else:
            print("Error en la solicitud de la ruta.")
    else:
        print("Error en la geocodificación de una o ambas ubicaciones.")