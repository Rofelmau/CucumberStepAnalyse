var myObj;

function Table_write_rows(SortBykey, SortBykeyValue, selectedSingleKeys, selectedMultiKeys) {
	for (var step in myObj) {
		if (SortBykey === "" || myObj[step][SortBykey] === SortBykeyValue) {
			span = myObj[step].params.length;
			stringrow = "";
					
			stringrow += '<tr>';
			var spanValue = 1;
			if (span > 1) {
				spanValue = span;
			}
			for (var key in selectedSingleKeys) {
				stringrow += '<td rowspan="' + spanValue + '">' + myObj[step][selectedSingleKeys[key]] + '</td>';
			}

			for (var key in selectedMultiKeys) {

				for (var subkey in selectedMultiKeys[key]) {
					if (span == 0) {
						stringrow += '<td></td>';
					}
					else if (span > 0) {				
						stringrow += '<td>' + myObj[step].params[0][selectedMultiKeys[key][subkey]] + '</td>';
					}
				}

			}
			stringrow += '</tr>'

			if (span > 1) {
				
				for (var i = 1; i < span; i++ ) {
					stringrow += '<tr>';
					for (var key in selectedMultiKeys) {
						for (var subkey in selectedMultiKeys[key]) {
							stringrow += '<td>' + myObj[step].params[i][selectedMultiKeys[key][subkey]] + '</td>';
						}
					}
					stringrow += '</tr>';
				}
				stringrow += '</tr>';
			}
			
			
			document.getElementById("demo").innerHTML += stringrow;	
		}
	}
}

function Table_display() {
	var selectedSingleKeys = {};
	var countSelections = 0
	for (var key in singleKeys) {
		if ($("#" + singleKeys[key]).is(":checked")) {
			selectedSingleKeys[countSelections] = singleKeys[key];
			countSelections += 1;
		}
	}
	
	var selectedMultiKeys = {};
	var countSelections = 0;
	for (var key in multiKeys) {
		selectedMultiKeys[countSelections] = {};
		var countSubSelections = 0;
		for (var subKey in multiKeys[key]) {
			if ($("#" + multiKeys[key][subKey]).is(":checked")) {
				selectedMultiKeys[countSelections][countSubSelections] = multiKeys[key][subKey];
				countSubSelections += 1;
			}
		}
	}
	
	var tabhead = "";
	var x = 1;
	for (var head in selectedSingleKeys) {
		tabhead += '<th class="column' + x + '">' + selectedSingleKeys[head] + '</th>';
		x += 1;
	}
	for (var head in selectedMultiKeys) {
		for (var subhead in selectedMultiKeys[head]) {
			tabhead += '<th class="column' + x + '">' + selectedMultiKeys[head][subhead] + '</th>';
			x += 1;
		}
	}
	document.getElementById("steptabHead").innerHTML = "";
	document.getElementById("steptabHead").innerHTML += tabhead;

	var e = document.getElementById("sortingSelection");
	var sortBy = e.options[e.selectedIndex].value;
	
	e = document.getElementById("sortingDirection");
	var sortDir = e.options[e.selectedIndex].value;
	console.log(sortDir);
	var sortedValues = [];
	
	if (sortBy === "") {
		sortedValues.push("");
	}
	else {
		for (var param in myObj) {
			if($.inArray(myObj[param][sortBy], sortedValues) === -1)
			{
				sortedValues.push(myObj[param][sortBy]);
			}
		}
		sortedValues.sort();
		if (sortDir == 2) {
			sortedValues.reverse();
		}
		
		console.log(sortedValues);
		
	}
	for (var obtype in sortedValues) {
			Table_write_rows(sortBy, sortedValues[obtype], selectedSingleKeys, selectedMultiKeys);
	}
}

Table_load = function() {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
	  if (this.readyState == 4 && this.status == 200) {
		
		myObj = JSON.parse(this.responseText);
		
		Table_display();
		
		
	  }
	  
	};
	xmlhttp.open("GET", "StepDefinitions.json", true);
	xmlhttp.send();	
}

