import sublime, sublime_plugin

#https://github.com/robertcollier4/MarkFromPane
#---------------------------------------------------------------
class MarksearchFromPane(sublime_plugin.WindowCommand):

	def run(self):
		self.window.show_input_panel("Marksearch: ", "", self.on_done, None, None)
		pass
	
	def on_done(self, text):
		view = self.window.active_view()
		# ExistingBookmarks = view.get_regions("bookmarks")
		view.erase_regions("bookmarks")
		# self.view.run_command("clear_bookmarks")
		RegionsFindResults = view.find_all(text, sublime.IGNORECASE | sublime.LITERAL)
		sublime.status_message("Marksearch has " + str(len(RegionsFindResults)) + " matches for " + text)
		view.add_regions("bookmarks", RegionsFindResults, "marks", "cross", sublime.DRAW_OUTLINED | sublime.PERSISTENT) # valid gutter icons are dot, circle, bookmark and cross

#---------------------------------------------------------------
class MarksearchFromCaret(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		# 32=space 9=tab 10=newline 13=carriagereturn 
		whiteChars = (chr(32), chr(9), chr(10), chr(13))
		SearchTerm = self.view.substr(view.sel()[0])

		for ThisRegion in view.sel():
			ThisRegionBegin = ThisRegion.begin() - 1
			while((view.substr(ThisRegionBegin) not in whiteChars) and (ThisRegionBegin >= 0)):
				ThisRegionBegin -= 1
			ThisRegionBegin += 1

			ThisRegionEnd = ThisRegion.end()
			while((view.substr(ThisRegionEnd) not in whiteChars) and (ThisRegionEnd < view.size())):
				ThisRegionEnd += 1

		SearchTerm = view.substr(sublime.Region(ThisRegionBegin, ThisRegionEnd))

		sublime.active_window().active_view().erase_regions("bookmarks")
		# self.view.run_command("clear_bookmarks")
		RegionsFindResults = sublime.active_window().active_view().find_all(SearchTerm, sublime.IGNORECASE | sublime.LITERAL)
		sublime.status_message("Marksearch has " + str(len(RegionsFindResults)) + " matches for " + SearchTerm)
		sublime.active_window().active_view().add_regions("bookmarks", RegionsFindResults, "marks", "cross", sublime.DRAW_OUTLINED | sublime.PERSISTENT) # valid gutter icons are dot, circle, bookmark and cross

#---------------------------------------------------------------
class MarkpersonalLine(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		caretLine = view.line(view.sel()[0])
		linenumberSelBegin = view.rowcol(view.sel()[0].begin())[0]
		linenumberSelEnd = view.rowcol(view.sel()[0].end())[0]
		sublime.status_message("MarkPersonal Added Line # " + str(linenumberSelBegin+1))
		oldBookmarks = view.get_regions("MarkPersonal")
		newBookmarks = []
		bookmarkFoundOnCaretLine = False
		for thisbookmark in oldBookmarks:
			# if thisbookmark.intersects(caretLine):
			if ( (thisbookmark.begin() >= caretLine.begin()) and (thisbookmark.begin() <= caretLine.end()) or
			     (thisbookmark.end() >= caretLine.begin()) and (thisbookmark.end() <= caretLine.end()) ):
				bookmarkFoundOnCaretLine = True
			else:
				newBookmarks.append(thisbookmark)
		if bookmarkFoundOnCaretLine:
			sublime.status_message("MarkPersonal Line # " + str(linenumberSelBegin+1) + " (Removed)")
		else:
			sublime.status_message("MarkPersonal Line # " + str(linenumberSelBegin+1))
			newBookmarks.append(view.sel()[0])
		sublime.active_window().active_view().add_regions("MarkPersonal", newBookmarks, "bookmarks", "circle", sublime.HIDDEN | sublime.PERSISTENT)

#---------------------------------------------------------------
class ClearMarkWithStatus(sublime_plugin.TextCommand):
	def run(self, edit, key="bookmarks"):
		sublime.status_message("key=" + str(key) + " Marks Cleared")
		#view = self.window.active_view()
		view = sublime.active_window().active_view()
		view.erase_regions(key)
		# view.run_command('clear_bookmarks')

#---------------------------------------------------------------
class MarkGotobyindex(sublime_plugin.TextCommand):
	def run(self, edit, key="bookmarks", index=0):
		view = self.view
		#view = sublime.active_window().active_view()
		RegionsMarksForThisKey = view.get_regions(key)

		if(len(RegionsMarksForThisKey) >= index+1):
			sublime.status_message("Going to Mark key=" + str(key) + " " + str(index+1))
			ThisRegion = RegionsMarksForThisKey[index]
			view.sel().clear()
			view.sel().add(ThisRegion)
			view.show(ThisRegion.begin())
			#view.show_at_center(ThisRegion.begin())
			#view.show_at_center(ThisRegion)
		else:
			sublime.status_message("No Mark key=" + str(key) + " " + str(index+1))
			#sublime.status_message("MarkFromPane.py MarkSelectbyIndex(): Did not find any marks of key=" + str(key))

#---------------------------------------------------------------
class MarkGotoNext(sublime_plugin.TextCommand):
	def run(self, edit, key="bookmarks", forward=True):
		view = self.view
		RegionsMarksForThisKey = view.get_regions(key)

		NumRegionsMarksForThisKey = len(RegionsMarksForThisKey)
		if(forward):
			PosCaretUser = view.sel()[0].end()
			for IndexThisRegion in range(NumRegionsMarksForThisKey):
				ThisRegion = RegionsMarksForThisKey[IndexThisRegion]
				PosBeginThisRegion = ThisRegion.begin()
				if(PosCaretUser <= PosBeginThisRegion):
					sublime.status_message("key="+ str(key) + " Going to mark " + str(IndexThisRegion+1))
					view.sel().clear()
					view.sel().add(ThisRegion)
					view.show(PosBeginThisRegion)
					return
			sublime.status_message("key="+ str(key) + " Did not find after mark=" + str(NumRegionsMarksForThisKey))
		else: #backward
			PosCaretUser = view.sel()[0].begin()
			for IndexThisRegion in reversed(range(NumRegionsMarksForThisKey)):
				if(RegionsMarksForThisKey[IndexThisRegion].begin() < PosCaretUser):
					sublime.status_message("key="+ str(key) + " Going to mark " + str(IndexThisRegion+1))
					view.sel().clear()
					view.sel().add(RegionsMarksForThisKey[IndexThisRegion])
					view.show(RegionsMarksForThisKey[IndexThisRegion].begin())
					return
			sublime.status_message("key="+ str(key) + " Did not find before mark 1")

#---------------------------------------------------------------
# JUNKYARD
#class MarkFromFindpanel(sublime_plugin.TextCommand):
#	def run(self, edit):
#		SearchTerm = self.view.substr(self.view.full_line(0))
#		# ExistingBookmarks = sublime.active_window().active_view().get_regions("bookmarks")
#		sublime.active_window().active_view().erase_regions("bookmarks")
#		# sublime.active_window().active_view().erase_regions("mark")
#		# self.view.run_command("clear_bookmarks")
#		RegionsFindResults = sublime.active_window().active_view().find_all(SearchTerm, sublime.IGNORECASE | sublime.LITERAL)
#		sublime.status_message("Bookmarked " + str(len(RegionsFindResults)) + " matches for " + SearchTerm)
#		sublime.active_window().active_view().add_regions("bookmarks", RegionsFindResults, "bookmarks", "circle", sublime.DRAW_OUTLINED | sublime.PERSISTENT) # valid gutter icons are dot, circle, bookmark and cross
#		sublime.active_window().run_command('hide_panel')

#---------------------------------------------------------------
