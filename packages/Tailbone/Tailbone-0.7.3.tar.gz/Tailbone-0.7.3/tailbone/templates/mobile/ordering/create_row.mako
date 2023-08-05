## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/create_row.mako" />

<%def name="page_title()">${h.link_to(index_title, index_url)} &raquo; ${h.link_to(instance_title, instance_url)} &raquo; Add Item</%def>

${parent.body()}
