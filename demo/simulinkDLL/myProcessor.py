from ctypesgen.processor.pipeline import *
from typing import Sequence
from argparse import *


class MyProcessor(object):
    def __init__(self, options: Namespace(), data: Sequence[str]):
        # super().__init__(data, options)

        if data is not None:
            self.data = data
        else:
            self.data = Sequence[str]

        if options is not None:
            self.options = options
        else:
            self.options = Sequence[str]

    def options(self):
        return self.options

    def process(self):
        status_message("Processing description list.")

        find_dependencies(self.data, self.options)

        automatically_typedef_structs(self.data, self.options)
        remove_NULL(self.data, self.options)
        remove_descriptions_in_system_headers(self.data, self.options)
        filter_by_regexes_exclude(self.data, self.options)
        filter_by_regexes_include(self.data, self.options)
        remove_macros(self.data, self.options)
        if self.options.output_language == "python":
            # this function is python specific
            fix_conflicting_names(self.data, self.options)
        find_source_libraries(self.data, self.options)

        self.calculate_final_inclusion()
        self.print_errors_encountered()
        self.calculate_final_inclusion()

    def can_include_desc(self, desc):
        if desc.can_include is None:
            if desc.include_rule == "no":
                desc.can_include = False
            elif desc.include_rule == "yes" or desc.include_rule == "if_needed":
                desc.can_include = True
                for req in desc.requirements:
                    if not self.can_include_desc(req):
                        desc.can_include = False
        return desc.can_include

    def do_include_desc(self, desc):
        if desc.included:
            return  # We've already been here
        desc.included = True
        for req in desc.requirements:
            self.do_include_desc(req)

    def calculate_final_inclusion(self):
        """Calculates which descriptions will be included in the output library.

        An object with include_rule="never" is never included.
        An object with include_rule="yes" is included if its requirements can be included.
        An object with include_rule="if_needed" is included if an object to be included
            requires it and if its requirements can be included.
        """
        for desc in self.data.all:
            desc.can_include = None  # None means "Not Yet Decided"
            desc.included = False

        for desc in self.data.all:
            if desc.include_rule == "yes":
                if self.can_include_desc(desc):
                    self.do_include_desc(desc)

    # noinspection PyMethodMayBeStatic
    def print_errors_encountered(self):
        # See descriptions.py for an explanation of the error-handling mechanism
        for desc in self.data.all:
            # If description have not been included, don't bother user by
            # printing warnings.
            if desc.included or self.options.show_all_errors:
                if self.options.show_long_errors or len(desc.errors) + len(desc.warnings) <= 2:
                    for error, cls in desc.errors:
                        # Macro errors will always be displayed as warnings.
                        if isinstance(desc, MacroDescription):
                            if self.options.show_macro_warnings:
                                warning_message(error, cls)
                        else:
                            error_message(error, cls)
                    for warning, cls in desc.warnings:
                        warning_message(warning, cls)

                else:
                    if desc.errors:
                        error1, cls1 = desc.errors[0]
                        error_message(error1, cls1)
                        num_errs = len(desc.errors) - 1
                        num_warns = len(desc.warnings)
                        if num_warns:
                            error_message(
                                "%d more errors and %d more warnings "
                                "for %s" % (num_errs, num_warns, desc.casual_name())
                            )
                        else:
                            error_message("%d more errors for %s " % (num_errs, desc.casual_name()))
                    else:
                        warning1, cls1 = desc.warnings[0]
                        warning_message(warning1, cls1)
                        warning_message(
                            "%d more errors for %s" % (len(desc.warnings) - 1, desc.casual_name())
                        )
            if desc.errors:
                # process() will recalculate to take this into account
                desc.include_rule = "never"
