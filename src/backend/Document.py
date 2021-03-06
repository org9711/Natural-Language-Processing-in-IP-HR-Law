from backend.FilesIO import FilesIO
from backend.PDFtext import PDFtext
from backend.PDFmetadata import PDFmetadata
from backend.Count import Count
from backend.ClassInformation import ClassInformation


"""
Stores data corresponding to each input document.
"""
class Document:

    io = FilesIO()


    def __init__(self, filename, title, journal, date, test, hrRat, ipRat,   \
            userRat, creatorRat):
        """
        Initialises a Document object corresponding to the document in
        $filename.

        Arguments:
        filename (str)
            -- the filename of the document
        title (str)
            -- the tile of the document
        journal (str)
            -- the journal that the document comes from
        date (datetime.datetime)
            -- the date that the document was published first
        test (int)
            -- an integer representing whether the document is test (1)
               or a training (0) document
        hrRat (float)
            -- a rating of how much the document has language
               typical of the topic of human rights law
        ipRat (float)
            -- a rating of how much the document has language
               typical of the topic of intellectual property law
        userRat (float)
            -- a rating of how much the document has language
               suggesting the protection of the user of intellectual
               property
        creatorRat (float)
            -- a rating of how much the document has language
               suggesting the protection of the creator of intellectual
               property
        """
        self._filename = filename
        self._pdfText = PDFtext(filename)
        self._pdfMetadata =                                                  \
            PDFmetadata(filename, self._pdfText, title, journal, date)
        self._count = Count(filename, self._pdfText.getText())
        self._classInformation = ClassInformation(test, hrRat, ipRat,        \
            userRat, creatorRat, self._pdfMetadata.getJournal())
        self.io.outputDocumentData(self)


    def getFilename(self):
        """
        Returns:
        self._filename (str)
            -- the filename of the document
        """
        return self._filename


    def getPDFtext(self):
        """
        Returns:
        self._pdfText (PDFtext)
            --
        """
        return self._pdfText


    def getPDFmetadata(self):
        """
        Returns:
        self._pdfMetadata (PDFmetadata)
            --
        """
        return self._pdfMetadata


    def getCount(self):
        """
        Returns:
        self._count (Count)
            --
        """
        return self._count


    def getClassInformation(self):
        """
        Returns:
        self._classInformation (ClassInformation)
            --
        """
        return self._classInformation


    def makeFormChanges(self, title, date, journal, test):
        """
        Arguments:
        title   (string)
            --
        date    ()
            --
        journal ()
            --
        test    ()
            --
        """
        self._pdfMetadata.setTitle(title)
        self._pdfMetadata.setDate(date)
        self._classInformation.setTest(test)

        if not journal == self.getPDFmetadata().getJournal():
            self._pdfMetadata.setJournal(journal)
            self._classInformation.deduceGt(journal)
            self._pdfText.cleanText(self._filename, journal)
        self.io.outputDocumentData(self)


    def removeData(self):
        """

        """
        self.io.removeDocumentData(self._filename)
        self.io.removeAssociatedFiles(self._filename)
