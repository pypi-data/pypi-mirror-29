## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">${instance_title_normal} @ ver ${transaction.id}</%def>

## TODO: this was basically copied from Revel diff template..need to abstract

<%def name="content_title()">
  <div style="float: right;">
    % if previous_transaction:
        ${h.link_to(u"« Older", url('{}.version'.format(route_prefix), uuid=instance.uuid, txnid=previous_transaction.id), class_='button')}
    % else:
        ${h.link_to(u"« Older", '#', class_='button', disabled='disabled')}
    % endif
    % if next_transaction:
        ${h.link_to(u"Newer »", url('{}.version'.format(route_prefix), uuid=instance.uuid, txnid=next_transaction.id), class_='button')}
    % else:
        ${h.link_to(u"Newer »", '#', class_='button', disabled='disabled')}
    % endif
  </div>
  <h1>${self.title()}</h1>
</%def>

<div class="form-wrapper">

  <div class="form">

    <div class="field-wrapper">
      <label>Changed</label>
      <div class="field">${h.pretty_datetime(request.rattail_config, changed)}</div>
    </div>

    <div class="field-wrapper">
      <label>Changed by</label>
      <div class="field">${transaction.user or ''}</div>
    </div>

    <div class="field-wrapper">
      <label>IP Address</label>
      <div class="field">${transaction.remote_addr}</div>
    </div>

    <div class="field-wrapper">
      <label>Comment</label>
      <div class="field">${transaction.meta.get('comment') or ''}</div>
    </div>

  </div>

</div><!-- form-wrapper -->

% for version in versions:

    <h2>${title_for_version(version)}</h2>

    % if version.previous and version.operation_type == continuum.Operation.DELETE:
        <table class="diff monospace deleted">
          <thead>
            <tr>
              <th>field name</th>
              <th>old value</th>
              <th>new value</th>
            </tr>
          </thead>
          <tbody>
            % for field in fields_for_version(version):
               <tr>
                 <td class="field">${field}</td>
                 <td class="value old-value">${repr(getattr(version.previous, field))}</td>
                 <td class="value new-value">&nbsp;</td>
               </tr>
            % endfor
          </tbody>
        </table>
    % elif version.previous:
        <table class="diff monospace dirty">
          <thead>
            <tr>
              <th>field name</th>
              <th>old value</th>
              <th>new value</th>
            </tr>
          </thead>
          <tbody>
            % for field in fields_for_version(version):
               <tr${' class="diff"' if getattr(version, field) != getattr(version.previous, field) else ''|n}>
                 <td class="field">${field}</td>
                 <td class="value old-value">${repr(getattr(version.previous, field))}</td>
                 <td class="value new-value">${repr(getattr(version, field))}</td>
               </tr>
            % endfor
          </tbody>
        </table>
    % else:
        <table class="diff monospace new">
          <thead>
            <tr>
              <th>field name</th>
              <th>old value</th>
              <th>new value</th>
            </tr>
          </thead>
          <tbody>
            % for field in fields_for_version(version):
               <tr>
                 <td class="field">${field}</td>
                 <td class="value old-value">&nbsp;</td>
                 <td class="value new-value">${repr(getattr(version, field))}</td>
               </tr>
            % endfor
          </tbody>
        </table>
    % endif

% endfor
