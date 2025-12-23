import pandas as pd
import logging
import re

class CSVParser:
    """
    Parser especializado para o formato de exportação do Google Forms/Excel.
    Converte respostas textuais em scores numéricos para a Engine.
    """
    
    @staticmethod
    def parse_score(value):
        """Extrai o primeiro número de uma string. Ex: '4. Concordo' -> 4."""
        if pd.isna(value):
            return 3 # Neutro em caso de nulo
        
        val_str = str(value).strip()
        # Procura por um dígito no início da string
        match = re.match(r'^(\d+)', val_str)
        if match:
            return int(match.group(1))
        return 3 # Fallback

    @staticmethod
    def load_data(filepath: str):
        """Lê o CSV e retorna um DataFrame limpo."""
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            # Se der erro de encoding, tenta latin1 (comum no Excel Brasil)
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, encoding='latin1')
            
        return df

    @staticmethod
    def extract_responses(row, start_idx=8, big5_count=50, dass_count=21):
        """
        Fatia as colunas de respostas baseada na posição.
        Ajustado para o CSV 'MINDSCAN...xlsx'.
        
        Args:
            row: Linha do Pandas
            start_idx: Índice onde começam as perguntas (coluna 8 no seu CSV)
        """
        # Pega todas as respostas a partir da coluna de perguntas
        raw_values = row.iloc[start_idx:].values
        
        # Converte tudo para int
        scores = [CSVParser.parse_score(v) for v in raw_values]
        
        # Garante que temos dados suficientes (padding com 3/0 se acabar antes)
        total_needed = big5_count + dass_count
        if len(scores) < total_needed:
            scores.extend([3] * (total_needed - len(scores)))
            
        big5_data = scores[:big5_count]
        dass_data = scores[big5_count:big5_count+dass_count]
        
        return big5_data, dass_data