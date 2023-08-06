
CHANGELOG
=========

0.7.5 (2018-03-12)
------------------

* Add desktop support for creating inventory batches.

* Expose vendor item code for purchase credits.

* Fix default create logic for vendors, products.

* Add changelog link for rattail-tempmon in upgrade diff.

* Add ``disable_submit_button()`` global JS function.

* Add basic support for making new product on-the-fly during mobile ordering.


0.7.4 (2018-02-27)
------------------

* Use all "normal" product form fields, for mobile view.

* Refactor ordering worksheet to use shared logic.

* Add download path for batch master views.

* Add basic mobile support for executing batches (with options).

* Add ``NumberInputWidget`` for ``<input type="number" />``.

* Add ``Form.mobile`` flag and set link button styles accordingly.

* Always show flash-error-style message when form has errors.

* Use ``Form.submit_label`` if present, or fall back to ``save_label``.

* Expose ``ship_method`` and ``notes_to_vendor`` for purchase, ordering batch.

* Bind batch to its execution options schema, when applicable.

* Don't set order date for new ordering batch when created via mobile.

* Don't allow row deletion if batch is marked complete.

* Add logic for editing default phone/email in base master view.

* Fix bug in users view when person field not present.


0.7.3 (2018-02-15)
------------------

* More tweaks for python 3.


0.7.2 (2018-02-14)
------------------

* Refactor all remaining forms to use colander/deform.

* Coalesce 'forms2' => 'forms' package.

* Remove dependencies: FormAlchemy, FormEncode, pyramid_simpleform, pyramid_debugtoolbar

* Misc. cleanup for Python 3.

* Add generic 'login_as_home' setting.

* Add tailbone version to base stylesheet URLs.


0.7.1 (2018-02-10)
------------------

* Make it easier to hide buttons for a form.

* Let forms choose *not* to auto-disable their cancel button.

* Add 'newstyle' behavior for ``Form.validate()``.

* Add some basic ORM object field types for new forms.

* Make sure each grid has unique set of actions.

* Add 'gridcore' jQuery plugin, for core behavior.

* Allow passing arbitrary attrs when rendering grid.

* Refactor mobile receiving to use colander/deform.

* Refactor mobile inventory to use colander/deform.

* Refactor user login, change password to use colander/deform.

* Fix some bugs with importer batch views.


0.7.0 (2018-02-07)
------------------

* Coalesce all master views back to single base class.

* Add ``append()`` and ``replace()`` methods for core Grid class.

* Show year dropdown by default for jQuery UI date pickers.

* Don't process file for new batch unless field is present.

* Add setting for "force home" mobile behavior.

* Add 'plain' and 'jquery' templates for deform select widget.

* Add "hidden" concept for form fields.

* Add ``Form.show_cancel`` flag, for hiding that button.

* Let each form define its "save" button text.

* Add master view for ``EmailAttempt``.

* Avoid "auto disable" button logic for new message form.

* Add better UPC validation for mobile receiving.


0.6.69 (2018-02-01)
-------------------

* Add proper enum for inventory batch "count mode" filter.

* Fix bugs when making inventory batch on mobile.


0.6.68 (2018-01-31)
-------------------

* Cap zope.sqlalchemy dependency at pre-1.0.


0.6.67 (2018-01-30)
-------------------

* Fix permission bug when adding row in mobile receiving.

* Fix mobile logout behavior.

* Always redirect to mobile home page, if "other" page is refreshed.


0.6.66 (2018-01-29)
-------------------

* Add support for detaching Person from Customer.

* Allow disabling auto-dismiss of flash messages on mobile.

* Add ``FieldList`` wrapper for grid columns list.

* Show "unit cost" column by default, for products grid.

* Improve case/unit quantity validation for order worksheet.

* Show new 'confirmed' field for brands table.

* Add support for extra column(s) in timesheet view table.

* Add generic "download results as XLSX" feature.

* Add vendor links in cost grid when viewing product.

* Show "buttons" when viewing an object, with forms2 (i.e. Execute Batch).

* Refactor "most" remaining batch views etc. to use master3.


0.6.65 (2018-01-24)
-------------------

* Fix some master3 edit issues for products view.

* Let custom inventory batch view override logic for mobile UPC scanning.

* Show new ``cashback`` field for Trainwreck transaction.

* Add 'delete-instance' class to delete link when viewing a record.


0.6.64 (2018-01-22)
-------------------

* Warn if user "scans" UPC with more than 14 digits, for mobile inventory.

* Add option for preventing new inventory batch rows for unknown products.

* Add ``creates_multiple`` flag for master view.

* Add basic support for per-page help URL.


0.6.63 (2018-01-16)
-------------------

* Fix bug when locating association proxy column.

* Fix client field when creating / editing tempmon probe.

* Allow editing of inventory batch count mode and reason code.


0.6.62 (2018-01-11)
-------------------

* Fix dialog button click event when executing price batch (for Chrome).

* Fix some mobile view URLs.

* Show case quantity for inventory batch rows.

* Let custom schema node start out with empty children.

* Allow passing None to ``Form.set_renderer()``.


0.6.61 (2018-01-11)
-------------------

* Provide some default readonly form field renderers.

* Fix row query bug when deleting batch row.


0.6.60 (2018-01-10)
-------------------

* Refactor several straggler views to use master3.

* Add first attempt at master3 for batch views.


0.6.59 (2018-01-08)
-------------------

* Fix bug when printing product label.


0.6.58 (2018-01-08)
-------------------

* Tweak diff styles when viewing upgrade.


0.6.57 (2018-01-07)
-------------------

* Fix some styles for execution options dialog.

* Show 'static_prices' flag for label batches.

* Add field name as wrapper class name.

* Change how select menus are enhanced for batch exec options.

* Add view for InventoryAdjustmentReason model.

* Stop setting execution details when multiple batches executed.

* Add empty default when displaying values in grid.

* Let grids be paginated even when they have no model class.

* Exclude JS for refreshing batch unless it's relevant.

* Tweak conditions for CSV row download link.

* Add basic support for row grid view links.

* Refactor away the ``row_route_prefix`` concept.

* Add ``row_title`` to template context for ``view_row``.

* Tweak ``diffs.css`` and refactor 'view_version' template to use it.

* Add basic UI support for "importer batch" feature.


0.6.56 (2018-01-05)
-------------------

* Fix bug when making batch from product query.


0.6.55 (2018-01-04)
-------------------

* Add "price required" flag to product view.

* Add a bit more flexibility to jquery time input values.

* Show row count field when viewing vendor catalog batch.

* Tweak product filter for report code name.

* Refactor forms logic when making batch from product query.


0.6.54 (2017-12-20)
-------------------

* Provide sane width for filter value dropdowns.


0.6.53 (2017-12-19)
-------------------

* Accept ``value_enum`` kwarg when creating grid filter.


0.6.52 (2017-12-08)
-------------------

* Add transaction "System ID" field for Trainwreck.

* Add ``Grid.set_sort_defaults()`` method.

* Change template prefix for vendor catalog batches.

* Add basic "helptext" support for forms2.

* Add cleared/selected callbacks for jquery autocomplete in forms2.

* Add ``Grid.remove_filter()`` method.

* Add custom schema type for jQuery time picker data.

* Refactor lots of views to use master3.


0.6.51 (2017-12-03)
-------------------

* Refactor customers view to use master3.

* Add custom ``FieldList`` class for forms2 field list.

* Auto-scroll window as needed to ensure drop-down choices are visible.

* Hide status when creating new purchasing batch.

* Add "manually priced" awareness to pricing batch UI.

* Add batch description to page body title.

* Fix batch row count when bulk-deleting rows.

* Allow bulk delete of label batch rows.

* Expose description and notes for label batches.

* Let batch views allow or deny "execute results" option.

* Allow "execute results" for inventory batches.

* Fix permission bug for mobile inventory batch.

* Expose default address for customers view.


0.6.50 (2017-11-21)
-------------------

* Set widget when defining enum for a form2 field.

* Add date/time-picker, autocomplete support for forms2 (deform).

* Add colander magic for association proxy fields.


0.6.49 (2017-11-19)
-------------------

* Improve auto-disable logic for some form buttons.

* Fix (hack) for editing some department flags.


0.6.48 (2017-11-11)
-------------------

* Accept ``None`` as valid arg for ``Grid.set_filter()``.


0.6.47 (2017-11-08)
-------------------

* Fix manifest to include *.pt deform templates


0.6.46 (2017-11-08)
-------------------

* Add ``json`` to global template context


0.6.45 (2017-11-01)
-------------------

* Add product and personnel flags for Department

* Add sorters, filters for Product regular, current price

* Add "text" type for new form fields

* Add description, notes for pricing batches


0.6.44 (2017-10-29)
-------------------

* Fix join bug for Upgrades table when sorting by executor


0.6.43 (2017-10-29)
-------------------

* Add "make user" button when viewing person w/ no user account


0.6.42 (2017-10-28)
-------------------

* Add cashier info, upload time for Trainwreck transaction views


0.6.41 (2017-10-25)
-------------------

* Add support for validator and required flag, for new forms

* Use master3 view for datasync changes


0.6.40 (2017-10-24)
-------------------

* Add grid filter which treats empty string as NULL

* Fix value auto-selection for enum grid filters

* Add ``item_id`` to trainwreck views

* Expose ``Person.users`` relationship (readonly)


0.6.39 (2017-10-20)
-------------------

* Fix bug with products view config


0.6.38 (2017-10-19)
-------------------

* Add "local" datetime renderer for new grids, forms

* Make CSRF protection optional (but on by default)

* Convert user feedback mechanism to use modal dialog

* Add 'active' column to Users table view

* Add "download row results as CSV" feature to master view

* Add support for setting default field values on new forms

* Add 'currency' field type for new forms

* Allow passing ``None`` to ``Grid.set_joiner()``


0.6.37 (2017-09-28)
-------------------

* Fix data type/size issue with CSV download

* Don't set batch input file on creation, if no file exists

* Add "auto-enhance" select field template for deform

* Add ability to override schema node for custom deform fields

* Fix deform widget resource inclusion for master/create template

* Pass form along to ``before_create_flush()`` in master3

* Add "populatable" for master views (populating new objects with progress)

* Add 'duration' type for new form fields


0.6.36 (2017-09-15)
-------------------

* Fix user field rendering when no person associated

* Add generic support for downloading list results as CSV

* Tweak title for master view row template


0.6.35 (2017-08-30)
-------------------

* Fix some bugs for rendering upgrade package diffs


0.6.34 (2017-08-18)
-------------------

* Fix mobile inventory template

* Add extra perms for creating inventory batch w/ different modes

* Allow batch execution to require options on a per-batch basis

* Convert more views to master3:
  departments, subdepartments, categories, brands, bouncer, customer groups

* Override deform template for checkbox field; fix label behavior

* Show all grid actions by default, if there are 3 or less

* Use shared logic for executing upgrade


0.6.33 (2017-08-16)
-------------------

* Add ``LocalDateTimeFieldRenderer`` for formalchemy

* Fix auto-disable button on form submit, per Chrome issues


0.6.32 (2017-08-15)
-------------------

* Add generic changelog link for rattail/tailbone packages

* Let handler delete files when deleting upgrade

* Add mechanism for user to bulk-change status for purchase credits

* Tweak how pyramid config is created during app startup, for tests

* Fix permission used for mobile receiving item lookup


0.6.31 (2017-08-13)
-------------------

* Add show all vs. show diffs for upgrade packages

* Add initial support for changelog links for upgrade package diffs

* Add prev/next buttons when viewing upgrade details

* Merge 'better' theme into base templates


0.6.30 (2017-08-12)
-------------------

* Make product field renderer allow override of link text rendering


0.6.29 (2017-08-11)
-------------------

* Various tweaks to inventory batch logic (zero-all mode etc.)

* Fix join bug for users grid

* Flush session once every 1000 records when bulk-deleting


0.6.28 (2017-08-09)
-------------------

* Fix clone config bug for label batches


0.6.27 (2017-08-09)
-------------------

* Improve inventory support, plus "hiding" person data while still using it

* Fix encoding bug when reading stdout during upgrade


0.6.26 (2017-08-09)
-------------------

* Add awareness of upgrade exit code, success/fail

* Add support for cloning an upgrade record

* Add running display of stdout.log when executing upgrade


0.6.25 (2017-08-08)
-------------------

* Specify ``expire_on_commit`` for tailbone db session


0.6.24 (2017-08-08)
-------------------

* Fix bug which caused new empty worked shift when editing time sheet


0.6.23 (2017-08-08)
-------------------

* Fix bulk-delete for batch rows, allow it for pricing batches

* Fix permission check for deleting single batch rows

* Fix numeric filter to allow 3 decimal places by default


0.6.22 (2017-08-08)
-------------------

* Remove unwanted import (which broke versioning)

* Add some links to employees grid


0.6.21 (2017-08-08)
-------------------

* Refactor progress bars somewhat to allow file-based sessions

* Fix recipients renderer for email settings grid

* Improve status tracking for upgrades; add package version diff


0.6.20 (2017-08-07)
-------------------

* Record become/stop root user events

* Make datasync changes bulk-deletable

* Add basic support for performing / tracking app upgrades


0.6.19 (2017-08-04)
-------------------

* Record basic user login/logout events

* Expose UserEvent table in UI


0.6.18 (2017-08-04)
-------------------

* Add progress support for bulk deletion

* Make tempmon readings bulk-deletable


0.6.17 (2017-08-04)
-------------------

* Various view tweaks


0.6.16 (2017-08-04)
-------------------

* Add auto-links for most grids

* Fix row highlighting for sources panel on product view


0.6.15 (2017-08-03)
-------------------

* Allow product field renderer to suppress hyperlink

* Add 'data-uuid' attr for mobile grid list items, if applicable

* Initial (partial) support for mobile ordering

* Some tweaks to ordering batch views

* Fix bug when request.user becomes unattached from session (?)

* Add view for consuming new batch ID

* Add some links to various grid columns

* Fix bug in master view_row


0.6.14 (2017-08-01)
-------------------

* Make login template use same logo as home page

* Fix how we detect grid settings presence in user session

* Improve verbiage for exception view

* Fix styles for message compose template

* Various improvements to batch worksheets, index links etc.

* Fix batch links when viewing purchase object

* Add "on order" count to products grid, tweak product notes panel


0.6.13 (2017-07-26)
------------------

* Allow master view to decide whether each grid checkbox is checked


0.6.12 (2017-07-26)
------------------

* Add basic support for product inventory and status

* Stop allowing pre-0.7 SQLAlchemy


0.6.11 (2017-07-18)
------------------

* Tweak some basic styles for forms/grids

* Add new v3 master with v2 forms, with colander/deform


0.6.10 (2017-07-18)
------------------

* Fix grid bug if "current page" becomes invalid


0.6.9 (2017-07-15)
------------------

* Expose version history for all supported tables


0.6.8 (2017-07-14)
------------------

* Provide default renderers for SA mapped tables, where possible

* Add flexible grid class for v3 grids for width=half etc.

* Final grid refactor; we now have just 'grids' :)

* Refactor (coalesce) all batch-related templates


0.6.7 (2017-07-14)
------------------

* Fix master view ``get_effective_data()`` for v3 grids


0.6.6 (2017-07-14)
------------------

* Fix bug for printing one-off product labels


0.6.5 (2017-07-14)
------------------

* Fix template/styles for v3 grid views, add purchasing batch status


0.6.4 (2017-07-14)
------------------

* Add new "v3" grids, refactor all views to use them


0.6.3 (2017-07-13)
------------------

* Sort mobile receiving batches by ID desc

* Add initial/basic support for "simple" mobile grid filter w/ radio buttons

* Add filter support for mobile row grid; plus mark receiving as complete

* Disable unused Clear button for mobile receiving

* Add logic for mobile receiving if product not in batch and/or system

* Prevent mobile receiving actions for batch which is complete or executed

* Fix bug with mobile receiving UPC lookup; require stronger "create row" perm

* Stop using popup for expiration date, for mobile receiving

* Add global key handler for mobile receiving, for scanner wedge input

* Make all batches support mobile by default

* Add basic support for viewing inventory batches on mobile

* Refactor keypad widget for mobile receiving

* Add unit cost for inventory batches


0.6.2 (2017-07-10)
------------------

* Fix CS/EA bug for mobile receiving


0.6.1 (2017-07-07)
------------------

* Switch license to GPL v3 (no longer Affero)

* Fix broken product image tag, per webhelpers2


0.6.0 (2017-07-06)
------------------

Main reason for bumping version is the (re-)addition of data versioning support
using SQLAlchemy-Continuum.  This feature has been a long time coming and while
not yet fully implemented, we have a significant head start.

* Add custom default grid row size for Trainwreck items

* Make hyperlink optional for employee field renderer

* Tweak how customer/person relationships are displayed

* Add initial support for expiration date for mobile receiving

* Make Person.employee field readonly

* Rearrange some imports to ensure ``rattail.db.model`` comes last

* Add basic versioning history support for master view

* Remove old-style continuum version views

* Remove all "old-style" (aka. version 1) grids

* Remove all old-style views: grids, CRUD, versions etc.

* Refactor to use webhelpers2 etc. instead of older 'webhelpers'


0.5.104 (2017-06-22)
--------------------

* Add basic views for Trainwreck transactions

* Add ``AlchemyLocalDateTimeFilter``

* Add row count as available column to batch header grids

* Try to keep batch status updated; display it for handheld batches

* Tweak display of inventory/label batches to reflect multiple handheld batches

* Add way to execute multiple handheld batches (search results) at once

* Fix batch row count when deleting a row

* Make case/unit quantities prettier within Inventory batch rows grid

* Sort (alphabetically) device type list field when making new handheld batch

* Allow bulk row deletion for vendor catalog batches


0.5.103 (2017-06-05)
--------------------

* Always add key as class to grid column headers; allow literal label


0.5.102 (2017-05-30)
--------------------

* Remove all views etc. for old-style batches

* Fix bug when updating Order Form data, if row.po_total is None


0.5.101 (2017-05-25)
--------------------

* Fix subtle bug when identifying purchase batch row on order form update

* Remove references to deprecated batch handler methods

* Add validation for unique name when creating new Setting

* Simplify page title display for mobile base template

* Refactor "purchasing" batch views, split off "ordering"

* Add initial (full-ish) support for mobile receiving views

* Add support for bulk-delete of Pricing Batches

* Pad session timeout warning by 10 seconds, to account for drift

* Add highlight to active row within Order Form view

* Make 'notes' field use textarea renderer by default, for all batches

* Add basic ability to download Ordering Batch as Excel spreadsheet


0.5.100 (2017-05-18)
--------------------

* Allow batch view to override execution failure message

* Tweak some customer view/field rendering, to allow more customization

* Remove customer view template (use master default)

* Add basic support for Trainwreck database connectivity

* Remove unused 'fake_error' view

* Add basic 'robots.txt' support to CommonView

* Cap our pyramid_tm version until we can upgrade to pyramid 1.9

* Add daily hour totals when viewing or editing single employee time sheet

* Let config cause time sheet hours to display as HH.HH for some users

* Expose full-time flag and start date for employee view

* Add convenience ``dialog_button()`` JS function


0.5.99 (2017-05-05)
-------------------

* Add allowance for Escape key, in numeric.js

* Let a batch disallow bulk-deletion of its rows

* Add basic support for deletion speedbump for row data

* Remove lower version for Pyramid dependency, but restrict to pre-1.9


0.5.98 (2017-04-18)
-------------------

* Auto-save time sheet day editor on Enter press if time field is focused

* Add simple flag to prevent multiple submits for Order Form AJAX


0.5.97 (2017-04-04)
-------------------

* Fix signature for ``MasterView.get_index_url()``


0.5.96 (2017-04-04)
-------------------

* Tweak logic for registering exception view, to avoid test breakage

* Add basic paging grid/index support for mobile

* Tweak field label styles for mobile

* Allow config to define home page image URL


0.5.95 (2017-03-29)
-------------------

* Tweak organization panel for product view template

* Add logic to core View class, to force logout if user becomes inactive

* Detect "backwards" shift when time sheet is edited, alert user

* Add default view for unhandled exceptions, configure only for production

* Add basic table listing view, with rough estimate row counts

* Add 'status' column to vendor cost table in product view

* Various template standardization tweaks


0.5.94 (2017-03-25)
-------------------

* Add ``CostFieldRenderer`` and tweak product view template

* Bump margin between grid and header table, i.e. buttons

* Broad refactor to improve customization of purchase order form etc.

* Fix route sequence for people autocomplete

* Fix bugs when checking for 'chuck' in demo mode

* Add unit item and pack size fields to product view


0.5.93 (2017-03-22)
-------------------

* Add 'is_any' verb to integer grid filters

* Add more variations of project name when creating via scaffold

* Various tweaks to the customer and person views/forms

* Add basic "mobile index" master view, plus support for demo mode

* Refactor the batch file field renderer somewhat

* Move ``notfound()`` method to core ``View`` class

* Add ``BatchMasterView.add_file_field()`` convenience method

* Add ``extra_main_fields()`` method to product view template

* Allow config to override jQuery UI version

* Add master view for Report Output data model


0.5.92 (2017-03-14)
-------------------

* Tweak grid configuration for Employees view

* Add trailing '?' for employee time sheet when hours are incomplete


0.5.91 (2017-03-03)
-------------------

* Add 'discontinued' flag to product view


0.5.90 (2017-03-01)
-------------------

* Add notes, ingredients to product view


0.5.89 (2017-02-24)
-------------------

* Expose/honor per-role session timeouts

* Fix daylight savings bug when cloning schedule from previous week

* Expose notes field for purchasing batches

* Add some product flags (kosher vegan etc.) to view fieldset

* Add initial support for native product images


0.5.88 (2017-02-21)
-------------------

* Fix session reference bug in schedule view


0.5.87 (2017-02-21)
-------------------

* Fix bug in DateFieldRenderer when no format specified


0.5.86 (2017-02-21)
-------------------

* Add initial/basic views for customer orders data

* Be less aggressive when validating schedule edit form POST


0.5.85 (2017-02-19)
-------------------

* Add generic "bulk delete" support to MasterView

* Add beginnings of mobile receiving views


0.5.84 (2017-02-17)
-------------------

* Tweak progress template to better handle reset to 0%

* Add ability to merge 2 user accounts

* Increase size of Roles select when editing a User

* Add ability to filter Sent Messages by recipient name


0.5.83 (2017-02-16)
-------------------

* Set form id for new purchasing batch page

* Make sure invoice number is saved when making new purchasing batch

* Tweak product view page styles (new grids etc.)

* Add support for client-side session timeout warning


0.5.82 (2017-02-14)
-------------------

* Collapse grid actions if there are only 2

* Add master view for generic exports

* Make some product fields readonly

* Make datasync changes viewable

* Redirect to login page when Forbidden happens with anonymous user

* Tweak styles for Send Message page

* Tweak form handling for sending a new message, for more customization

* Advance to password field when Enter pressed on username, login page

* Add way for ``login_user()`` to set different timeout depending on nature of login


0.5.81 (2017-02-11)
-------------------

* Add config for redirecting user to home page after logout

* Refactor logic used to login a user, for easier sharing

* Use ``pretty_hours()`` function where applicable


0.5.80 (2017-02-10)
-------------------

* Tweak renderer for Amount field for DepositLink view

* Tweak how regular/current price fields are handled for Product view

* Fix bug in base 'shifts' template if ``weekdays`` not in context


0.5.79 (2017-02-09)
-------------------

* Tweak product view template per rename of case_size field

* Refactor the Edit Time Sheet view for "autocommit" mode

* Don't render user field as hyperlink unless so configured

* Expose 'delay' field in tempmon client views

* Fix bug when first entry is empty for product on ordering form


0.5.78 (2017-02-08)
-------------------

* Add initial Find Roles/Users by Permission feature

* Fix sorting bug for Employee Time Sheet view


0.5.77 (2017-02-04)
-------------------

* Invoke timepicker to correct format of user input, for edit schedule/timesheet


0.5.76 (2017-02-04)
-------------------

* Add hyperlink to ``EmployeeFieldRenderer``

* Improve the grid for ``WorkedShift`` model a bit

* Add config flag for disabling option to "Clear Schedule"


0.5.75 (2017-02-03)
-------------------

* Fix probe filter for tempmon readings grid

* Be explicit about fieldset for pricing batch rows

* Let project override user authentication for login page

* Add basic support for per-user session timeout


0.5.74 (2017-01-31)
-------------------

* Refactor schedule / timesheet views for better separation of concerns


0.5.73 (2017-01-30)
-------------------

* Add pyramid_mako dependency, remove minimum version for rattail

* Add ability to edit employee time sheet

* Add 'target' kwarg for grid action links

* Add hyperlink to User field renderer

* Add min diff threshold param when making price batch from product query

* Add way for batch views to hide rows with given status code(s)


0.5.72 (2017-01-29)
-------------------

* Add basic support for cloning batches

* Tweaks to order form template etc., for purchasing batch

* Let master view with rows prevent sort/filter for row grid

* Add price diff column to pricing batch row grid

* Add warning highlight for pricing batch row if can't calculate price


0.5.71 (2017-01-24)
-------------------

* Improve columns, filters for TempMon Readings grid

* Add ability to merge subdepartments


0.5.70 (2017-01-11)
-------------------

* Fix CSRF token bug with email preview form, refactor to use webhelpers


0.5.69 (2017-01-06)
-------------------

* When making batch from products, build query *before* starting thread


0.5.68 (2017-01-03)
-------------------

* Prefer received quantities over ordered quantities, for Order Form history


0.5.67 (2017-01-03)
-------------------

* Add department UUID to JSON returned for "eligible purchases" when creating batch

* Set "order date" when creating new receiving batch

* Add "discarded" flag when receiving DMG/EXP products; add view for purchase credits

* Fix type error in grid numeric filter


0.5.66 (2016-12-30)
-------------------

* Tweak the "create" screen for purchase batches, for more customization


0.5.65 (2016-12-29)
-------------------

* Fix purchase batch execution, to redirect to Purchase *or* Batch

* Add extra perms for restricing which 'mode' of purchase batch user can create

* Refactor Order Form a bit to allow custom history data


0.5.64 (2016-12-28)
-------------------

* Tweak default "numeric" grid filter, to ignore UPC-like values

* Tweak default filter label for Batch ID


0.5.63 (2016-12-28)
-------------------

* Fix CSRF token bug for bulk-move message forms


0.5.62 (2016-12-22)
-------------------

* Fix CSRF token bug for old-style batch params form


0.5.61 (2016-12-21)
-------------------

* Fix master merge template/forms to include CSRF token


0.5.60 (2016-12-20)
-------------------

* Fix CSRF bug in Ordering Form template, make case quantity pretty

* Fix some bugs in product view template

* Update some enum references, render all purchase/batch cases/units fields as quantity


0.5.59 (2016-12-19)
-------------------

* Add ``QuantityFieldRenderer``

* Add style for 'half-width' grid


0.5.58 (2016-12-16)
-------------------

* Add ``ValidGPC`` formencode validator

* Overhaul the Receiving Form to account for "product not found" etc.

* Auto-append slash to URL when necessary

* Add "print receiving worksheet" feature, for 'ordered' purchases

* Add global CSRF protection

* Tweak some field renderers

* Overhaul product views a little, per customization needs


0.5.57 (2016-12-12)
-------------------

* Lots of changes for sake of mobile login / user menu etc.

* Add mobile support for datasync restart

* Make ``CurrencyFieldRenderer`` inherit from ``FloatFieldRenderer``

* Fix session bug in old CRUD views


0.5.56 (2016-12-11)
-------------------

* Show 'enabled' column in grid, fix prefix bug for email profiles

* Tweak flash message when sending email preview, in case it's disabled

* Hide first/last name for employee view, unless in readonly mode

* Add initial mobile templates: base, home, about


0.5.55 (2016-12-10)
-------------------

* Validate for unique tempmon probe config key

* Add 'restartable tempmon client' conditional logic


0.5.54 (2016-12-10)
-------------------

* Add new 'receiving form' for purchase batches

* Add support for 'department' field in purchases / batches

* Add generic 'not on file' product image for use as POD 404

* Add logic for handling Ctrl+V / Ctrl+X in numeric.js


0.5.53 (2016-12-09)
-------------------

* Fix bug when editing a data row


0.5.52 (2016-12-08)
-------------------

* Fix permission group label for email bounces

* Update footer text/link per new about page


0.5.51 (2016-12-07)
-------------------

* Fix permission / grid action bug for email profiles


0.5.50 (2016-12-07)
-------------------

* Tweak tempmon views a little, fix client restart logic

* Add 'extra_styles' to true base template

* Add new "bytestring" filter for grids that need it


0.5.49 (2016-12-05)
-------------------

* Allow delete for datasync changes

* Fix import bugs with tempmon views

* Use master view's session when creating form


0.5.48 (2016-12-05)
-------------------

* Tweak email config views, to support subject "templates"

* Refactor tempmon views to leverage rattail-tempmon database


0.5.47 (2016-11-30)
-------------------

* Fix bug in products view class


0.5.46 (2016-11-29)
-------------------

* Add basic 'about' page with some package versions

* Tweak fields for product view


0.5.45 (2016-11-28)
-------------------

* Fix styles for 'print schedule' page

* Add permission for bulk-delete of batch data rows


0.5.44 (2016-11-22)
-------------------

* Add some links between employees / people / customers views

* Add support for pricing batches

* Add initial views for tempmon clients/probes/readings


0.5.43 (2016-11-21)
-------------------

* Add support for receive/cost mode, purchase relation for purchase batches

* Bump jquery version

* Fix bug when downloading batch file


0.5.42 (2016-11-20)
-------------------

* Move ``get_batch_kwargs()`` to ``BatchMasterView``


0.5.41 (2016-11-20)
-------------------

* Add printer-friendly view for "full" employee schedule

* Fix some bugs etc. with batch views and templates


0.5.40 (2016-11-19)
-------------------

* Add size, extra link fields to product view template

* Refactor batch views / templates per rattail framework overhaul


0.5.39 (2016-11-14)
-------------------

* Make POD image for product view a bit more sane

* Disable save button when creating new object


0.5.38 (2016-11-11)
-------------------

* Tweak default factory for boolean grid filters

* Add support for more cases + units, more vendor fields, for new purchase batches


0.5.37 (2016-11-10)
-------------------

* Display sequence for product alt codes

* Change how we determine default 'grid key' for master views

* Add 'additive fields' concept to merge diff preview


0.5.36 (2016-11-09)
-------------------

* Add historical amounts to new purchase Order Form, allow extra columns etc.

* Tweak verbiage for merge template etc.


0.5.35 (2016-11-08)
-------------------

* Add support for new Purchase/Batch views, 'create row' master pattern

* Add basic views for label batches

* Add support for making new-style batches from products grid query

* Add initial support for viewing new purchase batch as Order Form

* Refactor how batch editing is done; don't include rows for that sometimes


0.5.34 (2016-11-02)
-------------------

* Add basic merge feature to ``MasterView``


0.5.33 (2016-10-27)
-------------------

* Fix template bug when deleting user

* Tweak default styles for home page

* Show vendor invoice rows as warning, if they have no case quantity

* Add 'vendor code' and 'vendor code (any)' filters for products grid

* Fix bug with how we auto-filter 'deleted' products (?)


0.5.32 (2016-10-19)
-------------------

* Fix / improve progress display somewhat

* Disable "true delete" button by default, when clicked

* Fix bug in batch ID field renderer, when displayed for new batch

* Add ``refresh_after_create`` flag for ``BatchMasterView``

* Disable a focus() call in menubar.js which messed with search filter focus

* Let any 'admin' user elevate to 'root' for full system access

* Update references to ``request.authenticated_userid``


0.5.31 (2016-10-14)
-------------------

* Add ability to edit employee schedule


0.5.30 (2016-10-10)
-------------------

* Tweak some things to make demo project more "out of the box"

* Add registration for 'rattail' template with Pyramid scaffold system

* Add 'tailbone' to global template context, update 'better' template footer

* Tweak how tailbone finds rattail config from pyramid settings

* Remove last references to 'edbob' package

* Strip whitespace from username field when editing User

* Fix couple of bugs for vendor catalog views

* Add size description to inventory report


0.5.29 (2016-10-04)
-------------------

* Add ``code`` field to Category views

* Add "bulk delete rows" feature to new batches view


0.5.28 (2016-09-30)
-------------------

* Add specific permissions for edit/delete of individual batch rows


0.5.27 (2016-09-26)
-------------------

* Add basic form validation when sending new messages

* Add "just in time" editable instance check for master view

* Add "refresh" button when viewing batch

* Add FormAlchemy-compatible validators for email address, phone number

* Improve validation for FormAlchemy date field renderer

* Fix row-level visibility for grid edit action

* Add a couple of extra verbs to base grid filter class

* Tweak how a grid filter factory is determined


0.5.26 (2016-09-01)
-------------------

* Add ``MasterView.listable`` flag for disabling grid view

* Fix permission group label bug for batch views

* Allow opt-out for "download batch row data as CSV" feature


0.5.25 (2016-08-23)
-------------------

* Tweak how we use DB session to fetch grid settings

* Add "sub-rows" support to MasterView class

* Refactor batch views to leverage MasterView sub-rows logic

* Refactor batch view/edit pages to share some "execution options" logic

* Add hook to customize timesheet shift rendering


0.5.24 (2016-08-17)
-------------------

* Fix bug in handheld batch view config


0.5.23 (2016-08-17)
-------------------

* Fix bug when viewing batch with no execution options


0.5.22 (2016-08-17)
-------------------

* Fix bug for handheld batch device type field


0.5.21 (2016-08-17)
-------------------

* Add ``MasterView.render()`` method for sake of common context/logic

* Add "empty" option to enum field renderers, if field allows empty value

* Add support for system-unique ID in batch views etc.

* Fix bug when deleting certain batches

* Fix bug in batch download URL

* Add basic support for batch execution options

* Add basic support for new handheld/inventory batches


0.5.20 (2016-08-13)
-------------------

* Add null / not null verbs back to default boolean grid filter


0.5.19 (2016-08-12)
-------------------

* Only show granted permissions when viewing role details

* Expose 'enabled' flag for email profile/settings

* Add permissions field when viewing user details


0.5.18 (2016-08-10)
-------------------

* Add ``render_progress()`` method to core view class

* Add hopefully generic ``FileFieldRenderer``


0.5.17 (2016-08-09)
-------------------

* Add support for 10-key hyphen/period keys for numeric input fields


0.5.16 (2016-08-05)
-------------------

* Fallback to empty string for email preview recipient, if current user has no address

* Allow negative sign, decimal point for "numeric" text fields


0.5.15 (2016-07-27)
-------------------

* Add initial attempt at 'better' theme

* Add ``CodeTextAreaFieldRenderer``, refactor label profile form to use it


0.5.14 (2016-07-08)
-------------------

* Allow extra kwargs to core ``View.redirect()`` method

* Add awareness of special 'Authenticated' role, in permissions UI etc.

* Always strip whitespace from label profile 'spec' field input


0.5.13 (2016-06-10)
-------------------

* Hopefully fix some CSS for form field values

* Add support for viewing single employee's schedule / time sheet


0.5.12 (2016-05-11)
-------------------

* Add support for "full" schedule and time sheet views.

* Move "full name" to front of Person grid columns.

* Add rattail config object to ``Session`` kwargs.


0.5.11 (2016-05-06)
-------------------

* Refactor some common FormEncode validators, plus add some more.

* Tweak styles for jQuery UI selectmenu dropdowns.

* Tweak timesheet styles, to give rows alternating background color.

* Disable autocomplete for password fields when editing user.

* Various incomplete improvements to the timesheet/schedule views.


0.5.10 (2016-05-05)
-------------------

* Refactor timesheet logic, add basic schedule view.

* Add prev/next/jump week navigation to time sheet, schedule views.

* Add hyperlinks to product UPC and description, within main grid.

* Fix bug in roles view.


0.5.9 (2016-05-02)
------------------

* Remove 'create batch from results' link on products index page.

* Fix bugs in batch grid URLs.

* Tweak how empty hours are displayed in time sheet.


0.5.8 (2016-05-02)
------------------

* Add ``MasterView.listing`` flag, for templates' sake.

* Overhaul newgrid template header a bit, to improve styles.

* Move ``Person.display_name`` to top of fieldset when viewing/editing.

* Add 'testing' image, for background / watermark.

* Add 'index title' setting to master view.

* Add auto-hide/show magic to message recipients field when viewing.

* Add initial support for grid index URLs.

* Add initial/basic user feedback form support.

* Stop trying to use PIL when generating product image tag.


0.5.7 (2016-04-28)
------------------

* Add master views for ``ScheduledShift`` model.

* Add initial (incomplete) Time Sheet view.


0.5.6 (2016-04-25)
------------------

* Add views for ``WorkedShift`` model.


0.5.5 (2016-04-24)
------------------

* Add workarounds for certain display bugs when rendering datetimes.

* Make currency field renderer display negative amounts in parentheses.

* Add commas to record/page count in grid footer.

* Tweak styles for form field labels.


0.5.4 (2016-04-12)
------------------

* Add support for column header title (tooltip) in new grids.

* Change default filter type for integer fields, in new grids.

* Add flag for rendering key value, for enum field renderers.

* Fix case-sensitivity when sorting permission group labels.


0.5.3 (2016-04-05)
------------------

* Fix redirect bug when attempting bulk row delete for nonexistent batch.

* Add comma magic back to ``CurrencyFieldRenderer``.

* Add the 'is any' verb to default list for most grid filters.

* Add new ``TimeFieldRenderer``, make it default for ``Time`` fields.

* Add last-minute check to ensure master views allows deletion.


0.5.2 (2016-03-11)
------------------

* Make ``tailbone.views.labels`` a subpackage instead of module.

* Add 'executed' to old batches grid view.

* Make all timestamps show "raw" by default (with "diff" tooltip).

* Improve grid filters for datetime fields (smarter verbs).

* Fix bug where batch creator was being set to current user anytime it was viewed..yikes.


0.5.1 (2016-02-27)
------------------

* Fix bug when rendering email bounce links.


0.5.0 (2016-02-15)
------------------

* Refactor products view(s) per new master pattern.

* Make our ``DateTimeFieldRenderer`` the default for datetime fields.

* Add new ``BatchMasterView`` for new-style batches.

* Overhaul vendor catalogs, vendor invoices views to use new batch master class.

* Refactor some more model views to use MasterView. (depositlink, tax, emailbounce)

* Make datasync views easier to customize.


0.4.42
------

* Add initial reply / reply-all support for messages.

* Add subscriber hook for setting inbox count in template context.


0.4.41
------

* Tweak how we connect a user to a batch, when refreshing.

* Add 'Move' button to message view template.


0.4.40
------

* Make rattail config object use our scoped session, when consulting db.


0.4.39
------

* Add support for sending new messages.


0.4.38
------

* Add 'password is/not null' filter to users list view.

* Remove style hack for message grid views.


0.4.37
------

* Add 'messages.list' permission, to protect inbox etc.


0.4.36
------

* Fix bug when marking batch as executed.


0.4.35
------

* Change default form buttons so Cancel is also a button.

* Add 'Stores' and 'Departments' fields to Employee fieldset.


0.4.34
------

* Add 'restart datasync' button to datasync changes list page.

* Add autocomplete vendor field renderer.

* Change vendor catalog upload, to allow vendor-less parsers.

* Stop depending on PIL...for now?


0.4.33
------

* Add employee/department relationships to employee and department views.


0.4.32
------

* Add edit mode for email "profile" settings.

* Fix auto-creation of grid sorter, when joined table is involved.

* Add initial support for 'messages' views.


0.4.31
------

* Add speed bump / confirmation page when deleting records.

* Add "grid tools" to "complete" grid template.

* Add ``Person.middle_name`` to the fieldset.


0.4.30
------

* Add config extension, to record data changes if so configured.

* Add mailing address to person fieldset.


0.4.29
------

* Fix some route names.


0.4.28
------

* Use sample data when generating subject for display in email profile settings.

* Convert (most?) basic views to use master view pattern.


0.4.27
------

* Change default sortkey for email profiles list.

* Add 'To' field to email profile settings grid.


0.4.26
------

* Add readonly support for email profile settings.


0.4.25
------

* Fix bug when 'edbob.permissions' setting is empty.

* Tweak some things to get Tailbone working on its own.

* Let subclass of MasterView override the database Session it uses.


0.4.24
------

* Render ``DataSyncChange.obtained`` as humanized timestamp within UI.


0.4.23
------

* Delete product costs for vendor when deleting vendor.

* Work around formalchemy config bug, caused by edbob.

* Add view to show DataSync changes, for basic troubleshooting.


0.4.22
------

* Remove format hack which isn't py2.6-friendly.


0.4.21
------

* Add "valueless verbs" concept to grid filters.

* Tweak labels for new grid filter form buttons.

* Configure logging when starting up.

* Add HTML5 doctype to base template.

* More grid filter improvements; add choice/enum/date value renderers.

* Treat filter by "contains X Y" as "contains X and contains Y".

* Tweak layout CSS so page body expands to fill screen.


0.4.20
------

* Add ``CurrencyFieldRenderer``.

* Add basic checkbox support to new grids.

* Add 'Default Filters' and 'Clear Filters' buttons to new grid filters form.

* Add "Save Defaults" button so user can save personal defaults for any new grid.

* Fix bug when rendering hidden field in FA fieldset.

* Remove some unused styles.

* Various tweaks to support "late login" idea when uploading new batch.

* Hard-code old grid pagecount settings, to avoid ``edbob.config``.

* Refactor app configuration to use ``rattail.config.make_config()``.

* Tweak label formatter instantiation, per rattail changes.

* Various tweaks to base batch views.

* Add ``CustomFieldRenderer`` and ``DateFieldRenderer``.

* Add ``configure_fieldset()`` stub for master view.

* Add progress indicator to batch execution.

* Add ability to download batch row data as CSV.


0.4.19
------

* Fix progress template, per jQuery CDN changes.


0.4.18
------

* Don't show flash message when user logs in.

* Add core JS/CSS to base template; use CDN instead of cached files.

* Add support for "new-style grids" and "model master views", and convert the
  following views to use it: roles, users, label profiles, settings.  Also
  overhaul how permissions are registered in app config.


0.4.17
------

* Log warning instead of error when refreshing batch fails.


0.4.16
------

* Add initial support for email bounce management.


0.4.15
------

* Fix missing import bug.


0.4.14
------

* Make anchor tags with 'button' class render as jQuery UI buttons.

* Tweak ``app.make_rattail_config()`` to allow caller to define some settings.

* Add ``display_name`` field to employee CRUD view.

* Allow batch handler to disable the Execute button.

* Add ``StoreFieldRenderer`` and ``DecimalFieldRenderer``.

* Tweak how default filter config is handled for batch grid views.

* Add list of assigned users to role view page.

* Add products autocomplete view.

* Add ``rattail_config`` attribute to base ``View`` class.

* Fix timezone issues with ``util.pretty_datetime()`` function.

* Add some custom FormEncode validators.


0.4.13
------

* Fix query bugs for batch row grid views (add join support).

* Make vendor field renderer show ID in readonly mode.

* Change permission requirement for refreshing a batch's data.

* Add flash message when any batch executes successfully.

* Add autocomplete view for current employees.

* Add autocomplete employee field renderer.

* Fix usage of ``Product.unit_of_measure`` vs. ``Product.weighed``.


0.4.12
------

* Fix bug when creating batch from product query.


0.4.11
------

* Tweak old-style batch execution call.


0.4.10
------

* Add 'fake_error' view to test exception handling.

* Add ability to view details (i.e. all fields) of a batch row.

* Fix bulk delete of batch rows, to set 'removed' flag instead.

* Fix vendor invoice validation bug.

* Add dept. number and friends to product details page.

* Add "extra panels" customization hook to product details template.


0.4.9
-----

* Hide "print labels" column on products list view if so configured.


0.4.8
-----

* Fix permission for deposit link list/search view.

* Fix permission for taxes list/search view.


0.4.7
-----

* Add views for deposit links, taxes; update product view.

* Add some new vendor and product fields.

* Add panels to product details view, etc.

* Fix login so user is sent to their target page after authentication.

* Don't allow edit of vendor and effective date in catalog batches.

* Add shared GPC search filter, use it for product batch rows.

* Add default ``Grid.iter_rows()`` implementation.

* Add "save" icon and grid column style.

* Add ``numeric.js`` script for numeric-only text inputs.

* Add product UPC to JSON output of 'products.search' view.


0.4.6
-----

* Add vendor catalog batch importer.

* Add vendor invoice batch importer.

* Improve data file handling for file batches.

* Add download feature for file batches.

* Add better error handling when batch refresh fails, etc.

* Add some docs for new batch system.

* Refactor ``app`` module to promote code sharing.

* Force grid table background to white.

* Exclude 'deleted' items from reports.

* Hide deleted field from product details, according to permissions.

* Fix embedded grid URL query string bug.


0.4.5
-----

* Add prettier UPCs to ordering worksheet report.

* Add case pack field to product CRUD form.


0.4.4
-----

* Add UI support for ``Product.deleted`` column.


0.4.3
-----

* More versioning support fixes, to allow on or off.


0.4.2
-----

* Rework versioning support to allow it to be on or off.


0.4.1
-----

* Only attempt to count versions for versioned models (CRUD views).


0.4.0
-----

This version primarily got the bump it did because of the addition of support
for SQLAlchemy-Continuum versioning.  There were several other minor changes as
well.

* Add department to field lists for category views.

* Change default sort for People grid view.

* Add category to product CRUD view.

* Add initial versioning support with SQLAlchemy-Continuum.


0.3.28
------

* Add unique username check when creating users.

* Improve UPC search for rows within batches.

* New batch system...


0.3.27
------

* Fix bug with default search filters for SA grids.

* Fix bug in product search UPC filter.

* Ugh, add unwanted jQuery libs to progress template.

* Add support for integer search filters.


0.3.26
------

* Use boolean search filter for batch column filters of 'FLAG' type.


0.3.25
------

* Make product UPC search view strip non-digit chars from input.


0.3.24
------

* Make ``GPCFieldRenderer`` display check digit separate from main barcode
  data.

* Add ``DateTimeFieldRenderer`` to show human-friendly timestamps.

* Tweak CRUD form buttons a little.

* Add grid, CRUD views for ``Setting`` model.

* Update ``base.css`` with various things from other projects.

* Fix bug with progress template, when error occurs.


0.3.23
------

* Fix bugs when configuring database session within threads.


0.3.22
------

* Make ``Store.database_key`` field editable.

* Add explicit session config within batch threads.

* Remove cap on installed Pyramid version.

* Change session progress API.


0.3.21
------

* Add monospace font for label printer format command.


0.3.20
------

* Refactor some label printing stuff, per rattail changes.


0.3.19
------

* Add support for ``Product.not_for_sale`` flag.


0.3.18
------

* Add explicit file encoding to all Mako templates.

* Add "active" filter to users view; enable it by default.


0.3.17
------

* Add customer phone autocomplete and customer "info" AJAX view.

* Allow editing ``User.active`` field.

* Add Person autocomplete view which restricts to employees only.


0.3.16
------

* Add product report codes to the UI.


0.3.15
------

* Add experimental soundex filter support to the Customers grid.


0.3.14
------

* Add event hook for attaching Rattail ``config`` to new requests.

* Fix vendor filter/sort issues in products grid.

* Add ``Family`` and ``Product.family`` to the general grid/crud UI.

* Add POD image support to product view page.


0.3.13
------

* Use global ``Session`` from rattail (again).

* Apply zope transaction to global Tailbone Session class.


0.3.12
------

* Fix customer lookup bug in customer detail view.

* Add ``SessionProgress`` class, and ``progress`` views.


0.3.11
------

* Removed reliance on global ``rattail.db.Session`` class.


0.3.10
------

* Changed ``UserFieldRenderer`` to leverage ``User.display_name``.

* Refactored model imports, etc.
    
  This is in preparation for using database models only from ``rattail``
  (i.e. no ``edbob``).  Mostly the model and enum imports were affected.

* Removed references to ``edbob.enum``.


0.3.9
-----

* Added forbidden view.

* Fixed bug with ``request.has_any_perm()``.

* Made ``SortableAlchemyGridView`` default to full (100%) width.

* Refactored ``AutocompleteFieldRenderer``.
    
  Also improved some organization of renderers.

* Allow overriding form class/factory for CRUD views.

* Made ``EnumFieldRenderer`` a proper class.

* Don't sort values in ``EnumFieldRenderer``.
    
  The dictionaries used to supply enumeration values should be ``OrderedDict``
  instances if sorting is needed.

* Added ``Product.family`` to CRUD view.


0.3.8
-----

* Fixed manifest (whoops).


0.3.7
-----

* Added some autocomplete Javascript magic.
    
  Not sure how this got missed the first time around.

* Added ``products.search`` route/view.
    
  This is for simple AJAX uses.

* Fixed grid join map bug.


0.3.6
-----

* Fixed change password template/form.


0.3.5
-----

* Added ``forms.alchemy`` module and changed CRUD view to use it.

* Added progress template.


0.3.4
-----

* Changed vendor filter in product search to find "any vendor".
    
  I.e. the current filter is *not* restricted to the preferred vendor only.
  Probably should still add one (back) for preferred only as well; hence the
  commented code.


0.3.3
-----

* Major overhaul for standalone operation.
    
  This removes some of the ``edbob`` reliance, as well as borrowing some
  templates and styling etc. from Dtail.

  Stop using ``edbob.db.engine``, stop using all edbob templates, etc.

* Fix authorization policy bug.
    
  This was really an edge case, but in any event the problem would occur when a
  user was logged in, and then that user account was deleted.

* Added ``global_title()`` to base template.

* Made logo more easily customizable in login template.


0.3.2
-----

* Rebranded to Tailbone.


0.3.1
-----

* Added some tests.

* Added ``helpers`` module.
    
  Also added a Pyramid subscriber hook to add the module to the template
  renderer context with a key of ``h``.  This is nothing really new, but it
  overrides the helper provided by ``edbob``, and adds a ``pretty_date()``
  function (which maybe isn't a good idea anyway..?).

* Added ``simpleform`` wildcard import to ``forms`` module.

* Added autocomplete view and template.

* Fixed customer group deletion.
    
  Now any customer associations are dropped first, to avoid database integrity
  errors.

* Stole grids and grid-based views from ``edbob``.

* Removed several references to ``edbob``.

* Replaced ``Grid.clickable`` with ``.viewable``.
    
  Clickable grid rows seemed to be more irritating than useful.  Now a view
  icon is shown instead.

* Added style for grid checkbox cells.

* Fixed FormAlchemy table rendering when underlying session is not primary.
    
  This was needed for a grid based on a LOC SMS session.

* Added grid sort arrow images.

* Improved query modification logic in alchemy grid views.

* Overhauled report views to allow easier template customization.

* Improved product UPC search so check digit is optional.

* Fixed import issue with ``views.reports`` module.


0.3a23
------

* Fixed bugs where edit links were appearing for unprivileged users.

* Added support for product codes.
    
  These are shown when viewing a product, and may be used to locate a product
  via search filters.


0.3a22
------

* Removed ``setup.cfg`` file.

* Added ``Session`` to ``rattail.pyramid`` namespace.

* Added Email Address field to Vendor CRUD views.

* Added extra key lookups for customer and product routes.
    
  Now the CRUD routes for these objects can leverage UUIDs of various related
  objects in addition to the primary object.  More should be done with this,
  but at least we have a start.

* Replaced ``forms`` module with subpackage; added some initial goodies (many
  of which are currently just imports from ``edbob``).

* Added/edited various CRUD templates for consistency.

* Modified several view modules so their Pyramid configuration is more
  "extensible."  This just means routes and views are defined as two separate
  steps, so that derived applications may inherit the route definitions if they
  so choose.

* Added Employee CRUD views; added Email Address field to index view.

* Updated ``people`` view module so it no longer derives from that of
  ``edbob``.

* Added support for, and some implementations of, extra key lookup abilities to
  CRUD views.  This allows URLs to use a "natural" key (e.g. Customer ID
  instead of UUID), for cases where that is more helpful.

* Product CRUD now uses autocomplete for Brand field.  Also, price fields no
  longer appear within an editable fieldset.

* Within Store index view, default sort is now ID instead of Name.

* Added Contact and Phone Number fields to Vendor CRUD views; added Contact and
  Email Address fields to index view.
  

0.3a21
------

- [feature] Added CRUD view and template.

- [feature] Added ``AutocompleteView``.

- [feature] Added Person autocomplete view and User CRUD views.

- [feature] Added ``id`` and ``status`` fields to Employee grid view.


0.3a20
------

- [feature] Sorted the Ordering Worksheet by product brand, description.

0.3a19
------

- [feature] Made batch creation and execution threads aware of
  `sys.excepthook`.  Updated both instances to use `rattail.threads.Thread`
  instead of `threading.Thread`.  This way if an exception occurs within the
  thread, the registered handler will be invoked.

0.3a18
------

- [bug] Label profile editing now uses stripping field renderer to avoid
  problems with leading/trailing whitespace.

- [feature] Added Inventory Worksheet report.

0.3a17
------

- [feature] Added Brand and Size fields to the Ordering Worksheet.  Also
  tweaked the template styles slightly, and added the ability to override the
  template via config.

- [feature] Added "preferred only" option to Ordering Worksheet.

0.3a16
------

- [bug] Fixed bug where requesting deletion of non-existent batch row was
  redirecting to a non-existent route.

0.3a15
------

- [bug] Fixed batch grid and CRUD views so that the execution time shows a
  pretty (and local) display instead of 24-hour UTC time.

0.3a14
------

- [feature] Added some more CRUD.  Mostly this was for departments,
  subdepartments, brands and products.  This was rather ad-hoc and still is
  probably far from complete.

- [general] Changed main batch route.

- [bug] Fixed label profile templates so they properly handle a missing or
  invalid printer spec.

0.3a13
------

- [bug] Fixed bug which prevented UPC search from working on products screen.

0.3a12
------

- [general] Fixed namespace packages, per ``setuptools`` documentation.

- [feature] Added support for ``LabelProfile.visible``.  This field may now be
  edited, and it is honored when displaying the list of available profiles to
  be used for printing from the products page.

- [bug] Fixed bug where non-numeric data entered in the UPC search field on the
  products page was raising an error.

0.3a11
------

- [bug] Fixed product label printing to handle any uncaught exception, and
  report the error message to the end user.

0.3a10
------

- [general] Updated category views and templates.  These were sorely out of
  date.

0.3a9
-----

- Add brands autocomplete view.

- Add departments autocomplete view.

- Add ID filter to vendors grid.

0.3a8
-----

- Tweak batch progress indicators.

- Add "Executed" column, filter to batch grid.

0.3a7
-----

- Add ability to restrict batch providers via config.

0.3a6
-----

- Add Vendor CRUD.

- Add Brand views.

0.3a5
-----

- Added support for GPC data type.

- Added eager import of ``rattail.sil`` in ``before_render`` hook.

- Removed ``rattail.pyramid.util`` module.

- Added initial batch support: views, templates, creation from Product grid.

- Added support for ``rattail.LabelProfile`` class.

- Improved Product grid to include filter/sort on Vendor.

- Cleaned up dependencies.

- Added ``rattail.pyramid.includeme()``.

- Added ``CustomerGroup`` CRUD view (read only).

- Added hot links to ``Customer`` CRUD view.

- Added ``Store`` index, CRUD views.

- Updated ``rattail.pyramid.views.includeme()``.

- Added ``email_preference`` to ``Customer`` CRUD.

0.3a4
-----

- Update grid and CRUD views per changes in ``edbob``.

0.3a3
-----

- Add price field renderers.

- Add/tweak lots of views for database models.

- Add label printing to product list view.

- Add (some of) ``Product`` CRUD.

0.3a2
-----

- Refactor category views.

0.3a1
-----

-  Initial port to Rattail v0.3.
