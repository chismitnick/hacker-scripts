"""
Author: Areeb Beigh
Created: 5th August 2016

Module to read the configuration of different hacker-scripts from the
given configuration file and return the results
"""

import configparser
import os

from src.filetools import getAllFiles


class ConfigReader:
    readMethods = {
        "hs-backup":     "_readBackup",
        "hs-browse":     "_readBrowse",
        "hs-desktop":    "_readDesktop",
        "hs-music":      "_readMusic",
        "hs-start":      "_readStart",
        "hs-wallpaper":  "_readWallpaper",
        "hs-work":       "_readWork",
    }

    def __init__(self, configFile):
        """ Creates a ConfigParser object and reads the given configuration
        file

        Parameters:
            configFile:
                The configuration file.
        """

        self.Config = configparser.ConfigParser()
        self.Config.read(configFile)

    def readConfig(self, script):
        """ Calls the appropriate read method to read the configuration
        of the given script, returns None if no method is available

        Parameters:
            script:
                The hacker-script of which the configuration is
                to be read.
                Example: "hs-music"
        """

        if script not in self.readMethods:
            return None

        return eval("self." + self.readMethods[script])(self.Config)

    def _readBackup(self, Config):
        """ Reads hs-backup configuration and returns a tuple of
        configuration values """

        purge = Config.get("hs-backup", "purge")
        retries = Config.get("hs-backup", "retries")
        backupLocation = Config.get("hs-backup", "backup_location")
        directories = []

        for option in Config.options("hs-backup"):
            value = Config.get("hs-backup", option)
            if option[0:9] == "directory" and value:
                directories.append(value)

        return purge, retries, backupLocation, directories

    def _readBrowse(self, Config):
        """ Reads hs-browse configuration and returns a list of
        urls """

        urls = []

        for option in Config.options("hs-browse"):
            url = Config.get("hs-browse", option)
            if url:
                urls.append(url)

        return urls

    def _readDesktop(self, Config):
        """ Reads hs-desktop configuration and returns a dict
        of the configuration values """

        paths = {
            "images": Config.get("hs-desktop", "images_directory"),
            "videos": Config.get("hs-desktop", "videos_directory"),
            "textFiles": Config.get("hs-desktop", "files_directory"),
        }

        return paths

    def _readMusic(self, Config):
        """ Reads hs-music configuration and returns a list of
        directories in it """

        extensions = [
            ".mp3",
            ".m4a",
            ".ogg",
            ".flac",
        ]
        musicFiles = []

        for option in Config.options("hs-music"):
            directory = Config.get("hs-music", option)
            if os.path.isdir(directory):
                musicFiles.extend(getAllFiles(directory, extensions))

        return musicFiles


    def _readStart(self, Config):
        """ Reads hs-start configuration and returns a list of programs/files
        in it """

        files = []

        for option in Config.options("hs-start"):
            if Config.get("hs-start", option):
                files.append(Config.get("hs-start", option))

        return files

    def _readWallpaper(self, Config):
        """ Reads hs-wallpaper configuration and returns a list of directories
        in it """

        extensions = [".png", ".jpg"]
        wallpapers = []

        for option in Config.options("hs-wallpaper"):
            directory = Config.get("hs-wallpaper", option)
            if os.path.isdir(directory):
                wallpapers.extend(getAllFiles(directory, extensions))

        return wallpapers

    def _readWork(self, Config):
        """ Reads the hs-work configuration and returns a list of files and
        the text editor to open them with """

        files = []
        editor = ""

        for option in Config.options("hs-work"):
            value = Config.get("hs-work", option)
            if option != "editor" and value:
                files.append(value)
            elif option == "editor":
                editor = value

        return files, editor