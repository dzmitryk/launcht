launcht
=======

Ubuntu indicator applet with configurable shortcut list for quick launch of terminal apps, somewhat inspired by [shuttle](https://github.com/fitztrev/shuttle) for OS X.

Installation and usage
=======

Application requires `appindicator` module to be installed. To do this in Ubuntu run the following command:

```
sudo apt-get install python-appindicator
```

After that is complete you can run the app:

```
git clone https://github.com/dzmitryk/launcht.git
cd launcht
./launcht.py
```

The shortcut list can be configured using JSON config file `.launcht_conf` which is located in user home directory (default configuration will be created automatically when you launch the app for the first time). Edit it to customize items in the launch menu.

### Basic configuration structure:

```json
{
	"shell-cmd": "gnome-terminal -x",
	"autostart":"false",
	"items": [
		{
			"type": "entry",
			"name": "top",
			"value": "top"
		},
		{
			"type": "separator"
		},
		{
			"type": "menu",
			"name": "editors",
			"value": [
				{
					"type": "entry",
					"name": "vi",
					"value": "vi"
				},
				{
					"type": "entry",
					"name": "nano",
					"value": "nano"
				}
			]
		}
	]
}
```

* `shell-cmd` specifies terminal shell command or any other command prefix i.e. default Ubuntu terminal `gnome-terminal -x`, this is usually set globally but can be overridden for specific entry
* `autostart` specifies whether the app should start automatically when user logs in
* `items` declares array of menu items
* `type` entry type, following types are supported:
  * `entry` specific app launch entry
  * `menu` menu enclosing more entries or other menus
  * `separator` menu separator
* `name` item name
* `value` command for `entry` type items and array of items for menus
