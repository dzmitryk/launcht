#!/usr/bin/python

# TODO: find monochrome icon for the app
# TODO: automatically generate .launcht_conf 
# TODO: installation


import os
import json
import gtk
import appindicator


SHELL_CMD = "gnome-terminal -x"
LAUNCHT_CONF_FILE = ".launcht_conf"


def menu_item_callback(menu_item, cmd):
    os.popen("%s %s &" % (SHELL_CMD, cmd))


def build_menu(items, menu):

    for item in items:
        menu_item = gtk.MenuItem(item["name"])

        if item["type"] == "entry":
            menu_item.connect("activate", menu_item_callback, item["value"])
        elif item["type"] == "menu":
            submenu = gtk.Menu()
            menu_item.set_submenu(submenu)
            build_menu(item["value"], submenu)

        menu_item.show()
        menu.append(menu_item)


def build_main_menu():

    conf_json = open("%s/%s" % (os.getenv("HOME"), LAUNCHT_CONF_FILE))

    conf = json.load(conf_json)

    main_menu = gtk.Menu()
    build_menu(conf["items"], main_menu)

    return main_menu


if __name__ == "__main__":
    indicator = appindicator.Indicator("launcht", "gtk-execute", appindicator.CATEGORY_APPLICATION_STATUS)
    indicator.set_label("launcht")
    indicator.set_status(appindicator.STATUS_ACTIVE)

    menu = build_main_menu()
    indicator.set_menu(menu)

    gtk.main()