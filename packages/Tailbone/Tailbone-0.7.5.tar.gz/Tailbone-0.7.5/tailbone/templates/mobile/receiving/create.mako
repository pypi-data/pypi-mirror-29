## -*- coding: utf-8; -*-
<%inherit file="/mobile/base.mako" />

<%def name="title()">Receiving &raquo; New Batch</%def>

<%def name="page_title()">${h.link_to("Receiving", url('mobile.receiving'))} &raquo; New Batch</%def>

${h.form(request.current_route_url(), class_='ui-filterable', name='new-purchasing-batch')}
${h.csrf_token(request)}

% if vendor is Undefined:

    <div class="field-wrapper vendor">
      <div class="field autocomplete" data-url="${url('vendors.autocomplete')}">
        ${h.hidden('vendor')}
        ${h.text('new-purchasing-batch-vendor-text', placeholder="Vendor name", autocomplete='off', **{'data-type': 'search'})}
        <ul data-role="listview" data-inset="true" data-filter="true" data-input="#new-purchasing-batch-vendor-text"></ul>
        <button type="button" style="display: none;">Change Vendor</button>
      </div>
    </div>

    <br />
    ${h.submit('submit', "Find purchase orders")}
    ## <button type="button">New receiving from scratch</button>

% else: ## vendor is known

    <div class="field-wrapper vendor">
      <div class="field">
        ${h.hidden('vendor', value=vendor.uuid)}
        ${vendor}
      </div>
    </div>

    % if purchases:
        ${h.hidden('purchase')}
        <ul data-role="listview" data-inset="true">
          % for uuid, purchase in purchases:
              <li data-uuid="${uuid}">${h.link_to(purchase, '#')}</li>
          % endfor
        </ul>
    % else:
        <p>(no eligible purchases found)</p>
    % endif

    ## ${h.link_to("Receive from scratch for {}".format(vendor), '#', class_='ui-btn ui-corner-all')}

% endif

${h.end_form()}
