#!/usr/bin/python


import os
import json
import gtk
import appindicator
import shutil
import sys


SHELL_CMD = "gnome-terminal -x"
LAUNCHT_CONF_FILE = ".launcht_conf"
ICON_FILE = "launcht.png"
DESKTOP_ICON_FILE = "launcht128.png"
DESKTOP_FILE = "launcht.desktop"
DESKTOP_FILE_SNIPPET = "[Desktop Entry]\nVersion=1.0\nName=launcht\nExec=%s\nPath=%s\nIcon=%s\nTerminal=false\nType=Application\nCategories=Utility;Application;"
AUTO_START_DIR = ".config/autostart"
DASH_SHORTCUT_DIR = ".local/share/applications"


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
    executable_file = sys.argv[0]

    conf_path = "%s/%s" % (os.getenv("HOME"), LAUNCHT_CONF_FILE)
    dash_shortcut_file_path = "%s/%s/%s" % (os.getenv("HOME"), DASH_SHORTCUT_DIR, DESKTOP_FILE)
    autostart_file_path = "%s/%s/%s" % (os.getenv("HOME"), AUTO_START_DIR, DESKTOP_FILE)

    # if no config file exists then create one by copying the default config
    if not os.path.isfile(conf_path):
        try:
            shutil.copy(LAUNCHT_CONF_FILE, conf_path)
        except IOError:
            print "Can't open default configuration file. Please ensure all the app files were downloaded correctly."
            sys.exit(1)

    # create desktop file for dash if needed
    if not os.path.isfile(dash_shortcut_file_path):
        create_shortcut(executable_file, dash_shortcut_file_path, DESKTOP_ICON_FILE)

    conf_json = open(conf_path)

    conf = json.load(conf_json)

    main_menu = gtk.Menu()

    # create/remove auto launch shortcut if needed
    if "autostart" in conf and conf["autostart"] == "true":
        if not os.path.isfile(autostart_file_path):
            create_shortcut(executable_file, autostart_file_path, DESKTOP_ICON_FILE)
    else:
        if os.path.isfile(autostart_file_path):
            os.remove(autostart_file_path)
        
    # init default shell command with gnome-terminal first
    default_shell_cmd = SHELL_CMD

    # if custom shell-cmd is set in .launcht_conf
    # then override the default with it
    if "shell-cmd" in conf:
        default_shell_cmd = conf["shell-cmd"]

    build_menu(conf["items"], main_menu, default_shell_cmd)

    quit_item = gtk.MenuItem("Quit")
    quit_item.connect("activate", lambda m: gtk.main_quit())
    quit_item.show()
    main_menu.append(quit_item)

    return main_menu


def create_shortcut(executable_file_name, desktop_file_path, icon_file_name):
    executable_path = os.path.realpath(executable_file_name)
    executable_dir = os.path.dirname(executable_path)
    icon_file_path = "%s/%s" % (executable_dir, icon_file_name)

    desktop_file = open(desktop_file_path, "w+")
    desktop_file.write(DESKTOP_FILE_SNIPPET % (executable_path, executable_dir, icon_file_path))
    desktop_file.close()


if __name__ == "__main__":
    indicator = appindicator.Indicator("launcht", os.path.realpath(ICON_FILE), appindicator.CATEGORY_APPLICATION_STATUS)
    indicator.set_status(appindicator.STATUS_ACTIVE)

    menu = build_main_menu()
    indicator.set_menu(menu)

    gtk.main()
