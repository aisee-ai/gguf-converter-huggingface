import unittest
from unittest.mock import patch
from subprocess import CalledProcessError
from llama_tools_aisee import run_llama_server
from llama_tools_aisee import server

class TestRunLlamaServer(unittest.TestCase):

    @patch("llama_tools_aisee.server.subprocess.run")
    @patch("llama_tools_aisee.server.os.path.isfile", return_value=True)
    def test_run_llama_server_success(self, mock_isfile, mock_run):
        run_llama_server("model.gguf")
        mock_run.assert_called_once_with(
            ["llama.cpp/build/bin/llama-server", "-m", "model.gguf"],
            check=True
        )

    @patch("llama_tools_aisee.server.os.path.isfile", return_value=False)
    def test_run_llama_server_binary_not_found(self, mock_isfile):
        with self.assertRaises(FileNotFoundError) as context:
            run_llama_server("model.gguf")
        self.assertIn("llama-server binary not found", str(context.exception))

    @patch("llama_tools_aisee.server.subprocess.run", side_effect=CalledProcessError(1, "cmd"))
    @patch("llama_tools_aisee.server.os.path.isfile", return_value=True)
    def test_run_llama_server_called_process_error(self, mock_isfile, mock_run):
        with self.assertRaises(CalledProcessError):
            run_llama_server("model.gguf")

    @patch("llama_tools_aisee.server.run_llama_server")
    def test_main_invocation(self, mock_run_llama_server):
        test_args = ["run_llama_server.py", "--gguf_model", "test.gguf"]
        with patch("sys.argv", test_args):
            server.main()
            mock_run_llama_server.assert_called_once_with(gguf_model="test.gguf")





            
