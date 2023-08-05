## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">

    var destination = null;

    function update_move_button() {
        var count = $('.grid tr:not(.header) td.checkbox input:checked').length;
        $('form[name="move-selected"] button')
            .button('option', 'label', "Move " + count + " selected to " + destination)
            .button('option', 'disabled', count < 1);
    }

    $(function() {

        update_move_button();

        $('.grid-wrapper').on('change', 'tr.header td.checkbox input', function() {
            update_move_button();
        });

        $('.grid-wrapper').on('click', 'tr:not(.header) td.checkbox input', function() {
            update_move_button();
        });

        $('form[name="move-selected"]').submit(function() {
            var uuids = [];
            $('.grid tr:not(.header) td.checkbox input:checked').each(function() {
                uuids.push($(this).parents('tr:first').data('uuid'));
            });
            if (! uuids.length) {
                return false;
            }
            $(this).find('[name="uuids"]').val(uuids.toString());
            $(this).find('button')
                .button('option', 'label', "Moving " + uuids.length + " messages to " + destination + "...")
                .button('disable');
        });

    });

  </script>
</%def>

<%def name="context_menu_items()">
  % if request.has_perm('messages.create'):
      <li>${h.link_to("Send a new Message", url('messages.create'))}</li>
  % endif
</%def>

${parent.body()}
