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
        description = 'Laumch a new Browser Defualt Context'


    class New_Page:
        name = u'New Page'
        description = 'Create a new page in arg(context))'


    class Goto_Url:
        name = u'Goto Url'
        description = 'load arg(url) on arg(page)'


    class Focus_Page:
        name = u'Focus Page'
        description = 'Focus on arg(page). Will support Index and Page Name'


    class Close_Page:
        name = u'Close Page'
        description = 'Close arg(page)'


    class Split_Page:
        name = u'Split Page'
        description = 'Open a new Page at same url as arg(page)'


    class Set_Page_Name:
        name = u'Set Page Name'
        description = 'Set arg(page) to arg(name)'


    class Set_Page_Size:
        name = u'Set Page Size'
        description = 'Setviewport on arg(page)'


    class Save_Session:
        name = u'Save Session'
        description = 'Save pages in arg(context) as arg(session)'


    class Load_Session:
        name = u'Load Session'
        description = 'Launch new context with pages saved to arg(session)'


    class Login:
        name = u'Login'
        description = 'Navigate focused page to arg(url) and search for login selectors'


    class Scrape_Page:
        name = u'Scrape Page'
        description = 'Scan focused page if not arg(page), and save data matching config patterns'


    class Scrape_Site:
        name = u'Scrape Site'
        description = 'Scan focused page if not arg(page), than navigate through nearby links and save data matching config patterns'


    class Screenshot_Page:
        name = u'Screenshot Page'
        description = 'Saves Screenshot of Focused page if not arg(page)'


    class Screenshot_Pages:
        name = u'Screenshot Pages'
        description = 'Saves Screenshots of focused page if not arg(page), than navigate through nearby pages and save arg(number) of Screenshots \\nThis is geared towards Websites configured for specfic data'


    class Clean_Up:
        name = u'Clean Up'
        description = 'Clean up Temp files not refered by active contexts. \\nThis is particularly useful when generating Gifs from timelapsed data feeds'


    class Click_Item:
        name = u'Click Item'
        description = 'Click on arg(instance) of arg(text) on focused if not arg(page)'


    class Focus_Item:
        name = u'Focus Item'
        description = 'Move cursor to arg(instance) of arg(text) on focused if not arg(page)'


    class Bookmark_Page:
        name = u'Bookmark Page'
        description = 'Save url of arg(page) to bookmarks.arg(name)'


    class Open_New_Browser_Context:
        name = u'Open New Browser Context'
        description = 'Create a new Browser Context other than Default'


    class Focus_Browser_Context:
        name = u'Focus Browser Context'
        description = 'Focus on arg(context) w/ option to focus arg(context.page)'


    class Pushd_Browser_Context:
        name = u'Pushd Browser Context'
        description = 'Save ID of focused if not arg(context) and change to arg(new_context)'


    class Popd_Browser_Context:
        name = u'Popd Browser Context'
        description = 'Return Focus to Saved ID of Pushd Context. Will change focus to Default context, if pushd not set.'


    class Pushd_Page:
        name = u'Pushd Page'
        description = 'Save ID of focused if not arg(page) and change to arg(new_page)'


    class Popd_Page:
        name = u'Popd Page'
        description = 'Return Focus to Saved ID of Pushd Context. Will change focus to Default context, if pushd not set.'


    class Store_Page:
        name = u'Store Page'
        description = 'Limit Resource use by storing *arg(page) in templist.'


    class Restore_Pagelist:
        name = u'Store Page'
        description = 'Restore pages to arg(context) stored in templist.'



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
        self.AddAction(Restore_Page)



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
        # launch
        # load sessions from eg.PersistantData
        pass

    def OnComputerSuspend(self):
        # Save temp session to eg.PersistantData
        # Close default context
        pass

    # This gets called when a plugin gets deleted from the tree. so here if
    # you use eg.PersistantData to store any data. that data needs to be
    # deleted when the plugin gets removed. this is where that gets done.
    def OnDelete(self):
        # clear all eg.PersistantData
        pass




class Launch_Browser(eg.ActionBase):
    def __init__(self, head, session, *args):
        self.head = head
        self.session = session
    # this code gets executed when the action gets run
    def __call__(self, *args):
        if self.head:
            return await launch({"headless": False})
        else:
            return await launch({"headless": True})

        while panel.Affirmed():
            panel.SetResult()

        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()


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

class Restore_Page(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()
