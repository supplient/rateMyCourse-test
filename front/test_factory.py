import types

from template import *

cls_dict = {}

SIGN_GENERATED = "_dsf34dfds_XXX"
FUNC_NAME = "initDriver"

def iterSubClsAddAttr(basic_cls, factor_name, attr_name, attr_value):
    '''Add some attr to basic_cls's all subclasses iteratively.
    Add factor_name in front of each generated subcls's name.
    Note, if one cls is generated by this func, 
        even if the cls is passed as basic_cls, it will not be processed.
    And basic_cls will not be processed.
    '''
    for sub_cls in basic_cls.__subclasses__():
        # Check if is generated subclass
        if hasattr(sub_cls, SIGN_GENERATED):
            continue

        # Iterate down
        iterSubClsAddAttr(sub_cls, factor_name, attr_name, attr_value)

        # Create new class
        new_name = factor_name + "_" + sub_cls.__name__
        dec_sub_cls = types.new_class(new_name, (sub_cls, ), {})
        dec_sub_cls.__module__ = __name__

        # Signed as generated subclass
        setattr(dec_sub_cls, SIGN_GENERATED, True)

        # Add attribute if without it
        if not hasattr(dec_sub_cls, attr_name):
            setattr(dec_sub_cls, attr_name, attr_value)

        # Save
        cls_dict[new_name] = dec_sub_cls


# Override module's meta info to provide Testcases
#   generated above for unittest runner.
# TODO This will override meta attributes like __name__
#   , which is not the feature I want.
def __dir__():
    return cls_dict.keys()

def __getattr__(name):
    if name in cls_dict.keys():
        return cls_dict[name]
    return None


# Search all TCFactor
import driver_tcfactor

factor_module_list = [
    driver_tcfactor
]

all_dict = {}
for factor_module in factor_module_list:
    names = dir(factor_module)
    for name in names:
        obj = getattr(factor_module, name)
        if isinstance(obj, classmethod):
            all_dict[name] = obj

# Generate Testcases
for name, func in all_dict.items():
    iterSubClsAddAttr(front_basic.FrontBasicTC, name, FUNC_NAME, func)