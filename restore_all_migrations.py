#!/usr/bin/env python
import os
import sys

def restore_migration_files():
    """Восстановить все необходимые файлы миграций"""
    
    # Найдем путь к Django
    django_path = None
    for path in sys.path:
        possible_path = os.path.join(path, 'django', 'db', 'migrations')
        if os.path.exists(possible_path):
            django_path = possible_path
            break
    
    if not django_path:
        print("Не найден путь к Django migrations!")
        return False
    
    print(f"Восстанавливаем файлы в: {django_path}")
    
    # 1. Создаем migration.py если нет
    migration_py = os.path.join(django_path, 'migration.py')
    if not os.path.exists(migration_py):
        print("Создаем migration.py...")
        with open(migration_py, 'w') as f:
            f.write('''
"""
Migration classes and utilities.
"""
import warnings

__all__ = ["Migration", "swappable_dependency"]


class Migration:
    """
    The base class for all migrations.
    """
    operations = []
    dependencies = []
    run_before = []
    replaces = []
    atomic = True

    def __init__(self, name, app_label):
        self.name = name
        self.app_label = app_label
        self.operations = list(self.__class__.operations)
        self.dependencies = list(self.__class__.dependencies)
        self.run_before = list(self.__class__.run_before)
        self.replaces = list(self.__class__.replaces)

    def __eq__(self, other):
        return (
            isinstance(other, Migration)
            and self.name == other.name
            and self.app_label == other.app_label
        )

    def __repr__(self):
        return "<Migration %s.%s>" % (self.app_label, self.name)

    def __hash__(self):
        return hash("%s.%s" % (self.app_label, self.name))

    def __str__(self):
        return "%s.%s" % (self.app_label, self.name)

    def mutate_state(self, project_state, preserve=True):
        new_state = project_state
        if preserve:
            new_state = project_state.clone()
        for operation in self.operations:
            operation.state_forwards(self.app_label, new_state)
        return new_state

    def apply(self, project_state, schema_editor, collect_sql=False):
        for operation in self.operations:
            old_state = project_state.clone()
            operation.state_forwards(self.app_label, project_state)
            if not schema_editor.connection.features.can_rollback_ddl and operation.atomic:
                warnings.warn(
                    "This database doesn't support transactional DDL. "
                    "Migrations will be applied in a single transaction.",
                    RuntimeWarning,
                )
            executed = False
            if not collect_sql:
                with schema_editor.connection.cursor() as cursor:
                    executed = True
                    operation.database_forwards(
                        self.app_label, schema_editor, old_state, project_state
                    )
            if not executed:
                operation.database_forwards(
                    self.app_label, schema_editor, old_state, project_state
                )
        return project_state

    def unapply(self, project_state, schema_editor, collect_sql=False):
        state = project_state.clone()
        operations = list(self.operations)
        operations.reverse()
        for operation in operations:
            old_state = state.clone()
            operation.state_forwards(self.app_label, state)
            if not schema_editor.connection.features.can_rollback_ddl and operation.atomic:
                warnings.warn(
                    "This database doesn't support transactional DDL. "
                    "Migrations will be applied in a single transaction.",
                    RuntimeWarning,
                )
            executed = False
            if not collect_sql:
                with schema_editor.connection.cursor() as cursor:
                    executed = True
                    operation.database_backwards(
                        self.app_label, schema_editor, old_state, state
                    )
            if not executed:
                operation.database_backwards(
                    self.app_label, schema_editor, old_state, state
                )
        return state


def swappable_dependency(value):
    """Turn a setting value into a dependency."""
    from django.conf import settings
    if value is None:
        return []
    if value == settings.AUTH_USER_MODEL:
        return [("auth", "user")]
    app_label, model_name = value.lower().split(".", 1)
    return [(app_label, model_name)]
''')
    
    # 2. Обновим __init__.py
    init_py = os.path.join(django_path, '__init__.py')
    with open(init_py, 'w') as f:
        f.write('''
"""
Django migrations support.
"""
from .migration import Migration, swappable_dependency

__all__ = ["Migration", "swappable_dependency"]
''')
    
    # 3. Проверим папку operations
    ops_path = os.path.join(django_path, 'operations')
    if not os.path.exists(ops_path):
        os.makedirs(ops_path, exist_ok=True)
    
    # 4. Создаем __init__.py в operations
    ops_init = os.path.join(ops_path, '__init__.py')
    if not os.path.exists(ops_init):
        with open(ops_init, 'w') as f:
            f.write('''
"""
Migration operation classes.
"""
from .base import Operation

__all__ = ["Operation"]
''')
    
    # 5. Создаем base.py в operations
    base_py = os.path.join(ops_path, 'base.py')
    if not os.path.exists(base_py):
        with open(base_py, 'w') as f:
            f.write('''
"""
Base classes for migration operations.
"""
class Operation:
    """Base class for all migration operations."""
    reversible = True
    atomic = True
    
    def __init__(self, model_name=None, name=None):
        self.model_name = model_name
        self.name = name
    
    def state_forwards(self, app_label, state):
        raise NotImplementedError(
            "subclasses of Operation must provide a state_forwards() method"
        )
    
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        raise NotImplementedError(
            "subclasses of Operation must provide a database_forwards() method"
        )
    
    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        raise NotImplementedError(
            "subclasses of Operation must provide a database_backwards() method"
        )
    
    def describe(self):
        return "Operation"
    
    def __eq__(self, other):
        return (
            isinstance(other, Operation) and
            self.model_name == other.model_name and
            self.name == other.name
        )
    
    def __repr__(self):
        return "<%s model_name=%r name=%r>" % (
            self.__class__.__name__,
            self.model_name,
            self.name,
        )
''')
    
    print("\n✓ Все необходимые файлы созданы!")
    return True

if __name__ == "__main__":
    print("=== Восстановление файлов миграций Django ===")
    if restore_migration_files():
        print("\nТеперь проверьте работу Django:")
        print("python manage.py check --version")
    else:
        print("\nНе удалось восстановить файлы")
