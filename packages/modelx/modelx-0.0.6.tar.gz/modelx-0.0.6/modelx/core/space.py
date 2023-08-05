# Copyright (c) 2017-2018 Fumito Hamamura <fumito.ham@gmail.com>

# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation version 3.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.  If not, see <http://www.gnu.org/licenses/>.

import builtins
from collections import Sequence
from textwrap import dedent
from types import FunctionType

from modelx.core.base import (
    ObjectArgs,
    get_impls,
    get_interfaces,
    Impl,
    NullImpl,
    Interface,
    LazyEval,
    LazyEvalDict,
    LazyEvalChainMap,
    ProxyDict,
    ProxyChainMap,
    ParentMixin,
    ImplDict,
    ImplChainMap,
    BaseMapProxy)
from modelx.core.formula import Formula, create_closure
from modelx.core.cells import Cells, CellsImpl, cells_to_argvals
from modelx.core.util import AutoNamer, is_valid_name, get_module


class SpaceArgs(ObjectArgs):
    """Combination of space and arguments to locate its subspace."""

    def __init__(self, space, args, kwargs=None):

        args, kwargs = cells_to_argvals(args, kwargs)
        ObjectArgs.__init__(self, space, args, kwargs)
        self.space = self.obj_

    def eval_formula(self):

        func = self.space.paramfunc.func
        codeobj = func.__code__
        name = self.space.name
        namespace = self.space.namespace

        closure = func.__closure__  # None normally.
        if closure is not None:     # pytest fails without this.
            closure = create_closure(self.space.interface)

        altfunc = FunctionType(codeobj, namespace,
                               name=name, closure=closure)

        return altfunc(**self.arguments)


class ParamFunc(Formula):
    def __init__(self, func):
        Formula.__init__(self, func)


class SpaceContainerImpl(Impl):
    """Base class of Model and Space to work as container of spaces.

    **Space Deletion**
    new_space(name)
    del_space(name)

    """

    state_attrs = ['_spaces',   # must be defined in subclasses
                   'spacenamer'] + Impl.state_attrs

    def __init__(self, system, if_class):

        Impl.__init__(self, if_class)

        self.system = system
        self.spacenamer = AutoNamer('Space')


    # ----------------------------------------------------------------------
    # Serialization by pickle

    def __getstate__(self):

        state = {key: value for key, value in self.__dict__.items()
                 if key in self.state_attrs}

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def restore_state(self, system):
        """Called after unpickling to restore some attributes manually."""

        self.system = system
        for space in self._spaces.values():
            space.restore_state(system)

    # ----------------------------------------------------------------------
    # Properties

    @property
    def model(self):
        return NotImplementedError

    @property
    def spaces(self):
        return self._spaces.get_updated()

    def has_space(self, name):
        return name in self.spaces

    def new_space(self, name=None, bases=None, paramfunc=None,
                  *, refs=None, arguments=None):
        """Create a child space.

        Args:
            name (str): Name of the space. If omitted, the space is
                created automatically.
            bases: If specified, the new space becomes a derived space of
                the `base` space.
            paramfunc: Function whose parameters used to set space parameters.
            refs: a mapping of refs to be added.
            arguments: ordered dict of space parameter names to their values.

        """

        if name is None:
            name = self.spacenamer.get_next(self.namespace)

        if self.has_space(name):
            raise ValueError("Name already assigned.")

        if not is_valid_name(name):
            raise ValueError("Invalid name '%s'." % name)

        space = SpaceImpl(parent=self, name=name, bases=bases,
                          paramfunc=paramfunc, refs=refs, arguments=arguments)

        self._set_space(space)
        return space

    def _set_space(self, space):
        """To be overridden in subclasses."""
        raise NotImplementedError

    def del_space(self, name):
        raise NotImplementedError

    @property
    def namespace(self):
        raise NotImplementedError

    def new_space_from_module(self, module_, recursive=False, **params):

        module_ = get_module(module_)

        if 'name' not in params or params['name'] is None:
            # xxx.yyy.zzz -> zzz
            name = params['name'] = module_.__name__.split('.')[-1]
        else:
            name = params['name']

        space = self.new_space(**params)
        space.new_cells_from_module(module_)

        if recursive and hasattr(module_, '_spaces'):
            for name in module_._spaces:
                submodule = module_.__name__ + '.' + name
                space.new_space_from_module(module_=submodule, recursive=True)

        return space

    def new_space_from_excel(self, book, range_, sheet=None,
                                name=None,
                                names_row=None, param_cols=None,
                                space_param_order=None,
                                cells_param_order=None,
                                transpose=False,
                                names_col=None, param_rows=None):

        import modelx.io.excel as xl

        param_order = space_param_order + cells_param_order

        cellstable = xl.CellsTable(book, range_, sheet,
                                   names_row, param_cols,
                                   param_order,
                                   transpose,
                                   names_col, param_rows)

        space_params = cellstable.param_names[:len(space_param_order)]
        cells_params = cellstable.param_names[len(space_param_order):]

        if space_params:
            space_sig = "=None, ".join(space_params) + "=None"
        else:
            space_sig = ""

        if cells_params:
            cells_sig = "=None, ".join(cells_params) + "=None"
        else:
            cells_sig = ""

        param_func = "def _param_func(" + space_sig + "): pass"
        blank_func = "def _blank_func(" + cells_sig + "): pass"

        space = self.new_space(name=name, paramfunc=param_func)

        for cellsdata in cellstable.items():
            for args, value in cellsdata.items():
                space_args = args[:len(space_params)]
                cells_args = args[len(space_params):]

                subspace = space.get_dyn_space(space_args)

                if cellsdata.name in subspace.cells:
                    cells = subspace.cells[cellsdata.name]
                else:
                    cells = subspace.new_cells(name=cellsdata.name,
                                                  func=blank_func)
                cells.set_value(cells_args, value)

        return space


class SpaceContainer(Interface):
    """A common base class shared by Model and Space.

    A base class for implementing (sub)space containment.
    """
    def new_space(self, name=None, bases=None, paramfunc=None, refs=None):
        """Create a (sub)space.

        Args:
            name (str, optional): Name of the space. Defaults to ``SpaceN``,
                where ``N`` is a number determined automatically.
            bases (optional): A space or a sequence of spaces to be the base
                space(s) of the created space.
            paramfunc (optional): Function to specify the parameters of
                dynamic (sub)spaces. The signature of this function is used
                for setting parameters for dynamic (sub)spaces.
                This function should return a mapping of keyword arguments
                to be passed to this method when the dynamic (sub)spaces
                are created.

        Returns:
            The new (sub)space.
        """
        space = self._impl.model.currentspace \
            = self._impl.new_space(name=name, bases=get_impls(bases),
                                   paramfunc=paramfunc, refs=refs)

        return space.interface

    def new_space_from_module(self, module_, recursive=False, **params):
        """Create a (sub)space from an module.

        Args:
            module_: a module object or name of the module object.
            recursive: Not yet implemented.
            **params: arguments to pass to ``new_space``

        Returns:
            The new (sub)space created from the module.
        """

        space = self._impl.model.currentspace \
            = self._impl.new_space_from_module(module_,
                                                  recursive=recursive,
                                                  **params)

        return get_interfaces(space)

    def new_space_from_excel(self, book, range_, sheet=None,
                                name=None,
                                names_row=None, param_cols=None,
                                space_param_order=None,
                                cells_param_order=None,
                                transpose=False,
                                names_col=None, param_rows=None):
        """Create a (sub)space from an Excel range.

        To use this method, ``openpyxl`` package must be installed.

        Args:
            book (str): Path to an Excel file.
            range_ (str): Range expression, such as "A1", "$G4:$K10",
                or named range "NamedRange1".
            sheet (str): Sheet name (case ignored).
            name (str, optional): Name of the space. Defaults to ``SpaceN``,
                where ``N`` is a number determined automatically.
            names_row (optional): an index number indicating
                what row contains the names of cells and parameters.
                Defaults to the top row (0).
            param_cols (optional): a sequence of index numbers
                indicating parameter columns.
                Defaults to only the leftmost column ([0]).
            names_col (optional): an index number, starting from 0,
                indicating what column contains additional parameters.
            param_rows (optional): a sequence of index numbers, starting from
                0, indicating rows of additional parameters, in case cells are
                defined in two dimensions.
            transpose (optional): Defaults to ``False``.
                If set to ``True``, "row(s)" and "col(s)" in the parameter
                names are interpreted inversely, i.e.
                all indexes passed to "row(s)" parameters are interpreted
                as column indexes,
                and all indexes passed to "col(s)" parameters as row indexes.
            space_param_order: a sequence to specify space parameters and
                their orders. The elements of the sequence denote the indexes
                of ``param_cols`` elements, and optionally the index of
                ``param_rows`` elements shifted by the length of
                ``param_cols``. The elements of this parameter and
                ``cell_param_order`` must not overlap.
            cell_param_order (optional): a sequence to reorder the parameters.
                The elements of the sequence denote the indexes of
                ``param_cols`` elements, and optionally the index of
                ``param_rows`` elements shifted by the length of
                ``param_cols``. The elements of this parameter and
                ``cell_space_order`` must not overlap.

        Returns:
            The new (sub)space created from the Excel range.
        """

        space = self._impl.new_space_from_excel(
            book, range_, sheet, name,
            names_row, param_cols,
            space_param_order,
            cells_param_order,
            transpose,
            names_col, param_rows)

        return get_interfaces(space)

    @property
    def spaces(self):
        """A mapping of the names of (sub)spaces to the Space objects"""
        return self._impl.spaces.interfaces

    # ----------------------------------------------------------------------
    # Current Space method

    def cur_space(self, name=None):
        """Set the current space to Space ``name`` and return it.

        If called without arguments, the current space is returned.
        Otherwise, the current space is set to the space named ``name``
        and the space is returned.
        """
        if name is None:
            return self._impl.model.currentspace.interface
        else:
            self._impl.model.currentspace = self._impl.spaces[name]
            return self.cur_space()


class BaseDict(LazyEvalDict):
    """Members of bases to be inherited to ``space``"""

    def __init__(self, derived):

        observer = [derived]
        LazyEvalDict.__init__(self, {}, observer)

        self.space = derived.parent
        for base in self.space.mro[1:]:
            base._self_members.append_observer(self)

        self.get_updated()

    def _update_data(self):

        self.data.clear()
        bases = list(reversed(self.space.mro))

        for base, base_next in zip(bases, bases[1:]):

            self.data.update(self.get_baseself(base))
            keys = self.data.keys() - base_next.self_members.keys()

            for name in list(self.data):
                if name not in keys:
                    del self.data[name]

    def get_baseself(self, base):
        raise NotImplementedError


class BaseSpaceDict(BaseDict):

    def get_baseself(self, base):
        return base.self_spaces


class BaseCellsDict(BaseDict):

    def get_baseself(self, base):
        return base.self_cells


class BaseRefsDict(BaseDict):

    def get_baseself(self, base):
        return base.self_refs


class SelfSpaceDict(ImplDict):

    def __init__(self, space, data=None, observers=None):
        ImplDict.__init__(self, space, SpaceMapProxy, data, observers)


class SelfCellsDict(ImplDict):

    def __init__(self, space, data=None, observers=None):
        ImplDict.__init__(self, space, CellsMapProxy, data, observers)


class BaseMixin:

    def __init__(self, basedict_class):
        self._basedict = basedict_class(self)

    @property
    def basedict(self):
        return self._basedict.get_updated()


class DerivedSpaceDict(BaseMixin, SelfSpaceDict):

    def __init__(self, space, data=None, observers=None):
        SelfSpaceDict.__init__(self, space, data, observers)
        BaseMixin.__init__(self, BaseSpaceDict)

    def _update_data(self):
        self.data.clear()
        for base_space in self.basedict.values():

            space = SpaceImpl(parent=self.parent, name=base_space.name,
                              bases=base_space,
                              paramfunc=base_space.paramfunc)

            self.data[space.name] = space

        SelfSpaceDict._update_data(self)


class DerivedCellsDict(BaseMixin, SelfCellsDict):

    def __init__(self, space, data=None, observers=None):
        SelfCellsDict.__init__(self, space, data, observers)
        BaseMixin.__init__(self, BaseCellsDict)

    def _update_data(self):
        keys = self.data.keys() - self.basedict.keys()
        for key in keys:
            del self.data[key]

        for key, base_cell in self.basedict.items():
            if key in self.data:
                if self.data[key].formula is base_cell.formula:
                    return
                else:
                    del self.data[key]

            cell = CellsImpl(space=self.parent, name=base_cell.name,
                             func=base_cell.formula)
            self.data[key] = cell

        SelfCellsDict._update_data(self)


class DerivedRefsDict(BaseMixin, ProxyDict):

    def __init__(self, space, data=None, observers=None):
        ProxyDict.__init__(self, space, data, observers)
        BaseMixin.__init__(self, BaseRefsDict)

    def _update_data(self):
        self.data.clear()
        self.data.update(self.basedict)

def _map_repr(self):
    result = [',\n '] * (len(self._data) * 2 -1)
    result[0::2] = sorted(list(self._data))
    return '{' + ''.join(result) + '}'


class CellsMapProxy(BaseMapProxy):

    def __delitem__(self, name):
        cells = self._data[name]._impl
        cells.space.del_cells(name)

    __repr__ = _map_repr


class SpaceMapProxy(BaseMapProxy):

    def __delitem__(self, name):
        space = self._data[name]._impl
        space.parent.del_space(name)

    __repr__ = _map_repr


class NamespaceMap(LazyEvalChainMap, ParentMixin):

    def __init__(self, space, maps):
        self.namespace = {}
        ParentMixin.__init__(self, space)
        LazyEvalChainMap.__init__(self, maps)

    def _update_data(self):

        for map_ in self.maps:
            if isinstance(map_, LazyEval):
                map_.get_updated()
        self.namespace.clear()
        self.namespace.update(get_interfaces(self.parent.cells))
        self.namespace.update(get_interfaces(self.parent.spaces))
        self.namespace.update(self.parent.refs)

    def __getstate__(self):

        state = self.__dict__.copy()
        if '__builtins__' in state['namespace']:
            ns = state['namespace'].copy()
            ns['__builtins__'] = '__builtins__'
            state['namespace'] = ns

        return state

    def __setstate__(self, state):

        if '__builtins__' in state['namespace']:
            state['namespace']['__builtins__'] = builtins

        self.__dict__.update(state)


class SpaceImpl(SpaceContainerImpl):
    """The implementation of Space class.

    Space objects have quite a few mapping members. Those are
    MappyingProxyTypes objects, which are essentially frozen dictionaries.

    ``namespace`` stores all names, with their associated objects,
    that can be referenced in the form of attribute access to the space.
    Those names can also be referenced from within the formulas of the
    cells contained in the space.

    ``namespace`` is broken down into ``cells``, ``spaces`` and ``refs`` maps.
    ``cells`` is a map of all the cells contained in the space,
    and ``spaces`` is a map of all the subspaces of the space.
    ``refs`` contains names and their associated objects that are not
    part of the space but are accessible from the space.

    ``cells`` is further broken down into ``self_cells`` and ``derived_cells``.
    ``self_cells`` contains cells that are newly defined or overridden
    in the class. On the other hand, ``derived_cells`` contains cells
    derived from the space's base class(s).

    ``space`` is first broken down into ``static_spaces`` and
    ``dynamic_spaces``. ``static_spaces`` contains subspaces of the space
    that are explicitly created by the user by the space's ``new_space``
    method or one of its variants. ``dynamic_spaces`` contains parametrized
    subspaces that are created dynamically by ``()`` or ``[]`` operation on
    the space.

    Objects with their associated names are::

        namespace

            cells
                derived_cells
                self_cells

            spaces
                dynamic_spaces
                static_spaces
                    derived_spaces
                    self_spaces

            refs
                derived_refs
                self_refs
                global_refs
                local_refs
                arguments

    Args:
        parent: SpaceImpl or ModelImpl to contain this.
        name: Name of the space.
        params: Callable or str or sequence.
        bases: SpaceImpl or a list of SpaceImpl.
        
    Attributes:
        space (Space): The Space associated with this implementation.
        parent: the space or model containing this space.
        name:   name of this space.
        signature: Function signature for child spaces. None if not specified.
        
        cells (dict):  Dict to contained cells
        _self_cells (dict): cells defined in this space.
        base_cells (dict): cells in base spaces to inherit in this space.
        _derived_cells (dict): cells derived from base cells.
        _self_refs
        _derived_refs
        
        cellsnamer (AutoNamer): AutoNamer to auto-name unnamed child cells.
        
        mro (list): MRO of base spaces.
                
        _namespace (dict)
    """
    def __init__(self, parent, name, bases, paramfunc,
                 refs=None, arguments=None):

        SpaceContainerImpl.__init__(self, parent.system, if_class=Space)

        self.name = name
        self.parent = parent
        self.cellsnamer = AutoNamer('Cells')

        self.param_spaces = {}
        if paramfunc is None:
            self.paramfunc = None
        else:
            self.paramfunc = ParamFunc(paramfunc)

        if arguments is None:
            self.is_dynamic = False
            self._arguments = LazyEvalDict()
        else:
            self.is_dynamic = True
            self._arguments = LazyEvalDict(arguments)

        self._bind_args(arguments)

        # Set up direct base spaces and mro
        if bases is None:
            self.direct_bases = []
        elif isinstance(bases, SpaceImpl):
            self.direct_bases = [bases]
        elif isinstance(bases, Sequence) \
                and all(isinstance(base, SpaceImpl) for base in bases):
            self.direct_bases = list(bases)
        else:
            raise TypeError('bases must be space(s).')

        self.mro = []
        self._update_mro()

        # ------------------------------------------------------------------
        # Construct member containers

        self._self_cells = SelfCellsDict(self)
        self._self_spaces = SelfSpaceDict(self)
        self._dynamic_spaces = ImplDict(self, SpaceMapProxy)
        self._self_refs = ProxyDict(self)

        self_members = [self._self_cells,
                        self._self_spaces,
                        self._self_refs]

        # Add observers later to avoid circular reference
        self._self_members = LazyEvalChainMap(self_members)

        self._derived_cells = DerivedCellsDict(self)
        self._cells = ImplChainMap(self, CellsMapProxy,
                                   [self._self_cells,
                                    self._derived_cells])

        self._derived_spaces = DerivedSpaceDict(self)

        self._static_spaces = ImplChainMap(self, SpaceMapProxy,
                                           [self._self_spaces,
                                            self._derived_spaces])
        self._spaces = ImplChainMap(self, SpaceMapProxy,
                                    [self._static_spaces,
                                     self._dynamic_spaces])
        self._derived_refs = DerivedRefsDict(self)

        self._local_refs = {'get_self': self.get_self_interface,
                            '_self': self.interface}

        self._refs = ProxyChainMap(self,
                                   [self.model._global_refs,
                                    self._local_refs,
                                    self._arguments,
                                    self._self_refs,
                                    self._derived_refs])

        derived = [self._derived_cells,
                   self._derived_spaces,
                   self._derived_refs]

        for observer in derived:
            self._self_members.append_observer(observer)

        self._namespace_impl = NamespaceMap(self, [self._cells,
                                                   self._spaces,
                                                   self._refs])

        # ------------------------------------------------------------------
        # Add initial refs members

        if refs is not None:
            self._self_refs.update(refs)
            self._self_refs.set_update()

    # ----------------------------------------------------------------------
    # Serialization by pickle

    state_attrs = [
        'direct_bases',
        'mro',
        '_self_cells',
        '_derived_cells',
        '_cells',
        '_self_spaces',
        '_derived_spaces',
        '_static_spaces',
        '_dynamic_spaces',
        '_local_refs',
        '_arguments',
        '_self_refs',
        '_derived_refs',
        '_refs',
        '_self_members',
        '_namespace_impl',
        'is_dynamic',
        'param_spaces',
        'paramfunc',
        'cellsnamer',
        'name',
        'can_have_none'] + SpaceContainerImpl.state_attrs

    def _bind_args(self, args):

        if self.is_dynamic:
            self.boundargs = self.parent.signature.bind(**args)
            self.argvalues = tuple(self.boundargs.arguments.values())
        else:
            self.boundargs = None
            self.argvalues = None

    def __getstate__(self):
        state = {key: value for key, value in self.__dict__.items()
                 if key in self.state_attrs}
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def restore_state(self, system):
        """Called after unpickling to restore some attributes manually."""

        self.system = system

        for space in self._spaces.values():
            space.restore_state(system)

        for cells in self._cells.values():
            cells.restore_state(system)

        # From Python 3.5, signature is pickable,
        # pickling logic involving signature may be simplified.
        self._bind_args(self._arguments)


    def __repr__(self):
        return '<SpaceImpl: ' + self.name + '>'

    @property
    def _repr_self(self):

        if self.is_dynamic:
            args = [repr(arg) for arg in self.argvalues]
            param = ', '.join(args)
            return "%s[%s]" % (self.parent.name, param)
        else:
            return self.name

    @property
    def _repr_parent(self):

        if self.is_dynamic:
            return self.parent._repr_parent
        else:
            if self.parent._repr_parent:
                return self.parent._repr_parent + '.' + self.parent._repr_self
            else:
                return self.parent._repr_self

    def get_self_interface(self):
        return self.interface

    def get_object(self, name):
        """Retrieve an object by a dotted name relative to the space."""

        parts = name.split('.')
        child = parts.pop(0)

        if parts:
            return self.spaces[child].get_object('.'.join(parts))
        else:
            return self._namespace_impl[child]

    @property
    def debug_info(self):

        message = dedent("""\
        name: %s
        self_cells:
            need_update=%s
            names:%s
        derived_cells:
            need_update=%s
            names:%s
        base_cells:
            need_update=%s
            names:%s
        cells: %s
        spaces: %s
        refs: %s
        """)

        return message % (
            self.name,
            self._self_cells.needs_update,
            list(self._self_cells.keys()),
            self._derived_cells.needs_update,
            list(self._derived_cells.keys()),
            self._derived_cells._basedict.needs_update,
            list(self._derived_cells._basedict.keys()),
            list(self._cells.keys()),
            list(self._spaces.keys()),
            list(self._refs.keys())
        )

    # ----------------------------------------------------------------------
    # Components and namespace

    @property
    def self_members(self):
        return self._self_members.get_updated()

    @property
    def cells(self):
        return self._cells.get_updated()

    @property
    def self_cells(self):
        return self._self_cells.get_updated()

    def self_cells_set_update(self):
        return self._self_cells.set_update(skip_self=False)

    @property
    def derived_cells(self):
        return self._derived_cells.get_updated()

    @property
    def self_spaces(self):
        return self._self_spaces.get_updated()

    @property
    def derived_spaces(self):
        return self._derived_spaces.get_updated()

    @property
    def static_spaces(self):
        return self._static_spaces.get_updated()

    @property
    def dynamic_spaces(self):
        return self._dynamic_spaces.get_updated()

    @property
    def refs(self):
        return self._refs.get_updated()

    @property
    def self_refs(self):
        return self._self_refs.get_updated()

    @property
    def derived_refs(self):
        return self._derived_refs.get_updated()

    @property
    def local_refs(self):
        return self._local_refs

    @property
    def arguments(self):
        return self._arguments.get_updated()

    @property
    def namespace_impl(self):
        return self._namespace_impl.get_updated()

    @property
    def namespace(self):
        return self._namespace_impl.get_updated().namespace

    # ----------------------------------------------------------------------
    # Inheritance

    def _update_mro(self):
        """Calculate the Method Resolution Order of bases using the C3 algorithm.

        Code modified from 
        http://code.activestate.com/recipes/577748-calculate-the-mro-of-a-class/

        Args:
            bases: sequence of direct base spaces.

        """
        seqs = [base.mro.copy() for base
                in self.direct_bases] + [self.direct_bases]
        res = []
        while True:
            non_empty = list(filter(None, seqs))

            if not non_empty:
                # Nothing left to process, we're done.
                self.mro.clear()
                self.mro.extend([self] + res)
                return

            for seq in non_empty:  # Find merge candidates among seq heads.
                candidate = seq[0]
                not_head = [s for s in non_empty if candidate in s[1:]]
                if not_head:
                    # Reject the candidate.
                    candidate = None
                else:
                    break

            if not candidate:
                raise TypeError(
                    "inconsistent hierarchy, no C3 MRO is possible")

            res.append(candidate)

            for seq in non_empty:
                # Remove candidate.
                if seq[0] == candidate:
                    del seq[0]

    # ----------------------------------------------------------------------
    # Properties

    def has_bases(self):
        return len(self.mro) > 1

    @property
    def signature(self):
        return self.paramfunc.signature

    @property
    def parameters(self):
        return self.paramfunc.signature.parameters

    def get_fullname(self, omit_model=False):

        fullname = self.name
        parent = self.parent
        while True:
            fullname = parent.name + '.' + fullname
            if parent.parent is not None:
                parent = parent.parent
            else:
                if omit_model:
                    separated = fullname.split('.')
                    separated.pop(0)
                    fullname = '.'.join(separated)

                return fullname

    @property
    def fullname(self):
        return self.parent.fullname + '.' + self.name

    @property
    def model(self):
        return self.parent.model

    # ----------------------------------------------------------------------
    # Attribute access

    def set_attr(self, name, value):
        """Implementation of attribute setting

        ``space.name = value`` by user script
        Called from ``Space.__setattr__``
        """

        if not is_valid_name(name):
            raise ValueError

        if name in self.namespace:
            if name in self.refs:
                if name in self.self_refs or name in self.derived_refs:
                    self.self_refs[name] = value
                    self.self_refs.set_update(skip_self=False)
                else:
                    raise KeyError("Ref '%s' cannot be changed" % name)

            elif name in self.cells:
                if self.cells[name].is_scalar():
                    self.cells[name].set_value((), value)
                else:
                    raise AttributeError("Cells '%s' is not a scalar." % name)
            else:
                raise ValueError
        else:
            self._self_refs.set_item(name, value)

    def del_attr(self, name):
        """Implementation of attribute deletion

        ``del space.name`` by user script
        Called from ``Space.__delattr__``
        """
        if name in self.namespace:
            if name in self.cells:
                if name in self.self_cells:
                    self.del_cells(name)
                elif name in self.derived_cells:
                    raise KeyError("Derived cells cannot be removed")
                elif name in self.dynamic_spaces:
                    self.del_cells(name)
                else:
                    raise RuntimeError("Must not happen")

            elif name in self.spaces:
                if name in self.self_spaces:
                    self.del_space(name)
                elif name in self.derived_cells:
                    raise KeyError("Derived space cannot be removed")
                else:
                    raise RuntimeError("Must not happen")

            elif name in self.refs:
                self.del_refs(name)

            else:
                raise RuntimeError("Must not happen")

        else:
            raise KeyError("'%s' not found in Space '%s'" % (name, self.name))

    # ----------------------------------------------------------------------
    # Space operation

    def _set_space(self, space):
        if space.is_dynamic:
            self._dynamic_spaces.set_item(space.name, space)
        else:
            self._self_spaces.set_item(space.name, space)

    def del_space(self, name):
        """Delete a space.

        Derived spaces are indelible.
        When a space is deleted, contained cells and spaces are also deleted.
        Values of the contained cells and dependent cells are deleted.

        """
        if name not in self.spaces:
            raise ValueError("Space '%s' does not exist" % name)

        if name in self.self_spaces:
            # TODO: Destroy space
            self.self_spaces.del_item(name, True)

        elif name in self.dynamic_spaces:
            # TODO: Destroy space
            self.dynamic_spaces.del_item(name, True)

        else:
            raise ValueError("Derived cells cannot be deleted")

    # ----------------------------------------------------------------------
    # Cells operation

    # --- Cells deletion -------------------------------------

    def del_cells(self, name):
        """Implementation of cells deletion

        ``del space.name`` where name is a cells, or
        ``del space.cells['name']``
        """
        if name in self.self_cells:
            # self._self_cells[name].parent = None
            cells = self.self_cells.pop(name)
            self.self_cells.set_update()

        elif name in self.dynamic_spaces:
            cells = self.dynamic_spaces.pop(name)
            self.dynamic_spaces.set_update()

        else:
            raise KeyError("Cells '%s' does not exist" % name)

        NullImpl(cells)

    def _del_derived_cells(self, name):

        if name in self.namespace:
            if name in self.derived_cells:
                self._derived_cells[name].parent = None
                del self._derived_cells[name]

            elif name in self._derived_spaces:
                self._derived_spaces[name].parent = None
                del self._derived_spaces[name]

            elif name in self._derived_refs:
                del self._derived_refs[name]

            else:
                raise RuntimeError("Name already assigned.")

            return True

        else:
            return False

    # --- Dynamic Space Operation -------------------------------------

    def get_dyn_space(self, args, kwargs=None):

        ptr = SpaceArgs(self, args, kwargs)

        if ptr.argvalues in self.param_spaces:
            return self.param_spaces[ptr.argvalues]

        else:
            last_self = self.system.self
            self.system.self = self

            try:
                space_args = ptr.eval_formula()

            finally:
                self.system.self = last_self

            if space_args is None:
                space_args = {}
            else:
                if 'bases' in space_args:
                    space_args['bases'] = get_impls(space_args['bases'])

            space_args['arguments'] = ptr.arguments
            space = self.new_space(**space_args)
            self.param_spaces[ptr.argvalues] = space
            return space

    def set_paramfunc(self, paramfunc):
        if self.paramfunc is None:
            self.paramfunc = ParamFunc(paramfunc)
        else:
            raise ValueError("paramfunc already assigned.")

    # --- Cells creation -------------------------------------

    def set_cells(self, name, cells):
        self._self_cells.set_item(name, cells, True)

    def new_cells(self, name=None, func=None):
        cells = CellsImpl(space=self, name=name, func=func)
        self.set_cells(cells.name, cells)
        return cells

    def new_cells_from_module(self, module_):
        # Outside formulas only

        module_ = get_module(module_)
        newcells = {}

        for name in dir(module_):
            func = getattr(module_, name)
            if isinstance(func, FunctionType):
                # Choose only the functions defined in the module.
                if func.__module__ == module_.__name__:
                    newcells[name] = \
                        self.new_cells(name, func)

        return newcells

    def new_cells_from_excel(self, book, range_, sheet=None,
                             names_row=None, param_cols=None,
                             param_order=None,
                             transpose=False,
                             names_col=None, param_rows=None):
        """Create multiple cells from an Excel range.

        Args:
            book (str): Path to an Excel file.
            range_ (str): Range expression, such as "A1", "$G4:$K10",
                or named range "NamedRange1".
            sheet (str): Sheet name (case ignored).
            names_row: Cells names in a sequence, or an integer number, or
              a string expression indicating row (or column depending on
              ```orientation```) to read cells names from.
            param_cols: a sequence of them
                indicating parameter columns (or rows depending on ```
                orientation```)
            param_order: a sequence of integers representing
                the order of params and extra_params.
            transpose: in which direction 'vertical' or 'horizontal'
            names_col: a string or a list of names of the extra params.
            param_rows: integer or string expression, or a sequence of them
                indicating row (or column) to be interpreted as parameters.
        """
        import modelx.io.excel as xl

        cellstable = xl.CellsTable(book, range_, sheet,
                                   names_row, param_cols, param_order,
                                   transpose, names_col, param_rows)

        if cellstable.param_names:
            sig = "=None, ".join(cellstable.param_names) + "=None"
        else:
            sig = ""

        blank_func = "def _blank_func(" + sig + "): pass"

        for cellsdata in cellstable.items():
            cells = self.new_cells(name=cellsdata.name, func=blank_func)
            for args, value in cellsdata.items():
                cells.set_value(args, value)

    # ----------------------------------------------------------------------
    # Reference operation

    def del_refs(self, name):

        if name in self.self_refs:
            del self.self_refs[name]
            self.self_refs.set_update()
        elif name in self.derived_refs:
            raise KeyError("Derived ref '%s' cannot be deleted" % name)
        elif name in self.arguments:
            raise ValueError("Argument cannot be deleted")
        elif name in self.local_refs:
            raise ValueError("Ref '%s' cannot be deleted" % name)
        elif name in self.model.global_refs:
            raise ValueError(
                "Global ref '%s' cannot be deleted in space" % name)
        else:
            raise KeyError("Ref '%s' does not exist" % name)

    # ----------------------------------------------------------------------
    # Pandas I/O

    def to_frame(self):

        from modelx.io.pandas import space_to_dataframe

        return space_to_dataframe(self)


class Space(SpaceContainer):
    """Container for cells and other objects referred in formulas.
    """

    # ----------------------------------------------------------------------
    # Manipulating cells

    def new_cells(self, name=None, func=None):
        """Create a cells in the space.

        Args:
            name: If omitted, the model is named automatically ``CellsN``,
                where ``N`` is an available number.
            func: The function to define the formula of the cells.

        Returns:
            The new cells.
        """
        # Outside formulas only
        return self._impl.new_cells(name, func).interface

    @property
    def cells(self):
        """A mapping of cells names to the cells objects in the space."""
        return self._impl.cells.interfaces

    @property
    def self_cells(self):
        """A mapping that associates names to cells defined in the space"""
        return self._impl.self_cells.interfaces

    @property
    def derived_cells(self):
        """A mapping associating names to derived cells."""
        return self._impl.derived_cells.interfaces

    @property
    def static_spaces(self):
        """A mapping associating names to static spaces."""
        return self._impl.static_spaces.interfaces

    @property
    def dynamic_spaces(self):
        """A mapping associating names to dynamic spaces."""
        return self._impl.dynamic_spaces.interfaces

    @property
    def argvalues(self):
        """A tuple of space arguments."""
        return self._impl.argvalues

    @property
    def parameters(self):
        """A tuple of parameter strings."""
        # TODO: Refactor out parameter methods common between Space and Cells.
        return tuple(self._impl.parameters.keys())

    @property
    def refs(self):
        """A map associating names to objects accessible by the names."""
        return self._impl.refs.mproxy

    def new_cells_from_module(self, module_):
        """Create a cells from a module."""
        # Outside formulas only

        newcells = self._impl.new_cells_from_module(module_)
        return get_interfaces(newcells)

    def new_cells_from_excel(self, book, range_, sheet=None,
                                names_row=None, param_cols=None,
                                param_order=None,
                                transpose=False,
                                names_col=None, param_rows=None):
        """Create multiple cells from an Excel range.

        This method reads values from a range in an Excel file,
        create cells and populate them with the values in the range.
        To use this method, ``openpyxl`` package must be installed.

        The Excel file to read data from is specified by ``book``
        parameters. The ``range_`` can be a range address, such as "$G4:$K10",
        or a named range. In case a range address is given,
        ``sheet`` must also be given.

        By default, cells data are interpreted as being laid out side-by-side.
        ``names_row`` is a row index (starting from 0) to specify the
        row that contains the names of cells and parameters.
        Cells and parameter names must be contained in a single row.
        ``param_cols`` accepts a sequence (such as list or tuple) of
        column indexes (starting from 0) that indicate columns that
        contain cells arguments.

        **2-dimensional cells definitions**

        The optional ``names_col`` and ``param_rows`` parameters are used,
        when data for one cells spans more than one column.
        In such cases, the cells data is 2-dimensional, and
        there must be parameter row(s) across the columns
        that contain arguments of the parameters.
        A sequence of row indexes that indicate parameter rows
        is passed to ``param_rows``.
        The names of those parameters must be contained in the
        same rows as parameter values (arguments), and
        ``names_col`` is to indicate the column position at which
        the parameter names are defined.

        **Horizontal arrangement**

        By default, cells data are interpreted as being placed
        side-by-side, regardless of whether one cells corresponds
        to a single column or multiple columns.
        ``transpose`` parameter is used to alter this orientation,
        and if it is set to ``True``, cells values are
        interpreted as being placed one above the other.
        "row(s)" and "col(s)" in the parameter
        names are interpreted inversely, i.e.
        all indexes passed to "row(s)" parameters are interpreted
        as column indexes,
        and all indexes passed to "col(s)" parameters as row indexes.


        Args:
            book (str): Path to an Excel file.
            range_ (str): Range expression, such as "A1", "$G4:$K10",
                or named range "NamedRange1".
            sheet (str): Sheet name (case ignored).
            names_row (optional): an index number indicating
                what row contains the names of cells and parameters.
                Defaults to the top row (0).
            param_cols (optional): a sequence of index numbers
                indicating parameter columns.
                Defaults to only the leftmost column ([0]).
            names_col (optional): an index number, starting from 0,
                indicating what column contains additional parameters.
            param_rows (optional): a sequence of index numbers, starting from
                0, indicating rows of additional parameters, in case cells are
                defined in two dimensions.
            transpose (optional): Defaults to ``False``.
                If set to ``True``, "row(s)" and "col(s)" in the parameter
                names are interpreted inversely, i.e.
                all indexes passed to "row(s)" parameters are interpreted
                as column indexes,
                and all indexes passed to "col(s)" parameters as row indexes.
            param_order (optional): a sequence to reorder the parameters.
                The elements of the sequence are the indexes of ``param_cols``
                elements, and optionally the index of ``param_rows`` elements
                shifted by the length of ``param_cols``.
        """
        return self._impl.new_cells_from_excel(
            book, range_, sheet, names_row, param_cols,
            param_order, transpose,
            names_col, param_rows)

    # ----------------------------------------------------------------------
    # Checking containing subspaces and cells

    def __contains__(self, item):
        """Check if item is in the space.

        item can be either a cells or space.

        Args:
            item: a cells or space to check.

        Returns:
            True if item is a direct child of the space, False otherwise.
        """

        if isinstance(item, Cells):
            return item._impl in self._impl._cells.values()

        elif isinstance(item, Space):
            return item._impl in self._impl.spaces.values()

    # ----------------------------------------------------------------------
    # Getting and setting attributes

    def __getattr__(self, name):
        return self._impl.namespace[name]

    def __setattr__(self, name, value):
        if name in self.properties:
            object.__setattr__(self, name, value)
        else:
            self._impl.set_attr(name, value)

    def __delattr__(self, name):
        self._impl.del_attr(name)

    # ----------------------------------------------------------------------
    # Manipulating subspaces

    def has_params(self):
        """Check if the parameter function is set."""
        # Outside formulas only
        return bool(self.signature)

    def __getitem__(self, args):
        return self._impl.get_dyn_space(args).interface

    def __call__(self, *args, **kwargs):
        return self._impl.get_dyn_space(args, kwargs).interface

    def set_paramfunc(self, paramfunc):
        """Set if the parameter function."""
        self._impl.set_paramfunc(paramfunc)

    # ----------------------------------------------------------------------
    # Conversion to Pandas objects

    def to_frame(self):
        """Convert the space itself into a Pandas DataFrame object."""
        return self._impl.to_frame()

    @property
    def frame(self):
        """Alias of ``to_frame()``."""
        return self._impl.to_frame()


