import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
from llama_tools_aisee.setup_llama_cpp import setup_llama, clone_llama_cpp

class TestSetupLlama(unittest.TestCase):
    @patch("llama_tools_aisee.setup_llama_cpp.subprocess.run")
    @patch("llama_tools_aisee.setup_llama_cpp.Path.exists")
    def test_clone_llama_cpp(self, mock_path_exists, mock_run):
        # Mock the .git directory to not exist (fresh clone scenario)
        mock_path_exists.return_value = False
        
        clone_llama_cpp()
        self.assertTrue(mock_run.called)
        
        # Check that git clone command was called
        clone_call_found = False
        for call in mock_run.call_args_list:
            args = call[0][0]  # Get the command arguments
            if len(args) >= 3 and args[0] == "git" and args[1] == "clone":
                clone_call_found = True
                break
        
        self.assertTrue(clone_call_found, "git clone command should be called when repository doesn't exist")

    @patch("llama_tools_aisee.setup_llama_cpp.subprocess.run")
    @patch("llama_tools_aisee.setup_llama_cpp.clone_llama_cpp")
    @patch("llama_tools_aisee.setup_llama_cpp.shutil.which")
    def test_setup_llama_basic(self, mock_which, mock_clone, mock_run):
        """Test basic setup_llama functionality."""
        # Mock successful setup with proper Path object
        import tempfile
        import os
        from pathlib import Path
        
        # Create a temporary directory to use as mock repo path
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_repo_path = Path(temp_dir)
            # Create a fake CMakeLists.txt
            (mock_repo_path / "CMakeLists.txt").touch()
            
            mock_clone.return_value = mock_repo_path
            mock_which.return_value = "/usr/bin/cmake"  # Tools are available
            
            setup_llama(jobs=2, create_venv=False)
            
            # Verify clone was called
            mock_clone.assert_called_once_with(repo_dir="llama.cpp")
            
            # Verify cmake commands were run
            self.assertEqual(mock_run.call_count, 2)  # cmake config + cmake build

    @patch("llama_tools_aisee.setup_llama_cpp.subprocess.run")
    @patch("llama_tools_aisee.setup_llama_cpp.clone_llama_cpp")
    @patch("llama_tools_aisee.setup_llama_cpp.shutil.which")
    @patch("llama_tools_aisee.setup_llama_cpp.create_virtualenv")
    def test_setup_llama_with_venv(self, mock_create_venv, mock_which, mock_clone, mock_run):
        """Test setup_llama with venv creation - covers lines 76-77."""
        # Mock successful setup with proper Path object
        import tempfile
        from pathlib import Path
        
        # Create a temporary directory to use as mock repo path
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_repo_path = Path(temp_dir)
            # Create a fake CMakeLists.txt
            (mock_repo_path / "CMakeLists.txt").touch()
            
            mock_clone.return_value = mock_repo_path
            mock_which.return_value = "/usr/bin/cmake"  # Tools are available
            
            setup_llama(jobs=4, create_venv=True)
            
            # Verify venv creation was called (line 76-77)
            mock_create_venv.assert_called_once()

    @patch("llama_tools_aisee.setup_llama_cpp.subprocess.run")
    @patch("llama_tools_aisee.setup_llama_cpp.clone_llama_cpp")
    @patch("llama_tools_aisee.setup_llama_cpp.shutil.which")
    def test_setup_llama_custom_repo_dir(self, mock_which, mock_clone, mock_run):
        """Test setup_llama with custom repository directory."""
        # Mock successful setup with proper Path object
        import tempfile
        from pathlib import Path
        
        # Create a temporary directory to use as mock repo path
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_repo_path = Path(temp_dir)
            # Create a fake CMakeLists.txt
            (mock_repo_path / "CMakeLists.txt").touch()
            
            mock_clone.return_value = mock_repo_path
            mock_which.return_value = "/usr/bin/cmake"  # Tools are available
            
            setup_llama(jobs=8, create_venv=False, repo_dir="custom_llama_dir")
            
            # Verify clone was called with custom directory
            mock_clone.assert_called_once_with(repo_dir="custom_llama_dir")

    @patch("llama_tools_aisee.setup_llama_cpp.subprocess.run")
    @patch("llama_tools_aisee.setup_llama_cpp.clone_llama_cpp")
    @patch("llama_tools_aisee.setup_llama_cpp.shutil.which")
    @patch("llama_tools_aisee.setup_llama_cpp.create_virtualenv")
    def test_setup_llama_with_venv(self, mock_create_venv, mock_which, mock_clone, mock_run):
        """Test setup_llama with venv creation - covers lines 76-77."""
        # Mock successful setup
        mock_repo_path = MagicMock()
        mock_repo_path.__truediv__ = MagicMock(return_value=MagicMock())
        mock_repo_path.__truediv__.return_value.exists.return_value = True
        mock_clone.return_value = mock_repo_path
        mock_which.return_value = "/usr/bin/cmake"  # Tools are available
        
        setup_llama(jobs=4, create_venv=True)
        
        # Verify venv creation was called (line 76-77)
        mock_create_venv.assert_called_once()

    @patch("llama_tools_aisee.setup_llama_cpp.clone_llama_cpp")
    def test_setup_llama_missing_cmake_lists(self, mock_clone):
        """Test setup_llama when CMakeLists.txt is missing - covers line 52."""
        # Mock repo path where CMakeLists.txt doesn't exist
        mock_repo_path = MagicMock()
        mock_cmake_file = MagicMock()
        mock_cmake_file.exists.return_value = False  # CMakeLists.txt missing
        mock_repo_path.__truediv__.return_value = mock_cmake_file
        mock_clone.return_value = mock_repo_path
        
        # The function should call sys.exit when CMakeLists.txt is missing
        with self.assertRaises(SystemExit) as cm:
            setup_llama(jobs=2, create_venv=False)
        
        # Verify the error message contains the expected text
        self.assertIn("No CMakeLists.txt found", str(cm.exception))

    @patch("llama_tools_aisee.setup_llama_cpp.clone_llama_cpp")
    @patch("llama_tools_aisee.setup_llama_cpp.shutil.which")
    def test_setup_llama_missing_cmake_tool(self, mock_which, mock_clone):
        """Test setup_llama when cmake tool is missing - covers line 57."""
        # Mock successful clone and CMakeLists.txt exists
        mock_repo_path = MagicMock()
        mock_cmake_file = MagicMock()
        mock_cmake_file.exists.return_value = True
        mock_repo_path.__truediv__.return_value = mock_cmake_file
        mock_clone.return_value = mock_repo_path
        
        # Mock cmake not found, ninja found
        def which_side_effect(tool):
            if tool == "cmake":
                return None  # cmake not found
            elif tool == "ninja":
                return "/usr/bin/ninja"
            return None
        mock_which.side_effect = which_side_effect
        
        # The function should call sys.exit when cmake is missing
        with self.assertRaises(SystemExit) as cm:
            setup_llama(jobs=2, create_venv=False)
        
        # Verify the error message contains the expected text
        self.assertIn("cmake not found", str(cm.exception))

    @patch("llama_tools_aisee.setup_llama_cpp.clone_llama_cpp")
    @patch("llama_tools_aisee.setup_llama_cpp.shutil.which")
    def test_setup_llama_missing_ninja_tool(self, mock_which, mock_clone):
        """Test setup_llama when ninja tool is missing - covers line 57."""
        # Mock successful clone and CMakeLists.txt exists
        mock_repo_path = MagicMock()
        mock_cmake_file = MagicMock()
        mock_cmake_file.exists.return_value = True
        mock_repo_path.__truediv__.return_value = mock_cmake_file
        mock_clone.return_value = mock_repo_path
        
        # Mock ninja not found, cmake found
        def which_side_effect(tool):
            if tool == "cmake":
                return "/usr/bin/cmake"
            elif tool == "ninja":
                return None  # ninja not found
            return None
        mock_which.side_effect = which_side_effect
        
        # The function should call sys.exit when ninja is missing
        with self.assertRaises(SystemExit) as cm:
            setup_llama(jobs=2, create_venv=False)
        
        # Verify the error message contains the expected text
        self.assertIn("ninja not found", str(cm.exception))

    @patch("llama_tools_aisee.setup_llama_cpp.subprocess.run")
    @patch("llama_tools_aisee.setup_llama_cpp.clone_llama_cpp")
    @patch("llama_tools_aisee.setup_llama_cpp.shutil.which")
    def test_setup_llama_custom_repo_dir(self, mock_which, mock_clone, mock_run):
        """Test setup_llama with custom repository directory."""
        # Mock successful setup
        mock_repo_path = MagicMock()
        mock_repo_path.__truediv__ = MagicMock(return_value=MagicMock())
        mock_repo_path.__truediv__.return_value.exists.return_value = True
        mock_clone.return_value = mock_repo_path
        mock_which.return_value = "/usr/bin/cmake"  # Tools are available
        
        setup_llama(jobs=8, create_venv=False, repo_dir="custom_llama_dir")
        
        # Verify clone was called with custom directory
        mock_clone.assert_called_once_with(repo_dir="custom_llama_dir")

    @patch("llama_tools_aisee.setup_llama_cpp.subprocess.run")
    @patch("llama_tools_aisee.setup_llama_cpp.Path")
    def test_clone_llama_cpp_with_custom_repo_dir(self, mock_path_class, mock_run):
        """Test clone_llama_cpp with custom repo directory - covers line 20."""
        # Create mock path objects
        mock_repo_path = MagicMock()
        mock_repo_path.parent.mkdir = MagicMock()
        mock_repo_path.__truediv__ = MagicMock()
        
        # Mock .git directory doesn't exist (fresh clone)
        mock_git_dir = MagicMock()
        mock_git_dir.exists.return_value = False
        mock_repo_path.__truediv__.return_value = mock_git_dir
        
        # Mock .gitmodules exists
        mock_gitmodules = MagicMock()
        mock_gitmodules.exists.return_value = True
        mock_repo_path.__truediv__.side_effect = lambda x: mock_git_dir if x == ".git" else mock_gitmodules
        
        # Mock Path constructor
        mock_path_class.return_value = mock_repo_path
        
        # Call with custom repo dir (covers line 20: repo_dir = Path(repo_dir))
        result = clone_llama_cpp(repo_dir="custom_repo_dir")
        
        # Verify Path was called with custom directory
        mock_path_class.assert_called_with("custom_repo_dir")
        
        # Verify git clone was called
        mock_run.assert_any_call(["git", "clone", "https://github.com/ggerganov/llama.cpp.git", str(mock_repo_path)], check=True)

    @patch("llama_tools_aisee.setup_llama_cpp.subprocess.run")
    @patch("llama_tools_aisee.setup_llama_cpp.Path")
    def test_clone_llama_cpp_existing_repo_with_submodules(self, mock_path_class, mock_run):
        """Test clone_llama_cpp when repo exists with submodules - covers lines 28-30."""
        # Create mock path objects
        mock_repo_path = MagicMock()
        mock_repo_path.parent.mkdir = MagicMock()
        
        # Mock .git directory exists (repo already cloned)
        mock_git_dir = MagicMock()
        mock_git_dir.exists.return_value = True
        
        # Mock .gitmodules exists
        mock_gitmodules = MagicMock()
        mock_gitmodules.exists.return_value = True
        
        mock_repo_path.__truediv__.side_effect = lambda x: mock_git_dir if x == ".git" else mock_gitmodules
        
        # Mock home path
        mock_home = MagicMock()
        mock_cache_path = MagicMock()
        mock_llama_path = MagicMock()
        mock_home.__truediv__.return_value = mock_cache_path
        mock_cache_path.__truediv__.return_value = mock_llama_path
        mock_llama_path.__truediv__.return_value = mock_repo_path
        
        mock_path_class.home.return_value = mock_home
        
        # Call without repo_dir (uses default path)
        result = clone_llama_cpp()
        
        # Verify git fetch and reset commands were called (lines 28-30)
        mock_run.assert_any_call(["git", "-C", str(mock_repo_path), "fetch", "--all", "--tags"], check=False)
        mock_run.assert_any_call(["git", "-C", str(mock_repo_path), "reset", "--hard", "origin/master"], check=False)
        mock_run.assert_any_call(["git", "-C", str(mock_repo_path), "submodule", "update", "--init", "--recursive"], check=True)

    @patch("llama_tools_aisee.setup_llama_cpp.subprocess.run")
    @patch("llama_tools_aisee.setup_llama_cpp.Path")
    def test_clone_llama_cpp_no_submodules(self, mock_path_class, mock_run):
        """Test clone_llama_cpp when no submodules exist - covers lines 34-38."""
        # Create mock path objects
        mock_repo_path = MagicMock()
        mock_repo_path.parent.mkdir = MagicMock()
        
        # Mock .git directory doesn't exist (fresh clone)
        mock_git_dir = MagicMock()
        mock_git_dir.exists.return_value = False
        
        # Mock .gitmodules doesn't exist (no submodules)
        mock_gitmodules = MagicMock()
        mock_gitmodules.exists.return_value = False
        
        mock_repo_path.__truediv__.side_effect = lambda x: mock_git_dir if x == ".git" else mock_gitmodules
        
        # Mock Path constructor
        mock_path_class.return_value = mock_repo_path
        
        # Call with custom repo dir
        result = clone_llama_cpp(repo_dir="test_repo")
        
        # Verify git clone was called
        mock_run.assert_any_call(["git", "clone", "https://github.com/ggerganov/llama.cpp.git", str(mock_repo_path)], check=True)
        
        # Verify submodule command was NOT called (since no .gitmodules)
        submodule_calls = [call for call in mock_run.call_args_list if "submodule" in str(call)]
        self.assertEqual(len(submodule_calls), 0, "Submodule command should not be called when .gitmodules doesn't exist")

if __name__ == "__main__":
    unittest.main()
