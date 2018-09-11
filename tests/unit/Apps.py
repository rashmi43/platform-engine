# -*- coding: utf-8 -*-
import asyncio
import select

from asyncy.Sentry import Sentry
import psycopg2
import pytest

from pytest import fixture, mark

from asyncy.Apps import Apps


@fixture
def exc():
    def foo(*args, **kwargs):
        raise Exception()

    return foo

@fixture
def db(patch, magic):
    def get():
        db = magic()
        patch.object(psycopg2, 'connect', return_value=db)
        return db

    return get


def test_listen_to_releases(patch, db, magic, config, logger, exc):
    conn = db()

    patch.object(asyncio, 'run_coroutine_threadsafe', side_effect=exc)
    patch.object(select, 'select', return_value=[([], [], []), ([], [], []),
                                                 False])
    patch.object(Apps, 'reload_app')
    notif = magic()
    notif.payload = 'app_id'
    conn.notifies = [notif]
    loop = magic()

    with pytest.raises(Exception):
        Apps.listen_to_releases(config, logger, loop)

    conn.cursor().execute.assert_called_with('listen release;')
    Apps.reload_app.assert_called_with(config, logger, 'app_id')
    conn.set_isolation_level.assert_called_with(
        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    asyncio.run_coroutine_threadsafe.assert_called_with(
        Apps.reload_app(), loop)


@mark.asyncio
async def test_destroy_all(patch, async_mock, magic):
    app = magic()
    app.destroy = async_mock()
    Apps.apps = {'app_id': app}
    app.app_id = 'app_id'
    await Apps.destroy_all()
    app.destroy.mock.assert_called()
    assert Apps.apps['app_id'] is None


@mark.parametrize('raise_error', [True, False])
@mark.asyncio
async def test_reload_app(patch, config, logger, db, async_mock,
                          magic, exc, raise_error):
    conn = db()
    old_app = magic()
    app_id = 'app_id'
    Apps.apps = {app_id: old_app}
    patch.object(Sentry, 'capture_exc')

    patch.object(Apps, 'destroy_app', new=async_mock())
    if raise_error:
        patch.object(Apps, 'deploy_release', new=async_mock(side_effect=exc))
    else:
        patch.object(Apps, 'deploy_release', new=async_mock())

    release = ['app_id', 'version', 'env', 'stories', 'maintenance']
    conn.cursor().fetchone.return_value = release

    await Apps.reload_app(config, logger, app_id)

    Apps.destroy_app.mock.assert_called_with(old_app, silent=True)
    Apps.deploy_release.mock.assert_called_with(
        config, logger, app_id,
        release[1], release[2], release[3], release[4])

    if raise_error:
        logger.error.assert_called()
        Sentry.capture_exc.assert_called()
    else:
        logger.error.assert_not_called()


@mark.parametrize('silent', [False, True])
@mark.asyncio
async def test_destroy_app_exc(patch, async_mock, magic, exc, silent):
    app = magic()
    app.destroy = async_mock(side_effect=exc)

    if silent:
        await Apps.destroy_app(app, silent)
    else:
        with pytest.raises(Exception):
            await Apps.destroy_app(app, silent)

    app.destroy.mock.assert_called()
