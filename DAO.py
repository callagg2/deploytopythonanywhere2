# a simple DAO for a database that does CRUD operations on a cycling routes table
# author: Gerry Callaghan
# student number G00472971

import mysql.connector
import urllib.parse # this might be needed to parse the route URL 
#from testing_dbconfig import config_details
from dbconfig_pythonanywhere import config_details


class RouteDAO: 

        # rather than save my personal details in the python file, 
        # i'm going to pull them in from a config file
    host = config_details['host']
    user = config_details['user']
    password = config_details['password']
    database = config_details['database']
    connection = ""
    cursor = ""

        # this how i initialise my cursor, I send it the loing details to the database 
    def get_cursor(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor

        # I'm closing the cursor and connection after i've finished with them so as to release the connections
    def close_all(self):
        self.cursor.close()
        self.connection.close()


        # this function add new cycling routes by sending SQL commands to a database
    def create_route(self, route):
        mycursor = self.get_cursor()# this creates a connection to the database and return a cursor object that we can use to execute SQL commands

        try: # it is possible that we could run into errors so i include error handling
            sql = "Insert into routes_table (destination, route_map, distance, elevation) values (%s, %s,%s, %s)"
            values = (route.get("destination"), route.get("route_map"), route.get("distance"),route.get("elevation")) # .get(" ") pulls the title, author, and price FROM the dictionary object 
             # which is the format it is stored in the database. If not set, get() will return None for the variable
       
            mycursor.execute(sql, values) # this passes the sql string and the values tuple to the execute function, which will insert the new record into the database. 
            # The %s in the sql string are placeholders for the values that will be passed in the values tuple. This is a common way to prevent SQL injection attacks, 
            # because it ensures that the values are properly escaped before being inserted into the database.

            self.connection.commit() # this is necessary to save the changes to the database, 
            route["id"] = mycursor.lastrowid # we can NOW add the id to the route dictionary object that was passed in
        
        except Exception as e:
            print("Error creating a routes", e)
            return None
        except mysql.connector.errors.InternalError as e:
            print(f"Database error: {e}")
            return None
        except mysql.connector.errors.IntegrityError as e:
            print(f"\nRoute format not valid, error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        
        self.close_all() 
        return route


        # the function get all routes from a database by sending SQL commands to a database
    def get_all_routes(self):
        mycursor = self.get_cursor()

        try: # it is possible that we could run into errors so i include error handling
            sql = "Select * from routes_table Order by destination, id" # this will select all records from the routes_table and order them in ascending order by destination then id 
        
            mycursor.execute(sql) 
            results = mycursor.fetchall() # this will return all records from the database as a list of tuples

            if results:
                #print(results)
                route_list = []
                for result in results:
                    route_list.append(self.convert_to_dict(result)) # this convert each tuple in the results list to a dictionary object using the convert_to_dict() function 
            else:
                print(f"A list of routes could not be found")
        except Exception as e:
            print("Error finding a list of routes", e)
            return None
        except mysql.connector.errors.InternalError as e:
            print(f"Database error: {e}")
            return None
        except mysql.connector.errors.IntegrityError as e:
            print(f"\nRoutes format not valid, error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
  
        self.close_all()
        return route_list


        # this function finds a route by its id by sending SQL to a database
    def find_route_by_id(self, id):
        mycursor = self.get_cursor()
        route_found = None

        try: # it is possible that we cannot find the id so we need error handling
            sql = "Select * from routes_table where id = %s"
            values = (id,)
            mycursor.execute(sql, values) # this passes the sql string and the values tuple to the execute function, which will insert the new record into the database. 
            
            results = mycursor.fetchone() # this will return a single record from the database that matches the specified id, as a tuple. 
           
            if results:
                #print(results)
                route_found = self.convert_to_dict(results) # this will convert the tuple returned by fetchone() to a dictionary object
            else:
                print(f"Route with ID: {id} not found")
        except Exception as e:
            print("Error finding route by id:", e)
            return None
        except mysql.connector.errors.InternalError as e:
            print(f"Database error: {e}")
            return None
        except mysql.connector.errors.IntegrityError as e:
            print(f"\nID: {id} is not valid, it must be an integer, error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None       

        self.close_all()
        return route_found


        # This function edits/updates a route by passing the new details in a SQL request to a database
    def update_route(self, id, route):
        route_to_be_updated= self.find_route_by_id(id) # this captures the original details of the route

        mycursor = self.get_cursor()
        
        try: # just more error handling
            sql = "Update routes_table set destination = %s, route_map = %s, distance = %s, elevation = %s where id = %s"
            values = (route.get("destination"), route.get("route_map"), route.get("distance"),route.get("elevation"),id) # use .get(" ")to get the title, author, and price out of the dictionary object. If not set, get will return None
        
            mycursor.execute(sql, values) # this passes the sql string and the values tuple to the execute function
            self.connection.commit() # this is necessary to save the update to the database, if you don't call commit, the changes will not be saved and will be lost when the connection is closed.
            #updated_id = mycursor.lastrowid#
            #print("1 record updated, ID:", routeid, "new route details are:", route.get("destination"), route.get("route_map"), route.get("distance"), route.get("elevation")) # this is for testing and prints the id of the record that was updated 
            # so you know you updated the correct record

        except Exception as e:
            print("Error updating route", e)
            return None
        except mysql.connector.errors.InternalError as e:
            print(f"Database error: {e}")
            return None
        except mysql.connector.errors.IntegrityError as e:
            print(f"\nRoute details are not valid, error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None       
 

        self.close_all()
        return route, route_to_be_updated # we return the route that was just updated, so that we can see what was updated in the test output, 
        # and also return the original route before it was updated, so that we can see the difference in the test output

        # this function deletes a route by passing an SQL request to a database 
    def delete_route(self, id):
        route_to_be_deleted= self.find_route_by_id(id) # this captures the original details of the route

        if route_to_be_deleted is None: # if the route doesn't exist
            return None # Exit early and not crash

        mycursor = self.get_cursor()

        try: 
            sql = "Delete from routes_table where id = %s"
            values = (id,)
        
            mycursor.execute(sql, values) # this passes the sql string and the values tuple to the execute function
            self.connection.commit() # this is necessary to save the deletion to the database, 
            #print("1 record deleted") # this is for testing and print a message to confirm that the record was deleted, so you know the delete operation was successful.
        
        except Exception as e:
            print("Error deleting route", e)
            return None
        except mysql.connector.errors.InternalError as e:
            print(f"Database error: {e}")
            return None
        except mysql.connector.errors.IntegrityError as e:
            print(f"\nRoute cannot be deleted, error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None 

        self.close_all()
        return route_to_be_deleted # we can return the route that was just deleted, so that we can see what was deleted

        # the following functions converts tuples to a dictionary object (SQL returns tuples but we want dict objects)
    def convert_to_dict(self, resultline):   
        routekeys = ["id", "destination", "route_map", "distance", "elevation"]
        current_key = 0
        route = {} 
        for attrib in resultline: # for each attribute in the tuple, add a key value pair to the route dictionary object, 
            # where the key is the corresponding column name from the routekeys list, and the value is the attribute from the tuple.
            route[routekeys[current_key]] = attrib  
            # First time through the loop, current_key will be 0, so the key will be "id" and the value will be the first attribute in the tuple (which is the id of the route).
            # second time through the loop, current_key will be 1, so the key will be "destination" and so on
            current_key += 1
        return route
        

routeDAO = RouteDAO() # make an instance of the DAO class to use again
