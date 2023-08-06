from unittest.mock import patch
from unittest.mock import MagicMock

from cauldron.test import support
from cauldron.test.support import scaffolds


class TestRefresh(scaffolds.ResultsTest):
    """ """

    def test_refresh(self):
        """ should refresh """

        r = support.run_command('open @examples:hello_cauldron')
        r = support.run_command('refresh')
        self.assertFalse(r.failed, 'should not have failed')
        self.assertEqual(r.messages[0].code, 'PROJECT_REFRESHED')
        support.run_command('close')

    def test_refresh_no_project(self):
        """ should refresh """

        r = support.run_command('refresh')
        self.assertTrue(r.failed, 'should have failed')
        self.assertEqual(r.errors[0].code, 'NO_OPEN_PROJECT')

        support.run_command('close')

    @patch('cauldron.session.projects.Project.write')
    def test_refresh_write_error(self, project_write: MagicMock):
        """ should refresh """

        project_write.side_effect = IOError('Fake Error')

        support.run_command('open @examples:hello_cauldron')

        r = support.run_command('refresh')
        self.assertTrue(r.failed, 'should have failed')
        self.assertEqual(r.errors[0].code, 'REFRESH_ERROR')

        support.run_command('close')

