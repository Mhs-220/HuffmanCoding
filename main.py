import os
import sys
import time

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import pyqtSlot
from PyQt5.QtWidgets import (
	QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton,
	QMessageBox
)

from huffman_compress   import compressor
from huffman_decompress import decompressor

class App(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'Mhs Huffman Coding'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.setStyleSheet("background-color: rgb(136, 138, 133);")
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		compress_button = QPushButton('Compress', self)
		# compress_button.setToolTip('This is an example button')
		compress_button.resize(180, 260)
		compress_button.move(50, 110)
		compress_button.clicked.connect(self.compressButtonAction)
		decompress_button = QPushButton('Decompress', self)
		# decompress_button.setToolTip('This is an example button')
		decompress_button.resize(180, 260)
		decompress_button.move(420, 110)
		decompress_button.clicked.connect(self.decompressButtonAction)

		self.show()


	@pyqtSlot()
	def compressButtonAction(self):
		files = self.openFileNamesDialog()
		savedFile = self.saveFileDialog()
		# print(files, savedFile)
		start = time.clock()
		compressor(files, savedFile[0])
		end = time.clock()
		run_time = "Complete in {:.2f} Seconds".format(end - start)
		changed_size = "Files compressed {:.2f}%".format(100 - (os.path.getsize(savedFile[0] + ".mhs") * 100 / sum(os.path.getsize(x) for x in files)))
		dialog_shown_text = "File compressed succesfully!\n{}\n{}".format(run_time, changed_size)
		buttonReply = QMessageBox.question(self, 'Compress Message', dialog_shown_text, QMessageBox.Ok, QMessageBox.Ok)

	@pyqtSlot()
	def decompressButtonAction(self):
		file = self.openFileNameDialog()
		savedPath = self.savePathDialog()
		# print(file, savedPath)
		# Set ability to select file to uncompress
		start = time.clock()
		decompressor(file, savedPath)
		end = time.clock()
		run_time = "Complete in {:.2f} Seconds".format(end - start)
		dialog_shown_text = "File decompressed succesfully!\n{}".format(run_time)
		buttonReply = QMessageBox.question(self, 'Decompress Message', dialog_shown_text, QMessageBox.Ok, QMessageBox.Ok)

	@pyqtSlot()
	def openFileNamesDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		files, _ = QFileDialog.getOpenFileNames(self,"Select files for compress", "","All Files (*);;Python Files (*.py)", options=options)
		if files:
			return files

	@pyqtSlot()
	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		files, _ = QFileDialog.getOpenFileName(self, "Select files for decompress", "","Mhs Compressed File (*.mhs)", options=options)
		if files:
			return files

	@pyqtSlot()
	def savePathDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName = QFileDialog.getExistingDirectory(self, "Select path for save your file", options=options)
		if fileName:
			return fileName

	@pyqtSlot()
	def saveFileDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName = QFileDialog.getSaveFileName(self, "Select path for save your file", options=options)
		if fileName:
			return fileName

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
