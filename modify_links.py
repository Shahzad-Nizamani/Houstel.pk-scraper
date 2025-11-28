import json

def modify_links():
    with open("links.json", 'r') as f:
        data = json.load(f)

    for city in data.keys():
        urls = []

        for link in data[city]:
            url = ""
            if "--" in link:
                url = link.replace("--", "-")
                urls.append(url)
            else:
                urls.append(link)
            
        data[city] = urls
    
    with open("links.json", 'w') as f:
        json.dump(data, f, indent=4)
    
    return data