launcht
=======

Easily configurable Ubuntu indicator applet for quick launch of terminal apps.

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

On first launch json configuration file `.launcht_conf` will be created in your home directory. Edit it to customize items in the launch menu.

### Basic configuration structure:

```json
{
	"shell-cmd": "gnome-terminal -x",
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
* `items` declares array of menu items
* `type` entry type, following types are supported:
  * `entry` specific app launch entry
  * `menu` menu enclosing more entries or other menus
  * `separator` menu separator
* `name` item name
* `value` command for `entry` type items and array of items for menus
