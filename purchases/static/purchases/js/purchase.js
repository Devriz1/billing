// ======================================================
// PURCHASE ENGINE
// Professional Billing System
// Part 1
// ======================================================

// ======================================================
// GLOBAL VARIABLES
// ======================================================

let products = [];

let rowNo = 1;

let supplierLoaded = false;

// GST Options

const GST_OPTIONS = [

    {
        value: 0,
        text: "NT"
    },

    {
        value: 5,
        text: "5%"
    },

    {
        value: 12,
        text: "12%"
    },

    {
        value: 18,
        text: "18%"
    },

    {
        value: 28,
        text: "28%"
    }

];

// ======================================================
// PAGE LOAD
// ======================================================

document.addEventListener("DOMContentLoaded", async function () {

    console.log("Purchase Module Started");

    await loadProducts();

    const itemsScript =
        document.getElementById("purchase-items");

    let existingItems = [];

    if (itemsScript && itemsScript.textContent.trim()) {

        try {

            existingItems = JSON.parse(
                itemsScript.textContent
            );

        } catch (err) {

            console.error(
                "Failed to parse purchase items:",
                err
            );

        }

    }

    if (existingItems.length > 0) {

        existingItems.forEach(function (item) {

            addRow(item);

        });

    } else {

        addRow();

    }

    document
        .getElementById("add-row")
        .addEventListener(
            "click",
            addRow
        );

});

// ======================================================
// LOAD PRODUCTS
// ======================================================

async function loadProducts() {

    try {

        const response = await fetch(
            "/purchases/products/"
        );

        products = await response.json();

        console.log(products);

    }

    catch (err) {

        console.error(err);

        alert("Unable to load products.");

    }

}

// ======================================================
// BUILD GST DROPDOWN
// ======================================================

function buildGSTOptions(selected = 0) {

    let html = "";

    GST_OPTIONS.forEach(function (gst) {

        html += `

<option value="${gst.value}"

${Number(selected) === Number(gst.value) ? "selected" : ""}>

${gst.text}

</option>

`;

    });

    return html;

}

// ======================================================
// ADD PURCHASE ROW
// ======================================================

function addRow(item = null) {

    const tbody = document.getElementById(
        "purchase-body"
    );

    const tr = document.createElement("tr");

    tr.innerHTML = `

<td class="slno">

${rowNo}

</td>

<td>

<input
type="text"
class="form-control barcode"
readonly>

</td>

<td>

<select class="form-select product">

<option value="">

Select Product

</option>

${products.map(product => `

<option value="${product.id}">

${product.barcode} - ${product.name}

</option>

`).join("")}

</select>

</td>

<td>

<input
type="text"
class="form-control unit"
readonly>

</td>

<td>

<input
    type="number"
    class="form-control qty"
    value="1"
    min="1"
    step="0.01"
    style="min-width:70px;">

</td>

<td>

<input
type="number"
value="0"
step="0.01"
class="form-control purchase-price">

</td>

<td>

<input
type="text"
class="form-control amount"
readonly>

</td>

<td>

<select class="form-select gst">

${buildGSTOptions()}

</select>

</td>

<td>

<input
type="text"
class="form-control gst-amount"
readonly>

</td>

<td>

<input
type="number"
value="0"
step="0.01"
class="form-control selling-price">

</td>

<td>

<input
type="text"
class="form-control total"
readonly>

</td>

<td>

<button
type="button"
class="btn btn-danger remove">

<i class="bi bi-trash"></i>

</button>

</td>

`;

    tbody.appendChild(tr);

    rowNo++;

    if (item) {

        try {

            const row = tbody.lastElementChild;

            if (!row)
                return;

            const productSelect =
                row.querySelector(".product");

            const productId = String(item.product);

            const existingOption =
                productSelect.querySelector(
                    `option[value="${productId}"]`
                );

            if (!existingOption) {

                const option =
                    document.createElement("option");

                option.value = productId;

                option.textContent = item.barcode
                    ? `${item.barcode} - ${item.product_name || "Product"}`
                    : `${item.product_name || "Product"}`;

                productSelect.appendChild(option);

            }

            productSelect.value = productId;

            row.querySelector(".barcode").value =
                item.barcode || "";

            row.querySelector(".unit").value =
                item.unit || "";

            row.querySelector(".qty").value =
                item.qty;

            row.querySelector(".purchase-price").value =
                Number(item.purchase_price).toFixed(2);

            row.querySelector(".selling-price").value =
                Number(item.selling_price).toFixed(2);

            const gstSelect =
                row.querySelector(".gst");

            const gstValue = Number(item.gst);

            if (
                GST_OPTIONS.some(function (g) {

                    return Number(g.value) === gstValue;

                })
            ) {

                gstSelect.value = gstValue;

            }

            calculateRow(row);

            console.log("Loaded purchase item:", item);

        } catch (rowErr) {

            console.error(
                "Failed to load purchase item:",
                rowErr,
                item
            );

        }

    }

}

// ======================================================
// PRODUCT SELECTED
// ======================================================

document.addEventListener("change", function (e) {

    if (!e.target.classList.contains("product"))
        return;

    const row = e.target.closest("tr");

    const productId = Number(e.target.value);

    if (!productId)
        return;

    // ==========================================
    // Prevent Duplicate Products
    // ==========================================

    let duplicate = false;

    document.querySelectorAll(".product").forEach(function (select) {

        if (
            select !== e.target &&
            Number(select.value) === productId
        ) {

            duplicate = true;

        }

    });

    if (duplicate) {

        alert("Product already added.");

        e.target.value = "";

        return;

    }

    // ==========================================
    // Find Product
    // ==========================================

    const product = products.find(function (p) {

        return Number(p.id) === productId;

    });

    if (!product)
        return;

    // ==========================================
    // Fill Product Details
    // ==========================================

    row.querySelector(".barcode").value =
        product.barcode;

    row.querySelector(".unit").value =
        product.unit;

    row.querySelector(".purchase-price").value =
        Number(product.purchase_price).toFixed(2);

    row.querySelector(".selling-price").value =
        Number(product.selling_price).toFixed(2);

    row.querySelector(".gst").value =
        Number(product.gst);

    // ==========================================
    // Calculate
    // ==========================================

    calculateRow(row);

    // ==========================================
    // Focus Qty
    // ==========================================

    row.querySelector(".qty").focus();

    row.querySelector(".qty").select();

});


// ======================================================
// RECALCULATE WHEN VALUE CHANGES
// ======================================================

document.addEventListener("input", function (e) {

    if (

        e.target.classList.contains("qty") ||

        e.target.classList.contains("purchase-price") ||

        e.target.classList.contains("selling-price")

    ) {

        calculateRow(

            e.target.closest("tr")

        );

    }

});


// ======================================================
// GST DROPDOWN CHANGED
// ======================================================

document.addEventListener("change", function (e) {

    if (!e.target.classList.contains("gst"))
        return;

    calculateRow(

        e.target.closest("tr")

    );

});


// ======================================================
// AUTO SELECT TEXT
// ======================================================

document.addEventListener("focusin", function (e) {

    if (

        e.target.classList.contains("qty") ||

        e.target.classList.contains("purchase-price") ||

        e.target.classList.contains("selling-price")

    ) {

        e.target.select();

    }

});
// ======================================================
// CALCULATE ONE ROW
// ======================================================

function calculateRow(row) {

    const qty = parseFloat(
        row.querySelector(".qty").value
    ) || 0;

    const purchaseRate = parseFloat(
        row.querySelector(".purchase-price").value
    ) || 0;

    const gstPercent = parseFloat(
        row.querySelector(".gst").value
    ) || 0;

    // ------------------------------------
    // Amount
    // ------------------------------------

    const amount = qty * purchaseRate;

    // ------------------------------------
    // GST Amount
    // ------------------------------------

    const gstAmount = amount * gstPercent / 100;

    // ------------------------------------
    // Total
    // ------------------------------------

    const total = amount + gstAmount;

    // ------------------------------------
    // Fill Fields
    // ------------------------------------

    row.querySelector(".amount").value =
        amount.toFixed(2);

    row.querySelector(".gst-amount").value =
        gstAmount.toFixed(2);

    row.querySelector(".total").value =
        total.toFixed(2);

    // ------------------------------------

    calculateInvoice();

}

// ======================================================
// CALCULATE ENTIRE INVOICE
// ======================================================

function calculateInvoice() {

    let subtotal = 0;

    let gstTotal = 0;

    let grandTotal = 0;

    // ------------------------------------

    document.querySelectorAll("#purchase-body tr")
        .forEach(function (row) {

            subtotal += parseFloat(

                row.querySelector(".amount").value

            ) || 0;

            gstTotal += parseFloat(

                row.querySelector(".gst-amount").value

            ) || 0;

            grandTotal += parseFloat(

                row.querySelector(".total").value

            ) || 0;

        });

    // ------------------------------------
    // Discount
    // ------------------------------------

    const discount = parseFloat(

        document.getElementById("id_discount").value

    ) || 0;

    grandTotal -= discount;

    if (grandTotal < 0)
        grandTotal = 0;

    // ------------------------------------
    // Update Screen
    // ------------------------------------

    document.getElementById("subtotal").innerHTML =
        subtotal.toFixed(2);

    document.getElementById("discount").innerHTML =
        discount.toFixed(2);

    document.getElementById("gst-total").innerHTML =
        gstTotal.toFixed(2);

    document.getElementById("grand-total").innerHTML =
        grandTotal.toFixed(2);

}

// ======================================================
// RECALCULATE WHEN DISCOUNT CHANGES
// ======================================================

document
.getElementById("id_discount")
.addEventListener(

    "input",

    calculateInvoice

);

// ======================================================
// DELETE ROW
// ======================================================

document.addEventListener("click", function (e) {

    const btn = e.target.closest(".remove");

    if (!btn)
        return;

    const rows = document.querySelectorAll("#purchase-body tr");

    // Keep at least one row
    if (rows.length === 1) {

        alert("At least one row is required.");

        return;

    }

    btn.closest("tr").remove();

    refreshRowNumbers();

    calculateInvoice();

});


// ======================================================
// REFRESH ROW NUMBERS
// ======================================================

function refreshRowNumbers() {

    rowNo = 1;

    document.querySelectorAll("#purchase-body tr").forEach(function (row) {

        row.querySelector(".slno").innerHTML = rowNo++;

    });

}


// ======================================================
// ENTER KEY NAVIGATION
// ======================================================

document.addEventListener("keydown", function (e) {

    if (e.key !== "Enter")
        return;

    const element = e.target;

    if (

        !element.classList.contains("qty") &&
        !element.classList.contains("purchase-price") &&
        !element.classList.contains("selling-price") &&
        !element.classList.contains("gst") &&
        !element.classList.contains("product")

    )
        return;

    e.preventDefault();

    const row = element.closest("tr");

    // Product -> Qty
    if (element.classList.contains("product")) {

        row.querySelector(".qty").focus();

        row.querySelector(".qty").select();

        return;

    }

    // Qty -> Purchase Rate
    if (element.classList.contains("qty")) {

        row.querySelector(".purchase-price").focus();

        row.querySelector(".purchase-price").select();

        return;

    }

    // Purchase Rate -> GST
    if (element.classList.contains("purchase-price")) {

        row.querySelector(".gst").focus();

        return;

    }

    // GST -> Selling Price
    if (element.classList.contains("gst")) {

        row.querySelector(".selling-price").focus();

        row.querySelector(".selling-price").select();

        return;

    }

    // Selling Price -> Next Row
    if (element.classList.contains("selling-price")) {

        const rows = document.querySelectorAll("#purchase-body tr");

        const lastRow = rows[rows.length - 1];

        // Automatically add new row if we're on the last one
        if (row === lastRow) {

            addRow();

        }

        const newRows = document.querySelectorAll("#purchase-body tr");

        const nextRow = newRows[
            [...newRows].indexOf(row) + 1
        ];

        if (nextRow) {

            nextRow.querySelector(".product").focus();

        }

    }

});


// ======================================================
// AUTO SELECT INPUT CONTENT
// ======================================================

document.addEventListener("focus", function (e) {

    if (

        e.target.classList.contains("qty") ||

        e.target.classList.contains("purchase-price") ||

        e.target.classList.contains("selling-price")

    ) {

        setTimeout(() => {

            e.target.select();

        }, 50);

    }

}, true);


// ======================================================
// PREVENT FORM SUBMIT ON ENTER
// ======================================================

document
.getElementById("purchase-form")
.addEventListener("keydown", function (e) {

    if (e.key === "Enter") {

        e.preventDefault();

    }

});


// ======================================================
// F2 = ADD PRODUCT ROW
// ======================================================

document.addEventListener("keydown", function (e) {

    if (e.key === "F2") {

        e.preventDefault();

        addRow();

    }

});
// ======================================================
// SAVE PURCHASE (AJAX)
// ======================================================

document
.getElementById("purchase-form")
.addEventListener("submit", async function (e) {

    e.preventDefault();

    // ---------------------------------------
    // Basic Validation
    // ---------------------------------------

    const supplier =
        document.getElementById("id_supplier").value;

    if (!supplier) {

        alert("Please select a supplier.");

        return;

    }

    const rows = [];

    let valid = true;

    // ---------------------------------------
    // Read Table
    // ---------------------------------------

    document.querySelectorAll("#purchase-body tr")
        .forEach(function (row) {

            const product =
                row.querySelector(".product").value;

            if (!product)
                return;

            const qty = parseFloat(
                row.querySelector(".qty").value
            ) || 0;

            if (qty <= 0) {

                valid = false;

                return;

            }

            rows.push({

                product: product,

                barcode:
                    row.querySelector(".barcode").value,

                unit:
                    row.querySelector(".unit").value,

                qty: qty,

                purchase_price:
                    parseFloat(
                        row.querySelector(".purchase-price").value
                    ) || 0,

                amount:
                    parseFloat(
                        row.querySelector(".amount").value
                    ) || 0,

                gst:
                    parseFloat(
                        row.querySelector(".gst").value
                    ) || 0,

                gst_amount:
                    parseFloat(
                        row.querySelector(".gst-amount").value
                    ) || 0,

                selling_price:
                    parseFloat(
                        row.querySelector(".selling-price").value
                    ) || 0,

                total:
                    parseFloat(
                        row.querySelector(".total").value
                    ) || 0

            });

        });

    if (!valid) {

        alert("Quantity must be greater than zero.");

        return;

    }

    if (rows.length === 0) {

        alert("Please add at least one product.");

        return;

    }

    // ---------------------------------------
    // Build JSON
    // ---------------------------------------

    const payload = {

        invoice_number:
            document.getElementById("id_invoice_number").value,

        supplier:

            supplier,

        purchase_date:

            document.getElementById("id_purchase_date").value,

        discount:

            parseFloat(
                document.getElementById("id_discount").value
            ) || 0,

        subtotal:

            parseFloat(
                document.getElementById("subtotal").innerText
            ) || 0,

        gst:

            parseFloat(
                document.getElementById("gst-total").innerText
            ) || 0,

        grand_total:

            parseFloat(
                document.getElementById("grand-total").innerText
            ) || 0,

        remarks:

            document.getElementById("id_remarks").value,

        items:

            rows

    };

    console.log(payload);

    // ---------------------------------------
    // Save
    // ---------------------------------------

    try {

        const response = await fetch(

            "/purchases/save/",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json",

                    "X-CSRFToken":

                        document.querySelector(
                            "[name=csrfmiddlewaretoken]"
                        ).value

                },

                body:

                    JSON.stringify(payload)

            }

        );

        const result = await response.json();

        if (result.success) {

            alert(result.message);

            window.location.href = "/purchases/";

        }

        else {

            alert(result.message);

        }

    }

    catch (err) {

        console.error(err);

        alert("Unable to save purchase.");

    }

});
// ======================================================
// PART 6
// POPUPS, REFRESH PRODUCTS & SHORTCUTS
// ======================================================


// ======================================================
// REFRESH PRODUCT LIST
// ======================================================

async function refreshProducts() {

    try {

        const response = await fetch("/purchases/products/");

        products = await response.json();

        document.querySelectorAll(".product").forEach(function(select){

            const selected = select.value;

            select.innerHTML = `
                <option value="">Select Product</option>
            `;

            products.forEach(function(product){

                select.innerHTML += `

                    <option value="${product.id}">

                        ${product.barcode} - ${product.name}

                    </option>

                `;

            });

            select.value = selected;

        });

    }

    catch(err){

        console.log(err);

    }

}


// ======================================================
// CALLED FROM PRODUCT POPUP
// ======================================================

window.productCreated = async function(productId){

    await refreshProducts();

    const rows = document.querySelectorAll("#purchase-body tr");

    if(rows.length===0){

        addRow();

    }

    const lastRow = document.querySelector("#purchase-body tr:last-child");

    const select = lastRow.querySelector(".product");

    select.value = productId;

    select.dispatchEvent(new Event("change"));

};


// ======================================================
// CALLED FROM SUPPLIER POPUP
// ======================================================

window.supplierCreated = function(id,name){

    const supplier = document.getElementById("id_supplier");

    supplier.innerHTML += `

        <option value="${id}">

            ${name}

        </option>

    `;

    supplier.value = id;

};


// ======================================================
// KEYBOARD SHORTCUTS
// ======================================================

document.addEventListener("keydown",function(e){

    // F3 = Add Product Master

    if(e.key==="F3"){

        e.preventDefault();

        window.open(

            "/products/add/?popup=1",

            "AddProduct",

            "width=1100,height=750"

        );

    }

    // F4 = Add Supplier

    if(e.key==="F4"){

        e.preventDefault();

        window.open(

            "/suppliers/add/?popup=1",

            "AddSupplier",

            "width=900,height=650"

        );

    }

    // F6 = New Row

    if(e.key==="F6"){

        e.preventDefault();

        addRow();

    }

});


// ======================================================
// BARCODE SUPPORT
// ======================================================

document.addEventListener("keydown",function(e){

    if(e.key!=="Enter")
        return;

    if(!e.target.classList.contains("barcode"))
        return;

    e.preventDefault();

    const code = e.target.value.trim();

    const product = products.find(function(p){

        return p.barcode===code;

    });

    if(!product){

        alert("Product not found.");

        return;

    }

    const row = e.target.closest("tr");

    row.querySelector(".product").value = product.id;

    row.querySelector(".product")
        .dispatchEvent(new Event("change"));

});


// ======================================================
// CLEAR FORM
// ======================================================

function clearPurchase(){

    document.getElementById("purchase-body").innerHTML="";

    rowNo=1;

    addRow();

    document.getElementById("id_discount").value=0;

    calculateInvoice();

}


// ======================================================
// DEBUG
// ======================================================

console.log("Purchase Module Loaded Successfully");