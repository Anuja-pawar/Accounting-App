
frappe.ready(function() {
    console.log("In main.js");
    $('.add-to-cart').on('click', function (){
        if (frappe.session.user === "Guest") {         
            setTimeout(function(){window.location.href = "/login"} , 2000);
        }
        else {
            var btn = $(this);
            var item = btn.val();
            add_to_cart(btn, item);
            
        }
    });
});

var add_to_cart = function(btn, item) {
    frappe.call({
        method: 'accounting_app.www.cart.add_to_cart',
        args: {
            user: frappe.session.user,
            item_name: item,
            save: true   
        },
        callback: function(data) {
            si = data.message
            if (si) {
                frappe.msgprint(__('Item added to the cart!'));
                btn.prop('disabled', 'true');
                total_qty= si.total_quantity
                $('#cart-count').html(total_qty);
            }
        }
    });

}


