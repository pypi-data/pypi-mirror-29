# -*- coding: utf-8 -*-
# module moustache

import os

import uno

from utils import OdtXmlBuilder


class FusionHelper:
    @staticmethod
    def create_uno_service(service_name):
        sm = uno.getComponentContext().ServiceManager
        return sm.createInstanceWithContext(service_name, uno.getComponentContext())

    @staticmethod
    def urlify(path):
        return uno.systemPathToFileUrl(os.path.realpath(path))

    def __init__(self, port, filepath):
        # get the uno component context from the PyUNO runtime
        local_context = uno.getComponentContext()
        # create the UnoUrlResolver
        resolver = local_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_context)
        # connect to the running office
        self.ctx = resolver.resolve(
            "uno:socket,host=localhost,port={0};urp;StarOffice.ComponentContext".format(str(port)))
        smgr = self.ctx.ServiceManager
        # get the central desktop object
        self.desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", self.ctx)
        self.comp = self.desktop.loadComponentFromURL(self.urlify(filepath), "_blank", 0, ())
        # access the current writer document
        self.model = self.desktop.getCurrentComponent()
        self.document = self.model.getCurrentController().getFrame()
        self.dispatcher = self.create_uno_service("com.sun.star.frame.DispatchHelper")

    @staticmethod
    def create_property_value(name, value):
        prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        prop.Name = name
        prop.Value = value
        return prop

    def search_and_select(self, text):
        properties = (
            self.create_property_value('SearchItem.SearchString', text),
        )
        self.dispatcher.executeDispatch(self.document, ".uno:ExecuteSearch", "", 0, properties)
        return not self.get_cursor().isCollapsed()

    def search_and_replace(self, text, replace):
        properties = (
            self.create_property_value('SearchItem.SearchString', text),
            self.create_property_value('SearchItem.ReplaceString', replace),
            self.create_property_value('SearchItem.Command', 3),
        )
        self.dispatcher.executeDispatch(self.document, ".uno:ExecuteSearch", "", 0, properties)

    def insert_odt(self, path):
        properties = (
            self.create_property_value('Name', self.urlify(path)),
        )
        self.dispatcher.executeDispatch(self.document, ".uno:InsertDoc", "", 0, properties)

    def insert_txt(self, txt):
        properties = (
            self.create_property_value('Text', txt),
        )
        self.dispatcher.executeDispatch(self.document, ".uno:InsertText", "", 0, properties)

    def _file2istream(self, fbytes):
        istream = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.io.SequenceInputStream", self.ctx)
        istream.initialize((uno.ByteSequence(fbytes),))
        return istream

    def load_graphic_context(self, img_data):
        graphic_provider = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.graphic.GraphicProvider",
                                                                             self.ctx)
        properties = (
            self.create_property_value('InputStream', self._file2istream(img_data)),
        )
        return graphic_provider.queryGraphic(properties)

    def insert_pdf(self, filename, quality=150):
        # Build a basic ODT from the PDF file
        odt_builder = OdtXmlBuilder(filename, quality)

        # load the file created to repair it (fill
        loaded_file = self.desktop.loadComponentFromURL(self.urlify(odt_builder.final_odt_path), "_blank", 0, ())
        if loaded_file is None:
            print("Can't insert %s" % filename)
        loaded_file.storeToURL(self.urlify("%s-OK.odt" % odt_builder.tmp_dir), ())
        # close the document
        loaded_file.dispose()

        self.insert_odt("%s-OK.odt" % odt_builder.tmp_dir)
        #  Close odt_builder to remove all temporary files
        odt_builder.close()
        #  Remove the injected ODT
        os.remove("%s-OK.odt" % odt_builder.tmp_dir)

    def insert_img(self, img_data):
        img = self.comp.createInstance('com.sun.star.text.TextGraphicObject')

        img.Graphic = self.load_graphic_context(img_data)
        img.Surround = uno.Enum("com.sun.star.text.WrapTextMode", "THROUGHT")
        img.Width = 21000
        img.Height = 29700

        text = self.comp.Text
        cursor = self.get_cursor()
        text.insertTextContent(cursor, img, False)

    def execute(self, cmd):
        self.dispatcher.executeDispatch(self.document, ".uno:{0}".format(cmd), "", 0, ())

    def get_cursor(self):
        return self.model.getCurrentController().getViewCursor()

    def save_and_close(self, path, pdf=False):
        args = (
            self.create_property_value("FilterName", "writer_pdf_Export"),
        ) if pdf else ()

        self.model.storeToURL(self.urlify(path), args)
        # close the document
        self.model.dispose()


# Pour exemple, le code suivant ajoute des annexes après avoir détécté le tag "ANNEXES" sur un document odt
if __name__ == '__main__':
    helper = FusionHelper(2002, "../test.odt")
    if helper.search_and_select("ANNEXES"):
        helper.insert_pdf("../lessentiel-pour-maitriser-docker-par-treeptik-slides.pdf", quality=100)

    helper.save_and_close("../saved.odt")
