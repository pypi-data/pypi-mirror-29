## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/view.mako" />

${parent.body()}

% if master.has_rows:
    % if master.mobile_rows_creatable and not batch.executed and not batch.complete:
        ${h.link_to("Add Item", url('mobile.{}.create_row'.format(route_prefix), uuid=instance.uuid), class_='ui-btn ui-corner-all')}
    % endif
    <br />
    ${grid.render_complete()|n}
% endif

% if not batch.executed and request.has_perm('{}.edit'.format(permission_prefix)):
    % if batch.complete:
        ${h.form(request.route_url('mobile.{}.mark_pending'.format(route_prefix), uuid=batch.uuid))}
        ${h.csrf_token(request)}
        ${h.hidden('mark-pending', value='true')}
        ${h.submit('submit', "Mark Batch as Pending")}
        ${h.end_form()}
    % else:
        ${h.form(request.route_url('mobile.{}.mark_complete'.format(route_prefix), uuid=batch.uuid))}
        ${h.csrf_token(request)}
        ${h.hidden('mark-complete', value='true')}
        ${h.submit('submit', "Mark Batch as Complete")}
        ${h.end_form()}
    % endif
% endif
