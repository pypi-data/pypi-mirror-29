## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/view.mako" />

<%def name="title()">${index_title} &raquo; ${parent_title} &raquo; ${instance_title}</%def>

<%def name="page_title()">${h.link_to(index_title, index_url)} &raquo; ${h.link_to(parent_title, parent_url)} &raquo; ${instance_title}</%def>

${parent.body()}

% if master.mobile_rows_editable and instance_editable and request.has_perm('{}.edit_row'.format(permission_prefix)):
  ${h.link_to("Edit", url('mobile.{}.edit_row'.format(route_prefix), uuid=instance.batch_uuid, row_uuid=instance.uuid), class_='ui-btn')}
% endif
