import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO
import argparse

# Import the main module
import llama_tools_aisee.__main__ as main_module


class TestMainCLI(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.original_argv = sys.argv.copy()

    def tearDown(self):
        """Clean up after each test method."""
        sys.argv = self.original_argv

    @patch('llama_tools_aisee.__main__.setup_llama')
    def test_setup_command(self, mock_setup_llama):
        """Test the setup command with required arguments."""
        sys.argv = ['llama-tools', 'setup', '--jobs', '4']
        
        main_module.main()
        
        mock_setup_llama.assert_called_once_with(jobs=4, create_venv=False)

    @patch('llama_tools_aisee.__main__.setup_llama')
    def test_setup_command_with_venv(self, mock_setup_llama):
        """Test the setup command with venv creation."""
        sys.argv = ['llama-tools', 'setup', '--jobs', '8', '--create-venv']
        
        main_module.main()
        
        mock_setup_llama.assert_called_once_with(jobs=8, create_venv=True)

    @patch('llama_tools_aisee.__main__.clone_llama_cpp')
    def test_clone_command(self, mock_clone_llama_cpp):
        """Test the clone command."""
        sys.argv = ['llama-tools', 'clone']
        
        main_module.main()
        
        mock_clone_llama_cpp.assert_called_once()

    @patch('llama_tools_aisee.__main__.create_virtualenv')
    def test_venv_command(self, mock_create_virtualenv):
        """Test the venv command."""
        sys.argv = ['llama-tools', 'venv']
        
        main_module.main()
        
        mock_create_virtualenv.assert_called_once()

    @patch('llama_tools_aisee.__main__.convert_model')
    def test_convert_command_basic(self, mock_convert_model):
        """Test the convert command with basic arguments."""
        sys.argv = [
            'llama-tools', 'convert',
            '--hf_model', 'facebook/opt-125m',
            '--gguf_output', 'model.gguf'
        ]
        
        main_module.main()
        
        mock_convert_model.assert_called_once_with(
            hf_model='facebook/opt-125m',
            gguf_output='model.gguf',
            quantized_output=None,
            quant_type=None,
            quant_algo='8'
        )

    @patch('llama_tools_aisee.__main__.convert_model')
    def test_convert_command_with_quantization(self, mock_convert_model):
        """Test the convert command with quantization options."""
        sys.argv = [
            'llama-tools', 'convert',
            '--hf_model', 'facebook/opt-125m',
            '--gguf_output', 'model.gguf',
            '--quantized_output', 'model-q4.gguf',
            '--quant_type', 'Q4_0',
            '--quant_algo', '16'
        ]
        
        main_module.main()
        
        mock_convert_model.assert_called_once_with(
            hf_model='facebook/opt-125m',
            gguf_output='model.gguf',
            quantized_output='model-q4.gguf',
            quant_type='Q4_0',
            quant_algo='16'
        )

    @patch('llama_tools_aisee.__main__.push_gguf')
    def test_upload_command(self, mock_push_gguf):
        """Test the upload command."""
        sys.argv = [
            'llama-tools', 'upload',
            '--repo_id', 'user/model-name',
            '--gguf_path', 'model.gguf'
        ]
        
        main_module.main()
        
        mock_push_gguf.assert_called_once_with(
            repo_id='user/model-name',
            gguf_path='model.gguf',
            local_repo_dir='./hf_tmp_repo'
        )

    @patch('llama_tools_aisee.__main__.push_gguf')
    def test_upload_command_with_custom_dir(self, mock_push_gguf):
        """Test the upload command with custom local repo directory."""
        sys.argv = [
            'llama-tools', 'upload',
            '--repo_id', 'user/model-name',
            '--gguf_path', 'model.gguf',
            '--local_repo_dir', './custom_repo'
        ]
        
        main_module.main()
        
        mock_push_gguf.assert_called_once_with(
            repo_id='user/model-name',
            gguf_path='model.gguf',
            local_repo_dir='./custom_repo'
        )

    @patch('llama_tools_aisee.__main__.run_llama_server')
    def test_run_server_command(self, mock_run_llama_server):
        """Test the run-server command."""
        sys.argv = [
            'llama-tools', 'run-server',
            '--gguf_model', 'model.gguf'
        ]
        
        main_module.main()
        
        mock_run_llama_server.assert_called_once_with(gguf_model='model.gguf')

    @patch('llama_tools_aisee.__main__.clean_build_dirs')
    def test_clean_command(self, mock_clean_build_dirs):
        """Test the clean command."""
        sys.argv = ['llama-tools', 'clean']
        
        main_module.main()
        
        mock_clean_build_dirs.assert_called_once()

    @patch('llama_tools_aisee.__main__.show_status')
    def test_status_command(self, mock_show_status):
        """Test the status command."""
        sys.argv = ['llama-tools', 'status']
        
        main_module.main()
        
        mock_show_status.assert_called_once()

    def test_missing_required_arguments_setup(self):
        """Test that missing required arguments for setup raise appropriate errors."""
        sys.argv = ['llama-tools', 'setup']
        
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                main_module.main()

    def test_missing_required_arguments_convert(self):
        """Test that missing required arguments for convert raise appropriate errors."""
        sys.argv = ['llama-tools', 'convert']
        
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                main_module.main()

    def test_missing_required_arguments_upload(self):
        """Test that missing required arguments for upload raise appropriate errors."""
        sys.argv = ['llama-tools', 'upload']
        
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                main_module.main()

    def test_missing_required_arguments_run_server(self):
        """Test that missing required arguments for run-server raise appropriate errors."""
        sys.argv = ['llama-tools', 'run-server']
        
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                main_module.main()

    def test_no_command_provided(self):
        """Test that no command provided raises an error."""
        sys.argv = ['llama-tools']
        
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                main_module.main()

    def test_invalid_command(self):
        """Test that invalid command raises an error."""
        sys.argv = ['llama-tools', 'invalid-command']
        
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                main_module.main()

    @patch('llama_tools_aisee.__main__.setup_llama')
    def test_setup_jobs_type_conversion(self, mock_setup_llama):
        """Test that jobs argument is properly converted to integer."""
        sys.argv = ['llama-tools', 'setup', '--jobs', '12']
        
        main_module.main()
        
        mock_setup_llama.assert_called_once_with(jobs=12, create_venv=False)

    def test_convert_command_missing_hf_model(self):
        """Test convert command missing hf_model argument."""
        sys.argv = ['llama-tools', 'convert', '--gguf_output', 'model.gguf']
        
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                main_module.main()

    def test_convert_command_missing_gguf_output(self):
        """Test convert command missing gguf_output argument."""
        sys.argv = ['llama-tools', 'convert', '--hf_model', 'facebook/opt-125m']
        
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                main_module.main()

    def test_upload_command_missing_repo_id(self):
        """Test upload command missing repo_id argument."""
        sys.argv = ['llama-tools', 'upload', '--gguf_path', 'model.gguf']
        
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                main_module.main()

    def test_upload_command_missing_gguf_path(self):
        """Test upload command missing gguf_path argument."""
        sys.argv = ['llama-tools', 'upload', '--repo_id', 'user/model']
        
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                main_module.main()


if __name__ == "__main__":
    unittest.main()