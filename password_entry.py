import hashlib
import random
import string
import re
import binascii


class Password_Entry:

    def __init__(self, titel, passwort, url, username, nummer):
        self.id = nummer
        self.titel = titel
        self.passwort = passwort
        self.url = url
        self.username = username

    def get_titel(self):
        return self.titel

    def get_id(self):
        return self.id

    def get_password(self):
        return self.passwort

    def get_url(self):
        return self.url

    def get_username(self):
        return self.username

    def get_id(self):
        return self.id
