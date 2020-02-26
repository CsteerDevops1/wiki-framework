import os
import configparser


class ConfigProvider:
    config_file_name = "config.ini"
    start_page = "index.html"
    side_bar = "sidebar"
    pages_folder = "pages"
    port = "8000"
    not_found_text = "Not Found!"
    main_title = "Wiki"


    def __init__(self):
        # If config file exists
        os.chdir("app")
        if os.path.isfile(self.config_file_name):
            config = configparser.RawConfigParser()
            config.read(self.config_file_name, encoding="utf-8")
            # Rewriting default values
            self.start_page = config.get("app_setting", "start_page")
            self.side_bar = config.get("app_setting", "side_bar")
            self.pages_folder = config.get("app_setting", "pages_folder")
            self.port = config.get("app_setting", "port")
            self.not_found_text = config.get("app_setting", "not_found_text")
            self.main_title = config.get("app_setting", "main_title")
