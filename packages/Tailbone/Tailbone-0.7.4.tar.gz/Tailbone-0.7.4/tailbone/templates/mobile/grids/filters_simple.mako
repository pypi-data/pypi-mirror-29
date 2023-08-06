## -*- coding: utf-8; -*-
<div class="simple-filter">
  ${h.form(request.current_route_url(_query=None), method='get')}

  % for filtr in grid.iter_filters():
      ${h.hidden('{}.verb'.format(filtr.key), value=filtr.verb)}
      <fieldset data-role="controlgroup" data-type="horizontal">
        % for value, label in filtr.iter_choices():
            ${h.radio(filtr.key, value=value, label=label, checked=value == filtr.value)}
        % endfor
      </fieldset>
  % endfor

  ${h.end_form()}
</div><!-- simple-filter -->
