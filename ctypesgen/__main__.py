"""
Command-line interface for ctypesgen
"""

import argparse

from ctypesgen import (
    messages as msgs,
    options as core_options,
    parser as core_parser,
    printer_python,
    printer_json,
    processor,
    version,
)


def find_names_in_modules(modules):
    names = set()
    for module in modules:
        try:
            mod = __import__(module)
        except Exception:
            pass
        else:
            names.update(dir(mod))
    return names


def main(givenargs=None):
    # TODO(geisserml) In the future, convert action="append" to nargs="*" - that's nicer to use

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=version.VERSION_NUMBER,
    )

    # Parameters
    parser.add_argument("headers", nargs="+", help="Sequence of header files")
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="write wrapper to FILE [default stdout]",
    )
    parser.add_argument(
        "-l",
        "--library",
        dest="libraries",
        action="append",
        default=[],
        metavar="LIBRARY",
        help="link to LIBRARY",
    )
    parser.add_argument(
        "--include",
        dest="other_headers",
        action="append",
        default=[],
        metavar="HEADER",
        help="include system header HEADER (e.g. stdio.h or stdlib.h)",
    )
    parser.add_argument(
        "-m",
        "--module",
        "--link-module",
        action="append",
        dest="modules",
        metavar="MODULE",
        default=[],
        help="use symbols from Python module MODULE",
    )
    parser.add_argument(
        "-I",
        "--includedir",
        action="append",
        dest="include_search_paths",
        default=[],
        metavar="INCLUDEDIR",
        help="add INCLUDEDIR as a directory to search for headers",
    )
    parser.add_argument(
        "-L",
        "-R",
        "--rpath",
        "--libdir",
        action="append",
        dest="universal_libdirs",
        default=[],
        metavar="LIBDIR",
        help="Add LIBDIR to the search path (both compile-time and run-time)",
    )
    parser.add_argument(
        "--compile-libdir",
        action="append",
        dest="compile_libdirs",
        metavar="LIBDIR",
        default=[],
        help="Add LIBDIR to the compile-time library search path.",
    )
    parser.add_argument(
        "--runtime-libdir",
        action="append",
        dest="runtime_libdirs",
        metavar="LIBDIR",
        default=[],
        help="Add LIBDIR to the run-time library search path.",
    )
    parser.add_argument(
        "--no-embed-preamble",
        action="store_false",
        dest="embed_preamble",
        default=True,
        help="Do not embed preamble and loader in output file. "
        "Defining --output as a file and --output-language to "
        "Python is a prerequisite.",
    )

    # Parser options
    parser.add_argument(
        "--cpp",
        dest="cpp",
        default="gcc -E",
        help="The command to invoke the c preprocessor, including any "
        "necessary options (default: gcc -E)",
    )
    parser.add_argument(
        "--allow-gnu-c",
        action="store_true",
        dest="allow_gnu_c",
        default=False,
        help="Specify whether to undefine the '__GNUC__' macro, "
        "while invoking the C preprocessor.\n"
        "(default: False. i.e. ctypesgen adds an implicit undefine using '-U __GNUC__'.)\n"
        "Specify this flag to avoid ctypesgen undefining '__GNUC__' as shown above.",
    )
    parser.add_argument(
        "-D",
        "--define",
        action="append",
        dest="cpp_defines",
        metavar="MACRO",
        default=[],
        help="Add a definition to the preprocessor via commandline",
    )
    parser.add_argument(
        "-U",
        "--undefine",
        action="append",
        dest="cpp_undefines",
        metavar="NAME",
        default=[],
        help="Instruct the preprocessor to undefine the specified macro via commandline",
    )
    parser.add_argument(
        "--save-preprocessed-headers",
        metavar="FILENAME",
        dest="save_preprocessed_headers",
        default=None,
        help="Save the preprocessed headers to the specified FILENAME",
    )
    parser.add_argument(
        "--optimize-lexer",
        dest="optimize_lexer",
        action="store_true",
        default=False,
        help="Run the lexer in optimized mode.  This mode requires write "
        "access to lextab.py file stored within the ctypesgen package.",
    )

    # Processor options
    parser.add_argument(
        "-a",
        "--all-headers",
        action="store_true",
        dest="all_headers",
        default=False,
        help="include symbols from all headers, including system headers",
    )
    parser.add_argument(
        "--builtin-symbols",
        action="store_true",
        dest="builtin_symbols",
        default=False,
        help="include symbols automatically generated by the preprocessor",
    )
    parser.add_argument(
        "--no-macros",
        action="store_false",
        dest="include_macros",
        default=True,
        help="Don't output macros.",
    )
    parser.add_argument(
        "--no-undefs",
        action="store_false",
        dest="include_undefs",
        default=True,
        help="Do not remove macro definitions as per #undef directives",
    )
    parser.add_argument(
        "-i",
        "--include-symbols",
        action="append",
        dest="include_symbols",
        metavar="REGEXPR",
        default=[],
        help="Regular expression for symbols to always include.  Multiple "
        "instances of this option will be combined into a single expression "
        "doing something like '(expr1|expr2|expr3)'.",
    )
    parser.add_argument(
        "-x",
        "--exclude-symbols",
        action="append",
        dest="exclude_symbols",
        metavar="REGEXPR",
        default=[],
        help="Regular expression for symbols to exclude.  Multiple instances "
        "of this option will be combined into a single expression doing "
        "something like '(expr1|expr2|expr3)'.",
    )
    parser.add_argument(
        "--no-stddef-types",
        action="store_true",
        dest="no_stddef_types",
        default=False,
        help="Do not support extra C types from stddef.h",
    )
    parser.add_argument(
        "--no-gnu-types",
        action="store_true",
        dest="no_gnu_types",
        default=False,
        help="Do not support extra GNU C types",
    )
    parser.add_argument(
        "--no-python-types",
        action="store_true",
        dest="no_python_types",
        default=False,
        help="Do not support extra C types built in to Python",
    )
    parser.add_argument(
        "--no-load-library",
        action="store_true",
        dest="no_load_library",
        default=False,
        help="Do not try to load library during the processing",
    )

    # Printer options
    parser.add_argument(
        "--header-template",
        dest="header_template",
        default=None,
        metavar="TEMPLATE",
        help="Use TEMPLATE as the header template in the output file.",
    )
    parser.add_argument(
        "--strip-build-path",
        dest="strip_build_path",
        default=None,
        metavar="BUILD_PATH",
        help="Strip build path from header paths in the wrapper file.",
    )
    parser.add_argument(
        "--insert-file",
        dest="inserted_files",
        default=[],
        action="append",
        metavar="FILENAME",
        help="Add the contents of FILENAME to the end of the wrapper file.",
    )
    parser.add_argument(
        "--output-language",
        dest="output_language",
        metavar="LANGUAGE",
        default="py",
        choices=("py", "json"),
        help="Choose output language",
    )
    parser.add_argument(
        "-P",
        "--strip-prefix",
        dest="strip_prefixes",
        default=[],
        action="append",
        metavar="REGEXPR",
        help="Regular expression to match prefix to strip from all symbols.  "
        "Multiple instances of this option will be combined into a single "
        "expression doing something like '(expr1|expr2|expr3)'.",
    )

    # Error options
    parser.add_argument(
        "--all-errors",
        action="store_true",
        default=False,
        dest="show_all_errors",
        help="Display all warnings and errors even if they would not affect output.",
    )
    parser.add_argument(
        "--show-long-errors",
        action="store_true",
        default=False,
        dest="show_long_errors",
        help="Display long error messages instead of abbreviating error messages.",
    )
    parser.add_argument(
        "--no-macro-warnings",
        action="store_false",
        default=True,
        dest="show_macro_warnings",
        help="Do not print macro warnings.",
    )
    parser.add_argument(
        "--debug-level",
        dest="debug_level",
        default=0,
        type=int,
        help="Run ctypesgen with specified debug level (also applies to yacc parser)",
    )
    parser.add_argument(
        "--no-macro-try-except",
        action="store_false",
        default=True,
        dest="use_macro_try_except",
        help="Do not use try-except for macros.",
    )
    parser.add_argument(
        "--no-source-comments",
        action="store_false",
        default=True,
        dest="print_source_comments",
        help="Do not include source file comments.",
    )

    parser.set_defaults(**core_options.default_values)
    args = parser.parse_args(givenargs)

    # Important: don't use +=, it modifies the original list instead of
    # creating a new one. This can be problematic with repeated API calls.
    args.compile_libdirs = args.compile_libdirs + args.universal_libdirs
    args.runtime_libdirs = args.runtime_libdirs + args.universal_libdirs

    # Figure out what names will be defined by imported Python modules
    args.other_known_names = find_names_in_modules(args.modules)

    if len(args.libraries) == 0:
        msgs.warning_message("No libraries specified", cls="usage")

    # Fetch printer for the requested output language
    if args.output_language == "py":
        printer = printer_python.WrapperPrinter
    elif args.output_language == "json":
        printer = printer_json.WrapperPrinter
    else:
        assert False  # handled by argparse choices

    # Step 1: Parse
    descriptions = core_parser.parse(args.headers, args)

    # Step 2: Process
    processor.process(descriptions, args)

    # Step 3: Print
    printer(args.output, args, descriptions)

    msgs.status_message("Wrapping complete.")

    # Correct what may be a common mistake
    if descriptions.all == []:
        if not args.all_headers:
            msgs.warning_message(
                "There wasn't anything of use in the "
                "specified header file(s). Perhaps you meant to run with "
                "--all-headers to include objects from included sub-headers? ",
                cls="usage",
            )


if __name__ == "__main__":
    main()
