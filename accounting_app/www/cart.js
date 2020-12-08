
frappe.ready(function() {
    console.log("In cart.js");
    if (frappe.session.user == "Guest") {
        setTimeout(function(){window.location.href = "/login"} , 2000);
    }
    frappe.call({
        method: 'accounting_app.www.cart.display_cart',
        args: {
            user: frappe.session.user,
        },
        callback: function(data) {
            si = data.message
            console.log("Si "+si)
            if (!si) {
                display_empty_cart_msg()
                return
            }
            si.items.forEach(function(item) {
                console.log("Item"+ item);
                $(".cart-items-list").append(display_item_in_cart(item))
            });
            update_total_qty_amount(si);            
            remove_item(si);
            update_cart(si);
            place_order(si);

        }
    })
});

var display_item_in_cart = function (item) {
    return (`<li class="list-group-item" >
                <div class="d-flex flex-row justify-content-start">
                <button class="btn btn-link" id="remove-item" data-item-name="${item.item_name}">
                <i class="fa fa-close"></i> Remove item</button>
                </div>
                <div class="d-flex flex-row rounded">
                    <div class="p-2">
                    <img src="${item.image}" alt="${item.item_name}" style="max-height:200px;"/>
                    </div>
                    <div class="p-2 pl-4">
                    <h4 class="">${item.item_name} </h4>
                    <p class="">${item.description} </p>
                    <h5 class="text-secondary float-left mr-3">Rs. ${item.rate} </h5>
                    <p>Qty
                    <input type="number" class="item-quantity" value="${item.quantity}" data-item-name="${item.item_name}" min="1" max="10">    
                    </p>   
                    </div>
                </div>
            </li>`)
}

var display_empty_cart_msg = function () {
    $(".no-product").removeClass("d-none");
    $(".cart-items").removeClass("d-flex").addClass("d-none");
    $(".total-bill").removeClass("d-flex").addClass("d-none");
}

var update_total_qty_amount = function (si){
    var total_qty = si.total_quantity
    var total_amt = si.total_amount
    $('#cart-count').html(total_qty);
    $(".total-quantity").html("Quantity: "+total_qty);
    $(".total-amount").html("Amount: Rs. "+total_amt);
}

var update_cart = function(si){
    $('.item-quantity').on('change', function (){
        var item = $(this).attr('data-item-name');
        var qty = $(this).val();
        frappe.call({
            method: 'accounting_app.www.cart.update_sales_invoice',
            args: {
                si: si.name,
                item_name: item,
                qty: qty,
                save: true
            },
            callback: function(data) {
                if (data) {
                    update_total_qty_amount(data.message)
                }
            }
        });
    });
}

var remove_item = function(si){
    $('#remove-item').on('click', function(){
        var item = $(this).attr('data-item-name');
        frappe.call({
            method: 'accounting_app.www.cart.remove_item',
            args: {
                si: si.name,
                item_name: item
            },
            callback: function(data) {
                if (data.message == "Null") {
                    frappe.msgprint(__('Item removed!'));
                    setTimeout(function(){window.location.href = "/products"} , 2000); 
                }
                else{
                    update_cart(data.message);
                }
            }
        });
    })
}

var place_order = function(si){
    $('#place-order').on('click', function(){
        frappe.call({
            method: 'accounting_app.www.cart.place_order',
            args: {
                si: si.name,
                submit: true  
            },
            callback: function(data) {
                if (data) {
                    frappe.msgprint(__('Order Placed! Thank you for shopping with us'));
                    setTimeout(function(){window.location.href = "/products"} , 5000); 
                }
            }
        });
    })
}
    

