---
layout: default
title: IsaacGymEnv Env Notes
parent: Isaac
nav_order: 8
---

# 6. Creating an Env in IsaacGymEnv

In order to understand how to create an environment in IsaacGymEnv, we take a look at the Abstract Base Class (ABC) in IsaacGymEnv.

```python
class FactoryABCEnv(ABC):
    @abstractmethod
    def __init__(self):
        """Initialize instance variables. Initialize base superclass. Acquire tensors."""
    @abstractmethod
    def _get_env_yaml_params(self):
        """Initialize instance variables from YAML files."""
    @abstractmethod
    def create_envs(self):
        """Set env options. Import assets. Create actors."""
    @abstractmethod
    def _import_env_assets(self):
        """Set asset options. Import assets."""
    @abstractmethod
    def _create_actors(self):
        """Set initial actor poses. Create actors. Set shape and DOF properties."""
    @abstractmethod
    def _acquire_env_tensors(self):
        """Acquire and wrap tensors. Create views."""
    @abstractmethod
    def refresh_env_tensors(self):
        """Refresh tensors."""
        # NOTE: Tensor refresh functions should be called once per step, before setters.
```

Here's a breakdown of how  these methods will be used:
- `_get_env_yaml_params`: this is called in `__init__` of the class that defines the method.
- `create_envs`: this will be called by `FactoryBase` instead of the subclass.
- `_import_env_assets`: called inside `create_envs` to import assets.
- `_create_actors`: called inside `create_envs` to create actors.
- `_acquire_env_tensors`: called in `__init__` of the class that defines the method.
- `refresh_env_tensors`: use it whenever you want environment tensors to match simulation context.

