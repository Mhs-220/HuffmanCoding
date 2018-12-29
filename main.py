import sys

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import pyqtSlot
from PyQt5.QtWidgets import (
	QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton
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
		compressor(files, savedFile[0])

	@pyqtSlot()
	def decompressButtonAction(self):
		file = self.openFileNameDialog()
		savedPath = self.savePathDialog()
		# print(file, savedPath)
		decompressor(file, savedPath)

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
