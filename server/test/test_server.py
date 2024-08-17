import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from server import app

client = TestClient(app)

@pytest.fixture
def temp_dir(tmp_path):
    temp_dir = tmp_path / "temp"
    temp_dir.mkdir()
    yield temp_dir
    for item in temp_dir.iterdir():
        if item.is_file():
            item.unlink()

    server_base_dir = tmp_path / "server_base"
    server_base_dir.mkdir()

    audiobooks_dir = server_base_dir / "audiobooks"
    audiobooks_dir.mkdir()

    server_file_path = audiobooks_dir / "files.txt"
    with server_file_path.open("w") as f:
        f.write("file1.mp3\nfile2.mp3\nfile3.mp3\n")

    return tmp_path

def test_write_file(temp_dir):
    file_path = temp_dir / "test.txt"
    response = client.post("/write", json={"file_path": str(file_path), "content": "Hello, World!"})
    assert response.status_code == 200
    assert response.json() == {"message": "File written successfully!"}
    assert file_path.exists()
    with file_path.open("r") as file:
        content = file.read()
    assert content == "Hello, World!"

def test_delete_file(temp_dir):
    file_path = temp_dir / "test.txt"
    with file_path.open("w") as file:
        file.write("This file will be deleted.")
    response = client.delete("/delete", json={"file_path": str(file_path)})
    assert response.status_code == 200
    assert response.json() == {"message": "File deleted successfully!"}
    assert not file_path.exists()

def test_delete_file_not_found(temp_dir):
    file_path = temp_dir / "non_existent.txt"
    response = client.delete("/delete", json={"file_path": str(file_path)})
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}

def test_list_files(temp_dir):
    file_path_1 = temp_dir / "file1.txt"
    file_path_2 = temp_dir / "file2.txt"
    file_path_1.touch()
    file_path_2.touch()
    response = client.get(f"/list?directory_path={str(temp_dir)}")
    assert response.status_code == 200
    files = response.json()["files"]
    assert len(files) == 2
    assert str(file_path_1) in files
    assert str(file_path_2) in files

def test_list_files_directory_not_found():
    response = client.get("/list?directory_path=/non_existent_directory")
    assert response.status_code == 404
    assert response.json() == {"detail": "Directory not found"}

def test_diff(setup_files, tmp_path):
    user_file_path = tmp_path / "files.txt"
    with user_file_path.open("w") as f:
        f.write("file1.mp3\nfile2.mp3\n")  # file3.mp3 is missing

    app.dependency_overrides[Path] = lambda: setup_files

    with open(user_file_path, "rb") as user_file:
        response = client.post("/compare-files/", files={"file": ("audiobooks/files.txt", user_file)})

    assert response.status_code == 200
    assert response.json() == {"missing_files": ["file3.mp3"]}

def test_compare_files_no_missing_files(setup_files, tmp_path):
    user_file_path = tmp_path / "files.txt"
    with user_file_path.open("w") as f:
        f.write("file1.mp3\nfile2.mp3\nfile3.mp3\n")

    app.dependency_overrides[Path] = lambda: setup_files

    with open(user_file_path, "rb") as user_file:
        response = client.post("/compare-files/", files={"file": ("audiobooks/files.txt", user_file)})

    assert response.status_code == 200
    assert response.json() == {"missing_files": []}

def test_compare_files_server_file_not_found(setup_files, tmp_path):
    user_file_path = tmp_path / "files.txt"
    with user_file_path.open("w") as f:
        f.write("file1.mp3\nfile2.mp3\nfile3.mp3\n")

    app.dependency_overrides[Path] = lambda: tmp_path / "non_existent_directory"

    with open(user_file_path, "rb") as user_file:
        response = client.post("/compare-files/", files={"file": ("audiobooks/files.txt", user_file)})

    assert response.status_code == 404
    assert response.json() == {"detail": "Server file not found"}
