# -*- coding: utf-8 -*-

import unittest


class TestClient(unittest.TestCase):
    def setUp(self):
        import configparser
        config = configparser.ConfigParser()
        config.read("setting.ini.sample")
        self.client_info = config['client']

    def test_summary(self):
        from kclient import Client
        client = Client(**self.client_info)
        resp = client.unread()
        # print(resp)

    def test_article_count(self):
        from kclient import Article
        from kclient import Groups
        client = Article(**self.client_info)
        resp = client.count(Groups.KEYAKIZAKA)
        # print(resp)

    def test_article_history(self):
        from kclient import Article
        from kclient import Groups
        client = Article(**self.client_info)
        resp = client.allhistory(Groups.KEYAKIZAKA, 1, True)
        # print(resp)


if __name__ == '__main__':
    unittest.main()