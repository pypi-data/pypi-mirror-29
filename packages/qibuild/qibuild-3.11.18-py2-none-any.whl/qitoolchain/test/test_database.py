# Copyright (c) 2012-2018 SoftBank Robotics. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the COPYING file.
import os

import mock

import qisys.archive
import qitoolchain.database
import qitoolchain.qipackage
import qitoolchain.svn_package
import qitoolchain.feed

from qisrc.test.conftest import git_server, svn_server  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name


def test_persistent(toolchain_db):
    foo_package = qitoolchain.qipackage.QiPackage("foo", version="1.3")
    foo_package.path = "/path/to/foo"
    toolchain_db.add_package(foo_package)
    toolchain_db.save()
    db2 = qitoolchain.database.DataBase("bar", toolchain_db.db_path)
    actual_package = db2.packages["foo"]
    assert actual_package == foo_package


def test_adding_same_package_twice(toolchain_db):
    foo_package = qitoolchain.qipackage.QiPackage("foo", version="1.3")
    foo_package.path = "/path/to/foo"
    toolchain_db.add_package(foo_package)
    toolchain_db.add_package(foo_package)
    assert len(toolchain_db.packages) == 1


def test_update(toolchain_db, feed):
    boost_package = qitoolchain.qipackage.QiPackage("boost", version="1.42")
    boost_package.path = "/path/to/boost"
    feed.add_package(boost_package)

    toolchain_db.update(feed.url)
    assert toolchain_db.packages["boost"] == boost_package

    new_boost_package = qitoolchain.qipackage.QiPackage("boost", version="1.44")
    new_boost_package.path = "/path/to/boost"
    feed.add_package(new_boost_package)
    toolchain_db.update(feed.url)
    assert toolchain_db.packages["boost"] == new_boost_package


def test_downloads_remote_package(toolchain_db, feed):
    boost_package = qitoolchain.qipackage.QiPackage("boost", version="1.42")
    feed.add_package(boost_package, with_path=False, with_url=True)

    toolchain_db.update(feed.url)
    assert toolchain_db.packages["boost"].path


def test_downloads_only_once(toolchain_db, feed):
    boost_package = qitoolchain.qipackage.QiPackage("boost", version="1.42")
    feed.add_package(boost_package, with_path=False, with_url=True)
    with mock.patch.object(qisys.remote, "download") as mock_dl:
        with mock.patch.object(qitoolchain.qipackage, "extract") as mock_extract:
            mock_dl.return_value = "/path/to/boost.zip"
            toolchain_db.update(feed.url)
            toolchain_db.update(feed.url)
    assert mock_dl.call_count == 1
    assert mock_extract.call_count == 1
    assert mock_extract.call_args_list[0][0][0] == "/path/to/boost.zip"


def test_package_removed_from_feed(toolchain_db, feed):
    boost_package = qitoolchain.qipackage.QiPackage("boost", version="1.42")
    feed.add_package(boost_package)
    toolchain_db.update(feed.url)
    boost_path = toolchain_db.get_package_path("boost")

    feed.remove_package("boost")
    toolchain_db.update(feed.url)
    assert not toolchain_db.packages
    assert not os.path.exists(boost_path)


def test_downgrading_package(toolchain_db, feed):
    boost_package = qitoolchain.qipackage.QiPackage("boost", version="1.44")
    feed.add_package(boost_package)

    toolchain_db.update(feed.url)
    assert toolchain_db.packages["boost"] == boost_package

    feed.remove_package("boost")
    old_boost_package = qitoolchain.qipackage.QiPackage("boost", version="1.42")
    feed.add_package(old_boost_package)
    toolchain_db.update(feed.url)
    assert toolchain_db.packages["boost"] == old_boost_package


def test_solve_deps(toolchain_db, tmpdir):
    bar_path = tmpdir.ensure("bar", dir=True)
    bar_path.join("package.xml").write("""
<package name="bar">
  <depends buildtime="true" names="foo" />
</package>
""")
    foo_path = tmpdir.ensure("foo", dir=True)
    bar_package = qitoolchain.qipackage.QiPackage("bar")
    bar_package.path = bar_path.strpath
    foo_package = qitoolchain.qipackage.QiPackage("foo")
    foo_package.path = foo_path.strpath
    toolchain_db.add_package(bar_package)
    toolchain_db.add_package(foo_package)
    res = toolchain_db.solve_deps([bar_package], dep_types=["build"])
    assert res == [foo_package, bar_package]


def test_git_feed(toolchain_db, feed, git_server):  # pylint: disable=unused-argument
    boost_package = qitoolchain.qipackage.QiPackage("boost", version="1.44")
    feed.add_package(boost_package)
    git_server.create_repo("toolchains.git")
    git_server.push_file("toolchains.git", "feeds/foo.xml", feed.feed_xml.read())
    url = git_server.get_repo("toolchains.git").clone_url

    toolchain = qitoolchain.toolchain.Toolchain("foo")
    toolchain.update(url, branch="master", name="foo")
    boost = toolchain.get_package("boost")
    assert boost.version == "1.44"

    new_boost_package = qitoolchain.qipackage.QiPackage("boost", version="1.55")
    feed.add_package(new_boost_package)
    git_server.push_file("toolchains.git", "feeds/foo.xml", feed.feed_xml.read())

    toolchain.update()
    boost = toolchain.get_package("boost")
    assert boost.version == "1.55"


def test_svn_package_conflict(toolchain_db, feed, svn_server):  # pylint: disable=unused-argument
    boost_package = qitoolchain.qipackage.QiPackage("boost", version="1.44")
    feed.add_package(boost_package)

    toolchain = qitoolchain.toolchain.Toolchain("foo")
    toolchain.update(feed.url)

    boost_url = svn_server.create_repo("boost")
    svn_server.commit_file("boost", "version.hpp", '#define BOOST_VERSION "1_55"\n')
    svn_package = qitoolchain.svn_package.SvnPackage("boost")
    svn_package.url = boost_url
    feed.add_svn_package(svn_package)

    toolchain.update(feed.url)


def test_package_with_flags(tmpdir, toolchain_db):
    feed = tmpdir.join("feed.xml")
    x_tools = tmpdir.join("x-tools")
    x_tools.ensure("sysroot", dir=True)
    x_tools.join("toolchain.cmake").ensure(file=True)
    x_tools.join("package.xml").write("""
<package name="x_tools" version="0.1" toolchain_file="toolchain.cmake" />
""")
    x_tools_package = tmpdir.join("x-tools-0.1.zip")
    qisys.archive.compress(x_tools.strpath, output=x_tools_package.strpath, flat=True)
    feed.write("""
<toolchain>
  <package name="x-tools" version="0.1" url="{url}" />
</toolchain>
""".format(url="file://" + x_tools_package.strpath))
    toolchain_db.update(feed.strpath)

    x_tools_in_db = toolchain_db.get_package("x-tools")
    assert x_tools_in_db.toolchain_file


def test_post_add(tmpdir, toolchain_db):
    boost = tmpdir.mkdir("boost")
    script = boost.join("post-add.sh")
    script.write(
        '#!/bin/sh\n'
        'echo $@ > foobar\n'
    )
    os.chmod(script.strpath, 0755)

    boost_package = tmpdir.join("boost-1.58.zip")
    qisys.archive.compress(boost.strpath, output=boost_package.strpath)

    feed = tmpdir.join("feed.xml")
    feed.write("""
<toolchain>
  <package name="boost" version="1.58" url="{url}" post-add="post-add.sh hello world" />
</toolchain>
""".format(url="file://" + boost_package.strpath))

    print boost.strpath
    print script.strpath
    print boost_package.strpath
    print feed.strpath

    toolchain_db.update(feed.strpath)

    boost_in_db = toolchain_db.get_package("boost")
    with open(os.path.join(boost_in_db.path, 'foobar')) as f:
        txt = f.read()

    assert "hello world" in txt
