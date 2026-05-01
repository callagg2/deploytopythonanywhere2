const url = "/routes";
let routes = [];

function getAllRoutes() {
  // Fetch() allows you to send and receive data from a server asynchronously without reloading the page thereby performing AJAX (Asynchronous JavaScript and XML) operations
  // it is the modern standard built into browsers and therefore generally preferred over older jQuery AJAX methods (Gemini).
  fetch(url)
    .then(response => response.json())
    .then(data => _displayRoutes(data))
    .catch(error => console.error("Unable to get all routes.", error));
}



// this function is the front end of the find_route_by_ID function in the DAO and the Flask API server, 
// it is called when the user clicks on the search button, 
// it takes the ID input from the search box (that is populates theform in the search modal) 
// and sends a GET request to the Flask API server with the id as a parameter
//and receives the route data in JSON format, 
// then it calls the _displayRoutes function to display the search result in the table
function find_route_by_id() {
  const idInput = document.getElementById("search-id");
  const id = idInput.value.trim();

  fetch(`${url}/${id}`)
    .then(response => {
      if (!response.ok) throw new Error("Route not found"); 
      return response.json();
    })
    .then(data => {
      _displayRoutes([data]);
      $('#searchRouteModal').modal('hide'); // Close popup search box on success
    })
    .catch(error => {
      console.error("Unable to find that route.", error); // Log the error in Console for debugging purposes - only for production    
      document.getElementById("error-message-text").innerText = `A route with ID "${id}" does not exist.`; // Display a user-friendly error message to user
      
      $('#searchRouteModal').modal('hide'); // Close popup search box 
      $('#searchErrorModal').modal('show'); // Replace closed popup search box with error message modal to inform user of the issue

      idInput.value = ""; // Clear the search input field after the search attempt, so a re-try can be made
    });

  return false; 
}

// this function outlines what the search button comprises and how it works, 
function findRouteForm(id) {
  const item = routes.find(item => item.id === id);
  document.getElementById("find-id").value = item.id;
}

$('#searchRouteModal').on('show.bs.modal', function () {
  document.getElementById("search-id").value = "";
});

// this function is called by the _displayRoutes function to add the blue (#xE8B6) search button to the table,
function _displayfindroute(data) {

  data.forEach(item => {
    let searchButton = document.createElement("a"); // create a button element to be used for the search button in the table
    searchButton.href = "#searchRouteModal"; // set the href attribute of the search button to the id of the modal that will be used to display the search results
    searchButton.className = "search"; // set the class name of the search button to "search" for styling purposes
    searchButton.setAttribute("onclick", `findRouteForm(${item.id})`); // set the onclick attribute of the search button to call the findRouteForm function with the id of the route item as an argument when the button is clicked
    searchButton.setAttribute("data-toggle", "modal"); // set the data-toggle attribute of the search button to "modal" to enable the modal functionality
    searchButton.innerHTML =
      "<i class='material-icons' data-toggle='tooltip' title='Search'>&#xE8B6;</i>";
  });
}



// this function is the front end of the add_route function in the DAO and the Flask API server,
// it is called when the user clicks on the add button,
// it takes the input from the add route form in the add route modal, 
// creates a new route object with the input data, 
// and sends a POST request to the Flask API server with the new route data in JSON format, 
// then it calls the getAllRoutes function to refresh the table with the new route added  
function addRoute() {
  /*const idInputText = document.getElementById("add-ID");*/
  const destinationInputText = document.getElementById("add-destination");
  const route_mapInputText = document.getElementById("add-route-map");
  const distanceInputText = document.getElementById("add-distance");
  const elevationInputText = document.getElementById("add-elevation");

  // Clear the input fields of the add route form for the user so they can populate the form with new data 
$('#addRouteModal').on('show.bs.modal', function () {
  /*document.getElementById("add-ID").value = "";*/
  document.getElementById("add-destination").value = "";
  document.getElementById("add-route-map").value = "";
  document.getElementById("add-distance").value = "";
  document.getElementById("add-elevation").value = "";
});

  const item = {
    //this id field is not needed because the database will automatically generate a unique id for each new route added
    // so we can omit it from the POST request body when adding a new route
    /*id: parseInt(idInputText.value.trim()),*/
    // the .trim() method is used to remove any leading or trailing whitespace from the input values, 
    // ensuring that the data sent to the server is clean and free of unintended spaces
    destination: destinationInputText.value.trim(),
     // I need to add hyperlink around the URL input
    route_map: `<a href="${route_mapInputText.value.trim()}" target="_blank">${route_mapInputText.value.trim()}</a>`,
    distance: parseFloat(distanceInputText.value.trim()),
    elevation: parseFloat(elevationInputText.value.trim())
  };
  console.log(JSON.stringify(item)); // Log the new route data to the console in JSON format for debugging purposes - only for production
  fetch(url, { //the following is the header of the POST request sent to the Flask API server to add a new route,
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(item)
  })
    .then(response => response.json())
    .then(() => { // the following is the body of the POST request sent to the Flask API server to add a new route,
      getAllRoutes();
      /*idInputText.value = "";*/
      destinationInputText.value = "";
      route_mapInputText.value = "";
      distanceInputText.value = "";
      elevationInputText.value = "";
    })
    .catch(error => console.error("Unable to add Route.", error));
}




// this function is the front end of the delete_route function in the DAO and the Flask API server,
// it is called when the user clicks on the delete button, 
// it takes the id of the route to be deleted (note the user does not input the id directly, 
// but rather clicks the delete button for the specific route they want to delete, 
// and the code populates a hidden input field in the delete route modal with the id of that route), 
// A DELETE request is then sent to the Flask API server with the id as a parameter, 
// then it calls the getAllRoutes function to refresh the table after the route is deleted
function deleteRoute() {
  const itemId = document.getElementById("delete-id").value.trim(); // Get the route ID from the hidden input field in the delete route modal

  fetch(`${url}/${itemId}`, { // Send a DELETE request to the Flask API server with the route ID as a parameter
    method: "DELETE"
  })
    .then(() => {
      getAllRoutes(); // Refresh the table after the route is deleted by calling the Get All function
      $('#deleteRouteModal').modal('hide'); 
    })
    .catch(error => console.error("Unable to delete Route.", error)); // Log any errors to the console for debugging purposes - only for production

  return false; // Return false to prevent the default form submission behavior
}
// this function outlines what the delete button comprises and how it works,
// it is called when the user clicks on the delete button for a specific route,
// it finds the specific route item using the id, 
// sets the hidden input field in the delete route modal with the id of that route, 
// and updates the popup text in the delete route modal to include the destination name of that route
function displayDeleteForm(id) {
  const item = routes.find(item => item.id === id); // Find the specific route item using the ID
  
  document.getElementById("delete-id").value = item.id; // Set the hidden input for the delete logic
  
  const messageElement = document.getElementById("delete-confirm-message");
  messageElement.innerText = `Are you sure you want to delete the route to ${item.destination}?`; // Update the popup text with the destination name
}


//this function is the front end to the updateRoute function in the DAO and flask API server
//the ID is hidden, it is taken from the row of the table that is chosen
//the user then updates whatever field needs to be updated
function updateRoute() {
  //const idElement = document.getElementById("edit-id");
  //const itemId = idElement ? idElement.value : "";
  const itemId = document.getElementById("edit-id").value.trim();

  if (!itemId) {
   console.error("No ID found for update");
    return false;
  }

  const item = {
    id: parseInt(document.getElementById("edit-id").value.trim()),
    destination: document.getElementById("edit-destination").value.trim(),
    // I need to add hyperlink around the URL input
    route_map: `<a href="${document.getElementById("edit-route-map").value.trim()}" target="_blank">${document.getElementById("edit-route-map").value.trim()}</a>`,
    //route_map: document.getElementById("edit-route-map").value.trim(),
    distance: parseFloat(document.getElementById("edit-distance").value.trim()),
    elevation: parseFloat(document.getElementById("edit-elevation").value.trim())
  };

  fetch(`${url}/${itemId}`, { // the following is the body of the PUT request sent to the Flask API server to update a route
    method: "PUT",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(item)
  })
    .then(response => {
      if (!response.ok) throw new Error('Update failed'); 
      
      getAllRoutes(); // if successful we want to hide the Edit popup box
      $('#editRouteModal').modal('hide'); 
    })
    .catch(error => { 
      console.error("Unable to update item.", error); // give an error if it can't be updated, to the console during production
      alert("Update failed."); // and an error message to the user
    });

  return false; 
}

// this function outlines the form you see when you want to click the Edit icon, the field are prepulated with existing entries
function displayEditForm(id) {
  const item = routes.find(item => item.id === id); 
  document.getElementById("edit-id").value = item.id;
  document.getElementById("edit-destination").value = item.destination;

  // FIX: Extract only the URL from the link string so the user sees a clean link to edit
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = item.route_map;
  const linkElement = tempDiv.querySelector('a');
  document.getElementById("edit-route-map").value = linkElement ? linkElement.getAttribute('href') : item.route_map; 

  document.getElementById("edit-distance").value = item.distance;
  document.getElementById("edit-elevation").value = item.elevation;
}


//this function adds a little counter under the table telling you how many rows are in the table
function _displayCount(itemCount) {
  const name = itemCount === 1 ? "route" : "routes";
  document.getElementById(
    "counter"
  ).innerHTML = `Showing <b>${itemCount}</b> ${name}`;
}


// this function describes how the table on the page will look
function _displayRoutes(data) {
  const tBody = document.getElementById("routes"); // get the table body element by its id
  tBody.innerHTML = "";
  _displayCount(data.length); // display the number of route items in the table
  const button = document.createElement("button"); // create a button element to be used for the edit and delete buttons in the table

  data.forEach(item => { // this telling it to put an edit and a delete button at the end of each row
    let editButton = document.createElement("a");
    editButton.href = "#editRouteModal";
    editButton.className = "edit";
    editButton.setAttribute("onclick", `displayEditForm(${item.id})`);
    editButton.setAttribute("data-toggle", "modal");
    editButton.innerHTML =
      "<i class='material-icons' data-toggle='tooltip' title='Edit'>&#xE254;</i>";

    let deleteButton = document.createElement("a");
    deleteButton.href = "#deleteRouteModal";
    deleteButton.className = "delete";
    deleteButton.setAttribute("onclick", `displayDeleteForm(${item.id})`);
    deleteButton.setAttribute("data-toggle", "modal");
    deleteButton.innerHTML =
      "<i class='material-icons' data-toggle='tooltip' title='Delete'>&#xE872;</i>";

    // each tr is a row in the table, so we insert a new row for each route  
    let tr = tBody.insertRow();
    // each td is a column in the table, so we insert 6 columns for each route
    let td1 = tr.insertCell(0);
    let textid = document.createTextNode(item.id);
    td1.appendChild(textid); // add the route id to the first column of the table

    let td2 = tr.insertCell(1);
    let textDestination = document.createTextNode(item.destination);
    td2.appendChild(textDestination); // add the destination to the second column of the table

    let td3 = tr.insertCell(2);
    td3.innerHTML = item.route_map; // add the route map to the third column of the table, using innerHTML to render the link
    
    let td4 = tr.insertCell(3);
    let textDistance = document.createTextNode(item.distance);
    td4.appendChild(textDistance); // add the route distance to the fourth column of the table

    let td5 = tr.insertCell(4);
    // .toLocaleString() automatically adds commas based on the user's regional settings, Ireland/US UK use commas for thousands, on the European continent they use decimal points
    let textElevation = document.createTextNode(item.elevation.toLocaleString());
    td5.appendChild(textElevation); // add the route elevation to the fifth column of the table

    let td6 = tr.insertCell(5);
    td6.appendChild(editButton);
    td6.appendChild(deleteButton);
  });

routes = data;
}