import unittest
from unittest.mock import patch, MagicMock, call
import os
import tempfile
import shutil
from llama_tools_aisee.push_gguf import push_gguf


class TestPushGGUF(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary GGUF file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_gguf_path = os.path.join(self.temp_dir, "test_model.gguf")
        with open(self.test_gguf_path, "wb") as f:
            f.write(b"fake gguf content for testing")
        
        self.repo_id = "test-user/test-model"
        self.local_repo_dir = os.path.join(self.temp_dir, "test_repo")

    def tearDown(self):
        """Clean up after each test method."""
        shutil.rmtree(self.temp_dir)

    @patch('llama_tools_aisee.push_gguf.whoami')
    @patch('llama_tools_aisee.push_gguf.Repository')
    @patch('llama_tools_aisee.push_gguf.shutil.copy')
    @patch('llama_tools_aisee.push_gguf.os.path.isdir')
    @patch('llama_tools_aisee.push_gguf.os.path.exists')
    def test_push_gguf_new_repo_clone(self, mock_exists, mock_isdir, mock_copy, mock_repository, mock_whoami):
        """Test pushing GGUF when local repo doesn't exist (new clone scenario)."""
        # Setup mocks
        mock_whoami.return_value = {"name": "test-user"}
        mock_isdir.return_value = False  # .git directory doesn't exist
        mock_exists.return_value = False  # local_repo_dir doesn't exist
        
        mock_repo = MagicMock()
        mock_repository.return_value = mock_repo
        
        # Call the function
        push_gguf(self.repo_id, self.test_gguf_path, self.local_repo_dir)
        
        # Verify authentication check
        mock_whoami.assert_called_once()
        
        # Verify repository cloning (new repo scenario)
        mock_repository.assert_called_once_with(
            local_dir=self.local_repo_dir,
            clone_from=self.repo_id,
            use_auth_token=True
        )
        
        # Verify file copy
        mock_copy.assert_called_once_with(
            self.test_gguf_path,
            os.path.join(self.local_repo_dir, "test_model.gguf")
        )
        
        # Verify push to hub
        mock_repo.push_to_hub.assert_called_once_with(commit_message="Upload test_model.gguf")

    @patch('llama_tools_aisee.push_gguf.whoami')
    @patch('llama_tools_aisee.push_gguf.Repository')
    @patch('llama_tools_aisee.push_gguf.shutil.copy')
    @patch('llama_tools_aisee.push_gguf.shutil.rmtree')
    @patch('llama_tools_aisee.push_gguf.os.path.isdir')
    @patch('llama_tools_aisee.push_gguf.os.path.exists')
    def test_push_gguf_existing_dir_not_git(self, mock_exists, mock_isdir, mock_rmtree, mock_copy, mock_repository, mock_whoami):
        """Test pushing GGUF when local directory exists but is not a git repo."""
        # Setup mocks
        mock_whoami.return_value = {"name": "test-user"}
        mock_isdir.return_value = False  # .git directory doesn't exist
        mock_exists.return_value = True   # local_repo_dir exists but isn't git repo
        
        mock_repo = MagicMock()
        mock_repository.return_value = mock_repo
        
        # Call the function
        push_gguf(self.repo_id, self.test_gguf_path, self.local_repo_dir)
        
        # Verify the existing directory is removed
        mock_rmtree.assert_called_once_with(self.local_repo_dir)
        
        # Verify new repository clone
        mock_repository.assert_called_once_with(
            local_dir=self.local_repo_dir,
            clone_from=self.repo_id,
            use_auth_token=True
        )

    @patch('llama_tools_aisee.push_gguf.whoami')
    @patch('llama_tools_aisee.push_gguf.Repository')
    @patch('llama_tools_aisee.push_gguf.shutil.copy')
    @patch('llama_tools_aisee.push_gguf.os.path.isdir')
    def test_push_gguf_existing_git_repo(self, mock_isdir, mock_copy, mock_repository, mock_whoami):
        """Test pushing GGUF when local git repository already exists."""
        # Setup mocks
        mock_whoami.return_value = {"name": "test-user"}
        mock_isdir.return_value = True  # .git directory exists
        
        mock_repo = MagicMock()
        mock_repository.return_value = mock_repo
        
        # Call the function
        push_gguf(self.repo_id, self.test_gguf_path, self.local_repo_dir)
        
        # Verify repository initialization for existing repo
        mock_repository.assert_called_once_with(local_dir=self.local_repo_dir)
        
        # Verify git pull is called
        mock_repo.git_pull.assert_called_once()
        
        # Verify file copy
        mock_copy.assert_called_once_with(
            self.test_gguf_path,
            os.path.join(self.local_repo_dir, "test_model.gguf")
        )
        
        # Verify push to hub
        mock_repo.push_to_hub.assert_called_once_with(commit_message="Upload test_model.gguf")

    @patch('llama_tools_aisee.push_gguf.subprocess.run')
    @patch('llama_tools_aisee.push_gguf.whoami')
    @patch('llama_tools_aisee.push_gguf.Repository')
    @patch('llama_tools_aisee.push_gguf.shutil.copy')
    @patch('llama_tools_aisee.push_gguf.os.path.isdir')
    def test_push_gguf_authentication_required(self, mock_isdir, mock_copy, mock_repository, mock_whoami, mock_subprocess_run):
        """Test pushing GGUF when authentication is required."""
        # Setup mocks - whoami fails first time, succeeds after login
        mock_whoami.side_effect = [Exception("Not authenticated"), {"name": "test-user"}]
        mock_isdir.return_value = True
        
        mock_repo = MagicMock()
        mock_repository.return_value = mock_repo
        
        # Call the function
        push_gguf(self.repo_id, self.test_gguf_path, self.local_repo_dir)
        
        # Verify authentication flow
        self.assertEqual(mock_whoami.call_count, 1)  # Called once, failed
        mock_subprocess_run.assert_called_once_with(["huggingface-cli", "login"], check=True)

    @patch('llama_tools_aisee.push_gguf.whoami')
    @patch('llama_tools_aisee.push_gguf.Repository')
    @patch('llama_tools_aisee.push_gguf.shutil.copy')
    @patch('llama_tools_aisee.push_gguf.os.path.isdir')
    @patch('builtins.print')
    def test_push_gguf_success_message(self, mock_print, mock_isdir, mock_copy, mock_repository, mock_whoami):
        """Test that success message is printed correctly."""
        # Setup mocks
        mock_whoami.return_value = {"name": "test-user"}
        mock_isdir.return_value = True
        
        mock_repo = MagicMock()
        mock_repository.return_value = mock_repo
        
        # Call the function
        push_gguf(self.repo_id, self.test_gguf_path, self.local_repo_dir)
        
        # Verify success message
        mock_print.assert_called_once_with(
            f"Uploaded `test_model.gguf` to https://huggingface.co/{self.repo_id}"
        )

    @patch('llama_tools_aisee.push_gguf.whoami')
    @patch('llama_tools_aisee.push_gguf.Repository')
    @patch('llama_tools_aisee.push_gguf.shutil.copy')
    @patch('llama_tools_aisee.push_gguf.os.path.isdir')
    def test_push_gguf_default_local_repo_dir(self, mock_isdir, mock_copy, mock_repository, mock_whoami):
        """Test push_gguf with default local repo directory."""
        # Setup mocks
        mock_whoami.return_value = {"name": "test-user"}
        mock_isdir.return_value = True
        
        mock_repo = MagicMock()
        mock_repository.return_value = mock_repo
        
        # Call the function without specifying local_repo_dir
        push_gguf(self.repo_id, self.test_gguf_path)
        
        # Verify default directory is used
        mock_repository.assert_called_once_with(local_dir="./hf_tmp_repo")
        
        # Verify file copy uses default directory
        mock_copy.assert_called_once_with(
            self.test_gguf_path,
            os.path.join("./hf_tmp_repo", "test_model.gguf")
        )

    @patch('llama_tools_aisee.push_gguf.whoami')
    @patch('llama_tools_aisee.push_gguf.Repository')
    @patch('llama_tools_aisee.push_gguf.shutil.copy')
    @patch('llama_tools_aisee.push_gguf.os.path.isdir')
    def test_push_gguf_filename_extraction(self, mock_isdir, mock_copy, mock_repository, mock_whoami):
        """Test that filename is correctly extracted from path."""
        # Setup mocks
        mock_whoami.return_value = {"name": "test-user"}
        mock_isdir.return_value = True
        
        mock_repo = MagicMock()
        mock_repository.return_value = mock_repo
        
        # Test with a complex path
        complex_path = "/path/to/models/my-complex-model-name.gguf"
        
        # Call the function
        push_gguf(self.repo_id, complex_path, self.local_repo_dir)
        
        # Verify correct filename extraction
        mock_copy.assert_called_once_with(
            complex_path,
            os.path.join(self.local_repo_dir, "my-complex-model-name.gguf")
        )
        
        # Verify commit message uses correct filename
        mock_repo.push_to_hub.assert_called_once_with(commit_message="Upload my-complex-model-name.gguf")


if __name__ == "__main__":
    unittest.main()