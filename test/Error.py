"""Module for testing error objects."""

import cx_Oracle
import pickle

class TestBooleanVar(BaseTestCase):

    def testPickleError(self):
        "test picking/unpickling an error object"
        errorObj = None
        try:
            self.cursor.execute("""
                    begin
                        raise_application_error(-20101, 'Test!');
                    end;""")
        except cx_Oracle.Error as e:
            errorObj, = e.args
        self.assertEqual(type(errorObj), cx_Oracle._Error)
        self.assertTrue("Test!" in errorObj.message)
        self.assertEqual(errorObj.code, 20101)
        self.assertEqual(errorObj.offset, 0)
        self.assertEqual(errorObj.context, "Cursor_InternalExecute()")
        pickledData = pickle.dumps(errorObj)
        newErrorObj = pickle.loads(pickledData)
        self.assertEqual(type(newErrorObj), cx_Oracle._Error)
        self.assertTrue(newErrorObj.message == errorObj.message)
        self.assertTrue(newErrorObj.code == errorObj.code)
        self.assertTrue(newErrorObj.offset == errorObj.offset)
        self.assertTrue(newErrorObj.context == errorObj.context)
