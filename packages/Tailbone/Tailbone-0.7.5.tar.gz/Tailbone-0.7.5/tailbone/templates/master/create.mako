## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">New ${model_title_plural if master.creates_multiple else model_title}</%def>

<%def name="context_menu_items()"></%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->
