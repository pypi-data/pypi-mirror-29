
/******************************************
 * jQuery Mobile plugins for Tailbone
 *****************************************/

/******************************************
 * mobile autocomplete
 *****************************************/

(function($) {
    
    $.widget('tailbone.mobileautocomplete', {

        _create: function() {
            var that = this;

            // snag some element references
            this.search = this.element.find('.ui-input-search');
            this.hidden_field = this.element.find('input[type="hidden"]');
            this.text_field = this.element.find('input[type="text"]');
            this.ul = this.element.find('ul');
            this.button = this.element.find('button');

            // establish our autocomplete URL
            this.url = this.options.url || this.element.data('url');

            // NOTE: much of this code was copied from the jquery mobile demo site
            // https://demos.jquerymobile.com/1.4.5/listview-autocomplete-remote/
            this.ul.on('filterablebeforefilter', function(e, data) {

                var $input = $( data.input ),
                    value = $input.val(),
                    html = "";
                that.ul.html( "" );
                if ( value && value.length > 2 ) {
                    that.ul.html( "<li><div class='ui-loader'><span class='ui-icon ui-icon-loading'></span></div></li>" );
                    that.ul.listview( "refresh" );
                    $.ajax({
                        url: that.url,
                        data: {
                            term: $input.val()
                        }
                    })
                        .then( function ( response ) {
                            $.each( response, function ( i, val ) {
                                html += '<li data-uuid="' + val.value + '">' + val.label + "</li>";
                            });
                            that.ul.html( html );
                            that.ul.listview( "refresh" );
                            that.ul.trigger( "updatelayout");
                        });
                }

            });

            // when user clicks autocomplete result, hide search etc.
            this.ul.on('click', 'li', function() {
                var $li = $(this);
                that.search.hide();
                that.hidden_field.val($li.data('uuid'));
                that.button.text($li.text()).show();
                that.ul.hide();
            });

            // when user clicks "change" button, show search etc.
            this.button.click(function() {
                that.button.hide();
                that.ul.empty().show();
                that.hidden_field.val('');
                that.search.show();
                that.text_field.focus();
            });

        }

    });
    
})( jQuery );
