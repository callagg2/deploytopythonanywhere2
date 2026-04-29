#author: Gerry Callaghan 


from urllib import response
import json
import requests


def findbyid(id):
    try:
        geturl = (url + "/" + str(id))
        response = requests.get(geturl)
        route_list = response.json()
        
        route_destination = (route_list['destination'])
        route_map = (route_list['route_map'])
        route_distance = (route_list['distance'])
        route_elevation = (route_list['elevation'])
        
        print_message=(f"The route to {route_destination} with the map {route_map}, distance {route_distance} and elevation {route_elevation} is found.")
    except requests.RequestException:
        print_message=(f"Error occurred: Route with id {id} not found.")
    
    return print_message


def createroute(newroute):
    # add the new route
    response = requests.post(url,json=newroute)
    
    # check if the route was successfully added 
    try:
        response = requests.get(url)
        response.raise_for_status()
        new_route_list = response.json()
        for route in new_route_list:
            last_route_added = (route['destination'])
            
        if last_route_added == newroute['destination']:
            print_message =(f"{newroute['destination']} with the map {newroute['route_map']} was added successfully") 
        else:
            print_message =(f"{newroute['destination']} with the map {newroute['route_map']} was not added successfully")
    except requests.exceptions.RequestException as e:
        print_message =(f"Error occurred: {e}") 
    
    return print_message

def readroutes():
    response = requests.get(url)
    print(response.status_code) # check for status code
    return response.json()


def updateroute(id,routediff):
    puturl = url + "/" + str(id)
    response = requests.put(puturl, json=routediff)
    
    # check if the update was successful 
    try:
        response = requests.get(puturl)
        response.raise_for_status()
        updated_route_list = response.json()
        print_message =(f"{updated_route_list['destination']} with the {updated_route_list['route_map']} was updated successfully") 
    except requests.exceptions.RequestException:
        print_message =(f"Error occurred: Route with id: {id} not found. Update failed.") 
    
    return print_message


def deleteroute(id):
    geturl = (url + "/" + str(id))
    response = requests.get(geturl)
    route_to_be_deleted = response.json()
    print(f"Route to be deleted: {route_to_be_deleted}")
    
    # Now we delete that route
    deleteurl = url + "/" + str(id)
    response = requests.delete(deleteurl)

    # check if the delete was successful (gemini helped here https://gemini.google.com/share/1e0dfbb28400)
    try:
        geturl = (url + "/" + str(id))
        response = requests.get(geturl)
        response.raise_for_status()
        print_message =(f"{route_to_be_deleted} was not deleted successfully") 
    except requests.exceptions.RequestException as e:
        print_message =(f"{route_to_be_deleted} was deleted successfully") 
    
    return print_message    


if __name__ == "__main__":

    url = "https://andrewbeatty1.pythonanywhere.com/books"
    id = 1728
    newbook = {
        'author': 'Joe Smith', 
        'id': 1677, 
        'price': 20, 
        'title': 'New Book'
        }
    bookdiff = {
        'author': 'Mary-Jane Doe', 
        'price': 14, 
        'title': 'Yet Another Book'
        }

    #print(readroutes())
    #print(createroute(newbook))
    #print(findbyid(id))
    #print(updateroute(id, bookdiff))
    #print(deleteroute(id))

