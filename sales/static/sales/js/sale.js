// ======================================================
// EASY BILL SALES ENGINE
// PART 1
// ======================================================

"use strict";

// ======================================================
// GLOBAL VARIABLES
// ======================================================

let products = [];
let customers = [];
let rowNo = 1;


// ======================================================
// PAGE LOAD
// ======================================================

document.addEventListener("DOMContentLoaded", async function () {

    console.log("Easy Bill Sales Loaded");

    try {

        await loadProducts();

        await loadCustomers();

        loadCustomerDropdown();

        const saleItemsScript =
            document.getElementById("sale-items");

        if (saleItemsScript && saleItemsScript.textContent.trim()) {

            try {

                const existingItems = JSON.parse(
                    saleItemsScript.textContent
                );

                if (existingItems.length > 0) {

                    existingItems.forEach(item => {

                        addRow(item);

                    });

                } else {

                    addRow();

                }

            } catch (parseErr) {

                console.error("Failed to parse sale items:", parseErr);

                addRow();

            }

        } else {

            addRow();

        }

        document.getElementById("add-row")
            .addEventListener("click", addRow);

    } catch (err) {

        console.error("Sales page initialization failed:", err);

        alert("Unable to initialize sales page. Please refresh.");

    }

});


// ======================================================
// PREVENT ENTER SUBMITTING FORM
// ======================================================

document.addEventListener("keydown", function (e) {

    if (
        e.key === "Enter" &&
        e.target.tagName !== "TEXTAREA"
    ) {

        e.preventDefault();

    }

});


// ======================================================
// LOAD PRODUCTS
// ======================================================

async function loadProducts() {

    try {

        const response = await fetch("/sales/products/");

        products = await response.json();

        console.log(products);

    }

    catch (err) {

        console.error(err);

        alert("Unable to load products.");

    }

}


// ======================================================
// LOAD CUSTOMERS
// ======================================================

async function loadCustomers() {

    try {

        const response = await fetch("/sales/customers/");

        customers = await response.json();

    }

    catch (err) {

        console.error(err);

        alert("Unable to load customers.");

    }

}


// ======================================================
// CUSTOMER DROPDOWN
// ======================================================

function loadCustomerDropdown() {

    const select = document.getElementById("id_customer");

    if (!select)
        return;

    select.innerHTML = `<option value="">Select Customer</option>`;

    customers.forEach(customer => {

        select.innerHTML += `

            <option value="${customer.id}">

                ${customer.customer_code} - ${customer.name}

            </option>

        `;

    });

}


// ======================================================
// PRODUCT OPTIONS
// ======================================================

function productOptions() {

    let html = "";

    products.forEach(product => {

        html += `

            <option value="${product.id}">

                ${product.barcode} - ${product.name}

            </option>

        `;

    });

    return html;

}


// ======================================================
// ADD ROW
// ======================================================

function addRow(item = null) {

    const tbody = document.getElementById("sale-body");

    const tr = document.createElement("tr");

    tr.innerHTML = `

        <td>${rowNo++}</td>

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

                ${productOptions()}

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
                min="1">

        </td>

        <td>

            <input
                type="number"
                class="form-control selling-price"
                value="0"
                step="0.01">

        </td>

        <td>

            <select class="form-select gst">

                <option value="0">0%</option>
                <option value="5">5%</option>
                <option value="12">12%</option>
                <option value="18">18%</option>
                <option value="28">28%</option>

            </select>

        </td>

        <td>

            <input
                type="text"
                class="form-control gst-amount"
                value="0.00"
                readonly>

        </td>

        <td>

            <input
                type="text"
                class="form-control total"
                value="0.00"
                readonly>

        </td>

        <td class="text-center">

            <button
                type="button"
                class="btn btn-danger btn-sm remove-row">

                <i class="bi bi-trash"></i>

            </button>

        </td>

    `;

    tbody.appendChild(tr);

    if (item) {

        try {

            const row = tbody.lastElementChild;

            if (!row) return;

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

            const barcodeField =
                row.querySelector(".barcode");

            if (barcodeField) {

                barcodeField.value = item.barcode || "";

            }

            const unitField =
                row.querySelector(".unit");

            if (unitField) {

                unitField.value = item.unit || "";

            }

            const qtyField =
                row.querySelector(".qty");

            if (qtyField) {

                qtyField.value = item.qty;

            }

            const priceField =
                row.querySelector(".selling-price");

            if (priceField) {

                priceField.value =
                    Number(item.selling_price).toFixed(2);

            }

            const gstField =
                row.querySelector(".gst");

            if (gstField) {

                gstField.value =
                    Number(item.gst);

            }

            calculateRow(row);

            console.log("Loaded sale item:", item);

        } catch (rowErr) {

            console.error("Failed to load sale item:", rowErr, item);

        }

    }

    calculateInvoice();

}


// ======================================================
// REMOVE ROW
// ======================================================

document.addEventListener("click", function (e) {

    const button = e.target.closest(".remove-row");

    if (!button)
        return;

    const row = button.closest("tr");

    row.remove();

    renumberRows();

    calculateInvoice();

});


// ======================================================
// RENUMBER ROWS
// ======================================================

function renumberRows() {

    rowNo = 1;

    document.querySelectorAll("#sale-body tr")
        .forEach(row => {

            row.cells[0].textContent = rowNo++;

        });

}
// ======================================================
// PRODUCT SELECTED
// ======================================================

document.addEventListener("change", function (e) {

    if (!e.target.classList.contains("product"))
        return;

    const row = e.target.closest("tr");

    const product = products.find(
        p => Number(p.id) === Number(e.target.value)
    );

    if (!product)
        return;

    // Barcode
    row.querySelector(".barcode").value = product.barcode;

    // Unit
    row.querySelector(".unit").value = product.unit;

    // Selling Price
    row.querySelector(".selling-price").value =
        Number(product.selling_price).toFixed(2);

    // GST
    row.querySelector(".gst").value = product.gst;

    // Stock Tooltip
    row.querySelector(".qty").title =
        `Available Stock : ${product.stock}`;

    // Focus Qty
    row.querySelector(".qty").focus();
    row.querySelector(".qty").select();

    calculateRow(row);

});


// ======================================================
// INPUT EVENTS
// ======================================================

document.addEventListener("input", function (e) {

    if (

        e.target.classList.contains("qty") ||

        e.target.classList.contains("selling-price")

    ) {

        calculateRow(
            e.target.closest("tr")
        );

    }

});


// ======================================================
// GST CHANGED
// ======================================================

document.addEventListener("change", function (e) {

    if (!e.target.classList.contains("gst"))
        return;

    calculateRow(
        e.target.closest("tr")
    );

});


// ======================================================
// DISCOUNT CHANGED
// ======================================================

document.addEventListener("input", function (e) {

    if (e.target.id === "id_discount") {

        calculateInvoice();

    }

});


// ======================================================
// CALCULATE SINGLE ROW
// ======================================================

function calculateRow(row) {

    const qty = parseFloat(
        row.querySelector(".qty").value
    ) || 0;

    const rate = parseFloat(
        row.querySelector(".selling-price").value
    ) || 0;

    const gst = parseFloat(
        row.querySelector(".gst").value
    ) || 0;

    const amount = qty * rate;

    const gstAmount = amount * gst / 100;

    const total = amount + gstAmount;

    row.querySelector(".gst-amount").value =
        gstAmount.toFixed(2);

    row.querySelector(".total").value =
        total.toFixed(2);

    calculateInvoice();

}


// ======================================================
// CALCULATE INVOICE
// ======================================================

function calculateInvoice() {

    let subtotal = 0;

    let gstTotal = 0;

    document.querySelectorAll("#sale-body tr")
        .forEach(row => {

            const qty = parseFloat(
                row.querySelector(".qty").value
            ) || 0;

            const rate = parseFloat(
                row.querySelector(".selling-price").value
            ) || 0;

            const gst = parseFloat(
                row.querySelector(".gst").value
            ) || 0;

            const amount = qty * rate;

            const gstAmount = amount * gst / 100;

            subtotal += amount;

            gstTotal += gstAmount;

        });

    const discount = parseFloat(
        document.getElementById("id_discount")?.value
    ) || 0;

    const grandTotal =
        subtotal +
        gstTotal -
        discount;

    document.getElementById("subtotal")
        .textContent = subtotal.toFixed(2);

    document.getElementById("gst-total")
        .textContent = gstTotal.toFixed(2);

    document.getElementById("discount-total")
        .textContent = discount.toFixed(2);

    document.getElementById("grand-total")
        .textContent = grandTotal.toFixed(2);

}


// ======================================================
// BARCODE SEARCH
// (Ready for Phone Scanner)
// ======================================================

document.addEventListener("change", function (e) {

    if (!e.target.classList.contains("barcode"))
        return;

    const barcode = e.target.value.trim();

    if (!barcode)
        return;

    const product = products.find(
        p => p.barcode === barcode
    );

    if (!product)
        return;

    const row = e.target.closest("tr");

    row.querySelector(".product").value = product.id;

    row.querySelector(".product")
        .dispatchEvent(new Event("change"));

});
// ======================================================
// SAVE SALE
// ======================================================

document.getElementById("save-sale").addEventListener("click", saveSale);

async function saveSale() {

    // ----------------------------
    // Basic Validation
    // ----------------------------

    const customer = document.getElementById("id_customer").value;
    const saleDate = document.getElementById("id_sale_date").value;
    const remarks = document.getElementById("id_remarks").value;
    const discount = parseFloat(document.getElementById("id_discount").value) || 0;

    if (!customer) {
        alert("Please select a customer.");
        return;
    }

    const rows = document.querySelectorAll("#sale-body tr");

    if (rows.length === 0) {
        alert("Please add at least one product.");
        return;
    }

    let items = [];

    let subtotal = 0;
    let gstTotal = 0;

    for (const row of rows) {

        const product = row.querySelector(".product").value;

        if (!product)
            continue;

        const qty = parseFloat(row.querySelector(".qty").value) || 0;
        const sellingPrice = parseFloat(row.querySelector(".selling-price").value) || 0;
        const gst = parseFloat(row.querySelector(".gst").value) || 0;

        const amount = qty * sellingPrice;
        const gstAmount = amount * gst / 100;

        subtotal += amount;
        gstTotal += gstAmount;

        items.push({

            product: Number(product),
            qty: qty,
            selling_price: sellingPrice,
            gst: gst

        });

    }

    if (items.length === 0) {
        alert("Please select at least one product.");
        return;
    }

    const grandTotal = subtotal + gstTotal - discount;

    // ----------------------------
    // Send to Django
    // ----------------------------

    const response = await fetch("/sales/save/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json",

            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value

        },

        body: JSON.stringify({

            customer: customer,
            sale_date: saleDate,
            subtotal: subtotal,
            discount: discount,
            gst: gstTotal,
            grand_total: grandTotal,
            remarks: remarks,
            items: items

        })

    });

    const result = await response.json();

    if (result.success) {

        alert(result.message);

        window.location.href = "/sales/";

    }
    else {

        alert(result.message);

    }

}
// ======================================================
// MOVE TO NEXT FIELD
// ======================================================

function moveNext(current) {

    const row = current.closest("tr");

    if (!row)
        return;

    const fields = [

        ".product",

        ".qty",

        ".selling-price",

        ".gst"

    ];

    let index = -1;

    fields.forEach((cls, i) => {

        if (current.matches(cls))
            index = i;

    });

    if (index === -1)
        return;

    // Last field
    if (index === fields.length - 1) {

        addRow();

        const rows = document.querySelectorAll("#sale-body tr");

        rows[rows.length - 1]
            .querySelector(".product")
            .focus();

        return;

    }

    row.querySelector(fields[index + 1]).focus();

}
// ======================================================
// KEYBOARD SHORTCUTS
// ======================================================

document.addEventListener("keydown", function (e) {

    // Prevent Enter from submitting the form
    if (e.key === "Enter") {

        if (
            e.target.tagName === "INPUT" ||
            e.target.tagName === "SELECT"
        ) {

            e.preventDefault();

            moveNext(e.target);

        }

    }

    // F2 = Add Product Row
    if (e.key === "F2") {

        e.preventDefault();

        addRow();

        const rows = document.querySelectorAll("#sale-body tr");

        rows[rows.length - 1]
            .querySelector(".product")
            .focus();

    }

    // F3 = New Product
    if (e.key === "F3") {

        e.preventDefault();

        window.open(
            "/products/add/",
            "_blank",
            "width=900,height=700"
        );

    }

    // F4 = New Customer
    if (e.key === "F4") {

        e.preventDefault();

        window.open(
            "/customers/add/",
            "_blank",
            "width=900,height=700"
        );

    }

});
// ======================================================
// AUTO SELECT INPUT
// ======================================================

document.addEventListener("focusin", function (e) {

    if (
        e.target.matches(
            ".qty,.selling-price"
        )
    ) {

        e.target.select();

    }

});
// ======================================================
// REMOVE ROW
// ======================================================

document.addEventListener("click", function (e) {

    if (!e.target.closest(".remove-row"))
        return;

    const rows = document.querySelectorAll("#sale-body tr");

    if (rows.length === 1) {

        alert("Cannot delete the last row.");

        return;

    }

    e.target.closest("tr").remove();

    calculateInvoice();

});
// ======================================================
// RENUMBER ROWS
// ======================================================

function renumberRows() {

    let n = 1;

    document.querySelectorAll("#sale-body tr").forEach(row => {

        row.cells[0].textContent = n++;

    });

}