#!/usr/bin/python

# TODO: find monochrome icon for the app
# TODO: installation


import os
import json
import gtk
import appindicator
import shutil
import sys


SHELL_CMD = "gnome-terminal -x"
LAUNCHT_CONF_FILE = ".launcht_conf"


def menu_item_callback(menu_item, cmd):
    os.popen(cmd)


def build_menu(items, menu, default_shell_cmd):

    for item in items:

        if item["type"] == "entry":
            menu_item = gtk.MenuItem(item["name"])

            shell_cmd = default_shell_cmd

            # if shell command is specified for entry
            # then need to override the default one with it

            if "shell-cmd" in item:
                shell_cmd = item["shell-cmd"]

            cmd = "%s %s &" % (shell_cmd, item["value"])
            menu_item.connect("activate", menu_item_callback, cmd)
        elif item["type"] == "menu":
            menu_item = gtk.MenuItem(item["name"])

            submenu = gtk.Menu()
            menu_item.set_submenu(submenu)
            build_menu(item["value"], submenu, default_shell_cmd)
        elif item["type"] == "separator":
            menu_item = gtk.SeparatorMenuItem()

        menu_item.show()
        menu.append(menu_item)


def build_main_menu():

    conf_path = "%s/%s" % (os.getenv("HOME"), LAUNCHT_CONF_FILE)

    # if no config file exists then create one by copying the default config
    if not os.path.isfile(conf_path):
        try:
            shutil.copy(LAUNCHT_CONF_FILE, conf_path)
        except IOError:
            print "Can't open default configuration file. Please ensure all the app files were downloaded correctly."
            sys.exit(1)

    conf_json = open(conf_path)

    conf = json.load(conf_json)

    main_menu = gtk.Menu()

    # init default shell command with gnome-terminal first
    default_shell_cmd = SHELL_CMD

    # if custom shell-cmd is set in .launcht_conf
    # then override the default with it
    if "shell-cmd" in conf:
        default_shell_cmd = conf["shell-cmd"]

    build_menu(conf["items"], main_menu, default_shell_cmd)

    return main_menu


if __name__ == "__main__":
    indicator = appindicator.Indicator("launcht", "gtk-execute", appindicator.CATEGORY_APPLICATION_STATUS)
    indicator.set_label("launcht")
    indicator.set_status(appindicator.STATUS_ACTIVE)

    menu = build_main_menu()
    indicator.set_menu(menu)

    gtk.main()
