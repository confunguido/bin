#!/usr/bin/python3
import re, sys, os,errno
import xdg.Menu, xdg.DesktopEntry, xdg.Config
from xml.sax.saxutils import escape

from PyQt5.QtWidgets import (QApplication, QWidget, QAbstractScrollArea,
                             QLineEdit, QLabel,QSizeGrip,QVBoxLayout,
                             QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSlot

#functions----------
def escape_utf8(s):
    if sys.version_info[0] < 3 and isinstance(s, unicode):
            s = s.encode('utf-8', 'xmlcharrefreplace')
    return escape(s)

def entry_name(entry):
    return escape_utf8(entry.getName())

def entry_command(entry):
    name = entry_name(entry.DesktopEntry)
    command = re.sub(' -caption "%c"| -caption %c',
             ' -caption "%s"' % name,
             escape_utf8(entry.DesktopEntry.getExec()))
    command = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', command)
    return command

def entry_exec(entry):
    name = entry_name(entry.DesktopEntry)
    command = re.sub(' -caption "%c"| -caption %c',
             ' -caption "%s"' % name,
             escape_utf8(entry.DesktopEntry.getExec()))
    command = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', command)
    if entry.DesktopEntry.getTerminal():
        command = 'xterm -title "%s" -e %s' % (name, command)
    return command

        
# GUI------------------
class Bar(QWidget):
    def __init__(self,file_in):
        super().__init__()
        self.initUI()
        self.fileout = file_in
        self.applications_items = list()
        self.matches_list = list()
        self.setGeometry(750,20,400,20)
        lang = os.environ.get('LANG')
        if lang:
            xdg.Config.setLocale(lang)
            
        # lie to get the same menu as in GNOME
        xdg.Config.setWindowManager('GNOME')
        
        menu = xdg.Menu.parse('applications.menu')
        list(map(self.populate_menu, menu.getEntries()))

    def initUI(self):
        qle = QLineEdit(self)        
        qle.setStyleSheet('background-color:#E0E0E0')
        qle.move(0,0)
        qle.setFixedWidth(400)
        qle.setFont(QFont("Arial", 20))
        qle.textChanged[str].connect(self.onChanged)
        qle.returnPressed.connect(self.onReturn)

        self.tableSearch = QTableWidget()
        self.tableSearch.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents
            )
        self.tableSearch.verticalHeader().setVisible(False)
        self.tableSearch.horizontalHeader().setVisible(False)
        self.tableSearch.verticalHeader().setDefaultSectionSize(45)
        self.tableSearch.horizontalHeader().setDefaultSectionSize(400)
        self.tableSearch.setMinimumSize(QSize(0,1))
        self.tableSearch.setStyleSheet('background-color: transparent')
        self.tableSearch.doubleClicked.connect(self.on_click)
        self.setAutoFillBackground(True)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(qle)
        mainLayout.addWidget(self.tableSearch)
        mainLayout.setContentsMargins(0,0,0,0)
        
        self.setLayout(mainLayout)
        p = self.palette()
        p.setColor(self.backgroundRole(),QColor(255,255,255,255))
        self.setPalette(p)
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()
        
    def keyPressEvent(self,event):
        if event.key()== Qt.Key_Escape:
            QApplication.instance().quit()
        if (event.key()==Qt.Key_Down and
            self.tableSearch.rowCount() > 0):
            if self.tableSearch.selectedItems()[0].row() < self.tableSearch.rowCount() - 1:
                self.tableSearch.selectRow(self.tableSearch.selectedItems()[0].row() + 1)
                print("down")
        if (event.key()==Qt.Key_Up and
            self.tableSearch.rowCount() > 0):
            if self.tableSearch.selectedItems()[0].row() > 0:
                self.tableSearch.selectRow(self.tableSearch.selectedItems()[0].row() - 1)
                print("up")
        
    @pyqtSlot()
    def on_click(self):
        if len(self.matches_list) > 0:
           os.system('%s & disown' %
                     (entry_exec(
                         self.matches_list[self.tableSearch.selectedItems()[0].row()])
                     )
           )
           QApplication.instance().quit()            
           

        
    def onChanged(self,text):
        if text != '':
            self.matches_list = self.find_matches(text, self.applications_items)
        else:
            self.matches_list = list()
        nmatches = len(self.matches_list)
        if nmatches >= 9 : nmatches = 9
        wsize = 40 + nmatches*49
        self.tableSearch.setRowCount(nmatches)
        self.tableSearch.setColumnCount(1)
        self.setGeometry(750,20,400,wsize)
        nn = 0
        for m in self.matches_list:
            str_tmp = '%s' % (entry_name(m.DesktopEntry))
            trow = QTableWidgetItem(str_tmp)
            trow.setSizeHint(QSize(400,40))
            trow.setBackground(QColor(255,255,255,255))
            self.tableSearch.setItem(nn,0,trow)  
            nn +=1
            if nn == 9 : break
        self.tableSearch.selectRow(0)
        
    def onReturn(self):
        if len(self.matches_list) > 0:
           os.system('%s & disown' %
                     (entry_exec(
                         self.matches_list[self.tableSearch.selectedItems()[0].row()])
                     )
           )
           QApplication.instance().quit()            
        
    def populate_menu(self,entry):
        if isinstance(entry, xdg.Menu.Menu) and entry.Show is True:
            list(map(self.populate_menu, entry.getEntries()))
        elif isinstance(entry, xdg.Menu.MenuEntry) and entry.Show is True:
            self.applications_items.append(entry)
                
    def match_entry(self,entry,search_str):
        return (
            re.compile(search_str, re.IGNORECASE).match(entry_name(entry.DesktopEntry)) or
            re.compile(search_str, re.IGNORECASE).match(entry_exec(entry))             
            )
    def semi_match_entry(self,entry,search_str):
        return (
            re.compile(search_str, re.IGNORECASE).search(entry_name(entry.DesktopEntry)) or
            re.compile(search_str, re.IGNORECASE).search(entry_exec(entry))             
            )
        
    def find_matches(self,search_str, app_list):
        match_list= list()
        semi_match_list= list()
        for m in app_list:
            if self.match_entry(m,search_str):
                match_list.append(m)
            elif self.semi_match_entry(m,search_str):
                semi_match_list.append(m)
                
        return(match_list + semi_match_list)
        

#main---------------
if __name__ == '__main__':
    outfile = '.config/apps_finder/search.txt'
    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile),exist_ok=True)
    
    app = QApplication(sys.argv)
    bbr = Bar(outfile)
    sys.exit(app.exec_())

