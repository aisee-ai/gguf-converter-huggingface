import unittest
from unittest.mock import patch, call
from llama_tools_aisee import convert_model
from subprocess import CalledProcessError

class TestConvertModel(unittest.TestCase):

    @patch("llama_tools_aisee.convert_and_quantize.subprocess.run")
    def test_convert_model_basic(self, mock_run):
        convert_model(
            hf_model="facebook/opt-125m",
            gguf_output="model.gguf"
        )
        # Only one subprocess.run call for conversion
        self.assertEqual(mock_run.call_count, 1)
        mock_run.assert_called_with([
            "python",
            "llama.cpp/convert_hf_to_gguf.py",
            "facebook/opt-125m",
            "--outfile",
            "model.gguf"
        ], check=True)

    @patch("llama_tools_aisee.convert_and_quantize.subprocess.run")
    def test_convert_model_with_quantization(self, mock_run):
        convert_model(
            hf_model="facebook/opt-125m",
            gguf_output="model.gguf",
            quantized_output="model-q.gguf",
            quant_type="Q4_0",
            quant_algo="8"
        )
        # Two subprocess.run calls: one for conversion, one for quantization
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_has_calls([
            call([
                "python",
                "llama.cpp/convert_hf_to_gguf.py",
                "facebook/opt-125m",
                "--outfile",
                "model.gguf"
            ], check=True),
            call([
                "llama.cpp/build/bin/llama-quantize",
                "model.gguf",
                "model-q.gguf",
                "Q4_0",
                "8"
            ], check=True)
        ])

    @patch("llama_tools_aisee.convert_and_quantize.subprocess.run")
    def test_convert_model_logs_error(self, mock_run):
        mock_run.side_effect = CalledProcessError(returncode=1, cmd="fake_command")

        with self.assertLogs("llama_tools_aisee.convert_and_quantize", level="ERROR") as cm:
            convert_model(hf_model="facebook/opt-125m", gguf_output="model.gguf")
        
        self.assertTrue(any("Model conversion failed!" in msg for msg in cm.output))
