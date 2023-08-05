## -*- coding: utf-8; -*-
<%inherit file="/mobile/base.mako" />

<%def name="title()">${index_title} &raquo; New Batch</%def>

<%def name="page_title()">${h.link_to(index_title, index_url)} &raquo; New Batch</%def>

${h.form(request.current_route_url(), class_='ui-filterable', name='new-purchasing-batch')}
${h.csrf_token(request)}

<div class="field-wrapper vendor">
  <div class="field autocomplete" data-url="${url('vendors.autocomplete')}">
    ${h.hidden('vendor')}
    ${h.text('new-purchasing-batch-vendor-text', placeholder="Vendor name", autocomplete='off', data_type='search')}
    <ul data-role="listview" data-inset="true" data-filter="true" data-input="#new-purchasing-batch-vendor-text"></ul>
    <button type="button" style="display: none;">Change Vendor</button>
  </div>
</div>

<br />
${h.submit('submit', "Make Batch")}
${h.end_form()}
