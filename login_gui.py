import wx

class LoginFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title)  #need to set size?
        
        #Student ID
        sizerID = wx.BoxSizer(wx.HORIZONTAL)
        sizerID.Add(wx.StaticText(self, label = "Student ID:", size = (70, -1)), 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.textID = wx.TextCtrl(self)
        sizerID.AddSpacer((5,0))
        sizerID.Add(self.textID, 5, wx.EXPAND | wx.ALL, 2)

        #Password
        sizerPassword = wx.BoxSizer(wx.HORIZONTAL)
        sizerPassword.Add(wx.StaticText(self, label = "Password:", size = (70,-1)), 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        self.textPassword = wx.TextCtrl(self, style = wx.TE_PASSWORD)
        sizerPassword.AddSpacer((5,0))
        sizerPassword.Add(self.textPassword, 5, wx.EXPAND | wx.ALL, 2)

        #buttons
        self.buttonLogin = wx.Button(self, label = "Login", size = (100,-1))
        self.buttonExit = wx.Button(self, label = "Exit", size = (100,-1))
        sizerButton = wx.BoxSizer(wx.HORIZONTAL)
        sizerButton.Add(self.buttonLogin, 1, wx.FIXED_MINSIZE,10)
        sizerButton.AddSpacer((15,0))
        sizerButton.Add(self.buttonExit, 1, wx.FIXED_MINSIZE,10)

        #Status Box
        self.textStatus = wx.TextCtrl(self, style = wx.TE_MULTILINE, size = (-1, 600))
        self.textStatus.SetEditable(False)
    
        #sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizerID,0,wx.ALIGN_CENTER | wx.ALL, 2)
        sizer.Add(sizerPassword,0,wx.ALIGN_CENTER | wx.ALL, 2)
        sizer.Add(sizerButton,0,wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add(self.textStatus, 0, wx.ALL | wx.EXPAND, 5)
       
        #binding event
        self.Bind(wx.EVT_BUTTON, self.Login, self.buttonLogin)
        self.Bind(wx.EVT_BUTTON, self.Exit, self.buttonExit)

        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        self.SetSize((350,400))
        self.SetMinSize((300,400))
        self.SetMaxSize((500,650))
        #self.sizer.SetMinSize((400,400))
        self.Show()

    def Login(self, event):
        ID = self.textID.GetValue()
        Password = self.textPassword.GetValue()
        print ID, Password
        self.textStatus.AppendText("ID:%s, PSW:%s" % (ID, Password) + '\n')
        newframe = LoginFrame(None, "NEW FRAME")
        self.Hide()
        newframe.Show()
    
    def Exit(self, event):
        self.Close(False)

app = wx.App(False)
frame = LoginFrame(None, "Login Window")
app.MainLoop()