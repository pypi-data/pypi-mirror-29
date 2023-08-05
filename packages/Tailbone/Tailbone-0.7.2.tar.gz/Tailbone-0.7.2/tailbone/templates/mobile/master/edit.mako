## -*- coding: utf-8; -*-
<%inherit file="/mobile/base.mako" />

<%def name="title()">${index_title} &raquo; ${instance_title} &raquo; Edit</%def>

<%def name="page_title()">${h.link_to(index_title, index_url)} &raquo; ${h.link_to(instance_title, instance_url)} &raquo; Edit</%def>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->
