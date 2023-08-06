## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    #product-main {
        margin-top: 1em;
        width: 80%;
    }
    #product-image {
        float: left;
    }
    .panel-wrapper {
        float: left;
        margin-right: 15px;
        width: 40%;
    }
  </style>
</%def>

##############################
## page body
##############################

<div class="form-wrapper">
  <ul class="context-menu">
    ${self.context_menu_items()}
  </ul>

  <div class="panel" id="product-main">
    <h2>Product</h2>
    <div class="panel-body">
      <div style="clear: none; float: left;">
        ${self.render_main_fields(form)}
      </div>
      % if image_url:
          ${h.image(image_url, "Product Image", id='product-image', width=150, height=150)}
      % endif
    </div>
  </div>

  <div class="panel-wrapper"> <!-- left column -->

    ${self.left_column()}

  </div> <!-- left column -->

  <div class="panel-wrapper"> <!-- right column -->

    ${self.right_column()}

  </div> <!-- right column -->

  % if buttons:
      ${buttons|n}
  % endif
</div>

##############################
## rendering methods
##############################

<%def name="render_main_fields(form)">
  ${form.render_field_readonly('upc')}
  ${form.render_field_readonly('brand')}
  ${form.render_field_readonly('description')}
  ${form.render_field_readonly('size')}
  ${form.render_field_readonly('unit_size')}
  ${form.render_field_readonly('unit_of_measure')}
  ${form.render_field_readonly('unit')}
  ${form.render_field_readonly('pack_size')}
  ${form.render_field_readonly('case_size')}
  ${self.extra_main_fields(form)}
</%def>

<%def name="left_column()">
  <div class="panel">
    <h2>Pricing</h2>
    <div class="panel-body">
      ${self.render_price_fields(form)}
    </div>
  </div>
  <div class="panel">
    <h2>Flags</h2>
    <div class="panel-body">
      ${self.render_flag_fields(form)}
    </div>
  </div>
  ${self.extra_left_panels()}
</%def>

<%def name="right_column()">
  ${self.organization_panel()}
  ${self.movement_panel()}
  ${self.sources_panel()}
  ${self.notes_panel()}
  ${self.ingredients_panel()}
  ${self.lookup_codes_panel()}
  ${self.extra_right_panels()}
</%def>

<%def name="extra_main_fields(form)"></%def>

<%def name="organization_panel()">
  <div class="panel">
    <h2>Organization</h2>
    <div class="panel-body">
      ${self.render_organization_fields(form)}
    </div>
  </div>
</%def>

<%def name="render_organization_fields(form)">
    ${form.render_field_readonly('department')}
    ${form.render_field_readonly('subdepartment')}
    ${form.render_field_readonly('category')}
    ${form.render_field_readonly('family')}
    ${form.render_field_readonly('report_code')}
</%def>

<%def name="render_price_fields(form)">
    ${form.render_field_readonly('price_required')}
    ${form.render_field_readonly('regular_price')}
    ${form.render_field_readonly('current_price')}
    ${form.render_field_readonly('current_price_ends')}
    ${form.render_field_readonly('deposit_link')}
    ${form.render_field_readonly('tax')}
</%def>

<%def name="render_flag_fields(form)">
    ${form.render_field_readonly('weighed')}
    ${form.render_field_readonly('discountable')}
    ${form.render_field_readonly('special_order')}
    ${form.render_field_readonly('organic')}
    ${form.render_field_readonly('not_for_sale')}
    ${form.render_field_readonly('discontinued')}
    ${form.render_field_readonly('deleted')}
</%def>

<%def name="movement_panel()">
  <div class="panel">
    <h2>Movement</h2>
    <div class="panel-body">
      ${self.render_movement_fields(form)}
    </div>
  </div>
</%def>

<%def name="render_movement_fields(form)">
    ${form.render_field_readonly('last_sold')}
</%def>

<%def name="lookup_codes_panel()">
  <div class="panel-grid" id="product-codes">
    <h2>Additional Lookup Codes</h2>
    <div class="grid full no-border">
      <table>
        <thead>
          <th>Seq</th>
          <th>Code</th>
        </thead>
        <tbody>
          % for code in instance._codes:
              <tr>
                <td>${code.ordinal}</td>
                <td>${code.code}</td>
              </tr>
          % endfor
        </tbody>
      </table>
    </div>
  </div>
</%def>

<%def name="sources_panel()">
  <div class="panel-grid" id="product-costs">
    <h2>Vendor Sources</h2>
    <div class="grid full no-border">
      <table>
        <thead>
          <th>Pref.</th>
          <th>Vendor</th>
          <th>Code</th>
          <th>Case Size</th>
          <th>Case Cost</th>
          <th>Unit Cost</th>
          <th>Status</th>
        </thead>
        <tbody>
          % for i, cost in enumerate(instance.costs, 1):
              <tr class="${'even' if i % 2 == 0 else 'odd'}">
                <td class="center">${'X' if cost.preference == 1 else ''}</td>
                <td>
                  % if request.has_perm('vendors.view'):
                      ${h.link_to(cost.vendor, request.route_url('vendors.view', uuid=cost.vendor_uuid))}
                  % else:
                      ${cost.vendor}
                  % endif
                </td>
                <td class="center">${cost.code or ''}</td>
                <td class="center">${h.pretty_quantity(cost.case_size)}</td>
                <td class="right">${'$ %0.2f' % cost.case_cost if cost.case_cost is not None else ''}</td>
                <td class="right">${'$ %0.4f' % cost.unit_cost if cost.unit_cost is not None else ''}</td>
                <td>${"discontinued" if cost.discontinued else "available"}</td>
              </tr>
          % endfor
        </tbody>
      </table>
    </div>
  </div>
</%def>

<%def name="notes_panel()">
  <div class="panel">
    <h2>Notes</h2>
    <div class="panel-body">
      <div class="field">${form.render_field_readonly('notes')}</div>
    </div>
  </div>
</%def>

<%def name="ingredients_panel()">
  <div class="panel">
    <h2>Ingredients</h2>
    <div class="panel-body">
      ${form.render_field_readonly('ingredients')}
    </div>
  </div>
</%def>

<%def name="extra_left_panels()"></%def>

<%def name="extra_right_panels()"></%def>
