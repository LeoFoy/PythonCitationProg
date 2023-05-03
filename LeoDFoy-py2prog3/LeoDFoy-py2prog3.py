#Leo David Foy - Python 2, Program 3

import wx 
import sqlite3

class InsertCitationBox(wx.Dialog):

    def __init__(self):

        wx.Dialog.__init__(self, None, title="New Citation", size=(400, 450))

        lbl = wx.StaticText(self, label='Create Citation', pos=(116, 10))
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        lbl.SetFont(font)

        self.stop_date = wx.TextCtrl(self, -1, '', pos=(115, 40))
        wx.StaticText(self, -1, 'Stop Date', pos=(230, 40))

        self.stop_time = wx.TextCtrl(self, -1, '', (115, 80))
        wx.StaticText(self, -1, 'Stop Time', (230, 80))

        self.actual_speed = wx.TextCtrl(self, -1, '', (115, 120))
        wx.StaticText(self, -1, 'Actual Speed', (230, 120))

        self.posted_speed = wx.TextCtrl(self, -1, '', (115, 160))
        wx.StaticText(self, -1, 'Posted Speed', (230, 160))

        self.mph_over = wx.TextCtrl(self, -1, '', (115, 200))
        wx.StaticText(self, -1, 'MPH Over', (230, 200))

        self.age = wx.TextCtrl(self, -1, '', (115, 240))
        wx.StaticText(self, -1, 'Age', (230, 240))

        self.violator_sex = wx.TextCtrl(self, -1, '', (115, 280))
        wx.StaticText(self, -1, 'Sex', (230, 280))

        ok_btn = wx.Button(self, id=wx.ID_OK, pos=(135, 330))  

class ShowData(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(815, 550))
        panel = wx.Panel(self, -1)

        self.table_name = wx.StaticText(panel, -1, 'Citation Data', pos=(30, 15))
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.table_name.SetFont(font)
        self.data = wx.ListCtrl(panel, -1, style=wx.LC_REPORT, pos=(20, 50), size=(750, 400))

        self.data.InsertColumn(0, 'Ticket ID', width=70)
        self.data.InsertColumn(1, 'Stop Date', width=100)
        self.data.InsertColumn(2, 'Stop Time', width=100)
        self.data.InsertColumn(3, 'Actual Speed', width=100)
        self.data.InsertColumn(4, 'Posted Speed', width=100)
        self.data.InsertColumn(5, 'MPH Over', width=100)
        self.data.InsertColumn(6, 'Age', width=70)
        self.data.InsertColumn(7, 'Sex', width=70)

        display = wx.Button(panel, -1, 'Display', size=(-1, 30), pos=(40, 470))
        insert = wx.Button(panel, -1, 'Add Citation', size=(-1, 30), pos=(140, 470))
        close = wx.Button(panel, -1, 'Close', size=(-1, 30), pos=(253, 470))

        display.Bind(wx.EVT_BUTTON, self.OnDisplay ) 
        insert.Bind(wx.EVT_BUTTON, self.AddCitation )
        close.Bind(wx.EVT_BUTTON, self.CloseApp)

    def GetData(self):
        self.data.DeleteAllItems()
        connect = sqlite3.connect('speeding_tickets.db')
        cursor = connect.cursor()

        cursor.execute('SELECT * FROM tickets')
        results = cursor.fetchall()
        for row in results:
            self.data.Append(row)
        
        cursor.close()
        connect.close()

    def OnDisplay(self, event):
        self.GetData()

    def AddCitation(self, event):
        dlg = InsertCitationBox()
        btnID = dlg.ShowModal()
        if btnID == wx.ID_OK:
            stop_date = dlg.stop_date.GetValue()  
            stop_time = dlg.stop_time.GetValue()
            actual_speed = dlg.actual_speed.GetValue()
            posted_speed = dlg.posted_speed.GetValue()
            mph_over = dlg.mph_over.GetValue()
            age = dlg.age.GetValue()
            violator_sex = dlg.violator_sex.GetValue()

        if stop_date != "" and stop_time != "" and actual_speed != "" and posted_speed != "" and mph_over != "" and age != "" and violator_sex != "":

            connect = sqlite3.connect('speeding_tickets.db')
            cursor = connect.cursor()
            
            sql = "INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

            cursor.execute(sql, (None, stop_date, stop_time, actual_speed, posted_speed, mph_over, age, violator_sex))
            connect.commit()

            self.GetData()
        
        dlg.Destroy()


    def CloseApp(self, event):
        self.Close()


app = wx.App()
sd = ShowData(None, -1, 'Citation Data')
sd.Show()
app.MainLoop()


