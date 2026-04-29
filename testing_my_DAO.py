
# author: gerry Callaghan

from DAO import routeDAO
import mysql.connector
from testing_dbconfig import config_details

route = {
    "id":"1",
    "destination": "test",
    "route_map": "some map",
    "distance": 130,
    "elevation": 900
}


# To test the create_route() function, we can run the following code:
route = routeDAO.create_route(route)
routeid = route["id"] # this is the id of the newly created route record, which I can use to test the other functions that require an id as an argument

# To test the get_all_routes() function, we can run the following code:
routes = routeDAO.get_all_routes()
print(f"\ntest get all routes:", routes) # returns a list of dict objects, each dict represents a route record in the database, with the keys being the column names and the values being the corresponding values for that record.

# To test the find_route_by_id() function, we can run the following code:
result= routeDAO.find_route_by_id(routeid)
print(f"\ntest create and find by id:", route) # returns a dict object representing the route record with the specified id in the routeid = route["id"] above, with the keys being the column names and the values being the corresponding values for that record.

# To test the update_route() function, we can run the following code:
updated_route = {   
    "destination": "updated test",
    "route_map": "some other map",
    "distance": 456,
    "elevation": 789
    }            
result = routeDAO.update_route(routeid, updated_route)
original_route = result[1] # we can return the route before it was updated
#print(f"\ntest update route: 1 record updated, ID: {routeid}, Destination: {result['destination']}, Route Map: {result['route_map']}, Distance: {result['distance']}, Elevation: {result['elevation']}", result) # returns a dict object representing the updated route record, with the keys being the column names and the values being the corresponding values for that record. The id key will still be the same as the original route, but the other keys will have the updated values.
print(f"\ntest update route: 1 record updated", "\noriginal route:", original_route, "\nupdated route:", result[0]) # returns a dict object representing the updated route record, with the keys being the column names and the values being the corresponding values for that record. The id key will still be the same as the original route, but the other keys will have the updated values.

# To test the delete_route() function, we can run the following code:
result = routeDAO.delete_route(routeid)
route_to_be_deleted= result[1] # we can return the route that was just deleted, so that we can see what was deleted in the test output
print(f"\ntest delete route: 1 record deleted", route_to_be_deleted, ", Deleted:", result[0]) # returns a boolean value indicating whether the delete operation was successful or not. If the route with the specified id was successfully deleted, it will return True, otherwise it will return False.

    