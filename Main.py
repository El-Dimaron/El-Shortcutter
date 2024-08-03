import shelve

import keyboard
import pyautogui

shortcuts_dict = {

	"rr": "Checked by Content Moderation Team due to Users Reports (post/chat/profile).",
	"rp\\": "Checked by Content Moderation Team due to Users Reports (profile).",
	"rpost\\": "Checked by Content Moderation Team due to Users Reports (post).",
	"rc\\": "Checked by Content Moderation Team due to Users Reports (chat).",
	"cs\\": "Due to report ID: ",

	"h\\": "(historic violation)",
	"nr\\": "Non-repeated violation:",
	"t\\": "timecode - ___).",
	"fu\\": "Media featuring Third-party Content/Multiple Participants removed (posts/chats).",
	"another\\": "The user has another account: ",

	"tpc\\": "TOS Third-party Content/Multiple Participants - detected in posts/chats. Alert Pop UP.",
	"tpcc\\": "TOS Third-party Content/Multiple Participants - detected in chats. Alert Pop UP.",
	"tpcp\\": "TOS Third-party Content/Multiple Participants - detected in posts. Alert Pop UP.",
	"tpch\\": "TOS Third-party Content/Multiple Participants - detected in posts/chats/vaults (historic violation).",
	"tpp\\": "TOS Third-Party Payments - detected in posts/chats/vaults.",
	"tppc\\": "TOS Third-Party Payments - detected in chats.",

	"sfs\\": "SFS/Promo account - status confirmed",
	"sfsn\\": "The account cannot be considered as SFS/Promo account",

	"missed\\": "Missed violation from the previous CM Review: ___",
	"dis\\": "Please disregard my comment ___. Correct one is:",
	"disp\\": """Please disregard my comment from ___ in the part:
___.
Correct one should have been:
___""",

}

with shelve.open("TestDB") as db:
	for key, value in shortcuts_dict.items():
		if key not in dict(db):
			db[key] = value
	for key in dict(db):
		keyboard.add_abbreviation(key, dict(db)[key], timeout=3)


def view_shortcuts():
	with shelve.open("TestDB") as db:
		sorted_list = sorted(dict(db).items(), key=lambda a: a[0], reverse=False)
		print("\nShortcuts:")
		for key, value in sorted_list:
			print(f"{key} - {value}")
		print()


def main():
	option_a = "View list of shortcuts"
	option_b = "Add a new shortcut"
	option_c = "Remove an existing shortcut"
	option_d = "Close the window"
	option_e = "Quit the program"

	while True:
		choice = pyautogui.confirm('Enter option.', buttons=[option_a, option_b, option_c, option_d, option_e])

		if choice == option_a:
			with shelve.open("TestDB") as db:
				if not db:
					print("No shortcuts added yet.")
				else:
					view_shortcuts()

		elif choice == option_b:
			key = pyautogui.prompt("What is the shortcut?")
			if not key:
				pyautogui.alert(text=f"No key was entered", title='Missing key', button='OK')
				continue

			value = pyautogui.prompt("What is the full version for this shortcut?")
			if not value:
				pyautogui.alert(text=f"No value was entered", title='Missing value', button='OK')
				continue

			with shelve.open("TestDB") as db:
				if key in db:
					message = f"The key is already in the database: {key}: {db[key]}. \nWould you like to overwrite the existing key?"
					choice = pyautogui.confirm(message, buttons=["Yes", "No"])
					if choice == "Yes":
						db[key] = value
					else:
						continue
				else:
					db[key] = value
			pyautogui.alert(text=f"A new shortcut was added: \n{key}: {value}", title='Success', button='OK')

		elif choice == option_c:
			with shelve.open("TestDB") as db:
				key = pyautogui.prompt("What is the shortcut's name you want to remove?")
				if not key:
					continue
				elif key not in list(db):
					pyautogui.alert(text=f"Entered key '{key}' is not in the database.", title='Not found', button='OK')
				else:
					pyautogui.alert(text=f"A shortcut was removed: \n{key}: {db[key]}", title='Success', button='OK')
					del db[key]

		elif choice == option_d:
			print("The program is running!")
			break

		elif choice == option_e:
			print("Have a nice one!")
			exit()

	keyboard.wait("Ctrl + Alt + L")


view_shortcuts()
print("The program is running!")

keyboard.wait("Ctrl + Alt + L")

while True:
	main()
