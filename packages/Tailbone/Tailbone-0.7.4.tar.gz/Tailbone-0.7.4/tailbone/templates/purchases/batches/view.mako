## -*- coding: utf-8; -*-
<%inherit file="/batch/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">
    $(function() {

        $('#order-form').click(function() {
            % if vendor_cost_count > vendor_cost_threshold:
                if (! confirm("This vendor has ${'{:,d}'.format(vendor_cost_count)} cost records.\n\n" +
                              "It is not recommended to use Order Form mode for such a large catalog.\n\n" +
                              "Are you sure you wish to do it anyway?")) {
                    return;
                }
            % endif
            $(this).button('disable').button('option', 'label', "Working, please wait...");
            location.href = '${url('purchases.batch.order_form', uuid=batch.uuid)}';
        });

        $('#receive-form').click(function() {
            $(this).button('disable').button('option', 'label', "Working, please wait...");
            location.href = '${url('purchases.batch.receiving_form', uuid=batch.uuid)}';
        });

    });
  </script>
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/purchases.css'))}
</%def>

<%def name="leading_buttons()">
  % if batch.mode == enum.PURCHASE_BATCH_MODE_ORDERING and not batch.complete and not batch.executed and request.has_perm('purchases.batch.order_form'):
      <button type="button" id="order-form">Ordering Form</button>
  % elif batch.mode == enum.PURCHASE_BATCH_MODE_RECEIVING and not batch.complete and not batch.executed and request.has_perm('purchases.batch.receiving_form'):
      <button type="button" id="receive-form">Receiving Form</button>
  % endif
</%def>

${parent.body()}
