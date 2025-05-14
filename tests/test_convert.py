import unittest
from unittest.mock import patch, call
from llama_tools_jaliya import convert_model
from subprocess import CalledProcessError

class TestConvertModel(unittest.TestCase):

    @patch("llama_tools_jaliya.convert_and_quantize.subprocess.run")
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

    @patch("llama_tools_jaliya.convert_and_quantize.subprocess.run")
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

    @patch("llama_tools_jaliya.convert_and_quantize.subprocess.run")
    def test_convert_model_raises_called_process_error(self, mock_run):
    # Simulate a failure during subprocess.run
        mock_run.side_effect = CalledProcessError(returncode=1, cmd="fake_command")

        with self.assertRaises(CalledProcessError):
            convert_model(
                hf_model="facebook/opt-125m",
                gguf_output="model.gguf"
            )
