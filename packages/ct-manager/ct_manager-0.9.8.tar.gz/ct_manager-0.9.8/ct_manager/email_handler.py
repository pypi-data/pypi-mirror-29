# -*- coding: utf-8 -*-

from ct_manager.base_handler import MiscHandler
from ct_manager.settings import Settings
from ct_manager.enums import MiscSetting


class EmailHandler(MiscHandler):
    def __init__(self, **kwargs):
        Settings.misc_setting = MiscSetting.EmailSetting
        super(EmailHandler, self).__init__(**kwargs)
        self.sender_ = self.misc_setting_params['sender']
        self.receiver_ = self.misc_setting_params['receiver']
        self.username_ = self.misc_setting_params['username']
        self.password_ = self.misc_setting_params['password']
        self.host_ = self.misc_setting_params['host']

    @property
    def sender(self):
        return self.sender_

    @property
    def reciever(self):
        return self.receiver_

    @property
    def username(self):
        return self.username_

    @property
    def password(self):
        return self.password_

    @property
    def host(self):
        return self.host_

