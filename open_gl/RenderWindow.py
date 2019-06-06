"""
/*******************************************************************************
 *
 *            #, #,         CCCCCC  VV    VV MM      MM RRRRRRR
 *           %  %(  #%%#   CC    CC VV    VV MMM    MMM RR    RR
 *           %    %## #    CC        V    V  MM M  M MM RR    RR
 *            ,%      %    CC        VV  VV  MM  MM  MM RRRRRR
 *            (%      %,   CC    CC   VVVV   MM      MM RR   RR
 *              #%    %*    CCCCCC     VV    MM      MM RR    RR
 *             .%    %/
 *                (%.      Computer Vision & Mixed Reality Group
 *
 ******************************************************************************/
/**          @copyright:   Hochschule RheinMain,
 *                         University of Applied Sciences
 *              @author:   Prof. Dr. Ulrich Schwanecke
 *             @version:   0.9
 *                @date:   03.06.2019
 ******************************************************************************/
/**         RenderWindow.py
 *
 *          Simple Python OpenGL program that uses PyOpenGL + GLFW to get an
 *          OpenGL 3.2 context and display some 2D animation.
 ****
"""

import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Scene:
	""" OpenGL 2D scene class """

	# initialization
	def __init__(self, width, height):
		# time
		self.t = 0
		self.showVector = True
		self.point = np.array([0, 0])
		self.vector = np.array([10, 10])
		self.pointsize = 3
		self.width = width
		self.height = height
		glPointSize(self.pointsize)
		glLineWidth(self.pointsize)


	# step
	def step(self):
		# move point
		self.point = self.point + 0.1 * self.vector

		# check borders
		if self.point[0] < -self.width / 2:  # point hits left border
			# mirror at n = [1,0]
			n = np.array([1, 0])
			self.vector = self.mirror(self.vector, n)
		elif self.point[0] > self.width / 2:  # point hits right border
			# mirrot at n = [-1,0]
			n = np.array([-1, 0])
			self.vector = self.mirror(self.vector, n)
		elif self.point[1] < -self.height / 2:  # point hits upper border
			# mirrot at n = [0,1]
			n = np.array([0, 1])
			self.vector = self.mirror(self.vector, n)
		elif self.point[1] > self.height / 2:  # point hits lower border
			# mirrot at n = [0,-1]
			n = np.array([0, -1])
			self.vector = self.mirror(self.vector, n)

	# print(self.point, self.vector)

	# mirror a vector v at plane with normal n
	def mirror(self, v, n):
		# normalize n
		normN = n / np.linalg.norm(n)
		# project negative v on n
		l = np.dot(-v, n)
		# mirror v
		mv = v + 2 * l * n
		return mv


	# render
	def render(self):
		# render a point
		glBegin(GL_POINTS)
		glColor(0.0, 0.0, 1.0)
		glVertex2fv(self.point)
		glEnd()

		# render the vector starting at the point
		if self.showVector:
			glColor(1.0, 0.0, 0.0)
			glBegin(GL_LINES)
			# the line from the point to the end of the vector
			glVertex2fv(self.point)
			glVertex2fv(self.point + self.vector)

			# make an arrow at the tip of the vector
			normvector = self.vector / np.linalg.norm(self.vector)
			rotnormvec = np.array([-normvector[1], normvector[0]])
			p1 = self.point + self.vector - 6 * normvector
			a = p1 + 3 * self.pointsize / 2 * rotnormvec
			b = p1 - 3 * self.pointsize / 2 * rotnormvec
			glVertex2fv(self.point + self.vector)
			glVertex2fv(a)
			glVertex2fv(self.point + self.vector)
			glVertex2fv(b)
			glEnd()


class RenderWindow:
	"""GLFW Rendering window class"""

	def __init__(self):

		# save current working directory
		cwd = os.getcwd()

		# Initialize the library
		if not glfw.init():
			return

		# restore cwd
		os.chdir(cwd)

		# version hints
		# glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, 3)
		# glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, 3)
		# glfw.WindowHint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
		# glfw.WindowHint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

		# buffer hints
		glfw.window_hint(glfw.DEPTH_BITS, 32)

		# define desired frame rate
		self.frame_rate = 100

		# make a window
		self.width, self.height = 640, 480
		self.aspect = self.width / float(self.height)
		self.window = glfw.create_window(self.width, self.height, "2D Graphics", None, None)
		if not self.window:
			glfw.terminate()
			return

		# Make the window's context current
		glfw.make_context_current(self.window)

		# initialize GL
		glViewport(0, 0, self.width, self.height)
		glEnable(GL_DEPTH_TEST)
		glClearColor(1.0, 1.0, 1.0, 1.0)
		glMatrixMode(GL_PROJECTION)
		glOrtho(-self.width / 2, self.width / 2, -self.height / 2, self.height / 2, -2, 2)
		glMatrixMode(GL_MODELVIEW)

		# set window callbacks
		glfw.set_mouse_button_callback(self.window, self.onMouseButton)
		glfw.set_key_callback(self.window, self.onKeyboard)
		glfw.set_window_size_callback(self.window, self.onSize)

		# create 3D
		self.scene = Scene(self.width, self.height)

		# exit flag
		self.exitNow = False

		# animation flag
		self.animation = True


	def onMouseButton(self, win, button, action, mods):
		print("mouse button: ", win, button, action, mods)


	def onKeyboard(self, win, key, scancode, action, mods):
		print("keyboard: ", win, key, scancode, action, mods)
		if action == glfw.PRESS:
			# ESC to quit
			if key == glfw.KEY_ESCAPE:
				self.exitNow = True
			if key == glfw.KEY_V:
				# toggle show vector
				self.scene.showVector = not self.scene.showVector
			if key == glfw.KEY_A:
				# toggle animation
				self.animation = not self.animation


	def onSize(self, win, width, height):
		print("onsize: ", win, width, height)
		self.width = width
		self.height = height
		self.aspect = width / float(height)
		glViewport(0, 0, self.width, self.height)


	def run(self):
		# initializer timer
		glfw.set_time(0.0)
		t = 0.0
		while not glfw.window_should_close(self.window) and not self.exitNow:
			# update every x seconds
			currT = glfw.get_time()
			if currT - t > 1.0 / self.frame_rate:
				# update time
				t = currT
				# clear
				glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

				# render scene
				if self.animation:
					self.scene.step()
				self.scene.render()

				glfw.swap_buffers(self.window)
				# Poll for and process events
				glfw.poll_events()
		# end
		glfw.terminate()


# main() function
def main():
	print("Simple glfw render Window")
	rw = RenderWindow()
	rw.run()


# call main
if __name__ == '__main__':
	main()
