=====================
DateTimePicker Widget
=====================

This package provides two datetimepicker based widgets. One can be used for
IDatetime fields and the other for IDate fields.


DateTimePickerWidget
--------------------

As for all widgets, the DateTimePickerWidget must provide the new ``IWidget``
interface:

  >>> import zope.schema
  >>> from zope.interface.verify import verifyClass
  >>> from z3c.form.interfaces import IWidget
  >>> from z3c.form.interfaces import INPUT_MODE
  >>> from z3c.form.converter import FieldWidgetDataConverter
  >>> from j01.datetimepicker import interfaces
  >>> from j01.datetimepicker.converter import DateTimePickerConverter
  >>> from j01.datetimepicker.widget import DateTimePickerWidget

  >>> verifyClass(IWidget, DateTimePickerWidget)
  True

The widget can be instantiated NOT only using the request like other widgets,
we need an additional schema field because our widget uses a converter for
find the right date formatter pattern.Let's setup a schema field now:

  >>> date = zope.schema.Date(
  ...     title=u"date",
  ...     description=u"date")

  >>> from z3c.form.testing import TestRequest
  >>> request = TestRequest()

  >>> widget = DateTimePickerWidget(request)
  >>> widget.field = date

Before rendering the widget, one has to set the name and id of the widget:

  >>> widget.id = 'widget.id'
  >>> widget.name = 'widget.date'

We also need to register the template for the widget:

  >>> import zope.component
  >>> from zope.pagetemplate.interfaces import IPageTemplate
  >>> from z3c.form.widget import WidgetTemplateFactory

  >>> import os
  >>> import j01.datetimepicker
  >>> def getPath(filename):
  ...     return os.path.join(os.path.dirname(j01.datetimepicker.__file__),
  ...     filename)

  >>> zope.component.provideAdapter(
  ...     WidgetTemplateFactory(getPath('input.pt'), 'text/html'),
  ...     (None, None, None, None, interfaces.IDateTimePickerWidget),
  ...     IPageTemplate, name=INPUT_MODE)

And we need our DateTimePickerConverter date converter:

  >>> zope.component.provideAdapter(FieldWidgetDataConverter)
  >>> zope.component.provideAdapter(DateTimePickerConverter)

If we render the widget we get a simple input element. The given input element
id called ``j01DateTimePickerWidget`` will display a nice date picker if you click
on it and load the selected date into the given input element with the id
``j01DateTimePickerWidget``:

  >>> widget.update()
  >>> print(widget.render())
  <input type="text" id="widget.id" name="widget.date" class="j01DateTimePickerWidget" value="" />
  <BLANKLINE>
  <script type="text/javascript">
      $("#widget\\.id").datetimepicker({
      format: "YYYY MMM DD  HH:mm:ss ",
      showClose: true,
      icons: {
           down: "fas fa-chevron-down",time: "far fa-clock",date: "far fa-calendar-alt",close: "far fa-minus-square",clear: "fas fa-trash",next: "fas fa-chevron-right",up: "fas fa-chevron-up",today: "far fa-calendar-times",previous: "fas fa-chevron-left"
      },
      locale: "en"});
  </script>
  <BLANKLINE>

A value will get rendered as simple text input:

  >>> widget.value = '24.02.1969'
  >>> print(widget.render())
  <input type="text" id="widget.id" name="widget.date" class="j01DateTimePickerWidget" value="24.02.1969" />
  <BLANKLINE>
  <script type="text/javascript">
      $("#widget\\.id").datetimepicker({
      format: "YYYY MMM DD  HH:mm:ss ",
      showClose: true,
      icons: {
           down: "fas fa-chevron-down",time: "far fa-clock",date: "far fa-calendar-alt",close: "far fa-minus-square",clear: "fas fa-trash",next: "fas fa-chevron-right",up: "fas fa-chevron-up",today: "far fa-calendar-times",previous: "fas fa-chevron-left"
      },
      locale: "en"});
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

the datetimepicker widget provides different options. This are:


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
  <input type="text" id="widget.id" name="widget.date" class="j01DateTimePickerWidget" value="24.02.1969" />
  <BLANKLINE>
  <script type="text/javascript">
      $("#widget\\.id").datetimepicker({
      format: "YYYY MMM DD  HH:mm:ss ",
      calendarWeeks: true,
      daysOfWeekDisabled: ["0","6"],
      showClose: true,
      icons: {
           down: "fas fa-chevron-down",time: "far fa-clock",date: "far fa-calendar-alt",close: "far fa-minus-square",clear: "fas fa-trash",next: "fas fa-chevron-right",up: "fas fa-chevron-up",today: "far fa-calendar-times",previous: "fas fa-chevron-left"
      },
      locale: "en"});
  </script>
  <BLANKLINE>

  >>> widget.request = TestRequest(form={'widget.date': '24.02.1969'})
  >>> widget.update()
  >>> widget.extract()
  u'24.02.1969'
