import base64
import zipfile
from io import BytesIO
from typing import List, IO
import re
import pandas as pd

class FileExtractor:
    @staticmethod
    def extract_java_files(zip_in_memory: IO) -> List[dict]:
        if zip_in_memory is None:
            raise ValueError("No data found in the source.")
        
        with zipfile.ZipFile(zip_in_memory, 'r') as zip_ref:
            java_files = [name for name in zip_ref.namelist() if name.endswith('.java')]
            if not java_files:
                raise FileNotFoundError("No .java files found in the ZIP file.")
            
            return [
                {"filename": name.split("/")[-1].replace('.java', ''), "content": zip_ref.open(name).read().decode('utf-8')}
                for name in java_files
            ]

class DataProcessor:    
    @staticmethod
    def clean_codes(lines: List[str]) -> List[str]:
        return [line.replace(";", "").strip() for line in lines]
    
    @staticmethod
    def extract_imports(file_content: str) -> List[str]:
        lines = file_content.split('\n')
        return [line.strip() for line in lines if line.strip().startswith('import')]
    
    @staticmethod
    def clean_imports(import_lines: List[str], filename_base: List[str]) -> List[str]:
        return [
            line.replace("import", "").split(".")[-1]   
            for line in import_lines
            if line.replace("import", "").split(".")[-1] in filename_base
        ]
    
    @staticmethod
    def extract_implements(file_content: str) -> List[str]:
        pattern = r'class\s+\w+\s+implements\s+([^\{]+)'
        matches = re.findall(pattern, file_content)
        implements = []
        for match in matches:
            interfaces = [interface.strip() for interface in match.split(',')]
            implements.extend(interfaces)
        return implements
    
    @staticmethod
    def clean_implements(implements_list: List[str], filename_base: List[str]) -> List[str]:
        return [interface for interface in implements_list if interface in filename_base]
    
    @staticmethod
    def contains_main_method(file_content: str) -> bool:
        """Checks if a file contains the main method."""
        pattern = r'public\s+static\s+void\s+main\s*\(\s*String\s*\[\s*\]\s*args\s*\)'
        return bool(re.search(pattern, file_content))
    
    @staticmethod
    def filter_imports_and_implements(df: pd.DataFrame) -> pd.DataFrame:
        filename_base = df['filename'].tolist()
        df["imports"] = df["code_imports"].apply(lambda imports: DataProcessor.clean_imports(imports, filename_base))
        df["implements"] = df["code_implements"].apply(lambda impls: DataProcessor.clean_implements(impls, filename_base))
        return df


class DataTransformer:   
    def __init__(self):
        self.file_extractor = FileExtractor()
        self.data_processor = DataProcessor()

    def transform(self, zip_data: dict) -> pd.DataFrame:
        try:
            zip_content = base64.b64decode(zip_data['content'])
            zip_in_memory = BytesIO(zip_content)
            
            extracted_files = self.file_extractor.extract_java_files(zip_in_memory)
            
            data = []
            for file in extracted_files:
                file_content = file["content"]
                imports = self.data_processor.extract_imports(file_content)
                imports_cleaned = self.data_processor.clean_codes(imports)
                implements = self.data_processor.extract_implements(file_content)
                implements_cleaned = self.data_processor.clean_codes(implements)
                is_main = self.data_processor.contains_main_method(file_content)
                
                data.append({
                    "filename": file["filename"],
                    "code_imports": imports_cleaned,
                    "code_implements": implements_cleaned,
                    "is_main": is_main
                })
                
            df = pd.DataFrame(data)
            df = self.data_processor.filter_imports_and_implements(df).drop(columns=["code_implements"])
            return df
        
        except Exception as e:
            raise RuntimeError(f"Error during data transformation: {str(e)}") from e