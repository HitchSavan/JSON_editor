import json
import sys
import os
import ast
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from fpdf import FPDF
import Editor
from pathlib import Path
global wrap
wrap=['','']
global saved
saved=1
global cutted
global copp
copp=0
path=os.getcwd()+"\\icons\\"
"""
	Editor class
	@class[editorApp]
	@param QtWidgets.QMainWindow
	@param Editor.Ui_MainWindow
"""
class editorApp(QtWidgets.QMainWindow, Editor.Ui_MainWindow):
	"""
		Main constructor
		@constructor
		@see initUi()
	"""
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.initUI()
	"""
		GUI triggers handler
	"""
	def initUI(self):
		self.setWindowTitle("JSON Editor")

		self.action_2.triggered.connect(self.openFile)

		self.action_2.setStatusTip('Выбрать файл')

		self.action_2.setShortcut('Ctrl+O')

		self.action.triggered.connect(self.createFile)

		self.action.setStatusTip('Создать новый файл')

		self.action_4.triggered.connect(self.saveAsFile)

		self.action_3.triggered.connect(self.saveFile)

		self.action_3.setStatusTip('Сохранить открытый файл')

		self.action_3.setShortcut('Ctrl+S')

		self.toolButton_9.clicked.connect(self.synchToTree)

		self.treeView.itemPressed.connect(self.enabling)

		self.toolButton_6.clicked.connect(self.deleteTreeItem)

		self.toolButton.clicked.connect(self.renameTreeItem)

		self.toolButton_4.clicked.connect(self.cutTreeItem)

		self.toolButton_5.clicked.connect(self.copyTreeItem)

		self.toolButton_3.clicked.connect(self.insertTreeItem)

		self.toolButton_10.clicked.connect(self.minific)

		self.toolButton_11.clicked.connect(self.formating)

		self.action_PDF.triggered.connect(self.toPDF)

		self.toolButton_7.clicked.connect(self.copyName)

		self.toolButton_8.clicked.connect(self.pasteName)

		self.action_5.triggered.connect(self.renameTreeItem)

		self.action_6.triggered.connect(self.changeType)

		self.action_8.triggered.connect(self.insertTreeBef)

		self.action_9.triggered.connect(self.insertTreeIn)

		self.action_10.triggered.connect(self.insertTreeAfter)

		self.action_11.triggered.connect(self.cutTreeItem)

		self.action_12.triggered.connect(self.copyTreeItem)

		self.action_13.triggered.connect(self.deleteTreeItem)

		self.action_14.triggered.connect(self.copyName)

		self.action_15.triggered.connect(self.pasteName)


		self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.treeView.customContextMenuRequested.connect(self.menuRMB)
		self.renameM = QtWidgets.QAction('Переименовать', self)
		self.renameM.triggered.connect(self.renameTreeItem)
		self.changeTypeM = QtWidgets.QAction('Изменить тип узла', self)
		self.changeTypeM.triggered.connect(self.changeType)
		self.insertM = QtWidgets.QAction('Вставить...', self)
		self.insertM.triggered.connect(self.insertTreeItem)
		self.cutM = QtWidgets.QAction('Вырезать', self)
		self.cutM.triggered.connect(self.cutTreeItem)
		self.copyM = QtWidgets.QAction('Копировать', self)
		self.copyM.triggered.connect(self.copyTreeItem)
		self.deleteM = QtWidgets.QAction('Удалить', self)
		self.deleteM.triggered.connect(self.deleteTreeItem)
		self.copyNameM = QtWidgets.QAction('Копировать значение', self)
		self.copyNameM.triggered.connect(self.copyName)
		self.pasteNameM = QtWidgets.QAction('Вставить значение', self)
		self.pasteNameM.triggered.connect(self.pasteName)	
	"""
		Select file from directory and open selected file
		@see ifNotSaved()
		@see saveFile()
		@see fillTree()
	"""
	def openFile(self):
		global wrap
		global saved
		if saved==0:
			sav=self.ifNotSaved()
			if sav=='Cancel':
				return 0
			elif sav=='Yes':
				self.saveFile()
		fname=QFileDialog.getOpenFileName(self, 'Окрыть файл', '/')[0]
		if fname=='':
			return 0
		saved=0
		wrap[0]=fname
		with open(fname, 'r', encoding='utf-8') as read_file:
			data=read_file.read()
		data=data.replace("'", "\"")
		dic=json.loads(data)
		self.textEdit.setText(json.dumps(dic, sort_keys=True, ensure_ascii=False, indent=4))
		self.treeView.headerItem().setText(0, wrap[0])
		widget=self.treeView
		self.fillTree(widget, dic)
		self.toolButton_10.setEnabled(True)
	"""
		Creates new blank file in chosen directory
		@see ifNotSaved()
		@see saveFile()
	"""
	def createFile(self):
		global wrap
		global saved
		if saved==0:
			sav=self.ifNotSaved()
			if sav=='Cancel':
				return 0
			elif sav=='Yes':
				self.saveFile()
		fname=QFileDialog.getSaveFileName(self, 'Создать в...', '/')[0]
		if fname=='':
			return 0
		saved=0
		wrap[0]=fname
		outtext=json.loads('{}')
		with open(fname, 'w', encoding='utf-8') as write_file:
			json.dump(outtext, write_file)
		self.textEdit.setText("{}")
		self.treeView.clear()
		self.toolButton_10.setEnabled(True)
	"""
		Save file from text in the editor in chosen directory
		@exception json.decoder.JSONDecodeError - errors in syntax
	"""
	def saveAsFile(self):
		global wrap
		global saved
		try:
			json.loads(self.textEdit.toPlainText())
		except json.decoder.JSONDecodeError:
			QMessageBox.about(self, "Ошибка", "Отсутствуют необходимые символы")
			return 0
		fname=QFileDialog.getSaveFileName(self, 'Сохранить файл как...', '/')[0]
		if fname=='':
			return 0
		saved=1
		wrap[0]=fname
		outtext=self.textEdit.toPlainText()
		outtext=outtext.replace("'", "\"")
		outtext=json.loads(outtext)
		with open(fname, 'w', encoding='utf-8') as write_file:
			json.dump(outtext, write_file)
	"""
		Rewrite file from text in the editor
		@exception json.decoder.JSONDecodeError - errors in syntax
	"""
	def saveFile(self):
		global wrap
		global saved
		try:
			json.loads(self.textEdit.toPlainText())
		except json.decoder.JSONDecodeError:
			QMessageBox.about(self, "Ошибка", "Отсутствуют необходимые символы")
			return 0
		saved=1
		if wrap[0]=='':
			return 0
		outtext=self.textEdit.toPlainText()
		if outtext=='':
			outtext+='{}'
		outtext=outtext.replace("'", "\"")
		outtext=json.loads(outtext)
		with open(wrap[0], 'w', encoding='utf-8') as write_file:
			json.dump(outtext, write_file)
	"""
		Warns that the file was not saved
		@returns "Yes" - pressed button
		@returns "No" - pressed button
		@returns "Cancel" - pressed button
	"""
	def ifNotSaved(self):
		res=QtWidgets.QMessageBox.question(self, 'Внимание!', "Файл не сохранен.\nСохранить?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
		if res==QtWidgets.QMessageBox.Yes:
			return 'Yes'
		elif res==QtWidgets.QMessageBox.No:
			return 'No'
		else:
			return 'Cancel'
	"""
		Ïnserts item in tree
		@param {QtWidgets.QTreeWidgetItem()} item - current item in tree
		@param value - inserting value
	"""
	def fillItem(self, item, value):
		item.setExpanded(True)
		if type(value) is dict:
			for key, val in sorted(value.items()):
				child=QtWidgets.QTreeWidgetItem()
				if type(val) is list:
					child.setText(0, str(key)+" [array]")
				elif type(val) is dict:
					child.setText(0, str(key)+" [object]")
				else:
					child.setText(0, str(key)+" [string]")
				item.addChild(child)
				self.fillItem(child, val)
		elif type(value) is list:
			for val in value:
				child=QtWidgets.QTreeWidgetItem()
				item.addChild(child)
				if type(val) is dict:
					child.setText(0, ' [object]')
					self.fillItem(child, val)
				elif type(val) is list:
					child.setText(0, ' [array]')
					self.fillItem(child, val)
				else:
					if type(val) is int:
						child.setText(0, str(val)+" [number (int)]")
					elif type(val) is float:
						child.setText(0, str(val)+" [number (real)]")
					else:
						child.setText(0, str(val)+" [string]")
				child.setExpanded(True)
		else:
			child=QtWidgets.QTreeWidgetItem()
			if type(value) is int:
				child.setText(0, str(value)+" [number (int)]")
			elif type(value) is float:
				child.setText(0, str(value)+" [number (real)]")
			else:
				child.setText(0, str(value)+" [string]")
			item.addChild(child)
	"""
		Fills tree with given dict
		@param {QtWidgets.QTreeWidget()} widget - tree widget
		@param {dict} value - dict from text from editor
		@see fillItem()
	"""
	def fillTree(self, widget, value):
		widget.clear()
		self.fillItem(widget.invisibleRootItem(), value)
	"""
		Fills tree with text from the editor
		@exception json.decoder.JSONDecodeError - errors with syntax
		@see fillTree()
		@see disabling()
	"""
	def synchToTree(self):
		global saved
		saved=0
		text=self.textEdit.toPlainText()
		if text=='':
			return 0
		try:
			json.loads(text)
		except json.decoder.JSONDecodeError:
			QMessageBox.about(self, "Ошибка", "Отсутствуют необходимые символы")
			return 0
		text=text.replace("'", "\"")
		dic=json.loads(text)
		widget=self.treeView
		self.fillTree(widget, dic)
		self.disabling()
	"""
		Converts tree widget to dict
		@returns {dict} result - dict from tree
		@see formatTree()
		@see unpack()
	"""
	def getDict(self):
		global saved
		saved=0
		self.formatTree()
		result={}
		"""
			Converts tree item to python type
			@param {QtWidgets.QTreeWidgetItem()} to_unpack - tree item
			@param {str} key - name of tree item
			@param source=None - current python type (of parent of current tree item)
		"""
		def unpack(to_unpack, key, source=None):
			if source is None:
				core=result
			else:
				core=source
			if key.rfind(" [object]")!=-1:
				if to_unpack.parent() is not None:
					if to_unpack.parent().text(0).rfind(" [array]")==-1:
						core.update({key[0:key.rfind(" [")]: {}})
				else:
					core.update({key[0:key.rfind(" [")]: {}})
			elif key.rfind(" [array]")!=-1:
				if to_unpack.parent() is not None:
					if to_unpack.parent().text(0).rfind(" [array]")==-1:
						core.update({key[0:key.rfind(" [")]: []})
				else:
					core.update({key[0:key.rfind(" [")]: []})
			for child_index in range(to_unpack.childCount()):
				child=to_unpack.child(child_index)
				child_text=child.text(0)
				try:
					child_text=float(child_text)
				except ValueError:
					try:
						child_text=int(child_text)
					except ValueError:
						pass
				if key.rfind(" [object]")!=-1:
					if child.childCount()>0:
						if to_unpack.parent() is not None:
							if to_unpack.parent().text(0).rfind(" [array]")!=-1:
								unpack(child, child_text, core)
								continue
						unpack(child, child_text, core[key[0:key.rfind(" [")]])
				elif key.rfind(" [array]")!=-1:
					if child_text.rfind(" [object]")!=-1:
						core[key[0:key.rfind(" [")]].append({})
					elif child_text.rfind(" [array]")!=-1:
						core[key[0:key.rfind(" [")]].append([])
					else:
						if child_text.rfind(" [number (int)]")!=-1:
							if to_unpack.parent() is not None:
								if to_unpack.parent().text(0).rfind(" [array]")!=-1:
									core.append(int(child_text[0:child_text.rfind(" [")]))
									continue
							core[key[0:key.rfind(" [")]].append(int(child_text[0:child_text.rfind(" [")]))
						elif child_text.rfind(" [number (real)]")!=-1:
							if to_unpack.parent() is not None:
								if to_unpack.parent().text(0).rfind(" [array]")!=-1:
									core.append(float(child_text[0:child_text.rfind(" [")]))
									continue
							core[key[0:key.rfind(" [")]].append(float(child_text[0:child_text.rfind(" [")]))
						else:
							if to_unpack.parent() is not None:
								if to_unpack.parent().text(0).rfind(" [array]")!=-1:
									core.append(child_text[0:child_text.rfind(" [")])
									continue
							core[key[0:key.rfind(" [")]].append(child_text[0:child_text.rfind(" [")])
					if child.childCount()>0:
						if child_text.rfind(" [object]")!=1 or child_text.rfind(" [array]")!=-1:
							unpack(child, child_text, core[key[0:key.rfind(" [")]][-1])
						else:
							unpack(child, child_text, core[key[0:key.rfind(" [")]])
				else:
					if type(core) is list:
						if child_text.rfind(" [number (int)]")!=-1:
							core.append(int(child_text[0:child_text.rfind(" [")]))
						elif child_text.rfind(" [number (real)]")!=-1:
							core.append(float(child_text[0:child_text.rfind(" [")]))
						else:
							core.append(child_text[0:child_text.rfind(" [")])
					elif type(core) is dict:
						if child_text.rfind(" [number (int)]")!=-1:
							core.update({key[0:key.rfind(" [")]: int(child_text[0:child_text.rfind(" [")])})
						elif child_text.rfind(" [number (real)]")!=-1:
							core.update({key[0:key.rfind(" [")]: float(child_text[0:child_text.rfind(" [")])})
						else:
							core.update({key[0:key.rfind(" [")]: child_text[0:child_text.rfind(" [")]})

		for index in range(self.treeView.topLevelItemCount()):
			parent=self.treeView.topLevelItem(index)
			element_text=parent.text(0)
			unpack(parent, element_text)
		return result
	"""
		Enables some of tree editor buttons
		@see disabling()
	"""
	def enabling(self):
		self.menu_2.setEnabled(True)
		self.toolButton.setEnabled(True)   #rename node
		self.toolButton_2.setEnabled(True) #change type of node
		self.toolButton_4.setEnabled(True) #cut
		self.toolButton_5.setEnabled(True) #copy
		self.toolButton_6.setEnabled(True) #delete
		self.toolButton_7.setEnabled(True) #val copy
	"""
		Disables some of tree editor buttons
		@see enabling()
	"""
	def disabling(self):
		self.menu_2.setDisabled(True)
		self.toolButton.setDisabled(True)
		self.toolButton_2.setDisabled(True)
		self.toolButton_4.setDisabled(True)
		self.toolButton_5.setDisabled(True)
		self.toolButton_6.setDisabled(True)
		self.toolButton_7.setDisabled(True)
	"""
		Delete selected item in tree
		@see getDict()
	"""
	def deleteTreeItem(self):
		root=self.treeView.invisibleRootItem()
		for item in self.treeView.selectedItems():
			if ((item.parent() or root).parent() or root).text(0).rfind(" [object]")!=-1:
				child=QtWidgets.QTreeWidgetItem()
				child.setText(0, " [null]")
				(item.parent() or root).addChild(child)
			(item.parent() or root).removeChild(item)
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
	"""
		Rename selected item in tree
		@see getDict()
	"""
	def renameTreeItem(self):
		root=self.treeView.invisibleRootItem()
		for item in self.treeView.selectedItems():
			text, ok=QInputDialog.getText(self, 'Enter', 'Переименовывание: ', text=item.text(0)[0:item.text(0).rfind(" [")])
			if ok:	
				if item.text(0).rfind(" [object]")!=-1 or item.text(0).rfind(" [array]")!=-1 or item.text(0).rfind(" [string]")!=-1:
					text=text+item.text(0)[item.text(0).rfind(" ["):-1]+"]"
				else:
					text=text+" [string]"
				item.setText(0, text)
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
	"""
		Cut selected tree item
		@see getDict()
	"""
	def cutTreeItem(self):
		global cutted
		global copp
		root=self.treeView.invisibleRootItem()
		for item in self.treeView.selectedItems():
			if ((item.parent() or root).parent() or root).text(0).rfind(" [object]")!=-1:
				child=QtWidgets.QTreeWidgetItem()
				child.setText(0, " [null]")
				(item.parent() or root).addChild(child)
			cutted=(item.parent() or root).takeChild((item.parent() or root).indexOfChild(item))
		self.toolButton_3.setEnabled(True)
		self.menu_3.setEnabled(True)
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
		copp=0
	"""
		Copy selected tree item
	"""
	def copyTreeItem(self):
		global copied
		global copp
		root=self.treeView.invisibleRootItem()
		for item in self.treeView.selectedItems():
			copied=(item or root).clone()
		self.toolButton_3.setEnabled(True)
		self.menu_3.setEnabled(True)
		copp=1
	"""
		Shows paste variants
		@see insertTreeBef()
		@see insertTreeIn()
		@see insertTreeAfter()
	"""
	def insertTreeItem(self):
		self.reply=QDialog()
		vbox=QVBoxLayout()
		label_dialog=QLabel()
		label_dialog.setText('Вставить...')
		button_bef=QPushButton(self.reply)
		button_bef.setText("Перед")
		button_bef.clicked.connect(lambda: self.insertTreeBef())
		button_in=QPushButton(self.reply)
		button_in.setText('Внутрь')
		button_in.clicked.connect(lambda: self.insertTreeIn())
		button_after=QPushButton(self.reply)
		button_after.setText('После')
		button_after.clicked.connect(lambda: self.insertTreeAfter())
		layout=QHBoxLayout()
		layout.addWidget(button_bef)
		layout.addWidget(button_in)
		layout.addWidget(button_after)
		vbox.addWidget(label_dialog)
		vbox.addSpacing(20)
		vbox.addLayout(layout)
		self.reply.setLayout(vbox)
		self.reply.exec()
	"""
		Inserts copied/cutted item in selected item as child
		@see getDict()
	"""
	def insertTreeIn(self):
		global cutted
		global copied
		global copp
		if copp==0:
			for item in self.treeView.selectedItems():
				if item.text(0).rfind(" [array]")!=-1:
					item.addChild(cutted)
				elif item.text(0).rfind(" [object]")!=-1:
					child=QtWidgets.QTreeWidgetItem()
					child.setText(0, " [null]")
					cutted.addChild(child)
					item.addChild(cutted)
				else:
					item.setText(0, item.text(0)[0: item.text(0).rfind(" [")]+" [string]")
					item.addChild(cutted)
					if item.parent() is not None:
						item.parent().setText(0, item.parent().text(0)[0: item.parent().text(0).rfind(" [")]+" [object]")
						for child_index in range(item.parent().childCount()):
							child=QtWidgets.QTreeWidgetItem()
							child.setText(0, " [null]")
							item.parent().child(child_index).setText(0, item.parent().child(child_index).text(0)[0: item.parent().child(child_index).text(0).rfind(" [")]+" [string]")
							item.parent().child(child_index).addChild(child)
					else:
						item.setText(0, item.text(0)[0: item.text(0).rfind(" [")]+" [array]")
			self.toolButton_3.setDisabled(True)
			self.menu_3.setDisabled(True)
		else:
			for item in self.treeView.selectedItems():
				if item.text(0).rfind(" [array]")!=-1:
					item.addChild(copied)
				elif item.text(0).rfind(" [object]")!=-1:
					child=QtWidgets.QTreeWidgetItem()
					child.setText(0, " [null]")
					copied.addChild(child)
					item.addChild(copied)
				else:
					item.setText(0, item.text(0)[0: item.text(0).rfind(" [")]+" [string]")
					item.addChild(copied)
					item.parent().setText(0, item.parent().text(0)[0: item.parent().text(0).rfind(" [")]+" [object]")
					for child_index in range(item.parent().childCount()):
						child=QtWidgets.QTreeWidgetItem()
						child.setText(0, " [null]")
						item.parent().child(child_index).setText(0, item.parent().child(child_index).text(0)[0: item.parent().child(child_index).text(0).rfind(" [")]+" [string]")
						item.parent().child(child_index).addChild(child)
				copied=item.child(item.childCount()-1).clone()
		self.reply.close()
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
	"""
		Inserts copied/cutted item in selected item's parent as child
		@see getDict()
	"""
	def insertTreeAfter(self):
		global cutted
		global copied
		global copp
		root=self.treeView.invisibleRootItem()
		if copp==0:
			for item in self.treeView.selectedItems():
				if (item.parent() or root).text(0).rfind(" [array]")!=-1:
					(item.parent() or root).addChild(cutted)
				elif (item.parent() or root).text(0).rfind(" [object]")!=-1:
					child=QtWidgets.QTreeWidgetItem()
					child.setText(0, " [null]")
					cutted.addChild(child)
					(item.parent() or root).addChild(cutted)
				elif item.parent() is None:
					child=QtWidgets.QTreeWidgetItem()
					child.setText(0, " [null]")
					cutted.addChild(child)
					root.addChild(cutted)
				else:
					(item.parent() or root).setText(0, (item.parent() or root).text(0)[0: (item.parent() or root).text(0).rfind(" [")]+" [string]")
					(item.parent() or root).addChild(cutted)
					((item.parent() or root).parent() or root).setText(0, ((item.parent() or root).parent() or root).text(0)[0: ((item.parent() or root).parent() or root).text(0).rfind(" [")]+" [object]")
					for child_index in range(((item.parent() or root).parent() or root).childCount()):
						child=QtWidgets.QTreeWidgetItem()
						child.setText(0, " [null]")
						((item.parent() or root).parent() or root).child(child_index).setText(0, ((item.parent() or root).parent() or root).child(child_index).text(0)[0: ((item.parent() or root).parent() or root).child(child_index).text(0).rfind(" [")]+" [string]")
						((item.parent() or root).parent() or root).child(child_index).addChild(child)
			self.toolButton_3.setDisabled(True)
			self.menu_3.setDisabled(True)
		else:
			for item in self.treeView.selectedItems():
				if (item.parent() or root).text(0).rfind(" [array]")!=-1:
					(item.parent() or root).addChild(copied)
				elif (item.parent() or root).text(0).rfind(" [object]")!=-1:
					child=QtWidgets.QTreeWidgetItem()
					child.setText(0, " [null]")
					copied.addChild(child)
					(item.parent() or root).addChild(copied)
				elif item.parent() is None:
					child=QtWidgets.QTreeWidgetItem()
					child.setText(0, " [null]")
					copied.addChild(child)
					root.addChild(copied)
				else:
					(item.parent() or root).setText(0, (item.parent() or root).text(0)[0: (item.parent() or root).text(0).rfind(" [")]+" [string]")
					(item.parent() or root).addChild(copied)
					(item.parent() or root).parent().setText(0, (item.parent() or root).parent().text(0)[0: (item.parent() or root).parent().text(0).rfind(" [")]+" [object]")
					for child_index in range((item.parent() or root).parent().childCount()):
						child=QtWidgets.QTreeWidgetItem()
						child.setText(0, " [null]")
						(item.parent() or root).parent().child(child_index).setText(0, (item.parent() or root).parent().child(child_index).text(0)[0: (item.parent() or root).parent().child(child_index).text(0).rfind(" [")]+" [string]")
						(item.parent() or root).parent().child(child_index).addChild(child)
				copied=(item.parent() or root).child((item.parent() or root).childCount()-1).clone()
		self.reply.close()
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
	"""
		Inserts copied/cutted item in selected item as parent
		@see getDict()
	"""
	def insertTreeBef(self):
		global cutted
		global copied
		global copp
		root=self.treeView.invisibleRootItem()
		if copp==0:
			for item in self.treeView.selectedItems():
				if item.parent() is None or item.parent().parent() is None:
					child=QtWidgets.QTreeWidgetItem()
					child.setText(0, " [null]")
					cutted.addChild(child)
					root.addChild(cutted)
				elif (item.parent().parent() or root).text(0).rfind(" [array]")!=-1:
					(item.parent().parent() or root).addChild(cutted)
				elif (item.parent().parent() or root).text(0).rfind(" [object]")!=-1:
					child=QtWidgets.QTreeWidgetItem()
					child.setText(0, " [null]")
					cutted.addChild(child)
					(item.parent().parent() or root).addChild(cutted)
				else:
					(item.parent().parent() or root).setText(0, (item.parent().parent() or root).text(0)[0: (item.parent().parent() or root).text(0).rfind(" [")]+" [string]")
					(item.parent().parent() or root).addChild(cutted)
					((item.parent().parent() or root).parent() or root).setText(0, ((item.parent().parent() or root).parent() or root).text(0)[0: ((item.parent().parent() or root).parent() or root).text(0).rfind(" [")]+" [object]")
					for child_index in range(((item.parent().parent() or root).parent() or root).childCount()):
						child=QtWidgets.QTreeWidgetItem()
						child.setText(0, " [null]")
						((item.parent().parent() or root).parent() or root).child(child_index).setText(0, ((item.parent().parent() or root).parent() or root).child(child_index).text(0)[0: ((item.parent().parent() or root).parent() or root).child(child_index).text(0).rfind(" [")]+" [string]")
						((item.parent().parent() or root).parent() or root).child(child_index).addChild(child)
			self.toolButton_3.setDisabled(True)
			self.menu_3.setDisabled(True)
		else:
			for item in self.treeView.selectedItems():
				if item.parent() is None or item.parent().parent() is None:
					child=QtWidgets.QTreeWidgetItem()
					child.setText(0, " [null]")
					copied.addChild(child)
					root.addChild(copied)
				elif (item.parent().parent() or root).text(0).rfind(" [array]")!=-1:
					(item.parent().parent() or root).addChild(copied)
				elif (item.parent().parent() or root).text(0).rfind(" [object]")!=-1:
					child=QtWidgets.QTreeWidgetItem()
					child.setText(0, " [null]")
					copied.addChild(child)
					(item.parent().parent() or root).addChild(copied)
				else:
					(item.parent().parent() or root).setText(0, (item.parent().parent() or root).text(0)[0: (item.parent().parent() or root).text(0).rfind(" [")]+" [string]")
					(item.parent().parent() or root).addChild(copied)
					((item.parent().parent() or root).parent() or root).setText(0, ((item.parent().parent() or root).parent() or root).text(0)[0: ((item.parent().parent() or root).parent() or root).text(0).rfind(" [")]+" [object]")
					for child_index in range(((item.parent().parent() or root).parent() or root).childCount()):
						child=QtWidgets.QTreeWidgetItem()
						child.setText(0, " [null]")
						((item.parent().parent() or root).parent() or root).child(child_index).setText(0, ((item.parent().parent() or root).parent() or root).child(child_index).text(0)[0: ((item.parent().parent() or root).parent() or root).child(child_index).text(0).rfind(" [")]+" [string]")
						((item.parent().parent() or root).parent() or root).child(child_index).addChild(child)
				copied=(item.parent().parent() or root).child((item.parent().parent() or root).childCount()-1).clone()
		self.reply.close()
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
	"""
		Minifies text in editor
	"""
	def minific(self):
		if self.textEdit.toPlainText()=='':
			return 0
		try:
			json.loads(self.textEdit.toPlainText())
		except json.decoder.JSONDecodeError:
			QMessageBox.about(self, "Ошибка", "Отсутствуют необходимые символы")
			return 0
		text=json.loads(self.textEdit.toPlainText())
		self.textEdit.setText(json.dumps(text, ensure_ascii=False).strip())
		self.toolButton_10.setDisabled(True)
		self.toolButton_11.setEnabled(True)
	"""
		Formats text in editor
		@exception json.decoder.JSONDecodeError - errors with syntax
	"""	
	def formating(self):
		if self.textEdit.toPlainText()=='':
			return 0
		try:
			json.loads(self.textEdit.toPlainText())
		except json.decoder.JSONDecodeError:
			QMessageBox.about(self, "Ошибка", "Отсутствуют необходимые символы")
			return 0
		text=self.textEdit.toPlainText()
		text=text.replace("'", "\"")
		dic=json.loads(text)
		self.textEdit.setText(json.dumps(dic, sort_keys=True, ensure_ascii=False, indent=4))
		self.toolButton_10.setEnabled(True)
		self.toolButton_11.setDisabled(True)
	"""
		Saves text from editor to PDF file
	"""
	def toPDF(self):
		if self.textEdit.toPlainText()=='':
			return 0
		pdf=FPDF()
		pdf.add_page()
		pdf.add_font('DejaVu', '', path+'DejaVuSansCondensed.ttf', uni=True)
		pdf.set_font('DejaVu', '', size=12)
		pdf.multi_cell(200, 10, txt=self.textEdit.toPlainText(), align="L")
		pdfname=QFileDialog.getSaveFileName(self, 'Экспортировать в PDF-файл...', '/')[0]
		if pdfname=='':
			return 0
		pdf.output(pdfname)
	"""
		Copies name of selected item
	"""
	def copyName(self):
		global wrap
		for item in self.treeView.selectedItems():
			wrap[1]=item.text(0)[0:item.text(0).rfind(" [")]
		self.toolButton_8.setEnabled(True)
		self.action_15.setEnabled(True)
	"""
		Replaces name of the selected item with copied name
		@see getDict()
	"""
	def pasteName(self):
		global wrap
		for item in self.treeView.selectedItems():
			item.setText(0, wrap[1]+item.text(0)[item.text(0).rfind(" ["):-1]+"[")
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
	"""
		Initialization right mouse button menu
		@see renameM()
		@see changeTypeM()
		@see insertM()
		@see cutM()
		@see copyM()
		@see deleteM()
		@see copyNameM()
		@see pasteNameM()
	"""
	def menuRMB(self):
		menu=QMenu(self)
		menu.addAction(self.renameM)
		menu.addAction(self.changeTypeM)
		menu.addAction(self.insertM)
		menu.addAction(self.cutM)
		menu.addAction(self.copyM)
		menu.addAction(self.deleteM)
		menu.addAction(self.copyNameM)
		menu.addAction(self.pasteNameM)
		self.curse=self.treeView.cursor()
		menu.exec_(self.curse.pos())
	"""
		Formatting tree
		@see unpack()
	"""
	def formatTree(self):
		"""
			Checks the opportunity to format tree item
			@param {QtWidgets.QTreeWidgetItem()} to_unpack - tree item
			@param {str} key - name of tree item
		"""
		return 0
		def unpack(to_unpack, key):
			if to_unpack.childCount()==0:
				childd=QtWidgets.QTreeWidgetItem()
				childd.setText(0, " [null]")
				to_unpack.addChild(childd)
				return 0
			for child_index in range(to_unpack.childCount()):
				child=to_unpack.child(child_index)
				child_text=child.text(0)
				try:
					child_text=float(child_text)
				except ValueError:
					try:
						child_text=int(child_text)
					except ValueError:
						pass
				if key.rfind(" [object]")!=-1:
					if to_unpack.childCount()==0:
						to_unpack.setText(0, key[0:key.rfind(" [")]+" [string]")
						childd=QtWidgets.QTreeWidgetItem()
						childd.setText(0, " [null]")
						to_unpack.addChild(childd)
					if child.childCount()>0:
						unpack(child, child_text)
				elif key.rfind(" [array]")!=-1:
					if to_unpack.childCount()==1:
						to_unpack.setText(0, key[0:key.rfind(" [")]+" [string]")
					elif to_unpack.childCount()==0:
						to_unpack.setText(0, key[0:key.rfind(" [")]+" [string]")
						childd=QtWidgets.QTreeWidgetItem()
						childd.setText(0, " [null]")
						to_unpack.addChild(childd)
					if child.childCount()>0:
						unpack(child, child_text)
		for index in range(self.treeView.topLevelItemCount()):
			parent=self.treeView.topLevelItem(index)
			element_text=parent.text(0)
			unpack(parent, element_text)
	"""
		Shows change menu of type of chosen tree item
		@see typeObj()
		@see typeArr()
		@see typeStr()
		@see typeInt()
		@see typeFloat()
	"""
	def changeType(self):
		self.reply=QDialog()
		vbox=QVBoxLayout()
		label_dialog=QLabel()
		label_dialog.setText('Изменить тип узла')
		button_object=QPushButton(self.reply)
		button_object.setText('object')
		button_object.clicked.connect(lambda: self.typeObj())
		button_array=QPushButton(self.reply)
		button_array.setText('array')
		button_array.clicked.connect(lambda: self.typeArr())
		button_string=QPushButton(self.reply)
		button_string.setText('string')
		button_string.clicked.connect(lambda: self.typeStr())
		button_int=QPushButton(self.reply)
		button_int.setText('number (int)')
		button_int.clicked.connect(lambda: self.typeInt())
		button_float=QPushButton(self.reply)
		button_float.setText('number (real)')
		button_float.clicked.connect(lambda: self.typeFloat())

		layout=QHBoxLayout()
		layout.addWidget(button_object)
		layout.addWidget(button_array)
		layout.addWidget(button_string)
		layout.addWidget(button_int)
		layout.addWidget(button_float)
		vbox.addWidget(label_dialog)
		vbox.addSpacing(20)
		vbox.addLayout(layout)
		self.reply.setLayout(vbox)
		self.reply.exec()
	"""
		Changes type of chosen tree item to object
		@exception type of item object
		@see getDict()
	"""
	def typeObj(self):
		for item in self.treeView.selectedItems():
			if item.text(0).rfind(" [object]")!=-1:
				self.reply.close()
				return 0
			item.setText(0, item.text(0)[0:item.text(0).rfind(" [")]+" [object]")
			for child_index in range(item.childCount()):
				child=QtWidgets.QTreeWidgetItem()
				child.setText(0, " [null]")
				item.child(child_index).addChild(child)
		self.reply.close()
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
	"""
		Changes type of chosen tree item to array
		@exception type of item is array or object
		@see getDict()
	"""
	def typeArr(self):
		for item in self.treeView.selectedItems():
			if item.text(0).rfind(" [array]")!=-1:
				self.reply.close()
				return 0
			if item.text(0).rfind(" [object]")!=-1:
				self.reply.close()
				message=QMessageBox()
				message.setIconPixmap(QPixmap(path+"mhG3jIf-Oe4.jpg"))
				message.about(self, "Ошибка", "Это у меня не выходит")
				message.exec()
				return 0
			item.setText(0, item.text(0)[0:item.text(0).rfind(" [")]+" [array]")
		self.reply.close()
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
	"""
		Changes type of chosen tree item to string
		@exception type of item is string
		@see getDict()
	"""
	def typeStr(self):
		for item in self.treeView.selectedItems():
			if item.text(0).rfind(" [string]")!=-1:
				self.reply.close()
				return 0
			item.setText(0, item.text(0)[0:item.text(0).rfind(" [")]+" [string]")
		self.reply.close()
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
	"""
		Changes type of chosen tree item to number(int)
		@exception type of item is number(int)
		@exception ValueError
		@see getDict()
	"""
	def typeInt(self):
		for item in self.treeView.selectedItems():
			if item.text(0).rfind(" [number (int)]")!=-1:
				self.reply.close()
				return 0
			try:
				int(item.text(0)[0:item.text(0).rfind(" [")])
			except ValueError:
				self.reply.close()
				QMessageBox.about(self, "Ошибка", "Несоответствие типов")
				return 0
			item.setText(0, item.text(0)[0:item.text(0).rfind(" [")]+" [number (int)]")
		self.reply.close()
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
	"""
		Changes type of chosen tree item to number(real)
		@exception type of item is number(real)
		@exception ValueError
		@see getDict()
	"""
	def typeFloat(self):
		for item in self.treeView.selectedItems():
			if item.text(0).rfind(" [number (real)]")!=-1:
				self.reply.close()
				return 0
			try:
				float(item.text(0)[0:item.text(0).rfind(" [")])
			except ValueError:
				self.reply.close()
				QMessageBox.about(self, "Ошибка", "Несоответствие типов")
				return 0
			item.setText(0, item.text(0)[0:item.text(0).rfind(" [")]+" [number (real)]")
		self.reply.close()
		data=self.getDict()
		self.textEdit.setText(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))







"""
	Main function
	@see editorApp()
"""
def main():
	app=QtWidgets.QApplication(sys.argv)
	window=editorApp()
	window.show()
	app.exec_()



if __name__=='__main__':
	main()