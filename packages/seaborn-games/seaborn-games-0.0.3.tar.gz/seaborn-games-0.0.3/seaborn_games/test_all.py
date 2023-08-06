import os, sys, unittest
if sys.version_info[0] == 2:
    import imp
else:
    if sys.version_info[1] < 5:
        from importlib.machinery import SourceFileLoader
    else:
        import importlib.util

IGNORE = ['request_client', 'meta', 'seaborn_table', 'SeabornTable']


def main():
    path = os.path.abspath(__file__).replace('\\', '/').rsplit('/',4)[0]
    print("Searching directory: %s" % path)
    sister_paths = ['%s/%s'%(path, subfolder) for subfolder in os.listdir(path)]
    test_modules = []
    for dir_ in sister_paths:
        if os.path.isdir(dir_ + '/test') and \
                        os.path.split(dir_)[1] not in IGNORE:
            test_modules += [dir_ + '/test/' + i
                            for i in os.listdir(dir_ + '/test') \
                            if 'test' in i and i.endswith('.py')]
            print(dir_)

    modules = []
    for path in test_modules:
        try:
            if sys.version_info[0] == 2:
                modules += [imp.load_source('', path)]
            else:
                if sys.version_info[1] < 5:
                    modules += [SourceFileLoader("", path).load_module()]
                else:
                    spec = importlib.spec_from_file_location('', path)
                    modules += [importlib.util.spec_from_file_location(spec)]
                    spec.loader.exec_module(modules[-1])
        except Exception as ex:
            print("Exception loading module %s with %s"%(path, ex))
        print("Found test:\t\t\t%s" % path)
    suite = unittest.TestSuite()

    for test in test_modules:
        print("Loading tests in:\t%s" % test)
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))
    unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    main()
