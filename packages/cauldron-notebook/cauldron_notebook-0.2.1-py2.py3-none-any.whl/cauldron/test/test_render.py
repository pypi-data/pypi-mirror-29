import builtins
import os
from unittest.mock import patch
from datetime import date

import pandas as pd
from cauldron import render
from cauldron.test.support import scaffolds


class TestRender(scaffolds.ResultsTest):
    """ """

    def test_table(self):
        """ should render a table """

        df = pd.DataFrame([
            {'a': 1, 'b': 'hello', 'c': True, 'd': date(2016, 9, 9)},
            {'a': 1, 'b': 'hello', 'c': True, 'd': date(2016, 9, 9)},
            {'a': 1, 'b': 'hello', 'c': True, 'd': date(2016, 9, 9)},
            {'a': 1, 'b': 'hello', 'c': True, 'd': date(2016, 9, 9)}
        ])

        result = render.table(df, 0.5, include_index=True)
        self.assertGreater(len(result), 1)

    def test_listing(self):
        """

        :return:
        """

        result = render.listing([1, 2, 3, 4, 5])
        self.assertGreater(len(result), 1)

        result = render.listing([1, 2, 3, 4, 5], True)
        self.assertGreater(len(result), 1)

    def test_json(self):
        """

        :return:
        """

        data = {'a': 1, 'b': 'hello', 'c': True, 'd': date(2016, 9, 9)}

        result = render.json(hello=data)
        self.assertGreater(len(result), 1)

    def test_html(self):
        """ should render html """

        dom = '<div class="test-me">me</div>'

        result = render.html(dom)
        self.assertGreater(len(result), 1)

    def test_code_block_from_file(self):
        """ should render a block of code from the specified path """

        result = render.code_block(
            path=__file__,
            title='Render Test',
            caption=__file__
        )

        self.assertGreaterEqual(len(result), 1)
        self.assertTrue(result.find('Render Test') != -1)

    def test_code_block_from_string(self):
        """ should render block of code from string argument """

        block = '\n'.join([
            'function add(a, b) {',
            ' return a + b;',
            '}',
            'var test = add(2, 3);',
            'console.log(test);'
        ])

        result = render.code_block(
            block=block,
            title='Render Test JavaScript',
            caption='This is a caption',
            language='js'
        )

        self.assertGreaterEqual(len(result), 1)
        self.assertTrue(result.find('caption') != -1)

    def test_svg(self):
        """ should properly insert arbitrary svg string """

        source = '<svg><circle r="1" cx="1" cy="1"></circle></svg>'

        dom = render.svg(source)
        self.assertGreater(dom.find(source), 0)

    def test_code_block_fail(self):
        """ should fail if the open command does not work properly """

        path = os.path.realpath(__file__)
        with patch('builtins.open') as open_func:
            open_func.side_effect = IOError('Fake Error')
            result = render.code_file(path)

        self.assertEqual(len(result), 0)

    def test_plotly_import_error(self):
        """ should fail if unable to import with plotly """

        real_import = builtins.__import__

        def fake_import(*args, **kwargs):
            if args and args[0] == 'plotly':
                raise ImportError('Fake Error')
            return real_import(*args, **kwargs)

        with patch('builtins.__import__') as import_func:
            import_func.side_effect = fake_import
            result = render.plotly({}, {})

        self.assertGreater(result.find('cd-ImportError'), 0)

    def test_status(self):
        """ should display status of specified data """

        df = pd.DataFrame([
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 1, 'b': 2, 'c': 3}
        ])

        source = dict(
            a=1,
            b=True,
            c='Hello',
            d=(1, 2, 3),
            e=[{'a': 1}, [1, 2, 3], self],
            f=df
        )

        result = render.status(source)
        self.assertGreater(len(result), 0)
