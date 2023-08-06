## -*- coding: utf-8; -*-
## ##############################################################################
## 
## Default master 'index' template.  Features a prominent data table and
## exposes a way to filter and sort the data, etc.  Some index pages also
## include a "tools" section, just above the grid on the right.
## 
## ##############################################################################
<%inherit file="/base.mako" />

<%def name="title()">${index_title}</%def>

<%def name="content_title()"></%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">
    $(function() {

        $('.grid-wrapper').gridwrapper();

        % if master.mergeable and request.has_perm('{}.merge'.format(permission_prefix)):

            $('form[name="merge-things"] button').button('option', 'disabled', $('.grid').gridcore('count_selected') != 2);

            $('.grid-wrapper').on('gridchecked', '.grid', function(event, count) {
                $('form[name="merge-things"] button').button('option', 'disabled', count != 2);
            });

            $('form[name="merge-things"]').submit(function() {
                var uuids = $('.grid').gridcore('selected_uuids');
                if (uuids.length != 2) {
                    return false;
                }
                $(this).find('[name="uuids"]').val(uuids.toString());
                $(this).find('button')
                    .button('option', 'label', "Preparing to Merge...")
                    .button('disable');
            });

        % endif

        % if master.bulk_deletable and request.has_perm('{}.bulk_delete'.format(permission_prefix)):

        $('form[name="bulk-delete"] button').click(function() {
            var count = $('.grid-wrapper').gridwrapper('results_count', true);
            if (count === null) {
                alert("There don't seem to be any results to delete!");
                return;
            }
            if (! confirm("You are about to delete " + count + " ${model_title_plural}.\n\nAre you sure?")) {
                return
            }
            $(this).button('disable').button('option', 'label', "Deleting Results...");
            $('form[name="bulk-delete"]').submit();
        });

        % endif
    });
  </script>
</%def>

<%def name="context_menu_items()">
  % if master.results_downloadable_csv and request.has_perm('{}.results_csv'.format(permission_prefix)):
      <li>${h.link_to("Download results as CSV", url('{}.results_csv'.format(route_prefix)))}</li>
  % endif
  % if master.results_downloadable_xlsx and request.has_perm('{}.results_xlsx'.format(permission_prefix)):
      <li>${h.link_to("Download results as XLSX", url('{}.results_xlsx'.format(route_prefix)))}</li>
  % endif
  % if master.creatable and request.has_perm('{}.create'.format(permission_prefix)):
      % if master.creates_multiple:
          <li>${h.link_to("Create new {}".format(model_title_plural), url('{}.create'.format(route_prefix)))}</li>
      % else:
          <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
      % endif
  % endif
</%def>

<%def name="grid_tools()">
  % if master.mergeable and request.has_perm('{}.merge'.format(permission_prefix)):
      ${h.form(url('{}.merge'.format(route_prefix)), name='merge-things')}
      ${h.csrf_token(request)}
      ${h.hidden('uuids')}
      <button type="submit">Merge 2 ${model_title_plural}</button>
      ${h.end_form()}
  % endif
  % if master.bulk_deletable and request.has_perm('{}.bulk_delete'.format(permission_prefix)):
      ${h.form(url('{}.bulk_delete'.format(route_prefix)), name='bulk-delete')}
      ${h.csrf_token(request)}
      <button type="button">Delete Results</button>
      ${h.end_form()}
  % endif
</%def>

${grid.render_complete(tools=capture(self.grid_tools).strip(), context_menu=capture(self.context_menu_items).strip())|n}
