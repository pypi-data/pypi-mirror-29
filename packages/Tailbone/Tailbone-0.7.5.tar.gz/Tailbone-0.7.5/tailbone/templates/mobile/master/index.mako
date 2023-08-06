## -*- coding: utf-8; -*-
## ##############################################################################
## 
## Default master 'index' template for mobile.  Features a somewhat abbreviated
## data table and (hopefully) exposes a way to filter and sort the data, etc.
## 
## ##############################################################################
<%inherit file="/mobile/base.mako" />

<%def name="title()">${index_title}</%def>

% if master.mobile_creatable and request.has_perm('{}.create'.format(permission_prefix)):
    ${h.link_to("New {}".format(model_title), url('mobile.{}.create'.format(route_prefix)), class_='ui-btn ui-corner-all')}
% endif

${grid.render_complete()|n}
