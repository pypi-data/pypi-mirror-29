## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">

    $(function() {

        $('.worksheet .current-entry input').focus(function(event) {
            $(this).parents('tr:first').addClass('active');
        });

        $('.worksheet .current-entry input').blur(function(event) {
            $(this).parents('tr:first').removeClass('active');
        });

    });
  </script>
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">

    .worksheet tr.active {
        border: 5px solid Blue;
    }

    .worksheet .current-entry {
        text-align: center;
    }

    .worksheet .current-entry input {
        text-align: center;
        width: 3em;
    }

  </style>
</%def>

<%def name="worksheet_grid()"></%def>


${self.worksheet_grid()}
