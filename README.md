# MarkFromPane
Bookmark words and lines with different classes from a panel and within editor. SublimeText ST3.

## 2 Classes of Marks - Marksearches and Markpersonal
This allows you to set 2 classes of marks - Marksearch and Markpersonal.  
Marksearch are outlined around words and shown as outlines around words and in gutter  
Markpersonal are line based and shown in gutter only  

Functions Provided:  
**MarksearchFromPane** - Clears the old Marksearch, and sets a Marksearch from a pane like a find pane. This is marked by a outline around the word searched for. And a arrow for the line on the gutter.  
**MarksearchFromCaret** - Clears the old Marksearch, and sets a Marksearch from the word your caret is on. This is marked by a outline around the word searched for. And a arrow for the line on the gutter.  
**MarkpersonalLine** - Sets a Markpersonal for the current line you are on. This is marked by a circle for the line on the gutter.  
**ClearMarksWithStatus** - Clears the old mark of key  
**MarkGotobyindex** - Go to mark of key of specified index  
**MarkGotoNext** - Go to previous or next mark of key  

## Key Bindings Configuration
Since these are replacing your basic find keys this package does not automatically overwrite your existing key bindings. You must choose to add the keybindings yourself for your specific OS.

For Windows, you can use the recommended keybindings by adding the following lines to your *[Sublime_Data_Dir](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory)\Packages\User\Default (Windows).sublime-keymap* file.
Make sure these keybindings are listed at the end of your keymap file - Later keybindings will override earlier ones listed.
```
{ "keys": ["ctrl+f"], "command": "marksearch_from_pane" },
{ "keys": ["ctrl+h"], "command": "marksearch_from_caret" },

{ "keys": ["ctrl+\\"], "command": "mark_gotobyindex", "args": {"key": "bookmarks", "index": 0} },

{ "keys": ["ctrl+["], "command": "mark_goto_next", "args": {"key": "bookmarks", "forward": false} },
{ "keys": ["ctrl+]"], "command": "mark_goto_next", "args": {"key": "bookmarks", "forward": true} },

{ "keys": ["ctrl+u"], "command": "clear_mark_with_status", "args": {"key": "bookmarks" } },

{ "keys": ["ctrl+shift+u"], "command": "clear_mark_with_status", "args": {"key": "MarkPersonal" } },

{ "keys": ["ctrl+shift+1"], "command": "markpersonal_line" },
{ "keys": ["ctrl+1"], "command": "mark_gotobyindex", "args": {"key": "MarkPersonal", "index": 0} },
{ "keys": ["ctrl+2"], "command": "mark_gotobyindex", "args": {"key": "MarkPersonal", "index": 1} },
{ "keys": ["ctrl+3"], "command": "mark_gotobyindex", "args": {"key": "MarkPersonal", "index": 2} },
{ "keys": ["ctrl+4"], "command": "mark_gotobyindex", "args": {"key": "MarkPersonal", "index": 3} },
{ "keys": ["ctrl+5"], "command": "mark_gotobyindex", "args": {"key": "MarkPersonal", "index": 4} },
{ "keys": ["ctrl+6"], "command": "mark_gotobyindex", "args": {"key": "MarkPersonal", "index": 5} },
{ "keys": ["ctrl+7"], "command": "mark_gotobyindex", "args": {"key": "MarkPersonal", "index": 6} },
{ "keys": ["ctrl+8"], "command": "mark_gotobyindex", "args": {"key": "MarkPersonal", "index": 7} },
{ "keys": ["ctrl+9"], "command": "mark_gotobyindex", "args": {"key": "MarkPersonal", "index": 8} },
{ "keys": ["ctrl+0"], "command": "mark_gotobyindex", "args": {"key": "MarkPersonal", "index": 9} },
```
