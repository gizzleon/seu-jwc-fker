# -*- coding: utf-8 -*-

import wx
import csv

class NumbersOnlyValidator(wx.PyValidator):
	def __init__(self):
		wx.PyValidator.__init__(self)
#		print "initate"
	def Clone(self):
		return NumbersOnlyValidator()
		
	def Validate(self, win):
		print "start"
		textCtrl = self.GetWindow()
		text = textCtrl.GetValue()
		print text
		for letter in text:
			if letter < '0' or letter > '9':
				wx.MessageBox("Enter numbers only", "Error")
				textCtrl.SetFocus()
				return False
		return True
	
	def TransferToWindow(self):
		return True
	def TransferFromWindow(self):
		return True

class SettingFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title)
		
		panel = wx.Panel(self, wx.ID_ANY)

		# File Operation: import & export
		sizerFileOp = wx.BoxSizer(wx.HORIZONTAL)
		self.buttonImport = wx.Button(panel, label = "import", size = (60, -1))
		self.buttonExport = wx.Button(panel, label = "export", size = (60, -1))
		sizerFileOp.Add(self.buttonImport, 1, wx.FIXED_MINSIZE | wx.ALL, 2)
		sizerFileOp.AddSpacer((5,0))
		sizerFileOp.Add(self.buttonExport, 1, wx.FIXED_MINSIZE | wx.ALL, 2)

		# Course List
		self.index = 0
		self.listCtrl = wx.ListCtrl(panel, size = (-1, 100), style = wx.LC_REPORT|wx.BORDER_SUNKEN)
		self.listCtrl.InsertColumn(0, "semester")
		self.listCtrl.InsertColumn(1, "type")
		self.listCtrl.InsertColumn(2, "course code")
		self.listCtrl.InsertColumn(3, "course name")

		
		# Semester
		sizerSemester = wx.BoxSizer(wx.VERTICAL)
		sizerSemester.Add(wx.StaticText(panel, label = "Semester"))	
		semesterList = ['1', '2', '3']
		self.choiceSemester = wx.Choice(panel, wx.ID_ANY, choices = semesterList)		
		sizerSemester.Add(self.choiceSemester, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
		
		# Course Type		
		sizerType = wx.BoxSizer(wx.VERTICAL)
		sizerType.Add(wx.StaticText(panel, label = "Type"))
		typeList = ['major', 'literature']
		self.choiceType = wx.Choice(panel, wx.ID_ANY, choices = typeList)
		sizerType.Add(self.choiceType, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
		
		# Course Code
		sizerCode = wx.BoxSizer(wx.VERTICAL)
		sizerCode.Add(wx.StaticText(panel, label = "Code"))
		self.textCode = wx.TextCtrl(panel, validator = NumbersOnlyValidator())
		sizerCode.Add(self.textCode, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)		
		
		# Course Name
		sizerName = wx.BoxSizer(wx.VERTICAL)
		sizerName.Add(wx.StaticText(panel, label = "Name"))
		self.textName = wx.TextCtrl(panel)
		sizerName.Add(self.textName, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		
		
		# buttons in editbar
		self.buttonSubmit = wx.Button(panel, label = "submit", size = (60, -1))
#		self.buttonSubmit.Disable()
#		self.buttonSubmit.Enable()
		self.buttonDelete = wx.Button(panel, id = wx.ID_DELETE, label = "delete", size = (60, -1))
		self.buttonDelete.Disable()
		
		
		# Edit Bar
		sizerEdit = wx.BoxSizer(wx.HORIZONTAL)
		sizerEdit.Add(sizerSemester, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
		sizerEdit.Add(sizerType, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
		sizerEdit.Add(sizerCode, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
		sizerEdit.Add(sizerName, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
		sizerEdit.Add(self.buttonSubmit, 2, wx.ALIGN_BOTTOM | wx.ALL, 2)
		sizerEdit.AddSpacer((5,0))
		sizerEdit.Add(self.buttonDelete, 2, wx.ALIGN_BOTTOM | wx.ALL, 2)
		
		# buttons
		self.buttonOkay = wx.Button(panel, label = "OK", size = (60, -1))		
		
		# sizer
		sizer = wx.BoxSizer(wx.VERTICAL)		
		sizer.Add(sizerFileOp, 0, wx.ALL | wx.FIXED_MINSIZE, 5)
		sizer.Add(self.listCtrl, 0, wx.ALL|wx.EXPAND, 5)
		sizer.Add(sizerEdit, 0, wx.ALL | wx.EXPAND, 5)
		sizer.Add(self.buttonOkay, 0, wx.ALL)
			
		# Events Binding
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.SelectEntry, self.listCtrl)
		self.Bind(wx.EVT_BUTTON, self.ImportFromFile, self.buttonImport)
		self.Bind(wx.EVT_BUTTON, self.ExportToFile, self.buttonExport)
		self.Bind(wx.EVT_BUTTON, self.AddEntry, self.buttonSubmit)
		self.Bind(wx.EVT_BUTTON, self.DeleteEntry, self.buttonDelete)
		self.Bind(wx.EVT_BUTTON, self.SubmitData, self.buttonOkay)			
		
		panel.SetSizer(sizer)
		self.SetSize((600, 400))
		self.Show()
		
	def CheckEntry(self):
		if self.choiceSemester.GetStringSelection() == "":
			return (False, "Please select semester!")
		if self.choiceType.GetStringSelection() == "":
			return (False, "Please select Type!")
		if self.textCode.GetValue() != "":
			for letter in self.textCode.GetValue():
				if letter < '0' or letter > '9':
					return (False, "Numbers only")
		if self.textCode.GetValue() == "" and self.textName.GetValue() == "":
			return (False, "At least enter one")
		return (True, "Success")

	def SelectEntry(self, event):	
		self.buttonDelete.Enable()
		
	def AddEntry(self, event):
		status = self.CheckEntry()
		if status[0] == False:
			wx.MessageBox(status[1],"Input Error")
			return
		self.listCtrl.InsertStringItem(self.index, self.choiceSemester.GetStringSelection())
		self.listCtrl.SetStringItem(self.index, 1, self.choiceType.GetStringSelection())
		self.listCtrl.SetStringItem(self.index, 2, self.textCode.GetValue())
		self.listCtrl.SetStringItem(self.index, 3, self.textName.GetValue())
		self.index += 1
		
	def DeleteEntry(self, event):
		selected = self.listCtrl.GetNextSelected(-1)
		while selected != -1:
			self.listCtrl.DeleteItem(selected)
			selected = self.listCtrl.GetNextSelected(-1)
			self.index -= 1
		self.buttonDelete.Disable()
	
	def ImportFromFile(self, event):
		openDlg = wx.FileDialog(None, style = wx.FD_OPEN, wildcard = "CSV Files (*.csv)|*.csv")
		openDlg.ShowModal()
		filePath = openDlg.GetPath()
		openDlg.Destroy()
		
		try:
			print "loading the file"
			csvfile = file(filePath, 'rb')
		except Exception, e:
			print e
			return
		
		try:
			print "ready to write"
			self.index = 0
			reader = csv.reader(csvfile)
			for row in reader:
				self.listCtrl.InsertStringItem(self.index, row[0])
				self.listCtrl.SetStringItem(self.index, 1, row[1])
				self.listCtrl.SetStringItem(self.index, 2, row[2])
				self.listCtrl.SetStringItem(self.index, 3, row[3].decode('utf-8'))
				self.index += 1
		except Exception, e:
			print e
		finally:
			csvfile.close()
	
	
	def ExportToFile(self, event):
		# File Dialog
		saveDlg = wx.FileDialog(None, style = wx.FD_SAVE, wildcard = "CSV Files (*.csv)|*.csv")		
		saveDlg.ShowModal()
		filePath = saveDlg.GetPath()
		print "file path get"
		saveDlg.Destroy()
		
		try:
			print "loading the file..."
			csvfile = file(filePath, 'wb')
		except:
			print "file openning failed"
			return
		try:
			print "ready to write the file"
			writer = csv.writer(csvfile)
			
			for i in range(self.index):
				courseInfo = []
				for j in range(4):
					courseInfo.append(self.listCtrl.GetItem(i, j).GetText().encode('utf-8'))  #solve the encoding problem
#				print courseInfo
				writer.writerow(courseInfo)
		except:
			print "writing failed"
		finally:
			csvfile.close()
	def GetCourseList(self):
		courseList = []
		for i in range(self.index):
			courseInfo = []
			for j in range(4):
				courseInfo.append(self.listCtrl.GetItem(i, j).GetText())  #solve the encoding problem
			courseList.append(courseInfo)
		return courseList
		
	def SubmitData(self, event):
		self.Hide()
class LoginFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title)  #need to set size?
		
		mainPanel = wx.Panel(self, wx.ID_ANY)
	
		
		# ---- LEFT SIZER ---
		panelLeft = wx.Panel(mainPanel, wx.ID_ANY)

		#Student ID
		sizerID = wx.BoxSizer(wx.HORIZONTAL)
		sizerID.Add(wx.StaticText(panelLeft, label = "Student ID:", size = (70, -1)), 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
		self.textID = wx.TextCtrl(panelLeft)
		sizerID.AddSpacer((5,0))
		sizerID.Add(self.textID, 5, wx.EXPAND | wx.ALL, 2)
		
		#Password
		sizerPassword = wx.BoxSizer(wx.HORIZONTAL)
		sizerPassword.Add(wx.StaticText(panelLeft, label = "Password:", size = (70,-1)), 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
		self.textPassword = wx.TextCtrl(panelLeft, style = wx.TE_PASSWORD)
		sizerPassword.AddSpacer((5,0))
		sizerPassword.Add(self.textPassword, 5, wx.EXPAND | wx.ALL, 2)
		
		#Buttons
		self.buttonLogin = wx.Button(panelLeft, label = "Login", size = (80,-1))
		self.buttonExit = wx.Button(panelLeft, label = "Exit", size = (80,-1))
		sizerButton = wx.BoxSizer(wx.HORIZONTAL)
		sizerButton.Add(self.buttonLogin, 1, wx.FIXED_MINSIZE)
		sizerButton.AddSpacer((15,0))
		sizerButton.Add(self.buttonExit, 1, wx.FIXED_MINSIZE)
		
		# Status Box
		self.textStatus = wx.TextCtrl(panelLeft, style = wx.TE_MULTILINE, size = (-1, 700))
		self.textStatus.SetEditable(False)
		
		# Button - setting panel control
		self.buttonSettingCtrl = wx.Button(panelLeft, label = "Collapse<<<", size = (100, -1))		
		
		#sizer
		sizerLeft = wx.BoxSizer(wx.VERTICAL)
		sizerLeft.Add(sizerID,0,wx.ALIGN_CENTER | wx.ALL, 2)
		sizerLeft.Add(sizerPassword,0,wx.ALIGN_CENTER | wx.ALL, 2)
		sizerLeft.Add(sizerButton,0,wx.ALIGN_CENTER | wx.ALL, 5)
		sizerLeft.Add(self.textStatus, 0, wx.ALL | wx.EXPAND, 5)	
		
		#binding events
		self.Bind(wx.EVT_BUTTON, self.Login, self.buttonLogin)
		self.Bind(wx.EVT_BUTTON, self.Exit, self.buttonExit)
		
		panelLeft.SetSizer(sizerLeft)


		# ---- RIGHT SIZER ---
		panelRight = wx.Panel(mainPanel, wx.ID_ANY)

		# Buttons - Operation
		sizerButtons = wx.BoxSizer(wx.HORIZONTAL)
		self.buttonImport = wx.Button(panelRight, label = "import", size = (70, -1))
		self.buttonExport = wx.Button(panelRight, label = "export", size = (70, -1))
		self.buttonApply = wx.Button(panelRight, label = "apply", size = (70, -1))
		self.buttonClear = wx.Button(panelRight, label = "clear", size = (70, -1))
		sizerButtons.Add(self.buttonImport, 1, wx.FIXED_MINSIZE | wx.ALL, 2)
		sizerButtons.AddSpacer((5,0))
		sizerButtons.Add(self.buttonExport, 1, wx.FIXED_MINSIZE | wx.ALL, 2)
		sizerButtons.AddSpacer((5,0))
		sizerButtons.Add(self.buttonApply, 1, wx.FIXED_MINSIZE | wx.ALL, 2)
		sizerButtons.AddSpacer((5,0))
		sizerButtons.Add(self.buttonClear, 1, wx.FIXED_MINSIZE | wx.ALL, 2)
		

		# Course List
		self.index = 0
		self.listCtrl = wx.ListCtrl(panelRight, style = wx.LC_REPORT|wx.BORDER_SUNKEN)
		self.listCtrl.InsertColumn(0, "semester")
		self.listCtrl.InsertColumn(1, "type")
		self.listCtrl.InsertColumn(2, "course code")
		self.listCtrl.InsertColumn(3, "course name")
		self.listCtrl.SetColumnWidth(0, 70)
		self.listCtrl.SetColumnWidth(1, 120)
		self.listCtrl.SetColumnWidth(2, 160)
		self.listCtrl.SetColumnWidth(3, 160)

		
		# Semester
		sizerSemester = wx.BoxSizer(wx.VERTICAL)
		sizerSemester.Add(wx.StaticText(panelRight, label = "Semester"))	
		semesterList = ['1', '2', '3']
		self.choiceSemester = wx.Choice(panelRight, wx.ID_ANY, choices = semesterList)		
		sizerSemester.Add(self.choiceSemester, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 2)
		
		# Course Type		
		sizerType = wx.BoxSizer(wx.VERTICAL)
		sizerType.Add(wx.StaticText(panelRight, label = "Type"))
		typeList = ['major', 'literature']
		self.choiceType = wx.Choice(panelRight, wx.ID_ANY, choices = typeList)
		sizerType.Add(self.choiceType, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 2)
		
		# Course Code
		sizerCode = wx.BoxSizer(wx.VERTICAL)
		sizerCode.Add(wx.StaticText(panelRight, label = "Code"))
		self.textCode = wx.TextCtrl(panelRight, validator = NumbersOnlyValidator())
		sizerCode.Add(self.textCode, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 2)		
		
		# Course Name
		sizerName = wx.BoxSizer(wx.VERTICAL)
		sizerName.Add(wx.StaticText(panelRight, label = "Name"))
		self.textName = wx.TextCtrl(panelRight)
		sizerName.Add(self.textName, 1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
		
		
		# buttons in editbar
		self.buttonAdd = wx.Button(panelRight, id = wx.ID_ADD, label = "Add", size = (70, -1))
#		self.buttonSubmit.Disable()
#		self.buttonSubmit.Enable()
		self.buttonDelete = wx.Button(panelRight, id = wx.ID_DELETE, label = "Delete", size = (70, -1))
		self.buttonDelete.Disable()
		
		
		# Edit Bar
		sizerEdit = wx.BoxSizer(wx.HORIZONTAL)
		sizerEdit.Add(sizerSemester, 0, wx.ALIGN_BOTTOM | wx.ALL, 2)
		sizerEdit.Add(sizerType, 0, wx.ALIGN_BOTTOM | wx.ALL, 2)
		sizerEdit.Add(sizerCode, 0, wx.ALIGN_BOTTOM | wx.ALL, 2)
		sizerEdit.Add(sizerName, 0, wx.ALIGN_BOTTOM | wx.ALL, 2)
		sizerEdit.Add(self.buttonAdd, 0, wx.ALIGN_BOTTOM | wx.ALL, 2)
		sizerEdit.Add(self.buttonDelete, 0, wx.ALIGN_BOTTOM | wx.ALL, 2)
		
		# sizer
		sizerRight = wx.BoxSizer(wx.VERTICAL)		
		sizerRight.Add(sizerButtons, 1, wx.ALL | wx.ALIGN_CENTER | wx.FIXED_MINSIZE, 5)
		sizerRight.Add(self.listCtrl, 50, wx.ALL|wx.EXPAND, 5)  # 50 - ensure the listctrl would expand	
		sizerRight.Add(sizerEdit, 0, wx.ALL | wx.ALIGN_CENTER , 5)
#		sizerRight.Add(self.buttonOkay, 0, wx.ALIGN_BOTTOM)
		
		# Events Binding
#		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.SelectEntry, self.listCtrl)
#		self.Bind(wx.EVT_BUTTON, self.ImportFromFile, self.buttonImport)
#		self.Bind(wx.EVT_BUTTON, self.ExportToFile, self.buttonExport)
#		self.Bind(wx.EVT_BUTTON, self.AddEntry, self.buttonSubmit)
#		self.Bind(wx.EVT_BUTTON, self.DeleteEntry, self.buttonDelete)
#		self.Bind(wx.EVT_BUTTON, self.SubmitData, self.buttonOkay)			
		
		panelRight.SetSizer(sizerRight)
	
		# ---- main panel setting ----
	
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		mainPanel.SetSizer(mainSizer)	
		mainSizer.Add(panelLeft, 1, wx.ALL | wx.ALIGN_CENTER, 2)
		mainSizer.AddSpacer((10, 0))
		mainSizer.Add(panelRight, 0, wx.ALL | wx.ALIGN_CENTER, 2)
		self.SetSize((900, 500))
		self.SetMinSize((780, 300))
		self.Show()

	def Login(self, event):
		ID = self.textID.GetValue()
		Password = self.textPassword.GetValue()
		print ID, Password
		self.textStatus.AppendText("ID:%s, PSW:%s" % (ID, Password) + '\n')
#		self.frameNew = SettingFrame(self, "setting window")
#		frameNew.ShowModal()
#		frameNew.Show()
#		frameNew.Destroy()
#        newframe = LoginFrame(None, "NEW FRAME")
#        self.Hide()
#        newframe.Show()

	def Exit(self, event):
		self.Close(False)

	def ShowMessage(self, message):
		print message
		self.textStatus.AppendText(message + '\n')
	
if __name__ == "__main__":
	app = wx.App(False)
	frame = LoginFrame(None, "Login Window")
	app.MainLoop()
#	print frame.GetCourseList
#	frame.Close()
	app.Destroy()