## -*- coding: utf-8; -*-
<%inherit file="/mobile/batch/view_row.mako" />
<%namespace file="/mobile/keypad.mako" import="keypad" />

## TODO: this is broken for actual page (header) title
<%def name="title()">${h.link_to("Inventory", url('mobile.batch.inventory'))} &raquo; ${h.link_to(instance.batch.id_str, url('mobile.batch.inventory.view', uuid=instance.batch_uuid))} &raquo; ${row.upc.pretty()}</%def>

<%
   unit_uom = 'LB' if row.product and row.product.weighed else 'EA'

   if row.cases:
       uom = 'CS'
   elif row.units:
       if row.product and row.product.weighed:
           uom = 'LB'
       else:
           uom = 'EA'
   elif row.case_quantity:
       uom = 'CS'
   else:
       uom = 'EA'
%>

<div class="ui-grid-a">
  <div class="ui-block-a">
    % if instance.product:
        <h3>${row.brand_name or ""}</h3>
        <h3>${row.description} ${row.size}</h3>
        <h3>${h.pretty_quantity(row.case_quantity)} ${unit_uom} per CS</h3>
    % else:
        <h3>${row.description}</h3>
    % endif
  </div>
  <div class="ui-block-b">
    ${h.image(product_image_url, "product image")}
  </div>
</div>

<p>
  currently:&nbsp; 
  % if uom == 'CS':
      ${h.pretty_quantity(row.cases or 0)}
  % else:
      ${h.pretty_quantity(row.units or 0)}
  % endif
  ${uom}
</p>

% if not row.batch.executed and not row.batch.complete:

    ${h.form(request.current_route_url())}
    ${h.csrf_token(request)}
    ${h.hidden('row', value=row.uuid)}
    ${h.hidden('cases')}
    ${h.hidden('units')}

    ${keypad(unit_uom, uom, quantity=row.cases or row.units or 1)}

    <fieldset data-role="controlgroup" data-type="horizontal" class="inventory-actions">
      <button type="button" class="ui-btn-inline ui-corner-all save">Save</button>
      <button type="button" class="ui-btn-inline ui-corner-all delete" disabled="disabled">Delete</button>
      ${h.link_to("Cancel", url('mobile.batch.inventory.view', uuid=row.batch.uuid), class_='ui-btn ui-btn-inline ui-corner-all')}
    </fieldset>

    ${h.end_form()}

% endif
