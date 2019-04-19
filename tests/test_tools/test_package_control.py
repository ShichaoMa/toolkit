from toolkit.tools.package_control import change_version


def test_version1(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("___version__ = '0.1.1'\n\n# 测试")

    change_version(3, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "___version__ = '0.1.2'\n\n# 测试"


def test_version2(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1'\n\n# 测试")

    change_version(2, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.2.0'\n\n# 测试"


def test_version3(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1'\n\n# 测试")

    change_version(1, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '1.0.0'\n\n# 测试"


def test_version4(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1d1'\n\n# 测试")

    change_version(3, True, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1.1d2'\n\n# 测试"


def test_version5(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1d'\n\n# 测试")

    change_version(3, True, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1.1d1'\n\n# 测试"


def test_version6(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1'\n\n# 测试")

    change_version(3, True, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1.2dev1'\n\n# 测试"


def test_version7(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1d2'\n\n# 测试")

    change_version(3, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1.1'  \n\n# 测试"


def test_version8(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1d19'\n\n# 测试")

    change_version(3, True, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1.1d20'\n\n# 测试"


def test_version9(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1d20'\n\n# 测试")

    change_version(2, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.2.0'   \n\n# 测试"


def test_version10(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1d19.1'\n\n# 测试")

    change_version(2, True, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1d20.0'\n\n# 测试"


def test_version11(join_root_dir):
    with open(join_root_dir("testdata/__init__.py") , "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1d19.1'\n\n# 测试")

    change_version(3, True, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1d19.2dev1'\n\n# 测试"


def test_version12(join_root_dir):
    with open(join_root_dir("testdata/__init__.py"), "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1d19.1d2'\n\n# 测试")

    change_version(3, True, package_name=join_root_dir("testdata"))

    with open(join_root_dir("testdata/__init__.py"), encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1d19.1d3'\n\n# 测试"
