
import unittest
from database.Database_SABER import Database_SABER
db = Database_SABER('dbTest.db')

#test table init
db.setupImageTable()
db.setupPathConfigTable()
db.loadPathConfig()
db.loadImagePaths()
db.setRedVal('image9.png',1)
db.setCircleVal('image9.png',0)
db.setCircleVal('image13.png',1)
db.setRedVal('image13.png',0)

IMAGE_NAMES_LIST = ['image9.png','image13.png','image35.png','red_circle.jpeg','ferrari.png','image_non.png','wsu.png','onions.jpeg','oopsallberries.png','tire.PNG']


def testTableInit(table):
    db.cursor.execute(f"PRAGMA table_info({table})")
    table_info = db.cursor.fetchall()
    return table_info

def testPathImport():
    db.cursor.execute(f"SELECT imageName FROM images ")
    return_list = db.cursor.fetchall()
    rlist = []
    for item in return_list:
        clean_item = db._cleanQuery(item)
        if clean_item != '':
            rlist.append(db._cleanQuery(str(clean_item)))
    return rlist



class Database_SABER_Test(unittest.TestCase):
    def testImageTableInit(self):
        columnNames = ['path','imageName','hasRed','hasCircle']
        result = testTableInit('images')
        output = [result[1][1],result[2][1],result[3][1],result[4][1]]
        self.assertEqual(output,columnNames)

    def testPathConfigTableInit(self):
        columnNames = ['type','path']
        result = testTableInit('pathConfig')
        output = [result[1][1],result[2][1]]
        self.assertEqual(output,columnNames)
    
    def testPathImportImages(self):
        image_names = IMAGE_NAMES_LIST
        image_names.sort()
        result = testPathImport()
        result.sort()
        self.assertEqual(result,image_names)

    def testSetGetRed_1(self):
        result = db._cleanQuery(db.getValue('images',1,'hasRed','imageName'))
        self.assertEqual(result, 'image9.png')
    def testSetGetRed_0(self):
        result = db._cleanQuery(db.getValue('images',0,'hasRed','imageName'))
        self.assertEqual(result, 'image13.png')
    def testSetGetCircle_1(self):
        result = db._cleanQuery(db.getValue('images',1,'hasCircle','imageName'))
        self.assertEqual(result, 'image13.png')
    def testSetGetCircle_0(self):
        result = db._cleanQuery(db.getValue('images',0,'hasCircle','imageName'))
        self.assertEqual(result, 'image9.png')
