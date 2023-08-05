## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">New ${model_title_plural if master.creates_multiple else model_title}</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  ${self.disable_button_js()}
</%def>

<%def name="disable_button_js()">
  <script type="text/javascript">

    $(function() {

        $('form').submit(function() {
            var submit = $(this).find('input[type="submit"]');
            if (submit.length) {
                submit.button('disable').button('option', 'label', "Saving, please wait...");
            }
        });

    });
  </script>
</%def>

<%def name="context_menu_items()"></%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->
