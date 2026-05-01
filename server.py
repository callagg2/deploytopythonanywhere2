# A simple Flask API server that will allow CRUD operations
# author: Gerry Callaghan
# student number G00472971

from flask import Flask, request, jsonify, redirect, url_for, abort 
from DAO import routeDAO

    # this command is used to initialize a flask app called app. 
    # The first argument is the name of the module or package that is being run, I've just left it as the default. 
    # The static_url_path is used to specify the URL path that will be used to access static files, 
    # I'm leaving it blank and the program will find them itself 
    # The the static files such as the HTML, CSS, and JavaScript files used for the front end 
    # are in a folder called "staticpages" and can be accessed at the root URL ("/").
app = Flask(__name__,static_url_path="", static_folder="staticpages")


    # When you are at the root URL ("/"), the function index() is called.
@app.route("/", methods=["GET"]) 
def index():
    return app.send_static_file("index.html") # This sends the user to the home page - index.html

    # To get all the routes from the database, map the URL "/routes" to the function get_all_routes() and specify that it should only respond to GET requests
@app.route("/routes", methods=["GET"]) # I'm . 
    
def get_all_routes():
    #return jsonify({"message": "List of routes"}) # this is used only for testing the endpoint in production
    # I can use either Postman (GET request) or run the curl command: "curl http://127.0.0.1:5000/routes" to test this endpoint "/routes"
    return jsonify(routeDAO.get_all_routes()) # we jsonify the dict object returned via the DAO


    # To find a specific record by passing in its id, map the URL "/routes/<int:id>" to this function and specify it should only respond to GET requests.
@app.route("/routes/<int:id>", methods=["GET"]) 
     
    # Here, the function queries the database and retrieves the details for the route with the specified ID and return that data in the JSON response.
def find_route_by_id(id):
    #return jsonify(f"Details for route with ID {id}") # used only for testing the endpoint
    # I can use either Postman (GET request) or run the curl command: "curl http://127.0.0.1:5000/routes/1" to test this endpoint "/routes/1" where 1 is route 1.

    route = jsonify(routeDAO.find_route_by_id(id)) # this assigns the jsonified dict object to a variable route

    if route: # if one exists
        return route
    else:
        return jsonify({"message": f"Route with ID {id} not found"}), 404 # this will return a JSON response with a message indicating that the route was not found, 
        # and a 404 status code to indicate that the resource was not found.   


    # To create a new route in the database, map the URL "/routes" to the function create_route() and specify that it should only respond to POST requests. 
@app.route("/routes", methods=["POST"]) 
    

def create_route():
    jsonstring = request.json  # this is the JSON string contains the information to be sent up to my server in the body of the request, 
    
    # Because it's possible that not all fields are provided, I'm checking for that and return an error if necessary
    # perhaps put the following code in a separate function to validate the input and return an error message if any required fields are missing
    # here is a list of error codes: - https://www.w3schools.com/tags/ref_httpmessages.asp
    # I've gone for 409 Conflict 	The request could not be completed because of a conflict in the request, insuficient data, or a logical error. 
    # This code is used in situations where the user might be able to resolve the conflict and resubmit the request. 
    route = {}
    if "destination" not in jsonstring:  # if destination is missing, return a 409 error
        abort(409)
    route["destination"] = jsonstring["destination"]

    if "route_map" not in jsonstring:  # if "route_map" in jsonstring else abort(409)
        abort(409)
    route["route_map"] = jsonstring["route_map"]

    if "distance" not in jsonstring:  # if "distance" in jsonstring else abort(409)
        abort(409)
    route["distance"] = jsonstring["distance"]

    if "elevation" not in jsonstring:  # if "elevation" in jsonstring else abort(409)
        abort(409)
    route["elevation"] = jsonstring["elevation"]
    
    #return jsonify({"message": "Route created", "data": jsonstring}) # this is for testing in production
    # I can use either Postman (POST request) or run the curl command: "curl -X POST -d "{\"destination\":\"Sallygap\", \"route_map\":\"some map\",\"distance\":110,,\"elevation\":800}" http://127.0.0.1:5000/routes" to test this endpoint "/routes"

    return jsonify(routeDAO.create_route(route))


    # To update/edit a route on the database, map the URL "/routes/<int:id>" to the function update_route() and specify it should only respond to PUT requests.
@app.route("/routes/<int:id>", methods=["PUT"]) # I'm 
    
def update_route(id):
    jsonstring = request.json # this is the data that is sent in the body of the request, it will be a JSON string that contains the updated information
    route = {}
    # unlike in the case for a NEW route where every field should be filled, here only new information is needed, we can leave fields as they are 
    if "destination" in jsonstring:
        route["destination"] = jsonstring["destination"]

    if "route_map" in jsonstring:
        route["route_map"] = jsonstring["route_map"]

    if "distance" in jsonstring:
        route["distance"] = jsonstring["distance"]

    if "elevation" in jsonstring:
        route["elevation"] = jsonstring["elevation"]

    #return f"update {id} {jsonstring}" # to be used for testing in production
    #I can use either Postman (PUT request) or run the curl command: "curl -X PUT -d "{\"destination\":\"Sallygap\", \"route_map\":\"some map\",\"distance\":60,,\"elevation\":800}" http://127.0.0.1:5000/routes/1" to test this endpoint "/routes/id"

    return jsonify(routeDAO.update_route(id, route))


    # To delete a record from the database, map the URL "/routes/<int:id>" to the function delete_route() and specify that it should only respond to DELETE requests
@app.route("/routes/<int:id>", methods=["DELETE"]) 
    
def delete_route(id):
    #return "delete" # to be used for testing in production
    # I can use either Postman (DELETE request) or run the curl command: "curl -X DELETE http://127.0.0.1:5000/routes/1" to test this endpoint "/routes/id"

    return jsonify(routeDAO.delete_route(id)) 

    # I want a function to map the URL "/invalid" to the function revert_to_index(), if the user accesses the /invalid endpoint 
@app.route("/invalid", methods=["GET"]) 
    
def revert_to_index():
    return redirect(url_for("index")) 

    # similar to invalid above, except This is a custom error handler for 404 errors (page not found), it redirect the user back to the index page
@app.errorhandler(404)

def page_not_found(e):
   
    return redirect(url_for("index"))


# this is to run the flask app, the debug=True parameter is used to enable debug mode, 
# which allows for easier debugging and automatic reloading of the server when code changes are made. 
if __name__ == '__main__':
    app.run(debug=True)
