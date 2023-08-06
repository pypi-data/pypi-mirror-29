=================
DatePicker Widget
=================

This package provides two datepicker based widgets. One can be used for
IDatetime fields and the other for IDate fields.


DatePickerWidget
----------------

As for all widgets, the DatePickerWidget must provide the new ``IWidget``
interface:

  >>> import zope.schema
  >>> from zope.interface.verify import verifyClass
  >>> from z3c.form.interfaces import IWidget
  >>> from z3c.form.interfaces import INPUT_MODE
  >>> from z3c.form.converter import FieldWidgetDataConverter
  >>> from j01.datepicker import interfaces
  >>> from j01.datepicker.converter import DatePickerConverter
  >>> from j01.datepicker.widget import DatePickerWidget

  >>> verifyClass(IWidget, DatePickerWidget)
  True

The widget can be instantiated NOT only using the request like other widgets,
we need an additional schema field because our widget uses a converter for
find the right date formatter pattern.Let's setup a schema field now:

  >>> date = zope.schema.Date(
  ...     title=u"date",
  ...     description=u"date")

  >>> from z3c.form.testing import TestRequest
  >>> request = TestRequest()

  >>> widget = DatePickerWidget(request)
  >>> widget.field = date

Before rendering the widget, one has to set the name and id of the widget:

  >>> widget.id = 'widget.id'
  >>> widget.name = 'widget.date'

We also need to register the template for the widget:

  >>> import zope.component
  >>> from zope.pagetemplate.interfaces import IPageTemplate
  >>> from z3c.form.widget import WidgetTemplateFactory

  >>> import os
  >>> import j01.datepicker
  >>> def getPath(filename):
  ...     return os.path.join(os.path.dirname(j01.datepicker.__file__),
  ...     filename)

  >>> zope.component.provideAdapter(
  ...     WidgetTemplateFactory(getPath('input.pt'), 'text/html'),
  ...     (None, None, None, None, interfaces.IDatePickerWidget),
  ...     IPageTemplate, name=INPUT_MODE)

And we need our DatePickerConverter date converter:

  >>> zope.component.provideAdapter(FieldWidgetDataConverter)
  >>> zope.component.provideAdapter(DatePickerConverter)

If we render the widget we get a simple input element. The given input element
id called ``j01DatePickerWidget`` will display a nice date picker if you click
on it and load the selected date into the given input element with the id
``j01DatePickerWidget``:

  >>> widget.update()
  >>> print(widget.render())
  <input type="text" id="widget.id" name="widget.date" class="j01DatePickerWidget" value="" />
  <BLANKLINE>
  <script type="text/javascript">
  ;(function($){
      $.fn.datepicker.dates['en'] = {
      daysShort: ["Sun","Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
      today: "today",
      format: "mm.dd.yyyy",
      daysMin: ["Su","Mo","Tu","We","Th","Fr","Sa","Su"],
      weekStart: "0",
      clear: "remove",
      months: ["January","February","March","April","May","June","July","August","September","October","November","December"],
      days: ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
      monthsShort: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]};
      $("#widget\\.id").datepicker({
      startDate: -Infinity,
      endDate: Infinity,
      todayHighlight: true,
      language: "en",
      format: "mm.dd.yyyy",
      autoclose: true});
  }(jQuery));
  </script>
  <BLANKLINE>

A value will get rendered as simple text input:

  >>> widget.value = '24.02.1969'
  >>> print(widget.render())
  <input type="text" id="widget.id" name="widget.date" class="j01DatePickerWidget" value="24.02.1969" />
  <BLANKLINE>
  <script type="text/javascript">
  ;(function($){
      $.fn.datepicker.dates['en'] = {
      daysShort: ["Sun","Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
      today: "today",
      format: "mm.dd.yyyy",
      daysMin: ["Su","Mo","Tu","We","Th","Fr","Sa","Su"],
      weekStart: "0",
      clear: "remove",
      months: ["January","February","March","April","May","June","July","August","September","October","November","December"],
      days: ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
      monthsShort: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]};
      $("#widget\\.id").datepicker({
      startDate: -Infinity,
      endDate: Infinity,
      todayHighlight: true,
      language: "en",
      format: "mm.dd.yyyy",
      autoclose: true});
  }(jQuery));
  </script>
  <BLANKLINE>

Let's now make sure that we can extract user entered data from a widget:

  >>> widget.request = TestRequest(form={'widget.date': '24.02.1969'})
  >>> widget.update()
  >>> widget.extract()
  u'24.02.1969'


If nothing is found in the request, the default is returned:

  >>> widget.request = TestRequest()
  >>> widget.update()
  >>> widget.extract()
  <NO_VALUE>


options
-------

the datepicker widget provides different options. This are:


  >>> widget.autoclose = False
  >>> widget.beforeShowDay = 'function beforeShowDay(date) {}'
  >>> widget.beforeShowMonth = 'function beforeShowMonth(date) {}'
  >>> widget.beforeShowYear = 'function beforeShowYear(date) {}'
  >>> widget.calendarWeeks = True
  >>> widget.clearBtn = True
  >>> widget.container = '#container'
  >>> widget.datesDisabled = ['03-03-2015']
  >>> widget.daysOfWeekDisabled = [0,6]
  >>> widget.daysOfWeekHighlighted = [1,30]
  >>> widget.defaultViewDate = 'year'
  >>> widget.disableTouchKeyboard = True
  >>> widget.enableOnReadonly = False
  >>> widget.forceParse = False
  >>> widget.immediateUpdates = True
  >>> widget.keyboardNavigation = False
  >>> widget.maxViewMode = 1
  >>> widget.minViewMode = 1
  >>> widget.multidate = True
  >>> widget.multidateSeparator = ';'
  >>> widget.orientation = 'left'
  >>> widget.showOnFocus = False
  >>> widget.startView = 1
  >>> widget.todayBtn = True
  >>> widget.todayHighlight = False
  >>> widget.toggleActive = True
  >>> widget.weekStart = 6
  >>> widget.zIndexOffset = 42
  >>> print(widget.render())
  <input type="text" id="widget.id" name="widget.date" class="j01DatePickerWidget" value="24.02.1969" />
  <BLANKLINE>
  <script type="text/javascript">
  ;(function($){
      $.fn.datepicker.dates['en'] = {
      daysShort: ["Sun","Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
      today: "today",
      format: "mm.dd.yyyy",
      daysMin: ["Su","Mo","Tu","We","Th","Fr","Sa","Su"],
      weekStart: "6",
      clear: "remove",
      months: ["January","February","March","April","May","June","July","August","September","October","November","December"],
      days: ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
      monthsShort: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]};
      $("#widget\\.id").datepicker({
      startDate: -Infinity,
      multidateSeparator: ";",
      keyboardNavigation: false,
      endDate: Infinity,
      orientation: "left",
      toggleActive: true,
      beforeShowMonth: function beforeShowMonth(date) {},
      beforeShowDay: function beforeShowDay(date) {},
      datesDisabled: ["03-03-2015"],
      maxViewMode: 1,
      calendarWeeks: true,
      weekStart: 6,
      disableTouchKeyboard: true,
      daysOfWeekDisabled: ["0","6"],
      todayBtn: true,
      defaultViewDate: "year",
      container: "#container",
      language: "en",
      immediateUpdates: true,
      multidate: true,
      format: "mm.dd.yyyy",
      enableOnReadonly: false,
      clearBtn: true,
      daysOfWeekHighlighted: ["1","30"],
      forceParse: false,
      zIndexOffset: 42,
      showOnFocus: false,
      minViewMode: 1,
      startView: 1,
      beforeShowYear: function beforeShowYear(date) {}});
  }(jQuery));
  </script>
  <BLANKLINE>

  >>> widget.request = TestRequest(form={'widget.date': '24.02.1969'})
  >>> widget.update()
  >>> widget.extract()
  u'24.02.1969'
