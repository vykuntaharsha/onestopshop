$(document).ready(function () {
    //contact form handler
    var contactForm = $('.contact-form');

    function displaySubmitting(submitBtn, defaultText, doSubmit){
        if (doSubmit){
          submitBtn.addClass("disabled");
          submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
        } else {
          submitBtn.removeClass("disabled");
          submitBtn.html(defaultText)
        }
    }

    contactForm.submit(function (e) {
        e.preventDefault();
        var contactFormMethod = contactForm.attr('method');
        var contactFormEndpoint = contactForm.attr('action');
        var contactFormData = contactForm.serialize();
        var contactSubmitButton = contactForm.find('[type="submit"]');
        var contactSubmitButtonTxt = contactSubmitButton.text();
        displaySubmitting(contactSubmitButton,'',true);

        $.ajax({
            url : contactFormEndpoint,
            method: contactFormMethod,
            data: contactFormData,

            success: function (data) {
                contactForm[0].reset();
                $.alert({
                    title: 'Submitted!',
                    content: 'we will reach out asap',
                    theme: 'modern'
                });
                setTimeout(function(){
                    displaySubmitting(contactSubmitButton, contactSubmitButtonTxt, false)
                }, 500)
            },

            error: function (errorData) {
                var error = errorData.responseJSON;
                var msg ='';

                $.each(error, function (key, value) {
                   msg += key + ': '+ value[0].message + '<br/>';
                });

                $.alert({
                    title: 'Oops!',
                    content: msg,
                    theme: 'modern'
                });
                setTimeout(function(){
                    displaySubmitting(contactSubmitButton, contactSubmitButtonTxt, false)
                }, 500)
            }

        });

    });


    // auto search
    var searchForm = $('.search-form');
    var searchInput = searchForm.find('[name="q"]');
    var typingTimer;
    var typingInterval = 500;
    var searchButton = searchForm.find('[type="submit"]');

    searchInput.keyup(function (e) {
        clearTimeout(typingTimer);
       typingTimer = setTimeout(performSearch,typingInterval)
    });

    searchInput.keydown(function (e) {
        clearTimeout(typingTimer);
    });

    function performSearch(){
        searchButton.addClass('disabled');
        searchButton.html('<i class="fa fa-spin fa-spinner"></i> Searching...');
        var query = searchInput.val();
        setTimeout(function () {
             window.location.href = '/search/?q='+query
        },1000)
    }

    // add to cart ajax
    var productAddToCart = $('.add_to_cart_form');

    productAddToCart.submit(function (e) {
        e.preventDefault();
        var addToCartForm = $(this);
        var actionEndPoint = addToCartForm.attr('data-endpoint');
        var httpMethod = addToCartForm.attr('method');
        var formData = addToCartForm.serialize();

        $.ajax({
            url: actionEndPoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                var submitSpan = addToCartForm.find('.submit-span');
                if(data.added){
                    submitSpan.html('<button type="button" class="btn btn-secondary btn-block">Added to cart </button>'+
                        '<button type="submit" class="btn btn-outline-danger btn-block"> Remove from Cart </button>'
                    );
                }else {
                    submitSpan.html('<button type="submit" class="btn btn-success btn-block"> Add to Cart </button>');
                }

                var cartCount = $('.cart-count');
                cartCount.text(data.cartProductsCount);

                var currentPath = window.location.href;
                if (currentPath.indexOf('cart') !== -1){
                   refreshCart()
                }

            },
            error: function (errorData) {
                $.alert({
                    title: 'Oops!',
                    content: 'error in adding to cart',
                    theme: 'modern'
                });
            }
        });

        function refreshCart() {
            var cartTable = $('.cart-table');
            var cartBody = cartTable.find('.cart-body');


            var refreshCartUrl = '/cart/api/';
            var refreshCartMethod = 'GET';
            var data = {};
            var currentUrl = window.location.href;

            $.ajax({
                url : refreshCartUrl,
                method : refreshCartMethod,
                data : data,

                success : function (data) {
                    var hiddenCartProductRemoveForm = $('.cart-product-remove-form');
                    if (data.products.length > 0){
                        var productsRows = cartBody.find('.cart-product');
                        productsRows.html('');

                        $.each(data.products, function (index, value) {
                            var newCartItemRemove = hiddenCartProductRemoveForm.clone();
                            newCartItemRemove.css('display','block');
                            newCartItemRemove.find('.cart-product-id').val(value.id);

                            cartBody.prepend('<tr><td><img src="'+ value.image+'"style="width: 40px; height: 40px" onerror="' +
                                'this.src=\'http://www.brandnmc.com/jbframework/uploads/2017/07/image_not_available.png\'">' +
                                '<a href="'+ value.url +'">'+ value.name +'</a></td><td>$'+ value.price +'</td><td>'+ newCartItemRemove.html()+'</td></tr>')

                        });
                        cartBody.find('.cart-subtotal').text('\$'+data.subtotal);
                        cartBody.find('.cart-shipping').text('\$'+data.shipping);
                    }else {
                        console.log(currentUrl);
                        window.location.href = currentUrl
                    }
                },
                error : function (errorData) {
                   $.alert({
                    title: 'Oops!',
                    content: 'error in adding to cart',
                    theme: 'modern'
                });
                }
            });
        }
    });
});