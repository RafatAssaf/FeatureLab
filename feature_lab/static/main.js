let client_input = document.getElementById('client')
let product_input = document.getElementById('product')
let product_area_input = document.getElementById('product_area')

// handle client input change
client_input.onchange = function() {
    $.ajax({ // fetch the products of the selected client
        url: '/products/' + client_input.value
    }).done(function(res) {
        console.log(res)
        if(res.products) {
            // update HTML content
            product_input.innerHTML = res.products.reduce(function(acc, prod){
                return acc + '<option value="' + prod.id + '">' + prod.name + '</option>'
            }, '')
            // update product areas as well
            update_areas(res.products[0].id)
        } else {
            product_input.innerHTML = '<option value="0">Invalid</option>'
        }
    })
}

let update_areas = function(product) {
    $.ajax({ // fetch areas for selected product
        url: '/product_areas/' + product
    }).done(function(res) {
        console.log(res)
        if(res.areas) {
            // update HTML content
            product_area_input.innerHTML = res.areas.reduce(function(acc, area){
                return acc + '<option value="' + area.name + '">' + area.name + '</option>'
            }, '')
        } else {
            product_area_input.innerHTML = '<option value="0">Invalid</option>'
        }
    })
}

// when changing the selected product, update product areas
product_input.onchange = function() {
    update_areas(product_input.value)
}