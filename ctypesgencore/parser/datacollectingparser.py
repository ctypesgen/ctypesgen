#!/usr/bin/env python

"""
DataCollectingParser subclasses ctypesparser.CtypesParser and builds Description
objects from the CtypesType objects and other information from CtypesParser.
After parsing is complete, a DescriptionCollection object can be retrieved by
calling DataCollectingParser.data(). 
"""

import ctypesparser
from ctypesgencore.descriptions import *
from ctypesgencore.ctypedescs import *
from ctypesgencore.expressions import *
from ctypesgencore.messages import *
from tempfile import NamedTemporaryFile

class DataCollectingParser(ctypesparser.CtypesParser,
                           ctypesparser.CtypesTypeVisitor):
    """Main class for the Parser component. Steps for use:
    p=DataCollectingParser(names_of_header_files,options)
    p.parse()
    data=p.data() #A dictionary of constants, enums, structs, functions, etc.
    """
    def __init__(self,headers,options):
        ctypesparser.CtypesParser.__init__(self,options)
        self.headers=headers
        self.options=options
        
        self.constants=[]
        self.typedefs=[]
        self.structs=[]
        self.enums=[]
        self.functions=[]
        self.variables=[]
        self.macros=[]
        
        self.all=[]
        self.output_order=[]
        
        # NULL is a useful macro to have defined
        null = ConstantExpressionNode(None)
        nullmacro = ConstantDescription("NULL",null,("<built-in>",1))
        self.constants.append(nullmacro)
        self.all.append(nullmacro)
        self.output_order.append(("constant", nullmacro))
        
        # A list of tuples describing macros; saved to be processed after
        # everything else has been parsed
        self.saved_macros = []
        # A set of structs that are already known
        self.already_seen_structs=set() 
        # A dict of structs that have only been seen in opaque form
        self.already_seen_opaque_structs={} 
        # A set of enums that are already known
        self.already_seen_enums=set() 
        # A dict of enums that have only been seen in opaque form
        self.already_seen_opaque_enums={}
            
    def parse(self):
        f = NamedTemporaryFile(suffix=".h")
        for header in self.options.other_headers:
            print >>f, '#include <%s>' % header
        for header in self.headers:
            print >>f, '#include "%s"' % header
        f.flush()
        ctypesparser.CtypesParser.parse(self,f.name,None)
        f.close()
        
        for name, params, expr, (filename,lineno) in self.saved_macros:
            self.handle_macro(name, params, expr, filename, lineno)
            
    def handle_define_constant(self, name, expr, filename, lineno):
        # Called by CParser
        # Save to handle later
        self.saved_macros.append((name, None, expr, (filename, lineno)))
    
    def handle_define_unparseable(self, name, params, value, filename, lineno):
        # Called by CParser
        if params:
            original_string = "#define %s(%s) %s" % \
                (name, ",".join(params), " ".join(value))
        else:
            original_string = "#define %s %s" % \
                (name, " ".join(value))
        macro = MacroDescription(name, params, original_string,
                                 src = (filename,lineno))
        macro.error("Could not parse macro \"%s\"" % original_string,
                    cls = 'macro')
        self.macros.append(macro)
        self.all.append(macro)
        self.output_order.append(('macro',macro))
    
    def handle_define_macro(self, name, params, expr, filename, lineno):
        # Called by CParser
        # Save to handle later
        self.saved_macros.append((name, params, expr, (filename,lineno)))
    
    def handle_ctypes_typedef(self, name, ctype, filename, lineno):
        # Called by CtypesParser
        ctype.visit(self)
        
        requirements,unresolvables,errors=self.walk_cobject(ctype)
        typedef=TypedefDescription(name,
                                   ctype,
                                   src=(filename,repr(lineno)))
        
        typedef.add_requirements(requirements)
        
        self.turn_unresolvables_into_errors(typedef,unresolvables)
        self.transfer_errors(typedef,errors)
        
        self.typedefs.append(typedef)
        self.all.append(typedef)
        self.output_order.append(('typedef',typedef))
    
    def handle_ctypes_new_type(self, ctype, filename, lineno):
        # Called by CtypesParser
        if isinstance(ctype,ctypesparser.CtypesEnum):
            self.handle_enum(ctype, filename, lineno)
        else:
            self.handle_struct(ctype, filename, lineno)
    
    def handle_ctypes_function(self, name, restype, argtypes, variadic,
                               filename, lineno):
        # Called by CtypesParser
        restype.visit(self)
        for argtype in argtypes:
            argtype.visit(self)
        
        requirements,unresolvables,errors=self.walk_cobject(restype)
        for argtype in argtypes:
            newreqs,newuns,newerrors = self.walk_cobject(argtype)
            requirements = newreqs.union(requirements)
            unresolvables = newuns.union(unresolvables)
            errors.extend(newerrors)
        
        function=FunctionDescription(name,
                                     restype,
                                     argtypes,
                                     variadic = variadic,
                                     src=(filename,repr(lineno)))
        
        function.add_requirements(requirements)
        
        self.turn_unresolvables_into_errors(function,unresolvables)
        self.transfer_errors(function,errors)
        
        self.functions.append(function)
        self.all.append(function)
        self.output_order.append(('function',function))

    def handle_ctypes_variable(self, name, ctype, filename, lineno):
        # Called by CtypesParser
        ctype.visit(self)
        requirements,unresolvables,errors=self.walk_cobject(ctype)
        
        variable=VariableDescription(name,
                                     ctype,
                                     src=(filename,repr(lineno)))
        
        variable.add_requirements(requirements)
        
        self.turn_unresolvables_into_errors(variable,unresolvables)
        self.transfer_errors(variable,errors)
        
        self.variables.append(variable)
        self.all.append(variable)
        self.output_order.append(('variable',variable))

    def handle_struct(self, ctypestruct, filename, lineno):
        # Called from within DataCollectingParser

        # When we find an opaque struct, we make a StructDescription for it
        # and record it in self.already_seen_opaque_structs. If we later
        # find a transparent struct with the same tag, we fill in the
        # opaque struct with the information from the transparent struct and
        # move the opaque struct to the end of the struct list.
        
        name = "%s %s"%(ctypestruct.variety,ctypestruct.tag)
        
        if name in self.already_seen_structs:
            return
        
        if ctypestruct.opaque:
            if name not in self.already_seen_opaque_structs:
                struct = StructDescription(ctypestruct.tag,
                                           ctypestruct.variety,
                                           None, # No members
                                           True, # Opaque
                                           ctypestruct,
                                           src=(filename,str(lineno)))
                
                self.already_seen_opaque_structs[name]=struct
                self.structs.append(struct)
                self.all.append(struct)
                self.output_order.append(('struct',struct))
        
        else:
            for (membername,ctype) in ctypestruct.members:
                ctype.visit(self)
            
            requirements,unresolvables,errors=self.walk_cobject(ctypestruct,
                                                            ignore_self = True)
            
            if name in self.already_seen_opaque_structs:
                # Fill in older version
                struct=self.already_seen_opaque_structs[name]
                struct.opaque = False
                struct.members = ctypestruct.members
                struct.ctype = ctypestruct
                struct.src = ctypestruct.src
                struct.add_requirements(requirements)
                
                self.output_order.append(('struct-body',struct))
                
                del self.already_seen_opaque_structs[name]
            
            else:
                struct = StructDescription(ctypestruct.tag,
                                           ctypestruct.variety,
                                           ctypestruct.members,
                                           False, # Not opaque
                                           src=(filename,str(lineno)),
                                           ctype=ctypestruct)
                struct.add_requirements(requirements)
                
                self.structs.append(struct)
                self.all.append(struct)
                self.output_order.append(('struct',struct))
                self.output_order.append(('struct-body',struct))
            
            self.already_seen_structs.add(name)
            
            self.turn_unresolvables_into_errors(struct,unresolvables)
            self.transfer_errors(struct,errors)
    
    def handle_enum(self, ctypeenum, filename, lineno):
        # Called from within DataCollectingParser.
        
        # Process for handling opaque enums is the same as process for opaque
        # structs. See handle_struct() for more details.
        
        tag = ctypeenum.tag
        if tag in self.already_seen_enums:
            return
            
        if ctypeenum.opaque:
            if tag not in self.already_seen_opaque_enums:
                enum=EnumDescription(ctypeenum.tag,
                             ctypeenum.enumerators,
                             ctypeenum,
                             src = (filename,str(lineno)))
                enum.opaque = True
                
                self.already_seen_opaque_enums[tag]=enum
                self.enums.append(enum)
                self.all.append(enum)
                self.output_order.append(('enum',enum))
                
        else:
            if tag in self.already_seen_opaque_enums:
                # Fill in older opaque version
                enum = self.already_seen_opaque_enums[tag]
                enum.opaque = False
                enum.ctype = ctypeenum
                enum.src = ctypeenum.src
            
                del self.already_seen_opaque_enums[tag]
            
            else:
                enum=EnumDescription(ctypeenum.tag,
                                None,
                                src=(filename,str(lineno)),
                                ctype=ctypeenum)
                enum.opaque = False
                
                self.enums.append(enum)
                self.all.append(enum)
                self.output_order.append(('enum',enum))
            
            self.already_seen_enums.add(tag)
            self.transfer_errors(enum,ctypeenum.errors)
            
            for (enumname,expr) in ctypeenum.enumerators:
                requirements,unresolvables,errors = self.walk_cobject(expr)
                
                constant=ConstantDescription(enumname, expr,
                                             src=(filename,lineno))
                constant.add_requirements(requirements)
                
                self.turn_unresolvables_into_errors(constant,unresolvables)
                self.transfer_errors(constant,errors)
                
                self.constants.append(constant)
                self.all.append(constant)
                self.output_order.append(('constant',constant))
    
    def handle_macro(self, name, params, expr, filename, lineno):
        # Called from within DataCollectingParser
        src = (filename,lineno)
        
        if expr==None:
            expr = ConstantExpressionNode(True)
            constant = ConstantDescription(name, expr, src)
            self.constants.append(constant)
            self.all.append(constant)
            return
        
        expr.visit(self)
        
        if isinstance(expr,CtypesType):
            if params:
                macro = MacroDescription(name, "", src)
                macro.error("%s has parameters but evaluates to a type. " \
                    "Ctypesgen does not support it." % macro.casual_name(),
                    cls = 'macro')
                self.macros.append(macro)
                self.all.append(macro)
                self.output_order.append(('macro',macro))
            
            else:
                requirements,unresolvables,errors = self.walk_cobject(expr)
                typedef = TypedefDescription(name, expr, src)
                typedef.add_requirements(requirements)
                self.turn_unresolvables_into_errors(typedef, unresolvables,
                    errcls = 'macro')
                self.transfer_errors(typedef, errors)
                self.typedefs.append(typedef)
                self.all.append(typedef)
                self.output_order.append(('typedef',typedef))
        
        else:
            if params:
                requirements,unresolvables,errors = self.walk_cobject(expr)
                macro = MacroDescription(name, params, expr, src)
                macro.add_requirements(requirements)
                unresolvables2 = []
                for (kind,name) in unresolvables:
                    if kind=="identifier" and name in params:
                        continue
                    unresolvables2.append((kind,name))
                self.turn_unresolvables_into_errors(macro,unresolvables2)
                self.transfer_errors(macro,errors)
                self.macros.append(macro)
                self.all.append(macro)
                self.output_order.append(('macro',macro))
            
            else:
                requirements,unresolvables,errors = self.walk_cobject(expr)
                macro = MacroDescription(name, None, expr, src)
                macro.add_requirements(requirements)
                self.turn_unresolvables_into_errors(macro,unresolvables)
                self.transfer_errors(macro,errors)
                self.macros.append(macro)
                self.all.append(macro)
                self.output_order.append(('macro',macro))
        
        # Macros could possibly contain things like __FILE__, __LINE__, etc...
        # This could be supported, but it would be a lot of work. It would
        # probably also bloat the Preamble considerably.
        
    def handle_error(self, message, filename, lineno):
        # Called by CParser
        error_message("%s:%d: %s" % (filename,lineno,message), cls='cparser')
    
    def handle_pp_error(self, message):
        # Called by PreprocessorParser
        error_message("%s: %s" % (self.options.cpp, message), cls = 'cparser')
    
    def handle_status(self, message):
        # Called by CParser
        status_message(message)
    
    def walk_cobject(self,cobject,ignore_self = False):
        """Find Description objects that are required for the given ctype or
        ExpressionNode, as well as errors associated with the ctype or
        ExpressionNode."""
                
        ctypestructs,ctypeenums,typedefnames,errors,identifiers = \
            visit_type_and_collect_info(cobject)
        
        requirements = set()
        unresolvables = set()
        
        for ctypestruct in ctypestructs:
            if ignore_self:
                if ctypestruct == cobject:
                    continue
            
            if "%s_%s" % (ctypestruct.variety,ctypestruct.tag) in \
                self.options.other_known_names:
                continue
            
            for struct in self.structs:
                if struct.tag == ctypestruct.tag and \
                    struct.variety==ctypestruct.variety:
                    requirements.add(struct)
                    break
            else:
                unresolvables.add(("struct",ctypestruct))
        
        for ctypeenum in ctypeenums:
            if ignore_self:
                if ctypeenum == cobject:
                    continue
            
            if "enum_%s" % ctypeenum.tag in self.options.other_known_names:
                continue
            
            for enum in self.enums:
                if enum.tag == ctypeenum.tag:
                    requirements.add(enum)
                    break
            else:
                unresolvables.add(("enum",ctypeenum))
        
        for typedefname in typedefnames:
            if typedefname in self.options.other_known_names:
                continue
            
            for typedef in self.typedefs:
                if typedefname == typedef.name:
                    requirements.add(typedef)
                    break
            else:
                unresolvables.add(("typedef",typedefname))
        
        for identifier in identifiers:
            if identifier in self.options.other_known_names:
                continue
            
            found = False
            
            for constant in self.constants:
                if identifier == constant.name:
                    requirements.add(constant)
                    found = True
                    break
            for function in self.functions:
                if identifier == function.name:
                    requirements.add(function)
                    found = True
                    break
            for variable in self.variables:
                if identifier == variable.name:
                    requirements.add(variable)
                    found = True
                    break
            for macro in self.macros:
                if identifier == macro.name:
                    requirements.add(macro)
                    found = True
                    break
            
            if not found:
                unresolvables.add(("identifier",identifier))
        
        return requirements,unresolvables,errors
    
    def turn_unresolvables_into_errors(self,desc,unresolvables,errcls=None):
        for kind,value in unresolvables:
            if kind=="identifier" or kind=="typedef":
                desc.error("%s depends on an unknown %s \"%s\". It " \
                    "will not be included in the output." % \
                    (desc.casual_name(), kind, value), cls = errcls)
            
            elif kind=="struct":
                desc.error("%s depends on an unknown %s \"%s\". It " \
                    "will not be included in the output." % \
                    (desc.casual_name(), value.variety, value.tag),
                    cls = errcls)
            
            else:
                desc.error("%s depends on an unknown enum \"%s\". It " \
                    "will not be included in the output." % \
                    (desc.casual_name(), value.tag),
                    cls = errcls)
    
    def transfer_errors(self,desc,errors):
        message = "%s will be skipped." % desc.casual_name()
        for error,cls in errors:
            desc.error(error + " " + message,cls)
    
    def visit_struct(self, struct):
        self.handle_struct(struct, struct.src[0], struct.src[1])
    
    def visit_enum(self,enum):
        self.handle_enum(enum, enum.src[0], enum.src[1])
    
    def data(self):
        return DescriptionCollection(self.constants,
                                     self.typedefs,
                                     self.structs,
                                     self.enums,
                                     self.functions,
                                     self.variables,
                                     self.macros,
                                     self.all,
                                     self.output_order)