import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import os
import subprocess
from visualize_dependencies import get_commit_files, generate_plantuml_graph, save_plantuml_graph

class TestGetCommitFiles(unittest.TestCase):

    @patch('os.chdir')
    @patch('subprocess.check_output')
    def test_get_commit_files(self, mock_check_output, mock_chdir):
        # Настройка mock
        mock_chdir.return_value = None
        mock_check_output.return_value = "commit_hash\nfile1\nfile2\n\ncommit_hash2\nfile3"

        expected_files_dict = {
            "commit_hash": ["file1", "file2"],
            "commit_hash2": ["file3"]
        }

        files_dict = get_commit_files('C:/Users/Kimesun/Projects/my-repo', 'main')

        self.assertEqual(files_dict, expected_files_dict)
        mock_chdir.assert_called_once_with('C:/Users/Kimesun/Projects/my-repo')
        mock_check_output.assert_called_once_with(
            ["git", "log", "--name-only", "--pretty=format:%H", 'main'],
            encoding='utf-8'
        )

class TestGeneratePlantUMLGraph(unittest.TestCase):
    def test_generate_plantuml_graph(self):
        files_dict = {
            "commit_hash": ["file1", "file2"],
            "commit_hash2": ["file3"]
        }
        expected_output = (
            "@startuml\n"
            "\"commit_hash\" --> \"file1\"\n"
            "\"commit_hash\" --> \"file2\"\n"
            "\"commit_hash2\" --> \"file3\"\n"
            "@enduml"
        )

        plantuml_graph = generate_plantuml_graph(files_dict)
        self.assertEqual(plantuml_graph, expected_output)

class TestSavePlantUMLGraph(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.run')
    @patch('os.rename')
    def test_save_plantuml_graph(self, mock_rename, mock_subprocess_run, mock_open):
        plantuml_graph = "@startuml\n@enduml"
        output_path = 'fake_output_path/graph.png'

        save_plantuml_graph(plantuml_graph, output_path)

        # Проверка открытия файла и записи в него
        mock_open.assert_called_once_with('graph.puml', 'w')
        mock_open().write.assert_called_once_with(plantuml_graph)

        # Проверка вызова subprocess.run
        mock_subprocess_run.assert_called_once_with(
            ["java", "-jar", "d:/dz2/plantuml.jar", 'graph.puml'], check=True
        )

        # Проверка переименования файла
        mock_rename.assert_called_once_with('graph.png', output_path)


if __name__ == '__main__':
    unittest.main()
