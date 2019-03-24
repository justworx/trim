keys = """
KEY_MIN 	Minimum key value
KEY_BREAK 	Break key (unreliable)
KEY_DOWN 	Down-arrow
KEY_UP 	Up-arrow
KEY_LEFT 	Left-arrow
KEY_RIGHT 	Right-arrow
KEY_HOME 	Home key (upward+left arrow)
KEY_BACKSPACE 	Backspace (unreliable)
KEY_F0 	Function keys. Up to 64 function keys are supported.
KEY_Fn 	Value of function key n
KEY_DL 	Delete line
KEY_IL 	Insert line
KEY_DC 	Delete character
KEY_IC 	Insert char or enter insert mode
KEY_EIC 	Exit insert char mode
KEY_CLEAR 	Clear screen
KEY_EOS 	Clear to end of screen
KEY_EOL 	Clear to end of line
KEY_SF 	Scroll 1 line forward
KEY_SR 	Scroll 1 line backward (reverse)
KEY_NPAGE 	Next page
KEY_PPAGE 	Previous page
KEY_STAB 	Set tab
KEY_CTAB 	Clear tab
KEY_CATAB 	Clear all tabs
KEY_ENTER 	Enter or send (unreliable)
KEY_SRESET 	Soft (partial) reset (unreliable)
KEY_RESET 	Reset or hard reset (unreliable)
KEY_PRINT 	Print
KEY_LL 	Home down or bottom (lower left)
KEY_A1 	Upper left of keypad
KEY_A3 	Upper right of keypad
KEY_B2 	Center of keypad
KEY_C1 	Lower left of keypad
KEY_C3 	Lower right of keypad
KEY_BTAB 	Back tab
KEY_BEG 	Beg (beginning)
KEY_CANCEL 	Cancel
KEY_CLOSE 	Close
KEY_COMMAND 	Cmd (command)
KEY_COPY 	Copy
KEY_CREATE 	Create
KEY_END 	End
KEY_EXIT 	Exit
KEY_FIND 	Find
KEY_HELP 	Help
KEY_MARK 	Mark
KEY_MESSAGE 	Message
KEY_MOVE 	Move
KEY_NEXT 	Next
KEY_OPEN 	Open
KEY_OPTIONS 	Options
KEY_PREVIOUS 	Prev (previous)
KEY_REDO 	Redo
KEY_REFERENCE 	Ref (reference)
KEY_REFRESH 	Refresh
KEY_REPLACE 	Replace
KEY_RESTART 	Restart
KEY_RESUME 	Resume
KEY_SAVE 	Save
KEY_SBEG 	Shifted Beg (beginning)
KEY_SCANCEL 	Shifted Cancel
KEY_SCOMMAND 	Shifted Command
KEY_SCOPY 	Shifted Copy
KEY_SCREATE 	Shifted Create
KEY_SDC 	Shifted Delete char
KEY_SDL 	Shifted Delete line
KEY_SELECT 	Select
KEY_SEND 	Shifted End
KEY_SEOL 	Shifted Clear line
KEY_SEXIT 	Shifted Exit
KEY_SFIND 	Shifted Find
KEY_SHELP 	Shifted Help
KEY_SHOME 	Shifted Home
KEY_SIC 	Shifted Input
KEY_SLEFT 	Shifted Left arrow
KEY_SMESSAGE 	Shifted Message
KEY_SMOVE 	Shifted Move
KEY_SNEXT 	Shifted Next
KEY_SOPTIONS 	Shifted Options
KEY_SPREVIOUS 	Shifted Prev
KEY_SPRINT 	Shifted Print
KEY_SREDO 	Shifted Redo
KEY_SREPLACE 	Shifted Replace
KEY_SRIGHT 	Shifted Right arrow
KEY_SRSUME 	Shifted Resume
KEY_SSAVE 	Shifted Save
KEY_SSUSPEND 	Shifted Suspend
KEY_SUNDO 	Shifted Undo
KEY_SUSPEND 	Suspend
KEY_UNDO 	Undo
KEY_MOUSE 	Mouse event has occurred
KEY_RESIZE 	Terminal resize event
KEY_MAX 	Maximum key value
""".splitlines()

events = []
for key in keys:
	events.append(key.split(maxsplit=1))


