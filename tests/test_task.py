import pytest
from src.exceptions import InvalidPriorityError, InvalidStateError, TaskError
from src.task import Task, TaskStatus

def test_task_creation():
    task = Task(id=1, payload={}, description="Test task")
    assert task.id == 1
    assert task.status == TaskStatus.NEW
    assert task.priority == 3
    assert task.description == "Test task"
    assert task.ready_for_execution

def test_task_priority_validation():
    task = Task(id=1, payload={}, description="Priority task")
    task.priority = 5
    assert task.priority == 5
    
    with pytest.raises(InvalidPriorityError):
        task.priority = 6
        
    with pytest.raises(InvalidPriorityError):
        task.priority = 0
        
    with pytest.raises(InvalidPriorityError):
        task.priority = "3"
        
    with pytest.raises(InvalidPriorityError):
        task.priority = True # bool is isinstance of int in python, so descriptor needs explicit check

def test_task_default_description():
    task = Task(id=1, payload={})
    assert task.description == "Без описания"
    
def test_task_state_transitions():
    task = Task(id=1, payload={})
    
    # New -> In Progress
    task.start()
    assert task.status == TaskStatus.IN_PROGRESS
    
    # In Progress -> Completed
    task.complete()
    assert task.status == TaskStatus.COMPLETED
    
def test_task_fail_transition():
    task = Task(id=1, payload={})
    task.start()
    task.fail()
    assert task.status == TaskStatus.FAILED

def test_invalid_state_transitions():
    task = Task(id=1, payload={})
    
    # Cannot complete a new task
    with pytest.raises(InvalidStateError):
        task.complete()
        
    task.start()
    task.complete()
    
    # Cannot start a completed task
    with pytest.raises(InvalidStateError):
        task.start()
        
    # Cannot fail a completed task
    with pytest.raises(InvalidStateError):
        task.fail()

def test_read_only_properties():
    task = Task(id=1, payload={})
    with pytest.raises(AttributeError):
        task.id = 2
        
    with pytest.raises(AttributeError):
        task.status = TaskStatus.IN_PROGRESS
        
    with pytest.raises(AttributeError):
        task.created_at = "now"

def test_ready_for_execution():
    task = Task(id=1, payload={})
    assert task.ready_for_execution
    
    task.start()
    assert not task.ready_for_execution
