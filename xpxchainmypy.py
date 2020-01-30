"""
    xpxchainmypy
    ========

    Custom plugin for annotating NEM's dynamic model classes.

    License
    -------

    Copyright 2019 NEM

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from mypy.plugin import Plugin
from mypy import nodes
from mypy import types
from mypy.plugins import common

GLOB_IMPORT = 'xpxchain.util.glob_import'
MODULE_IMPORT = 'xpxchain.util.module_import'
DATACLASS = 'xpxchain.util.dataclasses.dataclass'
INT_MIXIN = 'xpxchain.util.mixin.IntMixin'
MULTISIG_ACCOUNT_GRAPH_INFO = (
    'xpxchain.models.account.'
    'multisig_account_graph_info.'
    'MultisigAccountGraphInfo'
)


def is_model_field(sym: nodes.SymbolTableNode) -> bool:
    """Determine if a node is a model field."""

    return sym.type is not None and not sym.node.is_classvar


def add_model_init(ctx, var_types, var_fields) -> None:
    """Add dummy init method to class."""

    args = []
    for (var_type, var_field) in zip(var_types, var_fields):
        var = nodes.Var(var_field, var_type)
        args.append(nodes.Argument(
            variable=var,
            type_annotation=var_type,
            initializer=None,
            kind=nodes.ARG_POS
        ))

    common.add_method(ctx, '__init__', args, types.NoneTyp())


def add_model_asdict(ctx) -> None:
    """Add model asdict method."""

    bool_type = ctx.api.builtin_type('builtins.bool')
    dict_type = ctx.api.builtin_type('builtins.dict')
    var = nodes.Var('recurse', bool_type)
    recurse = nodes.Argument(
        variable=var,
        type_annotation=bool_type,
        initializer=nodes.NameExpr('True'),
        kind=nodes.ARG_NAMED_OPT
    )
    common.add_method(ctx, 'asdict', [recurse], dict_type)


def add_model_astuple(ctx) -> None:
    """Add model astuple method."""

    bool_type = ctx.api.builtin_type('builtins.bool')
    tuple_type = ctx.api.builtin_type('builtins.tuple')
    var = nodes.Var('recurse', bool_type)
    recurse = nodes.Argument(
        variable=var,
        type_annotation=bool_type,
        initializer=nodes.NameExpr('True'),
        kind=nodes.ARG_NAMED_OPT
    )
    common.add_method(ctx, 'astuple', [recurse], tuple_type)


def add_model_fields(ctx) -> None:
    """Add model fields method."""

    tuple_type = ctx.api.builtin_type('builtins.tuple')
    common.add_method(ctx, 'fields', [], tuple_type)


def add_model_replace(ctx) -> None:
    """Add model replace method."""

    any_type = types.AnyType(types.TypeOfAny.special_form)
    var = nodes.Var('change', any_type)
    kw_arg = nodes.Argument(
        variable=var,
        type_annotation=any_type,
        initializer=None,
        kind=nodes.ARG_STAR2
    )
    ret_type = types.Instance(ctx.cls.info, [])
    common.add_method(ctx, 'replace', [kw_arg], ret_type)


def add_model_set(ctx) -> None:
    """Add model fields method."""

    args = []
    str_type = ctx.api.builtin_type('builtins.str')
    name_var = nodes.Var('name', str_type)
    name_arg = nodes.Argument(
        variable=name_var,
        type_annotation=str_type,
        initializer=None,
        kind=nodes.ARG_POS
    )
    args.append(name_arg)

    any_type = types.AnyType(types.TypeOfAny.special_form)
    value_var = nodes.Var('value', any_type)
    value_arg = nodes.Argument(
        variable=value_var,
        type_annotation=any_type,
        initializer=None,
        kind=nodes.ARG_POS
    )
    args.append(value_arg)

    common.add_method(ctx, '_set', args, types.NoneTyp())


def add_dict_hook(ctx):
    """Add dict argument to the class context."""

    # Only add if not present.
    info = ctx.cls.info
    if '__init__' in info.names:
        func = info.names['__init__'].node
        func.body.body[:] = [nodes.PassStmt()]


def add_dataclass_hook(ctx):
    """Add dataclass information to the class context."""

    info = ctx.cls.info

    # Get the class annotated nodes.
    # The class variables include any variable assigned in the class,
    # which may be a lot of different things. Therefore, look for variables
    # annotated with a type: these are our type annotations.
    var_nodes = [i for i in info.names.values() if isinstance(i.node, nodes.Var)]
    member_vars = [i for i in var_nodes if is_model_field(i)]
    var_types = [i.type for i in member_vars]
    var_fields = [i.node.name.lstrip('_') for i in member_vars]

    # Don't override init if present.
    if '__init__' not in info.names.keys():
        add_model_init(ctx, var_types, var_fields)
    add_model_asdict(ctx)
    add_model_astuple(ctx)
    add_model_fields(ctx)
    add_model_replace(ctx)
    add_model_set(ctx)


class XPXPlugin(Plugin):
    """Plugin to support basic, automatically generated ProximaX Sirius models."""

    def get_class_decorator_hook(self, fullname: str):
        if fullname == DATACLASS:
            return add_dataclass_hook
        return None

    def get_customize_class_mro_hook(self, fullname: str):
        if fullname == MULTISIG_ACCOUNT_GRAPH_INFO:
            return add_dict_hook
        return None


def plugin(version: str) -> 'Plugin':
    """Get the application plugin."""

    return XPXPlugin
