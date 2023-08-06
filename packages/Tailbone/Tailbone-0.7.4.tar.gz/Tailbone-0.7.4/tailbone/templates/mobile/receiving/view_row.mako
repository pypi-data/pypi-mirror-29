## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/view_row.mako" />
<%namespace file="/mobile/keypad.mako" import="keypad" />

<%def name="title()">Receiving &raquo; ${instance.batch.id_str} &raquo; ${row.upc.pretty()}</%def>

<%def name="page_title()">${h.link_to("Receiving", url('mobile.receiving'))} &raquo; ${h.link_to(instance.batch.id_str, url('mobile.receiving.view', uuid=instance.batch_uuid))} &raquo; ${row.upc.pretty()}</%def>

<%
   unit_uom = 'LB' if row.product and row.product.weighed else 'EA'

   uom = 'CS'
   if row.units_ordered and not row.cases_ordered:
       uom = 'EA'
%>


<div class="ui-grid-a">
  <div class="ui-block-a">
    % if instance.product:
        <h3>${instance.brand_name or ""}</h3>
        <h3>${instance.description} ${instance.size}</h3>
        <h3>${h.pretty_quantity(row.case_quantity)} ${unit_uom} per CS</h3>
    % else:
        <h3>${instance.description}</h3>
    % endif
  </div>
  <div class="ui-block-b">
    ${h.image(product_image_url, "product image")}
  </div>
</div>

<table>
  <tbody>
    <tr>
      <td>ordered</td>
      <td>${h.pretty_quantity(row.cases_ordered or 0)} / ${h.pretty_quantity(row.units_ordered or 0)}</td>
    </tr>
    <tr>
      <td>received</td>
      <td>${h.pretty_quantity(row.cases_received or 0)} / ${h.pretty_quantity(row.units_received or 0)}</td>
    </tr>
    <tr>
      <td>damaged</td>
      <td>${h.pretty_quantity(row.cases_damaged or 0)} / ${h.pretty_quantity(row.units_damaged or 0)}</td>
    </tr>
    <tr>
      <td>expired</td>
      <td>${h.pretty_quantity(row.cases_expired or 0)} / ${h.pretty_quantity(row.units_expired or 0)}</td>
    </tr>
  </tbody>
</table>

% if request.session.peek_flash('receiving-warning'):
    % for error in request.session.pop_flash('receiving-warning'):
        <div class="receiving-warning">${error}</div>
    % endfor
% endif

% if not instance.batch.executed and not instance.batch.complete:

    ${h.form(request.current_route_url(), class_='receiving-update')}
    ${h.csrf_token(request)}
    ${h.hidden('row', value=row.uuid)}
    ${h.hidden('cases')}
    ${h.hidden('units')}

    ${keypad(unit_uom, uom)}

    <table>
      <tbody>
        <tr>
          <td>
            <fieldset data-role="controlgroup" data-type="horizontal" class="receiving-mode">
              ${h.radio('mode', value='received', label="received", checked=True)}
              ${h.radio('mode', value='damaged', label="damaged")}
              ${h.radio('mode', value='expired', label="expired")}
            </fieldset>
          </td>
        </tr>
        <tr id="expiration-row" style="display: none;">
          <td>
            <div style="padding:10px 20px;">
              <label for="expiration_date">Expiration Date</label>
              <input name="expiration_date" type="date" value="" placeholder="YYYY-MM-DD" />
            </div>
          </td>
        </tr>
        <tr>
          <td>
            <fieldset data-role="controlgroup" data-type="horizontal" class="receiving-actions">
              <button type="button" data-action="add" class="ui-btn-inline ui-corner-all">Add</button>
              <button type="button" data-action="subtract" class="ui-btn-inline ui-corner-all">Subtract</button>
              ## <button type="button" data-action="clear" class="ui-btn-inline ui-corner-all ui-state-disabled">Clear</button>
            </fieldset>
          </td>
        </tr>
      </tbody>
    </table>

    ${h.end_form()}
% endif
