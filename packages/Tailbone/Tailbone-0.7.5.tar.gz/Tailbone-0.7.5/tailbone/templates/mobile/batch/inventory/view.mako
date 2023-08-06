## -*- coding: utf-8; -*-
<%inherit file="/mobile/batch/view.mako" />

<%def name="title()">${h.link_to("Inventory", url('mobile.batch.inventory'))} &raquo; ${batch.id_str}</%def>

${form.render()|n}

% if not batch.executed and not batch.complete:
    <br />
    ${h.text('upc-search', class_='inventory-upc-search', placeholder="Enter UPC", autocomplete='off', **{'data-type': 'search', 'data-url': url('mobile.batch.inventory.row_from_upc', uuid=batch.uuid)})}
% endif

% if master.has_rows:
    <br />
    ${grid.render_complete()|n}
% endif

% if not batch.executed and not batch.complete:
    <br />
    ${h.form(request.route_url('mobile.batch.inventory.mark_complete', uuid=batch.uuid))}
    ${h.csrf_token(request)}
    ${h.hidden('mark-complete', value='true')}
    <button type="submit">Mark Batch as Complete</button>
% endif
