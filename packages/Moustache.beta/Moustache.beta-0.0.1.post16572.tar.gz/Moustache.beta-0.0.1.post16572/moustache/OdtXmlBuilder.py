# -*- coding: utf-8 -*-
# module moustache

import os
import shutil
import uuid
import xml.etree.ElementTree
import zipfile
from subprocess import Popen, DEVNULL

"""
Class to build an ODT file from PDF
It :
- Copy "minimal_odt" model to /tmp directory
- Extract PDF to pages with "pdftocairo" util (poppler-utils)
- Add images entries to ODT manifest
- Add XML elements to content
- Zip the all thing
"""


class OdtXmlBuilder:
    def __init__(self, filename, quality):
        # Init vars
        self._id = str(uuid.uuid4())
        self.tmp_dir = "/tmp/%s" % str(self._id)
        # Copy basic ODT tree to tmp file
        shutil.copytree("minimal_odt", self.tmp_dir, ignore=shutil.ignore_patterns(".*",))

        # get file basename
        self._basename = os.path.basename(filename)

        # Generate all images
        Popen([
            'pdftocairo',
            '-jpeg',
            '-r',
            str(quality),
            filename,
            "%s/Pictures/%s" % (self.tmp_dir, str(uuid.uuid4().hex)),
            ], stdout=DEVNULL).communicate()

        # List files and ignore hidden files, just in case
        self._files_list = os.listdir("%s/Pictures" % self.tmp_dir)
        # Sort alpha
        self._files_list.sort()

        # Prepare office namespace
        self._init_xml_namespace()
        # Build manifest.xml file
        self._build_manifest()
        # Build content.xml file
        self._build_content()
        # Zip final file
        self.final_odt_path = "%s.odt" % self.tmp_dir
        self._zipdir()

    """
    Init XML namespace, mandatory for python ElementTree search to work
    """
    @staticmethod
    def _init_xml_namespace():
        # Prepare libreoffice namespaces
        xml.etree.ElementTree.register_namespace("manifest", "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0")
        xml.etree.ElementTree.register_namespace("office", "urn:oasis:names:tc:opendocument:xmlns:office:1.0")
        xml.etree.ElementTree.register_namespace("style", "urn:oasis:names:tc:opendocument:xmlns:style:1.0")
        xml.etree.ElementTree.register_namespace("text", "urn:oasis:names:tc:opendocument:xmlns:text:1.0")
        xml.etree.ElementTree.register_namespace("draw", "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0")
        xml.etree.ElementTree.register_namespace("fo", "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0")
        xml.etree.ElementTree.register_namespace("xlink", "http://www.w3.org/1999/xlink")
        xml.etree.ElementTree.register_namespace("svg", "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0")
        xml.etree.ElementTree.register_namespace("form", "urn:oasis:names:tc:opendocument:xmlns:form:1.0")
        xml.etree.ElementTree.register_namespace("officeooo", "http://openoffice.org/2009/office")

    """
    Build the manifest.xml with "Pictures" entries from the PDF
    """
    def _build_manifest(self):
        # Edit manifest.xml file
        manifest_path = '%s/META-INF/manifest.xml' % self.tmp_dir
        manifest = xml.etree.ElementTree.parse(manifest_path)

        for index, filename in enumerate(self._files_list):
            new_tag = xml.etree.ElementTree.SubElement(manifest.getroot(), 'manifest:file-entry')
            new_tag.attrib['manifest:full-path'] = "Pictures/%s" % filename
            new_tag.attrib['manifest:media-type'] = "image/jpeg"

        manifest.write(manifest_path)

    """
    Build the content.xml with custom elements (jump page and full page image)
    """
    def _build_content(self):
        content_path = '%s/content.xml' % self.tmp_dir
        content = xml.etree.ElementTree.parse(content_path)

        office_ns = {"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0"}

        root = content.getroot()
        # Set missing namespace -> mandatory because ET removes it if not defined here !
        root.set("xmlns:svg", "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0")
        root.set("xmlns:xlink", "http://www.w3.org/1999/xlink")

        office_text = root.find("office:body", office_ns).find("office:text", office_ns)
        # Insert all content here

        for index, filename in enumerate(self._files_list):
            self._insert_image_element(index, filename, office_text)

        # Save content
        content.write(content_path, encoding="UTF-8")

    """
    Insert each Pictures in content.xml
    """
    def _insert_image_element(self, index, filename, office_text):
        p_elem = xml.etree.ElementTree.SubElement(office_text, 'text:p')
        p_elem.attrib['text:style-name'] = "P1"

        frame_elem = xml.etree.ElementTree.SubElement(p_elem, 'draw:frame')
        frame_elem.attrib['draw:style-name'] = "fr1"
        frame_elem.attrib['draw:name'] = "Image%d" % index
        frame_elem.attrib['text:anchor-type'] = "paragraph"
        frame_elem.attrib['svg:width'] = "21.001cm"
        frame_elem.attrib['svg:height'] = "29.7cm"
        frame_elem.attrib['draw:z-index'] = "0"

        image_elem = xml.etree.ElementTree.SubElement(frame_elem, 'draw:image')
        image_elem.attrib['xlink:href'] = "Pictures/%s" % filename
        image_elem.attrib['xlink:type'] = "simple"
        image_elem.attrib['xlink:show'] = "embed"
        image_elem.attrib['xlink:actuate'] = "onLoad"

        frame_elem.tail = "§§%s§§%d§§" % (self._basename, index)

    """
    Zip the whole directory to an odt file
    """
    def _zipdir(self):
        assert os.path.isdir(self.tmp_dir)
        from contextlib import closing
        with closing(zipfile.ZipFile(self.final_odt_path, "w", zipfile.ZIP_STORED)) as z:
            for root, dirs, files in os.walk(self.tmp_dir):
                for fn in files:
                    absfn = os.path.join(root, fn)
                    zfn = absfn[len(self.tmp_dir)+len(os.sep):]
                    z.write(absfn, zfn)

    """
    Remove all generated documents
    """
    def close(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        os.remove(self.final_odt_path)
