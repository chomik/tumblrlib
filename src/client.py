#!/usr/bin/env python
#-*- coding: utf-8 -*-

from ctypes import CDLL
from urllib import urlencode

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

from credentials import Credentials

tumblr = CDLL("../lib/libtumblrlib.so")
tumblr.tumblrlibinit.restype = None
tumblr.tumblrlibinit()

class Client(QtGui.QMainWindow):
    def __init__(self, *args):
        self.credentials_dialog = Credentials()
        self.email = ""
        self.password = ""
        self.verify_credentials()

        super(Client, self).__init__(*args)
        uic.loadUi('client.ui', self)

        self.publishers = {
                0: self.send_text,
                1: self.send_quote,
                2: self.send_chat,
                3: self.send_url,
                4: self.send_photo,
                5: self.send_video,
                6: self.send_audio}
        self.setWindowTitle(self.email)

    @QtCore.pyqtSlot()
    def on_photo_path_button_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Znajdź plik',
                    '/home')
        self.photo_path.setText(filename)

    @QtCore.pyqtSlot()
    def on_video_path_button_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Znajdź plik',
                    '/home', 'pliki wideo (*.asf *.asx *.avi *.divx *.dv *.dvx *.m4v *.mov *.mp4 *.mpeg *.mpg *.qt *.wmv *.3g2 *.3gp *.3ivx *.3vx)')
        self.video_path.setText(filename)

    @QtCore.pyqtSlot()
    def on_audio_path_button_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Znajdź plik',
                    '/home', 'pliki dźwiękowe (*.mp3 *.aiff *.aif)')
        self.audio_path.setText(filename)

    @QtCore.pyqtSlot()
    def on_publish_clicked(self):
        self.statusBar().showMessage(u'wysyłanie treści')
        result = self.publishers[self.tabs.currentIndex()]()
        self.show_status_message(result)

    def verify_credentials(self):
        self.credentials_dialog.exec_()
        self.email = self.credentials_dialog.email.text()
        self.password = self.credentials_dialog.password.text()
        if tumblr.validate_credentials(urlencode({'email': self.email,
                'password': self.password})) != 200:
            self.credentials_dialog.setWindowTitle(u'sprawdź poprawność danych')
            self.verify_credentials()

    def show_status_message(self, status):
        if status >= 200 and status < 300:
            self.statusBar().showMessage(u'treść opublikowana', 10000)
        elif status >= 400 and status < 500:
            self.statusBar().showMessage(u'błędne dane', 10000)
        elif status >= 500 and status < 600:
            self.statusBar().showMessage(u'błąd serwera', 10000)

    def send_text(self):
        params = urlencode({'email': self.email,
            'password': self.password,
            'type': 'regular',
            'title': self.regular_title.text().toLocal8Bit(),
            'body': self.regular_body.toPlainText().toLocal8Bit()})
        return tumblr.post_text(params, len(params)) 

    def send_quote(self):
        params = urlencode({'email': self.email,
            'password': self.password,
            'type': 'quote',
            'quote': self.quote_quote.toPlainText().toLocal8Bit(),
            'source': self.quote_source.toPlainText().toLocal8Bit()})
        return tumblr.post_text(params, len(params)) 

    def send_chat(self):
        params = urlencode({'email': self.email,
            'password': self.password,
            'type': 'conversation',
            'title': self.conversation_title.text().toLocal8Bit(),
            'conversation': self.conversation_conversation.toPlainText().toLocal8Bit()})
        return tumblr.post_text(params, len(params)) 

    def send_url(self):
        params = urlencode({'email': self.email,
            'password': self.password,
            'type': 'link',
            'name': self.link_name.text().toLocal8Bit(),
            'url': self.link_url.text().toLocal8Bit(),
            'description': self.link_description.toPlainText().toLocal8Bit()})
        return tumblr.post_text(params, len(params)) 

    def send_photo(self):
        params = urlencode({'email': self.email,
            'password': self.password,
            'type': 'photo',
            'data': open(self.photo_path.text()).read(),
            'caption': self.photo_caption.toPlainText().toLocal8Bit()})
        return tumblr.post_text(params, len(params)) 

    def send_video(self):
        params = urlencode({'email': self.email,
            'password': self.password,
            'type': 'video',
            'data': open(self.video_path.text()).read(),
            'caption': self.video_caption.toPlainText().toLocal8Bit()})
        return tumblr.post_text(params, len(params))

    def send_audio(self):
        params = urlencode({'email': self.email,
            'password': self.password,
            'type': 'audio',
            'data': open(self.audio_path.text()).read(),
            'caption': self.audio_caption.toPlainText().toLocal8Bit()})
        return tumblr.post_text(params, len(params))

