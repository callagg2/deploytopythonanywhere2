const url = "/routes";
let routes = [];

function getAllRoutes() {
  fetch(url)
    .then(response => response.json())
    .then(data => _displayRoutes(data))
    .catch(error => console.error("Unable to get routes.", error));
}

function getOneRoute() {
  const id = document.getElementById("search-id").value.trim();

  fetch(`${url}/${id}`)
    .then(response => {
      if (!response.ok) {
        throw new Error("Route not found");
      }
      return response.json();
    })
    .then(data => {
      _displayRoutes([data]); // show the route found
       $('#searchRouteModal').modal('hide');   // auto-close the modal
    })
    .catch(error => console.error("Unable to find that route.", error));

  return false; // prevent form reload
}

function findRouteForm(id) {
  const item = routes.find(item => item.id === id);
  document.getElementById("find-id").value = item.id;
}

$('#searchRouteModal').on('show.bs.modal', function () {
  document.getElementById("search-id").value = "";
});


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

function addRoute() {
  /*const idInputText = document.getElementById("add-ID");*/
  const destinationInputText = document.getElementById("add-destination");
  const route_mapInputText = document.getElementById("add-route-map");
  const distanceInputText = document.getElementById("add-distance");
  const elevationInputText = document.getElementById("add-elevation");

$('#addRouteModal').on('show.bs.modal', function () {
  /*document.getElementById("add-ID").value = "";*/
  document.getElementById("add-destination").value = "";
  document.getElementById("add-route-map").value = "";
  document.getElementById("add-distance").value = "";
  document.getElementById("add-elevation").value = "";
});

  const item = {
    /*id: parseInt(idInputText.value.trim()),*/
    destination: destinationInputText.value.trim(),
    route_map: `<a href="${route_mapInputText.value.trim()}" target="_blank">${route_mapInputText.value.trim()}</a>`,
    distance: parseFloat(distanceInputText.value.trim()),
    elevation: parseFloat(elevationInputText.value.trim())
  };
  console.log(JSON.stringify(item));
  fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(item)
  })
    .then(response => response.json())
    .then(() => {
      getAllRoutes();
      /*idInputText.value = "";*/
      destinationInputText.value = "";
      route_mapInputText.value = "";
      distanceInputText.value = "";
      elevationInputText.value = "";
    })
    .catch(error => console.error("Unable to add Route.", error));
}


function deleteRoute() {
  const itemId = document.getElementById("delete-id").value.trim();
  fetch(`${url}/${itemId}`, {
    method: "DELETE"
  })
    .then(() => getAllRoutes())
    .catch(error => console.error("Unable to delete Route.", error));
}

function displayDeleteForm(id) {
  const item = routes.find(item => item.id === id);
  document.getElementById("delete-id").value = item.id;
}

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
    route_map: `<a href="${document.getElementById("edit-route-map").value.trim()}" target="_blank">${document.getElementById("edit-route-map").value.trim()}</a>`,
    //route_map: document.getElementById("edit-route-map").value.trim(),
    distance: parseFloat(document.getElementById("edit-distance").value.trim()),
    elevation: parseFloat(document.getElementById("edit-elevation").value.trim())
  };

  fetch(`${url}/${itemId}`, {
    method: "PUT",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(item)
  })
    .then(response => {
      if (!response.ok) throw new Error('Update failed');
      // Success: Refresh and Close
      getAllRoutes();
      $('#editRouteModal').modal('hide'); 
    })
    .catch(error => {
      console.error("Unable to update item.", error);
      alert("Update failed. Check console for details.");
    });

  return false; 
}

function _displayCount(itemCount) {
  const name = itemCount === 1 ? "route" : "routes";
  document.getElementById(
    "counter"
  ).innerHTML = `Showing <b>${itemCount}</b> ${name}`;
}

function _displayRoutes(data) {
  const tBody = document.getElementById("routes"); // get the table body element by its id
  tBody.innerHTML = "";
  _displayCount(data.length); // display the number of route items in the table
  const button = document.createElement("button"); // create a button element to be used for the edit and delete buttons in the table

  data.forEach(item => {
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
    //let textRoute_map = document.createTextNode(item.route_map);
    td3.innerHTML = item.route_map; // add the route map to the third column of the table, using innerHTML to render the link
    
    let td4 = tr.insertCell(3);
    let textDistance = document.createTextNode(item.distance);
    td4.appendChild(textDistance); // add the route distance to the fourth column of the table

    let td5 = tr.insertCell(4);
    // .toLocaleString() automatically adds commas based on the user's regional settings
    let textElevation = document.createTextNode(item.elevation.toLocaleString());
    td5.appendChild(textElevation); // add the route elevation to the fifth column of the table

    let td6 = tr.insertCell(5);
    td6.appendChild(editButton);
    td6.appendChild(deleteButton);
  });

  routes = data;
}