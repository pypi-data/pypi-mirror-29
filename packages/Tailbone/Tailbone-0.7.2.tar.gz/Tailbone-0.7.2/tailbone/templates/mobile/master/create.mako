## -*- coding: utf-8; -*-
<%inherit file="/mobile/base.mako" />

<%def name="title()">New ${model_title}</%def>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->
