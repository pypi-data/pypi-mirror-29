
/************************************************************
 *
 * tailbone.mobile.js
 *
 * Global logic for mobile app
 *
 ************************************************************/


$(function() {

    // must init header/footer toolbars since ours are "external"
    $('[data-role="header"], [data-role="footer"]').toolbar({theme: 'a'});
});


$(document).on('pagecontainerchange', function(event, ui) {

    // in some cases (i.e. when no user is logged in) we may want the (external)
    // header toolbar button to change between pages.  here's how we do that.
    // note however that we do this *always* even when not technically needed
    var link = $('[data-role="header"] a');
    var newlink = ui.toPage.find('.replacement-header a');
    link.text(newlink.text());
    link.attr('href', newlink.attr('href'));
    link.removeClass('ui-icon-home ui-icon-user');
    link.addClass(newlink.attr('class'));
});


$(document).on('pagecreate', function() {

    // setup any autocomplete fields
    $('.field.autocomplete').mobileautocomplete();

});


/**
 * Automatically set focus to certain fields, on various pages
 * TODO: this should accept selector params instead of hard-coding..?
 */
function setfocus() {
    var el = null;
    var queries = [
        '#username',
        '#new-purchasing-batch-vendor-text',
        // '.receiving-upc-search',
    ];
    $.each(queries, function(i, query) {
        el = $(query);
        if (el.is(':visible')) {
            el.focus();
            return false;
        }
    });
}


$(document).on('pageshow', function() {

    setfocus();

});


// handle radio button value change for "simple" grid filter
$(document).on('change', '.simple-filter .ui-radio', function() {
    $(this).parents('form:first').submit();
});


// vendor validation for new purchasing batch
$(document).on('click', 'form[name="new-purchasing-batch"] input[type="submit"]', function() {
    var $form = $(this).parents('form');
    if (! $form.find('[name="vendor"]').val()) {
        alert("Please select a vendor");
        $form.find('[name="new-purchasing-batch-vendor-text"]').focus();
        return false;
    }
});

// submit new purchasing batch form on Purchase click
$(document).on('click', 'form[name="new-purchasing-batch"] [data-role="listview"] a', function() {
    var $form = $(this).parents('form');
    var $field = $form.find('[name="purchase"]');
    var uuid = $(this).parents('li').data('uuid');
    $field.val(uuid);
    $form.submit();
    return false;
});


// disable datasync restart button when clicked
$(document).on('click', '#datasync-restart', function() {
    $(this).button('disable');
});


// handle global keypress on product batch "row" page, for sake of scanner wedge
var product_batch_routes = [
    'mobile.batch.inventory.view',
    'mobile.receiving.view',
];
$(document).on('keypress', function(event) {
    var current_route = $('.ui-page-active [role="main"]').data('route');
    for (var route of product_batch_routes) {
        if (current_route == route) {
            var upc = $('.ui-page-active #upc-search');
            if (upc.length) {
                if (upc.is(':focus')) {
                    if (event.which == 13) {
                        if (upc.val()) {
                            $.mobile.navigate(upc.data('url') + '?upc=' + upc.val());
                        }
                    }
                } else {
                    if (event.which >= 48 && event.which <= 57) { // numeric (qwerty)
                        upc.val(upc.val() + event.key);
                        // TODO: these codes are correct for 'keydown' but apparently not 'keypress' ?
                        // } else if (event.which >= 96 && event.which <= 105) { // numeric (10-key)
                        //     upc.val(upc.val() + event.key);
                    } else if (event.which == 13) {
                        if (upc.val()) {
                            $.mobile.navigate(upc.data('url') + '?upc=' + upc.val());
                        }
                    }
                    return false;
                }
            }
        }
    }
});


// when numeric keypad button is clicked, update quantity accordingly
$(document).on('click', '.quantity-keypad-thingy .keypad-button', function() {
    var keypad = $(this).parents('.quantity-keypad-thingy');
    var quantity = keypad.find('.keypad-quantity');
    var value = quantity.text();
    var key = $(this).text();
    var changed = keypad.data('changed');
    if (key == 'Del') {
        if (value.length == 1) {
            quantity.text('0');
        } else {
            quantity.text(value.substring(0, value.length - 1));
        }
        changed = true;
    } else if (key == '.') {
        if (value.indexOf('.') == -1) {
            if (changed) {
                quantity.text(value + '.');
            } else {
                quantity.text('0.');
                changed = true;
            }
        }
    } else {
        if (value == '0') {
            quantity.text(key);
            changed = true;
        } else if (changed) {
            quantity.text(value + key);
        } else {
            quantity.text(key);
            changed = true;
        }
    }
    if (changed) {
        keypad.data('changed', true);
    }
});


// show/hide expiration date per receiving mode selection
$(document).on('change', 'fieldset.receiving-mode input[name="mode"]', function() {
    var mode = $(this).val();
    if (mode == 'expired') {
        $('#expiration-row').show();
    } else {
        $('#expiration-row').hide();
    }
});


// handle receiving action buttons
$(document).on('click', '.receiving-actions button', function() {
    var action = $(this).data('action');
    var form = $(this).parents('form:first');
    var uom = form.find('[name="keypad-uom"]:checked').val();
    var mode = form.find('[name="mode"]:checked').val();
    var qty = form.find('.keypad-quantity').text();
    if (action == 'add' || action == 'subtract') {
        if (qty != '0') {
            if (action == 'subtract') {
                qty = '-' + qty;
            }

            if (uom == 'CS') {
                form.find('[name="cases"]').val(qty);
            } else { // units
                form.find('[name="units"]').val(qty);
            }

            if (action == 'add' && mode == 'expired') {
                var expiry = form.find('input[name="expiration_date"]');
                if (! /^\d{4}-\d{2}-\d{2}$/.test(expiry.val())) {
                    alert("Please enter a valid expiration date.");
                    expiry.focus();
                    return;
                }
            }

            form.submit();
        }
    }
});


// handle inventory save button
$(document).on('click', '.inventory-actions button.save', function() {
    var form = $(this).parents('form:first');
    var uom = form.find('[name="keypad-uom"]:checked').val();
    var qty = form.find('.keypad-quantity').text();
    if (uom == 'CS') {
        form.find('input[name="cases"]').val(qty);
    } else { // units
        form.find('input[name="units"]').val(qty);
    }
    form.submit();
});
