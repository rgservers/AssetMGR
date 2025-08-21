async function getData() {
        var input = document.getElementById("asid").value;
        var outputDiv = document.getElementById("output");

        if (input) {
            try {
                const data = await fetchData(input);
                if (data) {
                    outputDiv.innerHTML = generateForm(data);
                } else {
                    outputDiv.innerHTML = "<p>No data found.</p>";
                }
            } catch (error) {
                console.error("Fetch error:", error);
                outputDiv.innerHTML = "<p>Error fetching data.</p>";
            }
        }
    }

    async function fetchData(input) {
        const urlse = '/ratpi/fetch_one?asid=' + encodeURIComponent(input);
        const response = await fetch(urlse);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const json = await response.json();
        return json;
    }

    function generateForm(data) {
        if (typeof data === "string") {
            try {
                data = JSON.parse(data);
            } catch (e) {
                return "<p>Invalid data format.</p>";
            }
        }
        let id = data._id && data._id["$oid"] ? data._id["$oid"] : data._id || "";
        return `
        <h2>Asset Details</h2>
        <p><strong>Asset ID:</strong> ${id}</p>
            <form id="editForm" class="center" onsubmit="return submitEditForm(event)">
                <input type="hidden" name="asid" value="${id}">
                <label>Description: <br><input name="assetdesc" value="${data.assetdesc || ""}"></label>
                <label>Category: <br><select name="category" id="category" required>
                    <option value="ACB" ${data.category === "ACB" ? "selected" : ""}>ACB</option>
                    <option value="RMU" ${data.category === "RMU" ? "selected" : ""}>RMU</option>
                    <option value="Transformer" ${data.category === "Transformer" ? "selected" : ""}>Transformer</option>
                    <option value="Kiosk" ${data.category === "Kiosk" ? "selected" : ""}>Kiosk</option>
                    <option value="MCCB" ${data.category === "MCCB" ? "selected" : ""}>MCCB</option>
                    <option value="MCB" ${data.category === "MCB" ? "selected" : ""}>MCB</option>
                    <option value="Switch" ${data.category === "Switch" ? "selected" : ""}>Switch</option>
                    <option value="EB_Meter" ${data.category === "EB_Meter" ? "selected" : ""}>EB Meter</option>
                    <option value="DG_Meter" ${data.category === "DG_Meter" ? "selected" : ""}>DG Meter</option>
                    <option value="Cables" ${data.category === "Cables" ? "selected" : ""}>Cables</option>
                    <option value="Panel" ${data.category === "Panel" ? "selected" : ""}>Panel</option>
                    <option value="LDB" ${data.category === "LDB" ? "selected" : ""}>LDB</option>
                    <option value="RPD" ${data.category === "RPD" ? "selected" : ""}>RPD</option>
                    <option value="ELDB" ${data.category === "ELDB" ? "selected" : ""}>ELDB</option>
                    <option value="Other" ${data.category === "Other" ? "selected" : ""}>Other</option>
                </select></label>
                <label>Location: <br>
                <select name="Location" id="Location" required>
                    <option value="B2" ${data.Location === "B2" ? "selected" : ""}>B2</option>
                    <option value="B1" ${data.Location === "B1" ? "selected" : ""}>B1</option>
                    <option value="Ground" ${data.Location === "Ground" ? "selected" : ""}>Ground Floor</option>
                    <option value="First" ${data.Location === "First" ? "selected" : ""}>First Floor</option>
                    <option value="Second" ${data.Location === "Second" ? "selected" : ""}>Second Floor</option>
                    <option value="Third" ${data.Location === "Third" ? "selected" : ""}>Third Floor</option>
                    <option value="Fourth" ${data.Location === "Fourth" ? "selected" : ""}>Fourth Floor</option>
                    <option value="Fifth" ${data.Location === "Fifth" ? "selected" : ""}>Fifth Floor</option>
                    <option value="Terrace" ${data.Location === "Terrace" ? "selected" : ""}>Terrace</option>
                </select>
                </label>
                <label>Manufacturer Serial Number: <br><input name="Manufacturer_Serial_Number" value="${data.Manufacturer_Serial_Number || ""}"></label>
                <label>Manufacturer: <br><input name="Manufacturer" value="${data.Manufacturer || ""}"></label>
                <label>Type: <br><input name="Type" value="${data.Type || ""}"></label>
                <label>Rated Capacity: <br><input name="Rated_Capacity" value="${data.Rated_Capacity || ""}"></label>
                <label>Activity: <br>
                <select name="Activity" id="Activity" required>
                    <option value="Active" ${data.Activity === "Active" ? "selected" : ""}>Active</option>
                    <option value="Stock" ${data.Activity === "Stock" ? "selected" : ""}>Stock</option>
                    <option value="Decommisioned" ${data.Activity === "Decommisioned" ? "selected" : ""}>Decommisioned</option>
                </select>
                </label>

                <button type="submit" class="btn">Update</button>
            </form>
            <div id="updateResult"></div>
        `;
    }

    async function submitEditForm(event) {
        event.preventDefault();
        const form = document.getElementById("editForm");
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        try {
            const response = await fetch('/ratpi/updateasset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });
            const result = await response.json();
            document.getElementById("updateResult").innerHTML = result.message 
                ? `<p style="color:green">${result.message}</p>` 
                : `<p style="color:red">${result.error}</p>`;
        } catch (error) {
            document.getElementById("updateResult").innerHTML = "<p style='color:red'>Update failed.</p>";
        }
        return false;
    }
    // script.js file

function domReady(fn) {
    if (
        document.readyState === "complete" ||
        document.readyState === "interactive"
    ) {
        setTimeout(fn, 1000);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

domReady(function () {

    // If found you qr code
    function onScanSuccess(decodeText, decodeResult) {
        alert("You Qr is : " + decodeText, decodeResult);
    }
// script.js file

function domReady(fn) {
    if (
        document.readyState === "complete" ||
        document.readyState === "interactive"
    ) {
        setTimeout(fn, 1000);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

domReady(function () {

    // If found you qr code
    function onScanSuccess(decodeText, decodeResult) {
        document.getElementById("asid").value = decodeText;
    }
 
    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader",
        { fps: 10, qrbos: 250 }
    );
    htmlscanner.render(onScanSuccess);
});
    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader",
        { fps: 10, qrbos: 250 }
    );
    htmlscanner.render(onScanSuccess);
});