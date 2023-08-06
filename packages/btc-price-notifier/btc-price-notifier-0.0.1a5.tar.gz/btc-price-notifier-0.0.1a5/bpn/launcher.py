# -*- coding: utf-8 -*-
"""
Copyright (C) 2018, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of MIT license

<https://opensource.org/licenses/MIT>
"""
import logging
from bpn.gui.frame import Application

def entry_point():
    #logging 層級設定
    logging.basicConfig(level=logging.INFO)
    
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    entry_point()