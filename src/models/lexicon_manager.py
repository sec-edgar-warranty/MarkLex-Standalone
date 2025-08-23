"""
Lexicon manager for loading and managing lexicon data
"""

import os
import pandas as pd
from pathlib import Path
from typing import Optional

from utils.app_dirs import AppDirs

class LexiconManager:
    """Manager for lexicon data"""
    
    def __init__(self, app_dirs: AppDirs):
        self.app_dirs = app_dirs
        self._lexicon_cache = None
    
    def load_lexicon(self) -> pd.DataFrame:
        """Load lexicon data with caching"""
        if self._lexicon_cache is not None:
            return self._lexicon_cache
        
        # Try to load from app data directory first
        lexicon_path = os.path.join(self.app_dirs.user_data_dir, "Lexicon List.xlsx")
        
        if os.path.exists(lexicon_path):
            try:
                df = pd.read_excel(lexicon_path)
                self._lexicon_cache = df
                return df
            except Exception as e:
                print(f"Error loading lexicon from {lexicon_path}: {e}")
        
        # Fallback to default lexicon
        default_lexicon = self.create_default_lexicon()
        self._lexicon_cache = default_lexicon
        return default_lexicon
    
    def create_default_lexicon(self) -> pd.DataFrame:
        """Create a default lexicon with multiple business dimensions"""
        return pd.DataFrame({
            'Entity': (['Marketing'] * 8 + 
                      ['ESG'] * 8 + 
                      ['DEI'] * 8 +
                      ['Risk & Security'] * 8 + 
                      ['Employee'] * 8 +
                      ['AI & Data'] * 8 +
                      ['Innovation'] * 8 +
                      ['Investor Focus'] * 8),
            'Keyword': [
                # Marketing
                'marketing', 'advertising', 'promotion', 'brand', 'campaign', 'customer', 'market', 'sales',
                # ESG
                'sustainability', 'environmental', 'governance', 'social', 'climate', 'carbon', 'green', 'renewable',
                # DEI
                'diversity', 'inclusion', 'equity', 'diverse', 'inclusive', 'equality', 'bias', 'dei',
                # Risk & Security
                'risk', 'security', 'compliance', 'audit', 'cyber', 'privacy', 'data protection', 'governance',
                # Employee
                'employee', 'workforce', 'talent', 'culture', 'training', 'development', 'engagement', 'retention',
                # AI & Data
                'artificial intelligence', 'machine learning', 'data', 'analytics', 'algorithm', 'automation', 'digital', 'technology',
                # Innovation
                'innovation', 'research', 'development', 'technology', 'patent', 'invention', 'creative', 'breakthrough',
                # Investor Focus
                'investor', 'shareholder', 'earnings', 'revenue', 'profit', 'financial', 'return', 'dividend'
            ]
        })
    
    def save_lexicon(self, df: pd.DataFrame) -> bool:
        """Save lexicon data"""
        try:
            lexicon_path = os.path.join(self.app_dirs.user_data_dir, "Lexicon List.xlsx")
            os.makedirs(os.path.dirname(lexicon_path), exist_ok=True)
            df.to_excel(lexicon_path, index=False)
            self._lexicon_cache = df  # Update cache
            return True
        except Exception as e:
            print(f"Error saving lexicon: {e}")
            return False
    
    def clear_cache(self):
        """Clear lexicon cache"""
        self._lexicon_cache = None
    
    def get_entities(self) -> list:
        """Get list of available entities"""
        lexicon = self.load_lexicon()
        if 'Entity' in lexicon.columns:
            return lexicon['Entity'].unique().tolist()
        return []
    
    def get_keywords_for_entity(self, entity: str) -> list:
        """Get keywords for a specific entity"""
        lexicon = self.load_lexicon()
        if 'Entity' in lexicon.columns and 'Keyword' in lexicon.columns:
            entity_data = lexicon[lexicon['Entity'] == entity]
            return entity_data['Keyword'].tolist()
        return []