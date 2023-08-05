## -*- coding: utf-8; -*-
## ##############################################################################
## 
## Default master 'versions' template, for showing an object's version history.
## 
## ##############################################################################
<%inherit file="/base.mako" />

<%def name="title()">${model_title_plural} » ${instance_title} » history</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">
    $(function() {
        $('.grid-wrapper').gridwrapper();
    });
  </script>
</%def>

<%def name="content_title()">
  <h1>History for ${instance_title}</h1>
</%def>

${grid.render_complete()|n}
