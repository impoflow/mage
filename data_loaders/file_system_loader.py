import base64
from io import BytesIO
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


class FileSourceReader:
    """Handles reading data sources from ZIP files."""
    
    def __init__(self):
        pass

    def read(self, source: str) -> BytesIO:
        """Reads and validates the ZIP source."""
        try:
            zip_in_memory = self.read_zip(source)
            
            if zip_in_memory is None or zip_in_memory.getbuffer().nbytes == 0:
                raise ValueError("The source contains no data or is invalid.")
            
            return zip_in_memory
        except Exception as e:
            raise RuntimeError(f"Error processing ZIP: {str(e)}") from e
    
    @staticmethod
    def read_zip(source: str) -> BytesIO:
        """Reads a ZIP file from the given path and returns it as a BytesIO object."""
        try:
            with open(source, "rb") as file:
                return BytesIO(file.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{source}' was not found.")
        except IOError as e:
            raise IOError(f"Error reading file '{source}': {str(e)}")


@data_loader
def load_data(*args, **kwargs):
    file_reader = FileSourceReader()
    zipfile = file_reader.read(f"data/{kwargs['project_name']}.zip")
    
    serialized_zip = {
        'filename': f"{kwargs['project_name']}.zip",
        'content': base64.b64encode(zipfile.getvalue()).decode('utf-8'),  # Encode binary content as base64
        'size': zipfile.getbuffer().nbytes
    }

    return serialized_zip


@test
def test_output(output, *args) -> None:
    assert isinstance(output, dict), 'The output must be a dictionary'
    assert 'filename' in output, 'The output must include a filename'
    assert 'content' in output, 'The output must include content'
    assert 'size' in output, 'The output must include size'