# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import eg

eg.RegisterPlugin(
    name=u'Eg_plugin_chromium',
    author=u'Dan Edens',
    version=u'0.0.1a',
    description=(
        u'Eventghost wrapper for Pyppeteer.\n'
        u'https://github.com/miyakogi/pyppeteer\n'
        u'\n
    ),
    kind=u'program',
    url=u'https://github.com/DanEdens/Eg_plugin_chromium',
    help=u'Please constact me with questions at Dan.Edens@Geo-instruments.com',
    canMultiLoad=False,
    createMacrosOnAdd=False,
    guid=u'{B8B58BA0-BEB7-4324-AB68-564427D72B53}',
    hardwareId=u'',
    icon=None
)





class Text:
    # add variables with string that you want to be able to have translated
    # using the language editor in here

    class Launch_Browser:
        name = u'Launch Browser'
        description = 'Action Launch Browser'


    class New_Page:
        name = u'New Page'
        description = 'Action New Page'


    class Goto_Url:
        name = u'Goto Url'
        description = 'Action Goto Url'


    class Focus_Page:
        name = u'Focus Page'
        description = 'Action Focus Page'


    class Close_Page:
        name = u'Close Page'
        description = 'Action Close Page'


    class Split_Page:
        name = u'Split Page'
        description = 'Action Split Page'


    class Set_Page_Name:
        name = u'Set Page Name'
        description = 'Action Set Page Name'


    class Set_Page_Size:
        name = u'Set Page Size'
        description = 'Action Set Page Size'


    class Save_Session:
        name = u'Save Session'
        description = 'Action Save Session'


    class Load_Session:
        name = u'Load Session'
        description = 'Action Load Session'


    class Login:
        name = u'Login'
        description = 'Action Login'


    class Scrape_Page:
        name = u'Scrape Page'
        description = 'Action Scrape Page'


    class Scrape_Site:
        name = u'Scrape Site'
        description = 'Action Scrape Site'


    class Screenshot_Page:
        name = u'Screenshot Page'
        description = 'Action Screenshot Page'


    class Screenshot_Pages:
        name = u'Screenshot Pages'
        description = 'Action Screenshot Pages'


    class Clean_Up:
        name = u'Clean Up'
        description = 'Action Clean Up'


    class Click_Item:
        name = u'Click Item'
        description = 'Action Click Item'


    class Focus_Item:
        name = u'Focus Item'
        description = 'Action Focus Item'


    class Bookmark_Page:
        name = u'Bookmark Page'
        description = 'Action Bookmark Page'


    class Open_New_Browser_Context:
        name = u'Open New Browser Context'
        description = 'Action Open New Browser Context'


    class Focus_Browser_Context:
        name = u'Focus Browser Context'
        description = 'Action Focus Browser Context'


    class Pushd_Browser_Context:
        name = u'Pushd Browser Context'
        description = 'Action Pushd Browser Context'


    class Popd_Browser_Context:
        name = u'Popd Browser Context'
        description = 'Action Popd Browser Context'


    class Pushd_Page:
        name = u'Pushd Page'
        description = 'Action Pushd Page'


    class Popd_Page:
        name = u'Popd Page'
        description = 'Action Popd Page'


    class Store_Page:
        name = u'Store Page'
        description = 'Action Store Page'


    class :
        name = u''
        description = 'Action '




class Eg_plugin_chromium(eg.PluginBase):
    text = Text

    # you want to add any variables that can be access from anywhere inside of
    # your plugin here
    def __init__(self):
        self.AddAction(Launch_Browser)
        self.AddAction(New_Page)
        self.AddAction(Goto_Url)
        self.AddAction(Focus_Page)
        self.AddAction(Close_Page)
        self.AddAction(Split_Page)
        self.AddAction(Set_Page_Name)
        self.AddAction(Set_Page_Size)
        self.AddAction(Save_Session)
        self.AddAction(Load_Session)
        self.AddAction(Login)
        self.AddAction(Scrape_Page)
        self.AddAction(Scrape_Site)
        self.AddAction(Screenshot_Page)
        self.AddAction(Screenshot_Pages)
        self.AddAction(Clean_Up)
        self.AddAction(Click_Item)
        self.AddAction(Focus_Item)
        self.AddAction(Bookmark_Page)
        self.AddAction(Open_New_Browser_Context)
        self.AddAction(Focus_Browser_Context)
        self.AddAction(Pushd_Browser_Context)
        self.AddAction(Popd_Browser_Context)
        self.AddAction(Pushd_Page)
        self.AddAction(Popd_Page)
        self.AddAction(Store_Page)
        self.AddAction()



    # you will want to add any startup parameters and also run any startup code
    # here
    def __start__(self, *args):
        pass

    # this gets called when eg is being closed and you can run code when that
    # happens
    def __close__(self):
        pass

    # this gets called as well when EG closes but it also gets called when a
    # plugin gets disabled. This is where you will do things like close any
    # open sockets
    def __stop__(self):
        pass

    # You will replace the code in this method if you want to make a plugin
    # configuration dialog.
    def Configure(self, *args):

        eg.PluginBase.Configure(self, *args)


    # The next 2 are pretty self explanatory
    def OnComputerResume(self):
        pass

    def OnComputerSuspend(self):
        pass

    # This gets called when a plugin gets deleted from the tree. so here if
    # you use eg.PersistantData to store any data. that data needs to be
    # deleted when the plugin gets removed. this is where that gets done.
    def OnDelete(self):
        pass




class Launch_Browser(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class New_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Goto_Url(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Focus_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Close_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Split_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Set_Page_Name(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Set_Page_Size(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Save_Session(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Load_Session(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Login(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Scrape_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Scrape_Site(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Screenshot_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Screenshot_Pages(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Clean_Up(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Click_Item(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Focus_Item(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Bookmark_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Open_New_Browser_Context(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Focus_Browser_Context(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Pushd_Browser_Context(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Popd_Browser_Context(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Pushd_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Popd_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class Store_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()


class (eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()
