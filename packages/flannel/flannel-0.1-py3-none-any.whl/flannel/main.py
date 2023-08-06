 #!/usr/bin/env python3 -u
"""
This file is part of flannel.

flannel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

flannel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
import logging
import time
import argparse

You should have received a copy of the GNU General Public License
along with flannel.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import logging
import argparse
import sys
import json
import re
from datetime import (
    datetime,
    timedelta
)
from PyQt5.QtCore import (
    QThread,
    pyqtSlot,
    pyqtSignal,
    QVariant,
)
from PyQt5.Qt import (
    QApplication,
    QSize,
    QAbstractTableModel,
    Qt,
    QModelIndex,
    QTimer,
    QAbstractItemModel
    )
from PyQt5.QtGui import (
    QGuiApplication,
    QTextCursor,
    QBrush,
    QColor,
)
from PyQt5.QtWidgets import (
    QWidget,
    QPlainTextEdit,
    QLayout,
    QFormLayout,
    QGridLayout,
    QTableView,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QAbstractScrollArea,
    QFrame,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QSplitter,
    QSizePolicy,
    QTabWidget,
    QStyle,
    QCompleter,
)

from lotconfig import Config

RE_JSON_ITEM = re.compile(r'^\{[^\}$]+\}', re.M).finditer


COLORS = {
    'BACKGROUND': {
        'DEBUG': QColor('cyan').lighter(),
        'ERROR': QColor('red').lighter(),
        'WARNING': QColor('yellow'),
        'INFO': QColor('lightGray').lighter(),
        'FATAL': QColor('black'),
    },
    'FOREGROUND': {
        'FATAL': QColor('red').lighter(),
    }
}

COLUMN_WIDTHS = {
    'msg': 400,
}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--columns',
                    help=str("Include only these columns in the output."
                             " Comma-seperated."
                             " For example: `msg,module,created`."
                             " default will be al columns"))

config = None

class LogModel(QAbstractTableModel):

    raw_buffer_updated = pyqtSignal(str)
    headers_changed = pyqtSignal()
    rows_inserted_actual = pyqtSignal()

    SIGNAL_INTERVAL = 100  # 100 ms

    def __init__(self, log_entries=[], *args, **kwargs):
        self.log_entries = log_entries
        self.raw = ''
        self._tmp_buf = ''
        self.headers = []
        self.visible = []
        self._last_signal_time = datetime.now()
        self._last_row_insert_delay = datetime.now()
        super(LogModel, self).__init__(*args, **kwargs)
        self.rowsInserted.connect(self.insertRowDelay)

    def rowCount(self, parent=QModelIndex()):
        return len(self.log_entries)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if index.column() >= len(self.headers):
            return

        n = self.headers[index.column()]
        ln = self.log_entries[index.row()]['levelname']

        if not index.isValid():
            return 'invalid index {}'.format(index)
        if role == Qt.SizeHintRole:
            # print("displaying column {}".format(index.column()))
            return
        if role == Qt.DisplayRole:
            return self.log_entries[index.row()][n]
        if role == Qt.BackgroundRole:
            if ln in COLORS['BACKGROUND']:
                return QBrush(COLORS['BACKGROUND'][ln])
        if role == Qt.ForegroundRole:
            if ln in COLORS['FOREGROUND']:
                return QBrush(COLORS['FOREGROUND'][ln])

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(self.index(0, 0), row, count)
        del self.log_entries[row:row+count]
        self.endRemoveRows()

    def clear(self):
        self.layoutAboutToBeChanged.emit()
        self.removeRows(0, self.rowCount())
        self.layoutChanged.emit()

    def request_headers(self, requested=None):
        if len(self.log_entries) < 0:
            return []
        all_headers = list(self.log_entries[0].keys())
        if ((requested is None) or (len(requested) == 0) or
           (len(requested) == 1 and requested[0] == '')):
            actual = all_headers
        else:
            actual = [i for i in requested if i in all_headers]
        for (i, h) in enumerate(actual):
            j = all_headers.index(h)
            if i != j:
                # print("moving column")
                self.moveColumn(self.index(0, 0), i, self.index(0, 0), j)
        self.visible = actual
        self.headers = self.visible + [i for i in all_headers if i not in actual]
        # print("Headers now {}".format(self.headers))
        self.headers_changed.emit()
        self.dataChanged.emit(self.index(0, 0),
                              self.index(len(self.headers),
                                         len(self.log_entries)))
        return actual

    def insertRowDelay(self):
        t = (self._last_row_insert_delay +
             timedelta(microseconds=(self.SIGNAL_INTERVAL * 10)))
        if (t < datetime.now()):
            return
        self.rows_inserted_actual.emit()
        self._last_row_insert_delay = datetime.now()

    def insertRows(self, position, rows, item, parent=QModelIndex()):
        self.beginInsertRows(QModelIndex(), len(self.log_entries),
                             len(self.log_entries))
        self.log_entries.append(item)
        self.endInsertRows()
        return True

    @property
    def _has_signal_passed(self):
        u_seconds = (datetime.now() - self._last_signal_time).microseconds
        m_seconds = u_seconds / 10
        return m_seconds > self.SIGNAL_INTERVAL

    def update_entries(self, buf):
        self.raw += buf  # add to raw buffer by default
        if self._has_signal_passed:
            self.raw_buffer_updated.emit(self.raw)
            self._last_signal_time = datetime.now()
        if buf.strip().startswith('{'):
            self._tmp_buf = buf
        else:
            self._tmp_buf += buf
        if not self._tmp_buf.strip().endswith('}'):
            return
        # Only continue if self._tmp_buf starts with '{'
        # and ends with '}'
        try:
            log_entry = json.loads(self._tmp_buf)
            for k in log_entry.keys():
                if k not in self.headers:
                    self.headers.append(k)
                    self.columnsInserted.emit(self.index(0, 0),
                                              len(self.headers),
                                              len(self.headers))
            self.insertRows(len(self.log_entries)-1, 1, log_entry)
        except json.decoder.JSONDecodeError as e:
            logger.error(self._tmp_buf)
            logger.error(e)
        self._tmp_buf = ''

    def headerData(self, section, orientation=Qt.Horizontal,
                   role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section >= len(self.headers):
                logger.warning('invalid section {}'.format(section))
                return None
            return self.headers[section]
        return None

    def sort(self, Ncol, order):
        import operator
        if Ncol >= len(self.headers):
            return
        self.layoutAboutToBeChanged.emit()
        self.log_entries = sorted(self.log_entries,
                                  key=operator.itemgetter(self.headers[Ncol]))
        if order == Qt.DescendingOrder:
            self.log_entries.reverse()
        self.layoutChanged.emit()

class ReaderThread(QThread):

    buffer_updated = pyqtSignal()

    TIMER_INTERVAL = 100  # 100 ms

    def __init__(self):
        self.model = LogModel()
        QThread.__init__(self)

    def start(self):
        self.is_running = True
        QThread.start(self)

    def stop(self):
        self.is_running = False
        self.timer.stop()

    def run(self):
        while 1:
            if not self.is_running:
                return
            line = sys.stdin.readline()
            if line:
                # print(line)
                self.model.update_entries(line)
            else:
                continue


class Window(QWidget):

    buffer_updated = pyqtSignal()
    text_filters_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        self.columns = kwargs.pop('columns_shown', None)

        kwargs['size'] = QSize(800, 400)
        super(Window, self).__init__(*args, **kwargs)
        self.create_widgets()

        self.runner_thread = ReaderThread()
        self.runner_thread.start()
        self.text_filters = {}
        self.buffer_table.setModel(self.runner_thread.model)
        self.buffer_table.setSortingEnabled(True)
        self.clear_button.pressed.connect(self.runner_thread.model.clear)
        self.runner_thread.model.rows_inserted_actual.connect(self.resize_columns)
        self.runner_thread.model.rows_inserted_actual.connect(self.filter_table)
        self.runner_thread.model.columnsInserted.connect(self.add_filters)
        self.runner_thread.model.raw_buffer_updated.connect(self.update_raw)
        self.runner_thread.model.headers_changed.connect(self.change_headings)
        self.text_filters_changed.connect(self.filter_table)
        self.filter_added = False

    def show(self):
        super(Window, self).show()

    def resize_columns(self):
        model = self.buffer_table.model()
        for (i, h) in enumerate(model.headers):
            if h not in ('msg'):  # don't resize to contents on these headers
                self.buffer_table.resizeColumnToContents(i)
            else:
                self.buffer_table.setColumnWidth(i, COLUMN_WIDTHS.get(h, 200))

    def filter_table(self):
        store = self.runner_thread.model.log_entries
        for (row_number, entry) in enumerate(store):
            self.buffer_table.showRow(row_number)
            for (field, value) in self.text_filters.items():
                if len(value or '') == 0:
                    continue
                if str(value).lower() not in str(entry[field]).lower():
                    self.buffer_table.hideRow(row_number)

    def change_headings(self):
        headings = self.buffer_table.model().headers
        visible = self.buffer_table.model().visible
        model = self.buffer_table.model()
        for (i, h) in enumerate(headings):
            self.buffer_table.showColumn(headings.index(h))
            if h not in visible:
                self.buffer_table.hideColumn(headings.index(h))
            # self.buffer_table.setColumnWidth(i, COLUMN_WIDTHS.get(h, 100))

    def destroy(self):
        super(Window, self).destroy()
        sys.stdin.close()
        self.runner_thread.stop = True
        del self.runner_thread

    def apply_text_filter(self, header):
        def _inner(text):
            self.text_filters[header] = text
            self.text_filters_changed.emit()
        return _inner

    def apply_header_filter(self, header):
        def _inner(state):
            headers = self.buffer_table.model().headers
            if state == Qt.Unchecked:
                self.buffer_table.hideColumn(headers.index(header))
            elif state == Qt.Checked:
                self.buffer_table.showColumn(headers.index(header))
        return _inner

    def _add_heading_filter(self, heading):
        cb_layout = QHBoxLayout()
        cb_layout.setSizeConstraint(QLayout.SetFixedSize)
        cb_widget = QWidget()
        checkbox = QCheckBox()
        checkbox.setCheckState(Qt.Checked)
        checkbox.stateChanged.connect(self.apply_header_filter(heading))
        label = QLabel(heading)
        cb_layout.addWidget(checkbox)
        cb_layout.addWidget(label)
        cb_widget.setLayout(cb_layout)
        self.heading_filter_layout.addWidget(cb_widget)

    def perform_column_filter(self, value):
        model = self.buffer_table.model()
        model.request_headers((value or '').split(','))

    def add_heading_filter(self, headings):
        if self.filter_added:
            return
        edit_widget = QLineEdit()
        edit_completer = QCompleter(headings)
        edit_widget.setCompleter(edit_completer)
        edit_widget.setPlaceholderText(','.join(headings))
        edit_widget.textChanged.connect(self.perform_column_filter)
        edit_widget.setToolTip('\n'.join(headings))
        if self.columns:
            edit_widget.setText(self.columns)
        self.heading_filter_layout.addWidget(edit_widget)
        self.filter_added = True

    def add_text_filter(self, heading):
        self.text_filters[heading] = None
        label = QLabel(heading)
        field = QLineEdit(width=50)
        field.textChanged.connect(self.apply_text_filter(heading))
        self.text_filter_layout.addRow(label, field)

    def update_raw(self, content):
        self.raw_output.setPlainText(content)
        self.raw_output.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)

    def add_filters(self):
        headers = self.runner_thread.model.headers
        for h in headers:
            if h in self.text_filters:
                continue
            self.add_text_filter(h)
        self.add_heading_filter(headers)
        self.perform_column_filter(self.columns)

    def create_widgets(self):
        # root
        root_layout = QVBoxLayout(self)
        root_widget = QSplitter(Qt.Vertical)

        # top
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)

        # top -> inner widget
        scroll_inner_widget = QWidget()

        # top -> inner layout
        filter_root_layout = QVBoxLayout()

        # top -> inner layout -> headings
        filter_heading_group = QGroupBox("Show Table Headings", root_widget)
        self.heading_filter_layout = QHBoxLayout()

        filter_heading_group.setLayout(self.heading_filter_layout)

        # top -> inner layout -> text
        filter_text_group = QGroupBox("Filter Content")
        self.text_filter_layout = QFormLayout()
        filter_text_group.setLayout(self.text_filter_layout)

        filter_root_layout.addWidget(filter_heading_group)
        filter_root_layout.addWidget(filter_text_group)
        filter_root_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        scroll_inner_widget.setLayout(filter_root_layout)
        scroll_area.setWidget(scroll_inner_widget)

        # bottom
        bottom_container = QWidget()
        bottom_layout = QGridLayout()
        bottom_container.setLayout(bottom_layout)

        self.clear_button = QPushButton("Clear")

        tab_widget = QTabWidget()
        self.buffer_table = QTableView(size=QSize(800, 200))
        self.raw_output = QPlainTextEdit()
        self.raw_output.setStyleSheet("font-family: monospace; ")
        self.raw_output.setReadOnly(True)
        tab_widget.addTab(self.buffer_table, 'Table')
        tab_widget.addTab(self.raw_output, 'Raw Output')
        bottom_layout.addWidget(self.clear_button, 0, 0, 1, 1)
        bottom_layout.addWidget(tab_widget, 0, 1, 4, 1)

        root_widget.addWidget(scroll_area)
        root_widget.addWidget(bottom_container)

        root_layout.addWidget(root_widget)
        self.setLayout(root_layout)

def main(inargs=sys.argv[1:]):
    args = parser.parse_args(inargs)
    global config
    config = Config.load_or_create('.flannel.yaml')
    app = QApplication(sys.argv)
    window = Window(columns_shown=args.columns)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
