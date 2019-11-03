from App.App import App
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__' :
	appWapper = QApplication(sys.argv)
	app = App( AppName='PointNet++ Analyzer' )
	sys.exit(appWapper.exec_())