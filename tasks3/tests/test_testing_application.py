import os
import tasks3 as tm


def _prepare_tmp(monkeypatch, tmp_path):
    tmpdir = tmp_path / "data"
    tmpdir.mkdir()
    monkeypatch.setattr(tm, "DATA_DIR", str(tmpdir))
    monkeypatch.setattr(tm, "DATA_FILE", str(tmpdir / "tasks.json"))


def test_add_and_read(monkeypatch, tmp_path):
    _prepare_tmp(monkeypatch, tmp_path)

    tm.add_task("Test Task 1", "Description for task 1", tags=["test", "task"])
    tm.add_task("Test Task 2", "Description for task 2", tags=["task"])

    tasks = tm.read_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Test Task 1"
    assert tasks[0].description == "Description for task 1"
    assert tasks[0].tags == ["test", "task"]


def test_search_and_filter(monkeypatch, tmp_path):
    _prepare_tmp(monkeypatch, tmp_path)

    tm.add_task("Buy milk", "from store", tags=["groceries"])
    tm.add_task("Read book", "novel", tags=["leisure"])

    # programmatic search using read_tasks (search_tasks prints results)
    tasks = tm.read_tasks()
    q = "milk"
    results = [t for t in tasks if q in t.title.lower() or q in (t.description or "").lower() or any(q in ta.lower() for ta in (t.tags or []))]
    assert len(results) == 1 and results[0].title == "Buy milk"

    # filter by tag
    groceries = [t for t in tasks if "groceries" in (t.tags or [])]
    assert len(groceries) == 1 and groceries[0].title == "Buy milk"