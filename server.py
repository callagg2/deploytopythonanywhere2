# author: Gerry Callaghan

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
@app.route("/", methods=["GET"]) # this is just some onscreen message that is used to map the URL "/" to the function index() and specify that it should only respond to GET requests.
def index():
    # This sends the user to the home page - index.html
    return app.send_static_file("index.html")

    # To retrieve or get all the routes on the server
@app.route("/routes", methods=["GET"]) # I'm mapping the URL "/routes" to the function get_all_routes() and specifying that it should only respond to GET requests. 
    # When a client sends a GET request to "/routes", the get_all_routes() function queries a database to retrieve the list of routes 
    # and returns that data in the JSON response.
def get_all_routes():
    #return jsonify({"message": "List of routes"}) # used only for testing the endpoint
    # I can use either Postman (GET request) or run the curl command: "curl http://127.0.0.1:5000/routes" to test this endpoint "/routes"
    return jsonify(routeDAO.get_all_routes())


    # To find a specific record by passing in its id
@app.route("/routes/<int:id>", methods=["GET"]) # I'm mapping the URL "/routes/<int:id>" to the function find_route_by_id() 
    # and specifying that it should only respond to GET requests. The <int:id> part of the URL is a variable that will be passed to the function as an argument. 
    # When a client sends a GET request to "/routes/1", for example, 
    # the find_route_by_id() function will be called with id set to 1. 
    # Here, the function queries the database and retrieves the details for the route with the specified ID and return that data in the JSON response.
def find_route_by_id(id):
    #return jsonify(f"Details for route with ID {id}") # used only for testing the endpoint
    # I can use either Postman (GET request) or run the curl command: "curl http://127.0.0.1:5000/routes/1" to test this endpoint "/routes"

    route = jsonify(routeDAO.find_route_by_id(id)) # this will call the find_route_by_id() function
    if route:
        return route
    else:
        return jsonify({"message": f"Route with ID {id} not found"}), 404 # this will return a JSON response with a message indicating that the route was not found, and a 404 status code to indicate that the resource was not found.   


    # To create a new record on the server
@app.route("/routes", methods=["POST"]) # I'm mapping the URL "/routes" to the function create_route() 
    #and specifying that it should only respond to POST requests. 
def create_route():
    jsonstring = request.json  # this is the data that is to be sent up to my server in the body of the request, 
    # it will be a JSON string contains the information for the new record
    
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
    
    #return jsonify({"message": "Route created", "data": jsonstring})
    # I can use either Postman (POST request) or run the curl command: "curl -X POST -d "{\"destination\":\"Sallygap\", \"route_map\":\"some map\",\"distance\":110,,\"elevation\":800}" http://127.0.0.1:5000/routes" to test this endpoint "/routes"

    return jsonify(routeDAO.create_route(route))

    # To update a route on the server
@app.route("/routes/<int:id>", methods=["PUT"]) # I'm mapping the URL "/routes/<int:id>" to the function update_route() 
    # and specifying that it should only respond to PUT requests. The <int:id> part of the URL is a variable that will be passed to the function as an argument. 
    # When a client sends a PUT request to "/routes/1", the update_route() function will be called with id set to 1. 
def update_route(id):
    jsonstring = request.json # this is the data that is sent in the body of the request, it will be a JSON string that contains the updated information
    route = {}
    if "destination" in jsonstring:
        route["destination"] = jsonstring["destination"]

    if "route_map" in jsonstring:
        route["route_map"] = jsonstring["route_map"]

    if "distance" in jsonstring:
        route["distance"] = jsonstring["distance"]

    if "elevation" in jsonstring:
        route["elevation"] = jsonstring["elevation"]

    #return f"update {id} {jsonstring}"
    #I can use either Postman (PUT request) or run the curl command: "curl -X PUT -d "{\"destination\":\"Sallygap\", \"route_map\":\"some map\",\"distance\":110,,\"elevation\":800}" http://127.0.0.1:5000/routes/1" to test this endpoint "/routes/id"

    return jsonify(routeDAO.update_route(id, route))

    # To delete a record from the server
@app.route("/routes/<int:id>", methods=["DELETE"]) #I'm mapping the URL "/routes/<int:id>" to the function delete_route() 
    #and specifying that it should only respond to DELETE requests. The <int:id> part of the URL is a variable that will be passed to the function as an argument. 
    # When a client sends a DELETE request to "/routes/1", for example, the delete_route() function will be called with route_id set to 1. 
def delete_route(id):
     
    #return "delete"
    # I can use either Postman (DELETE request) or run the curl command: "curl -X DELETE http://127.0.0.1:5000/routes/1" to test this endpoint "/routes/id"

    return jsonify(routeDAO.delete_route(id)) 


@app.route("/invalid", methods=["GET"]) # I'm mapping the URL "/invalid" to the function revert_to_index() and specifying that it should only respond to GET requests. 
    # When a client sends a GET request to "/invalid", the revert_to_index() function will be called. 
    # In this example, the function uses redirect() and url_for() to redirect the user to the index (home) page when they access the /invalid endpoint. 
    # The url_for("index") function generates the URL for the index() function, which is mapped to the root URL ("/"). So when a user accesses "/invalid", they will be redirected to "/".
def revert_to_index():
    return redirect(url_for("index")) # this will redirect the user to the index (home) page when they access the /invalid endpoint


@app.errorhandler(404)
    # This is a custom error handler for 404 errors (page not found). When a user tries to access a URL that does not exist on the server, this function will be called. 
    # It will redirect the user back to the index page instead of showing a 404 error message
def page_not_found(e):
    # This captures any invalid URL and sends the user back to the index
    return redirect(url_for("index"))


# this is to run the flask app, the debug=True parameter is used to enable debug mode, 
# which allows for easier debugging and automatic reloading of the server when code changes are made. 
if __name__ == '__main__':
    app.run(debug=True)
