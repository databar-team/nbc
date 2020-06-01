import pytest

from pathlib import Path


@pytest.fixture
def test_context():
    from config.context import WorkQueueContext

    test_path = './test_queue/{}'

    return WorkQueueContext(
        TYPE='filesystem',
        PATH=test_path
    )


@pytest.fixture
def test_queue(test_context):
    from util.queue.filesystem import FileSystemWorkQueue
    queue = FileSystemWorkQueue(test_context)
    yield queue
    import shutil
    shutil.rmtree(queue.context.PATH)


def test_work_queue_put(test_queue):
    # Given
    file_name = "test.txt"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_put")
    expected = (True, None)

    # When
    actual = test_queue.put(file_name)

    # Then
    assert actual == expected
    assert Path(test_queue.context.PATH, file_name).exists()


def test_work_queue_put_already_exists(test_queue):
    # Given
    file_name = "test"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_put_already_exists")
    expected = (False, "unlocked item already exists")
    path = Path(test_queue.context.PATH, file_name)
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=False)

    # When
    actual = test_queue.put(file_name)

    # Then
    assert actual == expected
    assert path.exists()


def test_work_queue_put_lock_already_exists(test_queue):
    # Given
    file_name = "test"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_put_lock_already_exists")
    expected = (False, "locked item already exists")
    path = Path(test_queue.context.PATH, f'{file_name}.lock')
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=False)

    # When
    actual = test_queue.put(file_name)

    # Then
    assert actual == expected
    assert not Path(test_queue.context.PATH, file_name).exists()
    assert path.exists()


def test_work_queue_get(test_queue):
    # Given
    file_name = "test"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_get")
    expected = file_name
    path = Path(test_queue.context.PATH, file_name)
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=False)

    # When
    actual = test_queue.get()

    # Then
    assert actual == expected
    assert not path.exists()
    assert Path(test_queue.context.PATH, f'{file_name}.lock').exists()


def test_work_queue_get_empty(test_queue):
    # Given
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_get_empty")
    expected = None
    dir_path = Path(test_queue.context.PATH)
    dir_path.mkdir(parents=True, exist_ok=True)

    # When
    actual = test_queue.get()

    # Then
    assert actual == expected
    assert len([i for i in dir_path.iterdir()]) == 0


def test_work_queue_get_only_item_locked(test_queue):
    # Given
    file_name = "test.lock"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_get_only_item_locked")
    expected = None
    path = Path(test_queue.context.PATH, file_name)
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=False)

    # When
    actual = test_queue.get()

    # Then
    assert actual == expected
    assert path.exists()


def test_work_queue_get_one_locked_one_ready(test_queue):
    # Given
    unlocked_file = "unlocked_file"
    lock_file = "lock_file.lock"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_get_one_locked_one_ready")
    expected_one = unlocked_file
    expected_two = None
    unlocked_path = Path(test_queue.context.PATH, unlocked_file)
    locked_path = Path(test_queue.context.PATH, lock_file)
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)
    unlocked_path.touch(exist_ok=False)
    locked_path.touch(exist_ok=False)

    # When
    actual_one = test_queue.get()
    actual_two = test_queue.get()

    # Then
    assert actual_one == expected_one
    assert actual_two == expected_two
    assert not unlocked_path.exists()
    assert Path(test_queue.context.PATH, f'{unlocked_file}.lock').exists()
    assert locked_path.exists()


def test_work_queue_done(test_queue):
    # Given
    file_name = "test"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_done")
    expected = True
    path = Path(test_queue.context.PATH, f'{file_name}.lock')
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=False)

    # When
    actual = test_queue.done(file_name)

    # Then
    assert actual == expected
    assert not path.exists()


def test_work_queue_done_does_not_exist(test_queue):
    # Given
    file_name = "test"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_done")
    expected = False
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)

    # When
    actual = test_queue.done(file_name)

    # Then
    assert actual == expected


def test_work_queue_reset(test_queue):
    # Given
    file_name = "test"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_reset")
    expected = True
    path = Path(test_queue.context.PATH, f'{file_name}.lock')
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)

    # When
    path.touch()
    actual = test_queue.reset_work(file_name)

    # Then
    assert actual == expected


def test_work_queue_reset_fail(test_queue):
    # Given
    file_name = "test"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_reset")
    expected = False
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)

    # When
    actual = test_queue.reset_work(file_name)

    # Then
    assert actual == expected


def test_work_queue_work_exists(test_queue):
    # Given
    file_name = "test"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_work_exists")
    expected = False
    path = Path(test_queue.context.PATH, file_name)
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)

    # When
    path.touch()
    actual = test_queue.empty

    # Then
    assert actual == expected


def test_work_queue_work_exists_locked(test_queue):
    # Given
    file_name = "test"
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_work_exists")
    expected = True
    path = Path(test_queue.context.PATH, f'{file_name}.lock')
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)

    # When
    path.touch()
    actual = test_queue.empty

    # Then
    assert actual == expected


def test_work_queue_work_exists_false(test_queue):
    # Given
    test_queue.context.PATH = test_queue.context.PATH.format("test_work_queue_work_exists")
    expected = True
    Path(test_queue.context.PATH).mkdir(parents=True, exist_ok=True)

    # When
    actual = test_queue.empty

    # Then
    assert actual == expected
