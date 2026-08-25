from tools.files import create_folder

def test_create_folder(tmp_path):
    folder = tmp_path / "ultron_test"
    create_folder(str(folder))
    assert folder.exists()
