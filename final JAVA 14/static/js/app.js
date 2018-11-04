// Get references from index.html file
var $tbody = document.querySelector("tbody");
var $dateInput = document.querySelector("#datetime");
var $cityInput = document.querySelector("#city");
var $stateInput = document.querySelector("#state");
var $countryInput = document.querySelector("#country");
var $shapeInput = document.querySelector("#shape");
var $searchBtn = document.querySelector("#search");
var $resetBtn = document.querySelector("#reset");

// Add an event listener 
$searchBtn.addEventListener("click", searchButtonClick);
$resetBtn.addEventListener("click", handleResetButtonClick);

// Set filteredData to dataSet initially
var filteredData = data;

// renderTable renders the filtered data to the tbody
function renderTable() {
  console.log(filteredData);
  $tbody.innerHTML = "";
  for (var i = 0; i < filteredData.length; i++) {
    // Get get the current sighting object and its fields
    var sighting = filteredData[i];
    var fields = Object.keys(sighting);

    // Create a new row in the tbody, set the index to be i + startingIndex
    var $row = $tbody.insertRow(i);
    for (var j = 0; j < fields.length; j++) {
      // For every field in the sighting object, create a new cell at set its inner text to be the current value at the current sighting's field
      var field = fields[j];
      var $cell = $row.insertCell(j);
      $cell.innerText = sighting[field];
    }
  }
}

function searchButtonClick() {
    var filterDate = $dateInput.value;
    console.log(filterDate);
        if (filterDate != "") {
        filteredData = data.filter(function (sighting) {
        var sightingDate = sighting.datetime;
        return sightingDate == filterDate;
        });
    };
   renderTable();
};


// Reset the data and search form after a search
function handleResetButtonClick() {
//filteredData = data;
//$dateInput.value = "";
//$cityInput.value = "";
//$stateInput.value = "";
//$countryInput.value = "";
//$shapeInput.value = "";
  renderTable();
}

// Render the table for the first time on page load
renderTable();