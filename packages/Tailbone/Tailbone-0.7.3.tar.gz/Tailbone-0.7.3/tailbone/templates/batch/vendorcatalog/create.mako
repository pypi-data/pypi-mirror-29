## -*- coding: utf-8; -*-
<%inherit file="/batch/create.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">

    var vendormap = {
        % for i, parser in enumerate(parsers, 1):
            '${parser.key}': ${parser.vendormap_value|n}${',' if i < len(parsers) else ''}
        % endfor
    };

    $(function() {

        if ($('select[name="parser_key"] option:first').is(':selected')) {
            $('.vendor_uuid .autocomplete-container').hide();
        } else {
            $('.vendor_uuid input[name="vendor_uuid"]').val('');
            $('.vendor_uuid .autocomplete-display').hide();
            $('.vendor_uuid .autocomplete-display button').show();
            $('.vendor_uuid .autocomplete-textbox').val('');
            $('.vendor_uuid .autocomplete-textbox').show();
            $('.vendor_uuid .autocomplete-container').show();
        }

        $('select[name="parser_key"]').on('selectmenuchange', function() {
            if ($(this).find('option:first').is(':selected')) {
                $('.vendor_uuid .autocomplete-container').hide();
            } else {
                var vendor = vendormap[$(this).val()];
                if (vendor) {
                    $('.vendor_uuid input[name="vendor_uuid"]').val(vendor.uuid);
                    $('.vendor_uuid .autocomplete-textbox').hide();
                    $('.vendor_uuid .autocomplete-display span:first').text(vendor.name);
                    $('.vendor_uuid .autocomplete-display button').hide();
                    $('.vendor_uuid .autocomplete-display').show();
                    $('.vendor_uuid .autocomplete-container').show();
                } else {
                    $('.vendor_uuid input[name="vendor_uuid"]').val('');
                    $('.vendor_uuid .autocomplete-display').hide();
                    $('.vendor_uuid .autocomplete-display button').show();
                    $('.vendor_uuid .autocomplete-textbox').val('');
                    $('.vendor_uuid .autocomplete-textbox').show();
                    $('.vendor_uuid .autocomplete-container').show();
                    $('.vendor_uuid .autocomplete-textbox').focus();
                }
            }
        });

    });
  </script>
</%def>

${parent.body()}
