# encoding: utf-8

import logging_helper
from tkinter import StringVar, BooleanVar
from tkinter.messagebox import askquestion
from tkinter.constants import HORIZONTAL, E, W, S, EW, NSEW
from uiutil.frame import BaseFrame
from uiutil.helper.layout import nice_grid
from configurationutil import Configuration
from networkutil.endpoint_config import Endpoints
from ...config import dns_lookup
from ..window.record import AddEditRecordWindow

logging = logging_helper.setup_logging()


class ZoneConfigFrame(BaseFrame):

    def __init__(self,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self,
                           *args,
                           **kwargs)

        self._selected_record = StringVar(self.parent)

        self.cfg = Configuration()

        self.dns_radio_list = {}
        self.dns_active_var_list = {}
        self.dns_active_list = {}

        self.columnconfigure(self.column.start(), weight=1)

        self.REDIRECT_ROW = self.row.next()
        self.rowconfigure(self.REDIRECT_ROW, weight=1)
        self.BUTTON_ROW = self.row.next()

        self._build_zone_frame()
        self._build_button_frame()

    def _build_zone_frame(self):

        self.record_frame = BaseFrame(self)
        self.record_frame.grid(row=self.REDIRECT_ROW,
                               column=self.column.current,
                               sticky=NSEW)

        left_col = self.record_frame.column.start()
        middle_col = self.record_frame.column.next()
        self.rowconfigure(middle_col, weight=1)
        right_col = self.record_frame.column.next()

        headers_row = self.record_frame.row.next()

        self.record_frame.label(text=u'Host',
                                row=headers_row,
                                column=left_col,
                                sticky=W)

        self.record_frame.label(text=u'Redirect',
                                row=headers_row,
                                column=middle_col,
                                sticky=W)

        self.record_frame.label(text=u'Active',
                                row=headers_row,
                                column=right_col,
                                sticky=W)

        self.record_frame.separator(orient=HORIZONTAL,
                                    row=self.record_frame.row.next(),
                                    column=left_col,
                                    columnspan=3,
                                    sticky=EW,
                                    padx=5,
                                    pady=5)

        for host, host_config in iter(dns_lookup.get_redirection_config().items()):

            redirect_row = self.record_frame.row.next()

            if not self._selected_record.get():
                self._selected_record.set(host)

            self.dns_radio_list[host] = self.record_frame.radiobutton(text=host,
                                                                      variable=self._selected_record,
                                                                      value=host,
                                                                      row=redirect_row,
                                                                      column=left_col,
                                                                      sticky=W)

            # Get the configured record
            text = host_config[u'redirect_host']

            # Check for a friendly name for host
            friendly_name = self._convert_host_to_friendly_name(text)

            if friendly_name is not None:
                text = u'{name} ({host})'.format(name=friendly_name,
                                                 host=text)

            self.record_frame.label(text=text,
                                    row=redirect_row,
                                    column=middle_col,
                                    sticky=W)

            self.dns_active_var_list[host] = BooleanVar(self.parent)
            self.dns_active_var_list[host].set(host_config[u'active'])

            self.dns_active_list[host] = self.record_frame.checkbutton(
                variable=self.dns_active_var_list[host],
                command=(lambda host=host,
                         flag=self.dns_active_var_list[host]:
                         self._update_active(host=host,
                                             flag=flag)),
                row=redirect_row,
                column=right_col,
                sticky=W
            )

        self.record_frame.separator(orient=HORIZONTAL,
                                    row=self.record_frame.row.next(),
                                    column=left_col,
                                    columnspan=3,
                                    sticky=EW,
                                    padx=5,
                                    pady=5)

        nice_grid(self.record_frame)

    def _build_button_frame(self):

        button_width = 15

        self.button_frame = BaseFrame(self)
        self.button_frame.grid(row=self.BUTTON_ROW,
                               column=self.column.current,
                               sticky=(E, W, S))

        self.button(frame=self.button_frame,
                    name=u'_delete_record_button',
                    text=u'Delete Record',
                    width=button_width,
                    command=self._delete_zone_record,
                    row=self.button_frame.row.start(),
                    column=self.button_frame.column.start(),
                    tooltip=u'Delete\nselected\nrecord')

        self.button(frame=self.button_frame,
                    name=u'_add_record_button',
                    text=u'Add Record',
                    width=button_width,
                    command=self._add_zone_record,
                    row=self.button_frame.row.current,
                    column=self.button_frame.column.next(),
                    tooltip=u'Add record\nto dns list')

        self.button(frame=self.button_frame,
                    name=u'_edit_record_button',
                    text=u'Edit Record',
                    width=button_width,
                    command=self._edit_zone_record,
                    row=self.button_frame.row.current,
                    column=self.button_frame.column.next(),
                    tooltip=u'Edit\nselected\nrecord')

        nice_grid(self.button_frame)

    def _add_zone_record(self):
        window = AddEditRecordWindow(fixed=True,
                                     parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

        window.transient()
        window.grab_set()
        self.parent.wait_window(window)

        self.record_frame.destroy()
        self._build_zone_frame()

        self.parent.master.update_geometry()

    def _edit_zone_record(self):
        window = AddEditRecordWindow(selected_record=self._selected_record.get(),
                                     edit=True,
                                     fixed=True,
                                     parent_geometry=(self.parent.winfo_toplevel().winfo_geometry()))

        window.transient()
        window.grab_set()
        self.parent.wait_window(window)

        self.record_frame.destroy()
        self._build_zone_frame()

        self.parent.master.update_geometry()

    def _delete_zone_record(self):
        result = askquestion(title=u"Delete Record",
                             message=u"Are you sure you "
                                     u"want to delete {r}?".format(r=self._selected_record.get()),
                             icon=u'warning',
                             parent=self)

        if result == u'yes':
            key = u'{c}.{h}'.format(c=dns_lookup.DNS_LOOKUP_CFG,
                                    h=self._selected_record.get())

            del self.cfg[key]

            self.record_frame.destroy()
            self._build_zone_frame()

            self.parent.master.update_geometry()

    def _update_active(self,
                       host,
                       flag):
        key = u'{c}.{h}.{active}'.format(c=dns_lookup.DNS_LOOKUP_CFG,
                                         h=host,
                                         active=dns_lookup.ACTIVE)

        self.cfg[key] = flag.get()

    @staticmethod
    def _convert_host_to_friendly_name(host):

        try:
            # Attempt to lookup friendly name
            return Endpoints().get_environment_for_host(host)

        except LookupError:
            logging.debug(u'No friendly name available for host: {host}'.format(host=host))
            return None
