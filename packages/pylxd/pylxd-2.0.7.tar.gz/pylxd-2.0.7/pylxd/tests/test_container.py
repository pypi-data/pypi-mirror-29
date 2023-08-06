import json

import mock

from pylxd import container, exceptions
from pylxd.tests import testing


class TestContainer(testing.PyLXDTestCase):
    """Tests for pylxd.container.Container."""

    def test_all(self):
        """A list of all containers are returned."""
        containers = container.Container.all(self.client)

        self.assertEqual(1, len(containers))

    def test_get(self):
        """Return a container."""
        name = 'an-container'

        an_container = container.Container.get(self.client, name)

        self.assertEqual(name, an_container.name)

    def test_get_not_found(self):
        """LXDAPIException is raised when the container doesn't exist."""
        def not_found(request, context):
            context.status_code = 404
            return json.dumps({
                'type': 'error',
                'error': 'Not found',
                'error_code': 404})
        self.add_rule({
            'text': not_found,
            'method': 'GET',
            'url': r'^http://pylxd.test/1.0/containers/an-missing-container$',  # NOQA
        })

        name = 'an-missing-container'

        self.assertRaises(
            exceptions.LXDAPIException,
            container.Container.get, self.client, name)

    def test_get_error(self):
        """LXDAPIException is raised when the LXD API errors."""
        def not_found(request, context):
            context.status_code = 500
            return json.dumps({
                'type': 'error',
                'error': 'Not found',
                'error_code': 500})
        self.add_rule({
            'text': not_found,
            'method': 'GET',
            'url': r'^http://pylxd.test/1.0/containers/an-missing-container$',  # NOQA
        })

        name = 'an-missing-container'

        self.assertRaises(
            exceptions.LXDAPIException,
            container.Container.get, self.client, name)

    def test_create(self):
        """A new container is created."""
        config = {'name': 'an-new-container'}

        an_new_container = container.Container.create(
            self.client, config, wait=True)

        self.assertEqual(config['name'], an_new_container.name)

    def test_fetch(self):
        """A sync updates the properties of a container."""
        an_container = container.Container(
            self.client, name='an-container')

        an_container.sync()

        self.assertTrue(an_container.ephemeral)

    def test_fetch_not_found(self):
        """LXDAPIException is raised on a 404 for updating container."""
        def not_found(request, context):
            context.status_code = 404
            return json.dumps({
                'type': 'error',
                'error': 'Not found',
                'error_code': 404})
        self.add_rule({
            'text': not_found,
            'method': 'GET',
            'url': r'^http://pylxd.test/1.0/containers/an-missing-container$',  # NOQA
        })

        an_container = container.Container(
            self.client, name='an-missing-container')

        self.assertRaises(exceptions.LXDAPIException, an_container.sync)

    def test_fetch_error(self):
        """LXDAPIException is raised on error."""
        def not_found(request, context):
            context.status_code = 500
            return json.dumps({
                'type': 'error',
                'error': 'An bad error',
                'error_code': 500})
        self.add_rule({
            'text': not_found,
            'method': 'GET',
            'url': r'^http://pylxd.test/1.0/containers/an-missing-container$',  # NOQA
        })

        an_container = container.Container(
            self.client, name='an-missing-container')

        self.assertRaises(exceptions.LXDAPIException, an_container.sync)

    def test_update(self):
        """A container is updated."""
        an_container = container.Container(
            self.client, name='an-container')
        an_container.architecture = 1
        an_container.config = {}
        an_container.created_at = 1
        an_container.devices = {}
        an_container.ephemeral = 1
        an_container.expanded_config = {}
        an_container.expanded_devices = {}
        an_container.profiles = 1
        an_container.status = 1

        an_container.save(wait=True)

        self.assertTrue(an_container.ephemeral)

    def test_rename(self):
        an_container = container.Container(
            self.client, name='an-container')

        an_container.rename('an-renamed-container', wait=True)

        self.assertEqual('an-renamed-container', an_container.name)

    def test_delete(self):
        """A container is deleted."""
        # XXX: rockstar (21 May 2016) - This just executes
        # a code path. There should be an assertion here, but
        # it's not clear how to assert that, just yet.
        an_container = container.Container(
            self.client, name='an-container')

        an_container.delete(wait=True)

    @testing.requires_ws4py
    @mock.patch('pylxd.container._StdinWebsocket')
    @mock.patch('pylxd.container._CommandWebsocketClient')
    def test_execute(self, _CommandWebsocketClient, _StdinWebsocket):
        """A command is executed on a container."""
        fake_websocket = mock.Mock()
        fake_websocket.data = 'test\n'
        _StdinWebsocket.return_value = fake_websocket
        _CommandWebsocketClient.return_value = fake_websocket

        an_container = container.Container(
            self.client, name='an-container')

        stdout, _ = an_container.execute(['echo', 'test'])

        self.assertEqual('test\n', stdout)

    def test_execute_no_ws4py(self):
        """If ws4py is not installed, ValueError is raised."""
        from pylxd import container
        old_installed = container._ws4py_installed
        container._ws4py_installed = False

        def cleanup():
            container._ws4py_installed = old_installed
        self.addCleanup(cleanup)

        an_container = container.Container(
            self.client, name='an-container')

        self.assertRaises(ValueError, an_container.execute, ['echo', 'test'])

    @testing.requires_ws4py
    def test_execute_string(self):
        """A command passed as string raises a TypeError."""
        an_container = container.Container(
            self.client, name='an-container')

        self.assertRaises(TypeError, an_container.execute, 'apt-get update')

    def test_migrate(self):
        """A container is migrated."""
        from pylxd.client import Client

        client2 = Client(endpoint='http://pylxd2.test')
        an_container = container.Container(
            self.client, name='an-container')

        an_migrated_container = an_container.migrate(client2)

        self.assertEqual('an-container', an_migrated_container.name)
        self.assertEqual(client2, an_migrated_container.client)

    def test_publish(self):
        """Containers can be published."""
        self.add_rule({
            'text': json.dumps({
                'type': 'sync',
                'metadata': {
                    'id': 'operation-abc',
                    'metadata': {
                        'fingerprint': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'  # NOQA
                        }
                    }
                }),
            'method': 'GET',
            'url': r'^http://pylxd.test/1.0/operations/operation-abc$',
        })

        an_container = container.Container(
            self.client, name='an-container')

        image = an_container.publish(wait=True)

        self.assertEqual(
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            image.fingerprint)


class TestContainerState(testing.PyLXDTestCase):
    """Tests for pylxd.container.ContainerState."""

    def test_get(self):
        """Return a container."""
        name = 'an-container'

        an_container = container.Container.get(self.client, name)
        state = an_container.state()

        self.assertEqual('Running', state.status)
        self.assertEqual(103, state.status_code)

    def test_start(self):
        """A container is started."""
        an_container = container.Container.get(self.client, 'an-container')

        an_container.start(wait=True)

    def test_stop(self):
        """A container is stopped."""
        an_container = container.Container.get(self.client, 'an-container')

        an_container.stop()

    def test_restart(self):
        """A container is restarted."""
        an_container = container.Container.get(self.client, 'an-container')

        an_container.restart()

    def test_freeze(self):
        """A container is suspended."""
        an_container = container.Container.get(self.client, 'an-container')

        an_container.freeze()

    def test_unfreeze(self):
        """A container is resumed."""
        an_container = container.Container.get(self.client, 'an-container')

        an_container.unfreeze()


class TestContainerSnapshots(testing.PyLXDTestCase):
    """Tests for pylxd.container.Container.snapshots."""

    def setUp(self):
        super(TestContainerSnapshots, self).setUp()
        self.container = container.Container.get(self.client, 'an-container')

    def test_get(self):
        """Return a specific snapshot."""
        snapshot = self.container.snapshots.get('an-snapshot')

        self.assertEqual('an-snapshot', snapshot.name)

    def test_all(self):
        """Return all snapshots."""
        snapshots = self.container.snapshots.all()

        self.assertEqual(1, len(snapshots))
        self.assertEqual('an-snapshot', snapshots[0].name)
        self.assertEqual(self.client, snapshots[0].client)
        self.assertEqual(self.container, snapshots[0].container)

    def test_create(self):
        """Create a snapshot."""
        snapshot = self.container.snapshots.create(
            'an-snapshot', stateful=True, wait=True)

        self.assertEqual('an-snapshot', snapshot.name)


class TestSnapshot(testing.PyLXDTestCase):
    """Tests for pylxd.container.Snapshot."""

    def setUp(self):
        super(TestSnapshot, self).setUp()
        self.container = container.Container.get(self.client, 'an-container')

    def test_rename(self):
        """A snapshot is renamed."""
        snapshot = container.Snapshot(
            self.client, container=self.container,
            name='an-snapshot')

        snapshot.rename('an-renamed-snapshot', wait=True)

        self.assertEqual('an-renamed-snapshot', snapshot.name)

    def test_delete(self):
        """A snapshot is deleted."""
        snapshot = container.Snapshot(
            self.client, container=self.container,
            name='an-snapshot')

        snapshot.delete(wait=True)

        # TODO: add an assertion here

    def test_delete_failure(self):
        """If the response indicates delete failure, raise an exception."""
        def not_found(request, context):
            context.status_code = 404
            return json.dumps({
                'type': 'error',
                'error': 'Not found',
                'error_code': 404})
        self.add_rule({
            'text': not_found,
            'method': 'DELETE',
            'url': r'^http://pylxd.test/1.0/containers/an-container/snapshots/an-snapshot$',  # NOQA
        })

        snapshot = container.Snapshot(
            self.client, container=self.container,
            name='an-snapshot')

        self.assertRaises(exceptions.LXDAPIException, snapshot.delete)

    def test_publish(self):
        """Snapshots can be published."""
        self.add_rule({
            'text': json.dumps({
                'type': 'sync',
                'metadata': {
                    'id': 'operation-abc',
                    'metadata': {
                        'fingerprint': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'  # NOQA
                        }
                    }
                }),
            'method': 'GET',
            'url': r'^http://pylxd.test/1.0/operations/operation-abc$',
        })

        snapshot = container.Snapshot(
            self.client, container=self.container,
            name='an-snapshot')

        image = snapshot.publish(wait=True)

        self.assertEqual(
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            image.fingerprint)


class TestFiles(testing.PyLXDTestCase):
    """Tests for pylxd.container.Container.files."""

    def setUp(self):
        super(TestFiles, self).setUp()
        self.container = container.Container.get(self.client, 'an-container')

    def test_put(self):
        """A file is put on the container."""
        data = 'The quick brown fox'

        self.container.files.put('/tmp/putted', data)

        # TODO: Add an assertion here

    def test_get(self):
        """A file is retrieved from the container."""
        data = self.container.files.get('/tmp/getted')

        self.assertEqual(b'This is a getted file', data)

    def test_get_not_found(self):
        """LXDAPIException is raised on bogus filenames."""
        def not_found(request, context):
            context.status_code = 500
        rule = {
            'text': not_found,
            'method': 'GET',
            'url': r'^http://pylxd.test/1.0/containers/an-container/files\?path=%2Ftmp%2Fgetted$',  # NOQA
        }
        self.add_rule(rule)

        self.assertRaises(
            exceptions.LXDAPIException,
            self.container.files.get, '/tmp/getted')

    def test_get_error(self):
        """LXDAPIException is raised on error."""
        def not_found(request, context):
            context.status_code = 503
        rule = {
            'text': not_found,
            'method': 'GET',
            'url': r'^http://pylxd.test/1.0/containers/an-container/files\?path=%2Ftmp%2Fgetted$',  # NOQA
        }
        self.add_rule(rule)

        self.assertRaises(
            exceptions.LXDAPIException,
            self.container.files.get, '/tmp/getted')
