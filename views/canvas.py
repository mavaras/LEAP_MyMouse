from PyQt4.QtGui import *
from PyQt4.QtCore import *
from views.gui_qtdesigner import *

from models.PCRecognizer import *


# CANVAS CLASS
class Widget_canvas(QWidget):
	points = []
	
	lp = Point(0, 0, -1)
	np = Point(0, 0, -1)
	path_points_0 = QPainterPath()
	path_points_1 = QPainterPath()
	path_points_2 = QPainterPath()
	path_points_3 = QPainterPath()
	path_points_4 = QPainterPath()
	canvas = None
	pen_color = Qt.black

	def __init__(self, parent):
		super(Widget_canvas, self).__init__(parent)

	def clear(self):
		aux = QPainterPath()
		self.path_points_0 = aux
		aux = QPainterPath()
		self.path_points_1 = aux
		aux = QPainterPath()
		self.path_points_2 = aux
		aux = QPainterPath()
		self.path_points_3 = aux
		aux = QPainterPath()
		self.path_points_4 = aux
		aux = QPainterPath()
		self.update()
		
	def paintEvent(self, event):
		canvas = QtGui.QPainter(self)
		pen = QPen()

		# drawing grid
		pen.setWidth(1.4)
		pen.setColor(Qt.black)
		canvas.setPen(pen)
		interval = 20
		for c in range(interval, canvas_width, interval):
			for j in range(interval, canvas_height, interval):
				canvas.drawLine(c, 0, c, canvas_height)
				canvas.drawLine(0, j, canvas_width, j)

		# finger 0 path
		pen.setWidth(2.4)
		pen.setColor(Qt.red)
		canvas.setPen(pen)
		canvas.drawPath(self.path_points_0)

		# finger 1 path
		pen.setColor(Qt.black)
		canvas.setPen(pen)
		canvas.drawPath(self.path_points_1)
		
		# finger 2 path
		pen.setColor(Qt.blue)
		canvas.setPen(pen)
		canvas.drawPath(self.path_points_2)

		# finger 3 path
		pen.setColor(Qt.green)
		canvas.setPen(pen)
		canvas.drawPath(self.path_points_3)

		# finger 4 path
		pen.setColor(Qt.yellow)
		canvas.setPen(pen)
		canvas.drawPath(self.path_points_4)
		

	def mousePressEvent(self, event):
		print("click")
		x = event.x()
		y = event.y()
		print("start point: ("+str(x)+","+str(y)+")")
		#self.path.moveTo(e.pos())
		self.path_points_1.addEllipse(QtCore.QRectF(x, y, 16, 16))
		global stroke_id#, points
		stroke_id += 1
		self.points.append(Point(x, y, stroke_id))
		self.lp.x, self.lp.y = x, y

	def mouseMoveEvent(self, event):
		#self.path.lineTo(event.pos())
		x = event.x()
		y = event.y()
		self.np = Point(x, y, -1)
		if distance(self.lp, self.np) > 5:
			self.path_points_1.addEllipse(QtCore.QRectF(x, y, 8, 8))
			global stroke_id#, points
			self.points.append(Point(x, y, stroke_id))
			self.lp.x, self.lp.y = x, y
			self.update()

	def mouseReleaseEvent(self, event):
		print("release")
		print("end point: ("+str(event.x())+","+str(event.y())+")")
