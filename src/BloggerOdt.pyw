#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import VistaAutentificar

class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frameAutentificacion = VistaAutentificar.VistaAutentificacion(None, -1, "")
        self.SetTopWindow(frameAutentificacion)
        frameAutentificacion.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
