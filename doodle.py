#!/usr/bin/env python
# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

import cairo
import gtk
import gtk.gdk

class ScreenDoodle:
	BRUSH_CIRCLE = 'circle'
	BRUSH_SQUARE = 'square'
	
	def __init__(self):
		self.brush = self.BRUSH_SQUARE
		self.background = (0.1, 0.1, 0.1)
		self.foreground = (1.0, 0.0, 0.0)
		self.colorbar_colors = [((255 - i) / 255.0, 0.0, i / 255.0) for i in range(0, 256)] + [(0.0, i / 255.0, (255 - i) / 255.0) for i in range(0, 256)] + [(i / 255.0, (255 - i) / 255.0, 0.0) for i in range(0, 256)]
		self.line_width = 5
		self.painting = False
		self.x = 0
		self.y = 0
		
		self.window = gtk.Window(gtk.WINDOW_POPUP)
		self.window.set_app_paintable(True)
		self.window.set_decorated(False)
		self.window.add_events(gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.KEY_PRESS_MASK)
		self.window.connect('delete-event', gtk.main_quit)
		self.window.connect('expose-event', self.on_expose)
		self.window.connect('button-press-event', self.on_button_pressed)
		self.window.connect('button-release-event', self.on_button_released)
		self.window.connect('motion-notify-event', self.on_motion)
		# self.window.connect('key-press-event', self.on_key_pressed)
		
		self.screen = self.window.get_screen()
		self.screen_width = self.screen.get_width()
		self.screen_height = self.screen.get_height()
		self.colorbar_height = self.screen_height / 20
		#self.colorbar_item_width = int(self.screen_width / len(self.colorbar_colors))
		
		self.window.move(0, 0)
		self.window.resize(self.screen_width, self.screen_height)
		self.window.show_all()
		self.drawable = self.window.window.cairo_create()
	
	def run(self):
		return gtk.main()
	
	def get_colorbar_color(self, x):
		color = self.colorbar_colors[int(min(x, self.screen_width - self.colorbar_height) * ((len(self.colorbar_colors) - 1) / float(self.screen_width - self.colorbar_height)))]
		return color
	
	def set_foreground_color(self, color):
		self.foreground = color
		self.update()
	
	def set_background_color(self, color):
		self.background = color
		self.clear()
	
	def set_line_width(self, line_width):
		self.line_width = int(line_width)
	
	def draw_colorbar(self, drawable):
		for i in range(self.screen_width - self.colorbar_height):
			color = self.get_colorbar_color(i)
			drawable.set_operator(cairo.OPERATOR_SOURCE)
			drawable.set_source_rgb(*color)
			drawable.rectangle(i, 0, 1, self.colorbar_height)
			drawable.fill()
		drawable.move_to(self.screen_width - self.colorbar_height, 0)
		drawable.line_to(self.screen_width, self.colorbar_height)
		drawable.stroke()
		drawable.move_to(self.screen_width - self.colorbar_height, self.colorbar_height)
		drawable.line_to(self.screen_width, 0)
		drawable.stroke()
	
	def update(self):
		self.drawable.set_operator(cairo.OPERATOR_SOURCE)
		self.drawable.set_source_rgb(*self.foreground)
	
	def clear(self):
		drawable = self.window.window.cairo_create()
		drawable.set_operator(cairo.OPERATOR_SOURCE)
		drawable.set_source_rgb(*self.background)
		drawable.paint()
		self.draw_colorbar(drawable)
		self.update()
	
	def draw(self):
		if self.brush == self.BRUSH_CIRCLE:
			pass
		elif self.brush == self.BRUSH_SQUARE:
			x = self.x - int(self.line_width / 2)
			y = self.y - int(self.line_width / 2)
			self.drawable.rectangle(x, y, self.line_width, self.line_width)
			self.drawable.fill()
	
	def on_expose(self, widget, event = None):
		self.clear()
	
	def on_button_pressed(self, widget, event = None):
		self.painting = True
		if event.y <= self.colorbar_height:
			if event.x <= self.screen_width - self.colorbar_height:
				self.set_foreground_color(self.get_colorbar_color(event.x))
				self.set_line_width(event.y)
			else:
				self.clear()
		else:
			self.draw()
	
	def on_button_released(self, widget, event = None):
		self.painting = False
	
	def on_motion(self, widget, event = None):
		self.x = event.x
		self.y = max(event.y, self.colorbar_height + self.line_width / 2)
		if self.painting:
			self.draw()

def main():
	d = ScreenDoodle()
	try:
		d.run()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()