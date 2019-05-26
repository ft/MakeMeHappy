defaultCMakeVersion = "3.1.0"
defaultProjectName = "MakeMeHappy"
defaultLanguages = "C CXX ASM"

def generateHeader(fh):
    for s in ["cmake_minimum_required(VERSION 3.1.0)".format(defaultCMakeVersion),
              "project({} {})".format(defaultProjectName, defaultLanguages)]:
        print(s, file = fh)

def modAppend(fh, p, m):
    print("list(APPEND CMAKE_MODULE_PATH \"{}/{}\")".format(p,m),
          file = fh)

def generateCMakeModulePath(fh, moddirs):
    for (p,ds) in moddirs:
        for d in ds:
            modAppend(fh, p, d)

def generateTestHeader(fh):
    # TODO: Check if it's benign to have this in unconditionally
    print("include(CTest)", file = fh)
    print("enable_testing()", file = fh)

def generateDependencies(fh, deps, thirdParty):
    for dep in deps:
        if (dep in thirdParty):
            print("include({})".format(thirdParty[dep]['module']), file = fh)
            print("{}(deps/{})".format(thirdParty[dep]['include'],
                                       dep),
                  file = fh)
        else:
            print("add_subdirectory(deps/{})".format(dep), file = fh)

def generateFooter(fh):
    print("add_subdirectory(code-under-test)", file = fh)

def generateToplevel(log, cfg, src, trace, mod, fname):
    with open(fname, 'w') as fh:
        generateHeader(fh)
        # TODO: This needs the equivalent for all module carrying dependencies
        # in "deps/".
        moddirs = [ ("${PROJECT_SOURCE_DIR}/code-under-test",
                     [ mod.cmakeModules() ] ) ]
        generateCMakeModulePath(fh, moddirs)
        generateTestHeader(fh)
        tp = mod.cmake3rdParty()
        generateDependencies(fh, trace.deps(), tp)
        generateFooter(fh)
