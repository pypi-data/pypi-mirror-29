## -*- coding: utf-8; -*-
## ##############################################################################
## 
## Default master 'view' template for mobile.  Features a basic field list, and
## links to edit/delete the object when appropriate.
## 
## ##############################################################################
<%inherit file="/mobile/base.mako" />

<%def name="title()">${index_title} &raquo; ${instance_title}</%def>

<%def name="page_title()">${h.link_to(index_title, index_url)} &raquo; ${instance_title}</%def>

${form.render()|n}
