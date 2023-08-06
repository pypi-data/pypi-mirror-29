import os
import shutil
import uuid
from subprocess import Popen, DEVNULL

import uno


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
        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", self.ctx)
        self.comp = desktop.loadComponentFromURL(self.urlify(filepath), "_blank", 0, ())
        # access the current writer document
        self.model = desktop.getCurrentComponent()
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

    def insert_pdf(self, filename):
        # get file basename
        basename = os.path.basename(filename)
        tmp_dir = "/tmp/%s" % str(uuid.uuid4())

        # TAG for search and replace multiple PDF
        self.insert_txt("++-=0=-++")

        os.mkdir(tmp_dir)
        Popen([
            'pdftocairo',
            '-jpeg',
            filename,
            '%s/image-' % tmp_dir,
        ], stdout=DEVNULL).communicate()

        files_list = os.listdir(tmp_dir)
        # Sort alpha
        files_list.sort()

        for index, filename in enumerate(files_list):
            with open("%s/%s" % (tmp_dir, filename), 'rb') as img:
                self.search_and_select("++-={0}=-++".format(str(index)))
                self.execute("InsertPagebreak")
                self.insert_txt("§§{0}§§{1}§§".format(basename, str(index + 1)))
                self.insert_txt("++-={0}=-++".format(str(index + 1)))
                self.insert_img(img.read())
                self.execute("SetAnchorToPage")

        self.search_and_replace("++-={0}=-++".format(str(len(files_list))), "")
        shutil.rmtree(tmp_dir, ignore_errors=True)

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

    def save_and_close(self, path):
        self.model.storeToURL(self.urlify(path), ())
        # close the document
        self.model.dispose()


# Pour exemple, le code suivant ajoute des annexes après avoir détécté le tag "ANNEXES" sur un document odt
if __name__ == '__main__':
    helper = FusionHelper(2002, "../test.odt")
    if helper.search_and_select("ANNEXES"):
        helper.insert_pdf("../lessentiel-pour-maitriser-docker-par-treeptik-slides.pdf")

    helper.save_and_close("../saved.odt")
