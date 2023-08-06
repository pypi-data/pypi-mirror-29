## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Ordering Worksheet</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  ${h.javascript_link(request.static_url('tailbone:static/js/numeric.js'))}
  <script type="text/javascript">

    var submitting = false;

    $(function() {

        $('.order-form td.current-order input').focus(function(event) {
            $(this).parents('tr:first').addClass('active');
        });

        $('.order-form td.current-order input').blur(function(event) {
            $(this).parents('tr:first').removeClass('active');
        });

        $('.order-form td.current-order input').keydown(function(event) {
            if (key_allowed(event) || key_modifies(event)) {
                return true;
            }
            if (event.which == 13) {
                if (! submitting) {
                    submitting = true;
                    var row = $(this).parents('tr:first');
                    var form = $('#item-update-form');
                    form.find('[name="product_uuid"]').val(row.data('uuid'));
                    form.find('[name="cases_ordered"]').val(row.find('input[name^="cases_ordered_"]').val() || '0');
                    form.find('[name="units_ordered"]').val(row.find('input[name^="units_ordered_"]').val() || '0');
                    $.post(form.attr('action'), form.serialize(), function(data) {
                        if (data.error) {
                            alert(data.error);
                        } else {
                            row.find('input[name^="cases_ordered_"]').val(data.row_cases_ordered);
                            row.find('input[name^="units_ordered_"]').val(data.row_units_ordered);
                            row.find('td.po-total').html(data.row_po_total);
                            $('.po-total .field').html(data.batch_po_total);
                        }
                        submitting = false;
                    });
                }
            }
            return false;
        });

    });
  </script>
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">

    .order-form th.department {
        border-top: 1px solid black;
        font-size: 1.2em;
        padding: 15px;
        text-align: left;
        text-transform: uppercase;
    }

    .order-form th.subdepartment {
        background-color: white;
        border-bottom: 1px solid black;
        border-top: 1px solid black;
        padding: 15px;
        text-align: left;
    }

    .order-form tr.active {
        border: 5px solid Blue;
    }

    .order-form td {
        border-right: 1px solid #000000;
        border-top: 1px solid #000000;
    }

    .order-form td.upc,
    .order-form td.case-qty,
    .order-form td.code,
    .order-form td.preferred,
    .order-form td.scratch_pad {
        text-align: center;
    }

    .order-form td.scratch_pad {
        width: 40px;
    }

    .order-form td.current-order input {
        text-align: center;
        width: 3em;
    }

    .order-form td.unit-cost,
    .order-form td.po-total {
        text-align: right;
    }

  </style>
</%def>


<%def name="context_menu_items()">
  <li>${h.link_to("Back to {}".format(model_title), url('ordering.view', uuid=batch.uuid))}</li>
</%def>


##############################
## page body
##############################

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">

  <div class="field-wrapper">
    <label>Vendor</label>
    <div class="field">${h.link_to(vendor, url('vendors.view', uuid=vendor.uuid))}</div>
  </div>

  <div class="field-wrapper">
    <label>Vendor Email</label>
    <div class="field">${vendor.email or ''}</div>
  </div>

  <div class="field-wrapper">
    <label>Vendor Fax</label>
    <div class="field">${vendor.fax_number or ''}</div>
  </div>

  <div class="field-wrapper">
    <label>Vendor Contact</label>
    <div class="field">${vendor.contact or ''}</div>
  </div>

  <div class="field-wrapper">
    <label>Vendor Phone</label>
    <div class="field">${vendor.phone or ''}</div>
  </div>

  ${self.extra_vendor_fields()}

  <div class="field-wrapper po-total">
    <label>PO Total</label>
    <div class="field">$${'{:0,.2f}'.format(batch.po_total or 0)}</div>
  </div>

</div><!-- form-wrapper -->

${self.order_form_grid()}

${h.form(url('ordering.worksheet_update', uuid=batch.uuid), id='item-update-form', style='display: none;')}
${h.csrf_token(request)}
${h.hidden('product_uuid')}
${h.hidden('cases_ordered')}
${h.hidden('units_ordered')}
${h.end_form()}


##############################
## methods
##############################

<%def name="extra_vendor_fields()"></%def>

<%def name="extra_count()">0</%def>

<%def name="extra_th()"></%def>

<%def name="extra_td(cost)"></%def>

<%def name="order_form_grid()">
  <div class="grid">
    <table class="order-form">
      <% column_count = 8 + len(header_columns) + (0 if ignore_cases else 1) + int(capture(self.extra_count)) %>
      % for department in sorted(departments.values(), key=lambda d: d.name if d else ''):
          <thead>
            <tr>
              <th class="department" colspan="${column_count}">Department
                % if department.number or department.name:
                    ${department.number} ${department.name}
                % else:
                    (N/A)
                % endif
              </th>
            </tr>
            % for subdepartment in sorted(department._order_subdepartments.values(), key=lambda s: s.name if s else ''):
                <tr>
                  <th class="subdepartment" colspan="${column_count}">Subdepartment
                    % if subdepartment.number or subdepartment.name:
                        ${subdepartment.number} ${subdepartment.name}
                    % else:
                        (N/A)
                    % endif
                  </th>
                </tr>
                <tr>
                  % for title in header_columns:
                      <th>${title}</th>
                  % endfor
                  % for data in history:
                      <th>
                        % if data:
                            % if data['purchase']['date_received']:
                                Rec.<br />
                                ${data['purchase']['date_received'].strftime('%m/%d')}
                            % elif data['purchase']['date_ordered']:
                                Ord.<br />
                                ${data['purchase']['date_ordered'].strftime('%m/%d')}
                            % else:
                                ??
                            % endif
                        % endif
                      </th>
                  % endfor
                  % if not ignore_cases:
                      <th>
                        ${batch.date_ordered.strftime('%m/%d')}<br />
                        Cases
                      </th>
                  % endif
                  <th>
                    ${batch.date_ordered.strftime('%m/%d')}<br />
                    Units
                  </th>
                  <th>PO Total</th>
                  ${self.extra_th()}
                </tr>
              </thead>
              <tbody>
                % for i, cost in enumerate(subdepartment._order_costs, 1):
                    <tr data-uuid="${cost.product_uuid}" class="${'even' if i % 2 == 0 else 'odd'}">
                      ${self.order_form_row(cost)}
                      % for data in history:
                          <td class="scratch_pad">
                            % if data:
                                <% item = data['items'].get(cost.product_uuid) %>
                                % if item:
                                    % if ignore_cases:
                                        % if item['units_received'] is not None:
                                            ${int(item['units_received'] or 0)}
                                        % elif item['units_ordered'] is not None:
                                            ${int(item['units_ordered'] or 0)}
                                        % endif
                                    % else:
                                        % if item['cases_received'] is not None or item['units_received'] is not None:
                                            ${'{} / {}'.format(int(item['cases_received'] or 0), int(item['units_received'] or 0))}
                                        % elif item['cases_ordered'] is not None or item['units_ordered'] is not None:
                                            ${'{} / {}'.format(int(item['cases_ordered'] or 0), int(item['units_ordered'] or 0))}
                                        % endif
                                    % endif
                                % endif
                            % endif
                          </td>
                      % endfor
                      % if not ignore_cases:
                          <td class="current-order">
                             ${h.text('cases_ordered_{}'.format(cost.uuid), value=int(cost._batchrow.cases_ordered or 0) if cost._batchrow else None)}
                          </td>
                      % endif
                      <td class="current-order">
                         ${h.text('units_ordered_{}'.format(cost.uuid), value=int(cost._batchrow.units_ordered or 0) if cost._batchrow else None)}
                      </td>
                      <td class="po-total">${'${:0,.2f}'.format(cost._batchrow.po_total or 0) if cost._batchrow else ''}</td>
                      ${self.extra_td(cost)}
                    </tr>
                % endfor
              </tbody>
          % endfor
      % endfor
    </table>
  </div>
</%def>

<%def name="order_form_row(cost)">
  <td class="upc">${get_upc(cost.product)}</td>
  <td class="brand">${cost.product.brand or ''}</td>
  <td class="desc">${cost.product.description} ${cost.product.size or ''}</td>
  <td class="case-qty">${h.pretty_quantity(cost.case_size)} ${"LB" if cost.product.weighed else "EA"}</td>
  <td class="code">${cost.code or ''}</td>
  <td class="preferred">${'X' if cost.preference == 1 else ''}</td>
  <td class="unit-cost">
    % if cost.unit_cost is not None:
        $${'{:0.2f}'.format(cost.unit_cost)}
    % endif
  </td>
</%def>
