
async function fetchData() {
    var filter = document.getElementById("filterID").value;
    var input = document.getElementById("lookupinnput").value;
    var outputDiv = document.getElementById("output");
    const urlse = '/ratpi/getfilter?filter=' + encodeURIComponent(filter) + '&lookup=' + encodeURIComponent(input);
    outputDiv.innerHTML = "<span class='info-message'><i class='fas fa-spinner fa-spin'></i> Fetching data...</span>";
    try {
        const response = await fetch(urlse);
        if (!response.ok) {
            outputDiv.innerHTML = "<span class='error-message'><i class='fas fa-exclamation-triangle'></i> Network error.</span>";
            return;
        }
        const json = await response.json();
        if (!Array.isArray(json) || json.length === 0) {
            outputDiv.innerHTML = "<span class='info-message'><i class='fas fa-info-circle'></i> No data found.</span>";
            return;
        }
        let table = "<table><thead><tr>";
        const keys = Object.keys(json[0]);
        // Map database keys to display names
        const displayNames = {
            "_id": "Asset ID",
            "assetdesc": "Asset Description",
            "Location": "Location",
            "Manufacturer_Serial_Number": "MF Serial Number",
            "Manufacturer": "Manufacturer",
            "Type": "Type",
            "Rated_Capacity": "Rated Capacity",
            "Activity": "Activity"
        };
        for (const key of keys) {
            table += `<th>${displayNames[key] || key}</th>`;
        }
        table += "</tr></thead><tbody>";
        for (const row of json) {
            table += "<tr>";
            for (const key of keys) {
                let value = row[key];
                // Convert MongoDB ObjectId to string
                if (value && typeof value === 'object' && value.hasOwnProperty('$oid')) {
                    value = value.$oid;
                } else if (typeof value === 'object' && value !== null) {
                    value = JSON.stringify(value);
                }
                table += `<td>${value}</td>`;
            }
            table += "</tr>";
        }
        table += "</tbody></table>";
        outputDiv.innerHTML = table;
    } catch (err) {
        outputDiv.innerHTML = "<span class='error-message'><i class='fas fa-exclamation-triangle'></i> Error fetching data.</span>";
    }
}