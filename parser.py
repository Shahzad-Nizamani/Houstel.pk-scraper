import requests 
from bs4 import BeautifulSoup
import json

def get_data():

    with open("links.json", 'r') as f:
        urls =json.load(f)
    
    hostels = {
        "hostels" : []
    }

    for city in urls.keys():

        for url in urls[city]:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            if response.status_code != 200:
                print("❌ Failed:", url, "Status:", response.status_code)
                continue

            sample_hostel = soup.find("div", "mt-2")
            if not sample_hostel:
                hostel = {}

                h_name = soup.find("h1", "hostel-title").text.split('|')
                h_name = h_name[0].strip()
                hostel["name"] = h_name
                print(h_name)

                owner_name = soup.find("div", "host-name").text.split('y')
                owner_name = owner_name[1].strip()
                hostel["owner_name"] = owner_name
                print(owner_name)

                location = soup.find("div", "info-item").text.split("in")

                gender = location[0].split()
                gender = gender[1].strip()
                hostel["gender"] = gender
                print(gender)

                location = location[1].strip()
                print(location)

                price_details = "\n\nROOMS AND PRICE DETAILS: \n\n" 
                description = soup.find("div", id="description-content").text.strip()
                hostel["description"] = description + price_details

                try:
                    room = soup.find("div", "room-header-row").text
                    room = room.strip()
                    room = room.split("Floor")
                    price = room[1].split("Rs.")[1]
                    price = price.split('/')[0].replace(',', "").strip()
                    hostel["price"] = price
                except Exception as e:
                    print(e)
                    
                print(price)

                all_rooms = soup.find_all("div", "room-content")

                for card in all_rooms:
                  try:
                    room = card.find("div", "room-header-row").text
                    room = room.strip()
                    
                    if "floor" in room:
                        room = room.split("floor")
                    else:
                       room = room.split("Floor")

                  except Exception as e:
                   print(e)
                  
                  p = card.find("span", "price-amount-small").text + "\n"
                  room = room[0] + "Floor = "
                  rent = room + p
                  hostel["description"] += rent

                print(hostel["description"])
                
                hostel["phone"] = "+923463789314"
                hostel["city"] = city

                hostels["hostels"].append(hostel)

                print(len(hostels["hostels"]))
    
    with open("hostels.json", 'w') as f:
        json.dump(hostels, f, indent=4)

get_data()