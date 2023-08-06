## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/view.mako" />

<%def name="title()">Receiving &raquo; ${instance.id_str}</%def>

<%def name="page_title()">${h.link_to("Receiving", url('mobile.receiving'))} &raquo; ${instance.id_str}</%def>

${form.render()|n}
<br />

% if not instance.executed and not instance.complete:
    ${h.text('upc-search', class_='receiving-upc-search', placeholder="Enter UPC", autocomplete='off', **{'data-type': 'search', 'data-url': url('mobile.receiving.lookup', uuid=batch.uuid)})}
    <br />
% endif

${grid.render_complete()|n}

% if not instance.executed and not instance.complete:
    <br /><br />
    ${h.form(request.route_url('mobile.receiving.mark_complete', uuid=instance.uuid))}
    ${h.csrf_token(request)}
    ${h.hidden('mark-complete', value='true')}
    <button type="submit">Mark Batch as Complete</button>
% endif
