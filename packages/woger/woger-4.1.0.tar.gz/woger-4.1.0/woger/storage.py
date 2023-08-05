import warnings
from operator import attrgetter, itemgetter
from typing import List, Optional, Iterable, Type

import os

from .base_data import BaseData
from .base_path_structure import BasePathStructure
from .workspace import Workspace


class WorkspaceStorage:
    """Stores workspaces"""
    
    def _init_workspaces(self, workspaces):
        if workspaces is None:
            workspaces = []
        else:
            try:
                workspaces = list(workspaces)
            except TypeError:
                raise ValueError('Invalid list of workspaces')

            for ws in workspaces:
                if not isinstance(ws, Workspace):
                    raise ValueError('Invalid list of workspaces')
        
        return workspaces
        
    def __init__(self, workspaces: Optional[Iterable[Workspace]] = None, limit: Optional[int] = None):
        """Creates a WorkspaceStorage object
        
        Attributes
        ----------
        workspaces: list of Workspaces
        limit: int
            Maximum number of workspaces
        """
        workspaces = self._init_workspaces(workspaces)
        
        if limit is None:
            limit = float('+inf')

        self.workspaces = [
            (ws.id, ws)
            for ws
            in sorted(workspaces, key=attrgetter('id'))
        ]

        self.limit = limit

        if len(self.workspaces) > self.limit:
            warnings.warn('Workspace count is greater than limit')

    @classmethod
    def load_from_directory(cls,
                            root,
                            *,
                            path_structure_cls=None,
                            data_cls=None,
                            workspace_cls=None):
        """Creates a workspaces instance and loads 
        all the workspaces from the `root` path
        
        Attributes
        ----------
        root: str
            Storage root path
        path_structure_cls: BasePathStructure class object
        data_cls: BaseData class object
        workspace_cls: Workspace class object
        
        """
        if workspace_cls is None:
            workspace_cls = Workspace
        if data_cls is None:
            data_cls = BaseData
        if path_structure_cls is None:
            path_structure_cls = BasePathStructure

        return WorkspaceStorage(_construct_workspaces(
            str(root),
            path_structure_cls,
            data_cls,
            workspace_cls,
        ))

    def __iter__(self):
        yield from self.keys()

    def keys(self):
        yield from (key for key, _ in self.workspaces)

    def values(self) -> List[Workspace]:
        yield from (value for _, value in self.workspaces)

    def items(self):
        yield from self.workspaces

    def __getitem__(self, item) -> Optional[Workspace]:
        """Gets workspace from storage by id"""
        workspaces = dict(self.workspaces)
        return workspaces[item] if item in workspaces else None

    def at(self, index) -> Optional[Workspace]:
        """Gets workspace from storage by index

        To get the oldest workspace use index 0
        To get the latest workspace use index -1
        """
        if index >= len(self.workspaces):
            return None

        pair = self.workspaces[index]
        return pair[1]

    def add(self, workspace: Workspace):
        """Add a workspace

        Parameters
        ----------
        workspace: Workspace
            Workspace to be added
        """
        if not isinstance(workspace, Workspace):
            raise ValueError('Value must be of type {}'.format(Workspace.__name__))

        pair = (workspace.id, workspace)

        workspaces = list(self.workspaces)
        workspaces.append(pair)
        workspaces = sorted(workspaces, key=itemgetter(0))
        self.workspaces = workspaces

    def __repr__(self):
        return '<WorkspaceStorage {}>'.format(list(self.keys()))

    def __len__(self):
        return len(self.workspaces)


def _construct_workspaces(root,
                          path_structure_cls: Type[BasePathStructure],
                          data_cls: Type[BaseData],
                          workspace_cls: Type[Workspace]):
    path_list = (
        os.path.join(root, name)
        for name
        in os.listdir(root)
    )
    filtered = filter(os.path.isdir, path_list)
    return [
        workspace_cls.construct(
            path,
            path_structure_cls,
            data_cls,
        )
        for path
        in filtered
    ]
