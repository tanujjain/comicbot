import unittest
from src.fb_test_bot import fbtestbot


class TestStuff(unittest.TestCase):

    def test_ok_reponse(self):
        ret_im = fbtestbot.dilbert()
        if ret_im:
            im_ret = True
        #print(ret_im)
        self.assertTrue(im_ret)