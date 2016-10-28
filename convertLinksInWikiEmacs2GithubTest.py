'''
imitate dive into python roman.py & romantest.py
'''

#TODO test conversion of a few files on disk; existing code only tests conversion of a single line
#TODO test conversion of two .md files which link to each other

import convertLinksInWikiEmacs2Github as CLW
import unittest

class SanityCheckOfLineConversion(unittest.TestCase):
    def testSanity1(self):
        '''first add .md then remove .md: does a line remain the same?'''

        #TODO not sure if line ends with newline or not; assuming yes
        testLine='blather blather [descr1](link1) blather blather [descr2](link2) blather blather [descr3](link3)\n'
        f1=CLW.add_md_to_links_in_line
        f2=CLW.remove_md_from_links_in_line
        newLine1=f1(testLine)
        newLine2=f2(newLine1)
        self.assertEqual(testLine,newLine2)

    def testSanity2(self):
        '''first remove .md then add .md: does a line remain the same?'''

        #TODO not sure if line ends with newline or not; assuming yes
        testLine='blather blather [descr1](link1.md) blather blather [descr2](link2.md) blather blather [descr3](link3.md)\n'
        f1=CLW.remove_md_from_links_in_line
        f2=CLW.add_md_to_links_in_line
        newLine1=f1(testLine)
        newLine2=f2(newLine1)
        self.assertEqual(testLine,newLine2)

    #head
    # def testSanity3(self):
    #     '''
    #     f1=CLW.add_md_to_links_in_line
    #     f2=CLW.remove_md_from_links_in_line
    #     line='blather blather [descr1](link1.ext1) blather blather [descr2](link2.ext2) blather blather [descr3](link3.ext3)\n'
    #     f2(f1(line))==line
    #     '''
    #     #do not currently need to worry about links with non-md file extensions, so disregard

class ValueTestOfLineConversion(unittest.TestCase):
    extList=['.jpg','.JPG','.doc','.html','.pdf','.mm','.MP3','.WMA','.svg','.jpeg','.odt','.xlsx','.dia','.dxf','.xoj','.ods']
    weblinksToTest=['https://docs.python.org/2.7/howto/regex.html']
    weblinksToTest.append('http://orgmode.org/manual/Hyperlinks.html#Hyperlinks')
    weblinksToTest.append('https://www.pythonlearn.com/book.php')
    weblinksToTest.append('http://emacs.stackexchange.com/questions/15120/how-do-i-install-solarized-theme')

    #head
    def testAddDotMD1(self):
        '''add .md to a line; does line transform correctly?  [descr](link) > [descr](link.md)'''

        testLine='blather blather [descr1](link1) blather blather [descr2](link2) blather blather [descr3](link3)\n'
        correctResult='blather blather [descr1](link1.md) blather blather [descr2](link2.md) blather blather [descr3](link3.md)\n'
        f1=CLW.add_md_to_links_in_line
        newLine1=f1(testLine)
        self.assertEqual(newLine1,correctResult)

    def testAddDotMD2(self):
        '''add .md to a line; does line transform correctly?  [descr](link.md) > [descr](link.md)'''

        testLine='blather blather [descr1](link1.md) blather blather [descr2](link2.md) blather blather [descr3](link3.md)\n'
        correctResult=testLine
        f1=CLW.add_md_to_links_in_line
        newLine1=f1(testLine)
        self.assertEqual(newLine1,correctResult)

    def testAddDotMD3(self):
        '''add .md to a line; does line transform correctly?  [descr](link.ext) > [descr](link.ext) where ext is not md'''

        f1=CLW.add_md_to_links_in_line

        for ext in ValueTestOfLineConversion.extList:
            testLine='[descr1](link1'+ext+')'
            correctResult=testLine
            newLine1=f1(testLine)
            self.assertEqual(newLine1,correctResult)

    def testAddDotMD4(self):
        '''do not add .md to a weblink'''

        f1=CLW.add_md_to_links_in_line

        for weblink in ValueTestOfLineConversion.weblinksToTest:
            testLine='[descr1]('+weblink+')'
            correctResult=testLine
            newLine1=f1(testLine)
            self.assertEqual(newLine1,correctResult)

    #head
    def testRemoveDotMD1(self):
        '''remove .md from a line; does line transform correctly?  [descr](link.md) > [descr](link)'''

        testLine='blather blather [descr1](link1.md) blather blather [descr2](link2.md) blather blather [descr3](link3.md)\n'
        correctResult='blather blather [descr1](link1) blather blather [descr2](link2) blather blather [descr3](link3)\n'
        f1=CLW.remove_md_from_links_in_line
        newLine1=f1(testLine)
        self.assertEqual(newLine1,correctResult)
    def testRemoveDotMD2(self):
        '''remove .md from a line; does line transform correctly?  [descr](link.ext) > [descr](link.ext) where ext is not md'''

        f1=CLW.remove_md_from_links_in_line

        for ext in ValueTestOfLineConversion.extList:
            testLine='blather blather [descr1](link1'+ext+') blather blather [descr2](link2'+ext+') blather blather [descr3](link3'+ext+')\n'
            correctResult=testLine

            newLine1=f1(testLine)
            self.assertEqual(newLine1,correctResult)

    def testRemoveDotMD3(self):
        '''remove .md from a line; does line transform correctly?  [descr](weblink) > [descr](weblink)'''

        f1=CLW.remove_md_from_links_in_line

        for weblink in ValueTestOfLineConversion.weblinksToTest:
            testLine='blather blather [descr1]('+weblink+') blather blather [descr2]('+weblink+') blather blather [descr3]('+weblink+')\n'
            correctResult=testLine

            newLine1=f1(testLine)
            self.assertEqual(newLine1,correctResult)

#head
if __name__ == "__main__":
    unittest.main()


