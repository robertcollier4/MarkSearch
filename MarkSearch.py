import sublime, sublime_plugin

#https://github.com/robertcollier4/MarkSearch
#---------------------------------------------------------------
class MarksearchFromPane(sublime_plugin.WindowCommand):

	def run(self):
		self.window.show_input_panel("MarkSearch: ", "", self.on_done, None, None)
		pass
	
	def on_done(self, text):
		view = self.window.active_view()
		# ExistingBookmarks = view.get_regions("MarkSearch")
		view.erase_regions("MarkSearch")
		# self.view.run_command("clear_bookmarks")
		RegionsFindResults = view.find_all(text, sublime.IGNORECASE | sublime.LITERAL)
		view.set_status("MarkSearch", text + " - " + str(len(RegionsFindResults)) + " matches")
		#sublime.status_message("MarkSearch has " + str(len(RegionsFindResults)) + " matches for " + text)
		view.add_regions("MarkSearch", RegionsFindResults, "marks", "cross", sublime.DRAW_OUTLINED | sublime.PERSISTENT) # valid gutter icons are dot, circle, bookmark and cross

#---------------------------------------------------------------
class MarksearchFromCaret(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		# 32=space 9=tab 10=newline 13=carriagereturn 
		whiteChars = (chr(32), chr(9), chr(10), chr(13))

		if(view.sel()[0].a == view.sel()[0].b):
			for ThisRegion in view.sel():
				ThisRegionBegin = ThisRegion.begin() - 1
				while((view.substr(ThisRegionBegin) not in whiteChars) and (ThisRegionBegin >= 0)):
					ThisRegionBegin -= 1
				ThisRegionBegin += 1
	
				ThisRegionEnd = ThisRegion.end()
				while((view.substr(ThisRegionEnd) not in whiteChars) and (ThisRegionEnd < view.size())):
					ThisRegionEnd += 1
			SearchTerm = view.substr(sublime.Region(ThisRegionBegin, ThisRegionEnd))
		else:
			SearchTerm = self.view.substr(view.sel()[0])
			
		sublime.active_window().active_view().erase_regions("MarkSearch")
		# self.view.run_command("clear_bookmarks")
		RegionsFindResults = sublime.active_window().active_view().find_all(SearchTerm, sublime.IGNORECASE | sublime.LITERAL)
		view.set_status("MarkSearch", SearchTerm + " - " + str(len(RegionsFindResults)) + " match")
		#sublime.status_message("MarkSearch has " + str(len(RegionsFindResults)) + " matches for " + SearchTerm)
		sublime.active_window().active_view().add_regions("MarkSearch", RegionsFindResults, "marks", "cross", sublime.DRAW_OUTLINED | sublime.PERSISTENT) # valid gutter icons are dot, circle, bookmark and cross

#---------------------------------------------------------------
class MarkpersonalLine(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		caretLine = view.line(view.sel()[0])
		linenumberSelBegin = view.rowcol(view.sel()[0].begin())[0]
		linenumberSelEnd = view.rowcol(view.sel()[0].end())[0]
		sublime.status_message("MarkPersonal Added Line # " + str(linenumberSelBegin+1))
		oldBookmarks = view.get_regions("bookmarks")
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
		sublime.active_window().active_view().add_regions("bookmarks", newBookmarks, "bookmarks", "circle", sublime.HIDDEN | sublime.PERSISTENT)

#---------------------------------------------------------------
class ClearMarkWithStatus(sublime_plugin.TextCommand):
	def run(self, edit, key="bookmarks"):
		view = sublime.active_window().active_view()
		#view = self.window.active_view()

		sublime.status_message(str(key) + " mark cleared")
		view.erase_regions(key)
		# view.run_command('clear_bookmarks')

		if(key == "MarkSearch"):
			#print("MarkSearch key matched removing set_status")
			view.set_status("MarkSearch", "")

#---------------------------------------------------------------
class MarkGotobyindex(sublime_plugin.TextCommand):
	def run(self, edit, key="bookmarks", index=0):
		view = self.view
		#view = sublime.active_window().active_view()
		RegionsMarksForThisKey = view.get_regions(key)

		if(len(RegionsMarksForThisKey) >= index+1):
			if(key == "MarkSearch"):
				sublime.status_message(str(index+1) + " Match")
			else:
				sublime.status_message(str(index+1) + " Match (" + str(key) + ")")
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
				if(PosBeginThisRegion > PosCaretUser):
					if(key == "MarkSearch"):
						sublime.status_message(str(IndexThisRegion+1) + " Match")
					else:
						sublime.status_message(str(IndexThisRegion+1) + " Match (" + str(key) + ")")
					view.sel().clear()
					view.sel().add(ThisRegion)
					view.show(PosBeginThisRegion)
					return
			if(key == "MarkSearch"):
				sublime.status_message("Did not find any more match")
			else:
				sublime.status_message("Did not find any more match (" + str(key) + ")")
		else: #backward
			PosCaretUser = view.sel()[0].begin()
			for IndexThisRegion in reversed(range(NumRegionsMarksForThisKey)):
				if(RegionsMarksForThisKey[IndexThisRegion].begin() < PosCaretUser):
					if(key == "MarkSearch"):
						sublime.status_message(str(IndexThisRegion+1) + " Match")
					else:
						sublime.status_message(str(IndexThisRegion+1) + " Match (" + str(key) + ")")
					view.sel().clear()
					view.sel().add(RegionsMarksForThisKey[IndexThisRegion])
					view.show(RegionsMarksForThisKey[IndexThisRegion].begin())
					return
			if(key == "MarkSearch"):
				sublime.status_message("Did not find any match before")
			else:
				sublime.status_message("Did not find any match before (" + str(key) + ")")

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
