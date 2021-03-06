import unittest


class TestCal(unittest.TestCase):
    def setUp(self) -> None:
        self.log.info("--------测试开始---------")

    def test_add(self):
        self.assertEqual(self.cal.add(2, 3), 5, msg='测试不通过，2+3 != 6')

    def test_sub(self):
        self.assertEqual(self.cal.sub(3, 2), 1, msg='测试不通过，实际结果：%s' % self.cal.sub(3, 2))

    def tearDown(self) -> None:
        self.log.info("--------测试结束---------")


if __name__ == "__main__":
    unittest.main()
