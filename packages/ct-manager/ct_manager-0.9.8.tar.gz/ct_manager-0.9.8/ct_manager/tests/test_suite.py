# -*- coding: utf-8 -*-

from xutils import (add_parent_path,
                    TestRunner,
                    CustomLogger)

add_parent_path(__file__, 3)
from ct_manager.tests.test_api_function import TestAPI
from ct_manager.tests.test_utils import TestUtils

if __name__ == '__main__':
    logger = CustomLogger('CT_Manager_Test')
    test_runner = TestRunner([TestAPI,
                              TestUtils],
                             logger=logger)
    test_runner.run()
