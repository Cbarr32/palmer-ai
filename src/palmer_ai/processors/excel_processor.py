"""
Palmer AI Excel Intelligence Engine
Transform messy distributor Excel files into actionable intelligence
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path
import openpyxl
from datetime import datetime
import re

from src.palmer_ai.core.logger import get_logger

logger = get_logger(__name__)

class ExcelIntelligenceEngine:
    """
    Transform messy distributor Excel files into actionable intelligence
    This replaces $10K/year Excel consultants
    """
    
    def __init__(self):
        self.patterns = {
            'inventory': [
                'sku', 'part', 'item', 'product', 'stock', 'quantity',
                'on hand', 'available', 'qty', 'units'
            ],
            'pricing': [
                'price', 'cost', 'msrp', 'list', 'dealer', 'wholesale',
                'margin', 'markup', 'discount'
            ],
            'vendor': [
                'supplier', 'vendor', 'manufacturer', 'mfg', 'brand',
                'source', 'distributor'
            ],
            'customer': [
                'customer', 'client', 'account', 'buyer', 'purchaser',
                'sold to', 'ship to', 'bill to'
            ]
        }
        
    async def analyze_excel(self, file_path: str) -> Dict[str, Any]:
        """Main entry point - turn Excel chaos into intelligence"""
        logger.info(f"Analyzing Excel file: {file_path}")
        
        try:
            excel_file = pd.ExcelFile(file_path)
            sheets_data = {}
            
            for sheet_name in excel_file.sheet_names:
                df = excel_file.parse(sheet_name)
                sheet_analysis = await self._analyze_sheet(df, sheet_name)
                sheets_data[sheet_name] = sheet_analysis
            
            insights = self._generate_insights(sheets_data)
            metrics = self._calculate_metrics(sheets_data)
            opportunities = self._find_opportunities(sheets_data, metrics)
            
            return {
                'file_name': Path(file_path).name,
                'analysis_date': datetime.utcnow(),
                'sheets_analyzed': len(sheets_data),
                'total_rows': sum(s['row_count'] for s in sheets_data.values()),
                'data_quality_score': self._calculate_quality_score(sheets_data),
                'insights': insights,
                'metrics': metrics,
                'opportunities': opportunities,
                'sheets_data': sheets_data
            }
            
        except Exception as e:
            logger.error(f"Excel analysis failed: {str(e)}")
            raise
            
    async def _analyze_sheet(self, df: pd.DataFrame, sheet_name: str) -> Dict[str, Any]:
        """Analyze individual sheet"""
        detected_type = self._detect_sheet_type(df)
        df.columns = [self._clean_column_name(col) for col in df.columns]
        key_columns = self._identify_key_columns(df)
        patterns = self._analyze_patterns(df, key_columns)
        anomalies = self._find_anomalies(df, detected_type)
        
        return {
            'sheet_name': sheet_name,
            'detected_type': detected_type,
            'row_count': len(df),
            'column_count': len(df.columns),
            'key_columns': key_columns,
            'patterns': patterns,
            'anomalies': anomalies,
            'summary_stats': self._get_summary_stats(df, key_columns)
        }
        
    def _detect_sheet_type(self, df: pd.DataFrame) -> str:
        """Detect what kind of data this sheet contains"""
        columns_lower = [col.lower() for col in df.columns.astype(str)]
        
        type_scores = {}
        for data_type, keywords in self.patterns.items():
            score = sum(1 for keyword in keywords 
                       for col in columns_lower if keyword in col)
            type_scores[data_type] = score
            
        return max(type_scores, key=type_scores.get)
        
    def _find_opportunities(self, sheets_data: Dict, metrics: Dict) -> List[Dict]:
        """Find revenue opportunities in the data"""
        opportunities = []
        
        if 'inventory_turnover' in metrics and metrics['inventory_turnover'] < 4:
            opportunities.append({
                'type': 'inventory_optimization',
                'title': 'Slow-Moving Inventory Detected',
                'description': f"Inventory turnover of {metrics['inventory_turnover']:.1f}x is below industry standard of 6x",
                'potential_impact': '$50K-200K working capital improvement',
                'palmer_ai_solution': 'AI-powered demand forecasting and automated reorder points'
            })
            
        if 'average_margin' in metrics and metrics['average_margin'] < 0.25:
            opportunities.append({
                'type': 'pricing_optimization',
                'title': 'Margin Improvement Opportunity',
                'description': f"Average margin of {metrics['average_margin']:.1%} has room for improvement",
                'potential_impact': '2-5% revenue increase',
                'palmer_ai_solution': 'Competitive pricing intelligence and dynamic pricing engine'
            })
            
        return opportunities
        
    def _clean_column_name(self, col_name: str) -> str:
        """Clean messy column names"""
        cleaned = re.sub(r'[^\w\s]', '', str(col_name))
        cleaned = re.sub(r'\s+', '_', cleaned.strip())
        return cleaned.lower()
        
    def _identify_key_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """Identify important columns"""
        key_cols = {}
        columns_lower = df.columns.str.lower()
        
        for col in ['sku', 'part_number', 'item_code', 'product_id']:
            matches = columns_lower.str.contains(col.replace('_', '|'))
            if matches.any():
                key_cols['product_id'] = df.columns[matches][0]
                break
                
        price_patterns = ['price', 'cost', 'amount']
        for pattern in price_patterns:
            matches = columns_lower.str.contains(pattern)
            if matches.any():
                for col in df.columns[matches]:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        key_cols['price'] = col
                        break
                        
        return key_cols
        
    def _analyze_patterns(self, df: pd.DataFrame, key_columns: Dict) -> Dict:
        """Find patterns in the data"""
        patterns = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if df[col].notna().sum() > 0:
                patterns[col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'outliers': int((df[col] > df[col].mean() + 3*df[col].std()).sum())
                }
                
        return patterns
        
    def _find_anomalies(self, df: pd.DataFrame, sheet_type: str) -> List[Dict]:
        """Find data anomalies that need attention"""
        anomalies = []
        
        if 'product_id' in df.columns:
            duplicates = df[df.duplicated(subset=['product_id'], keep=False)]
            if len(duplicates) > 0:
                anomalies.append({
                    'type': 'duplicate_products',
                    'severity': 'high',
                    'count': len(duplicates),
                    'message': f"Found {len(duplicates)} duplicate product entries"
                })
                
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if 'price' in col.lower() or 'qty' in col.lower() or 'quantity' in col.lower():
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    anomalies.append({
                        'type': 'negative_values',
                        'severity': 'medium',
                        'column': col,
                        'count': int(negative_count),
                        'message': f"Found {negative_count} negative values in {col}"
                    })
                    
        return anomalies
        
    def _calculate_metrics(self, sheets_data: Dict) -> Dict[str, float]:
        """Calculate business metrics from the data"""
        metrics = {}
        
        inventory_sheets = [s for s in sheets_data.values() 
                          if s['detected_type'] == 'inventory']
        if inventory_sheets:
            total_skus = sum(s['row_count'] for s in inventory_sheets)
            metrics['total_skus'] = total_skus
            
        pricing_sheets = [s for s in sheets_data.values() 
                        if s['detected_type'] == 'pricing']
        if pricing_sheets:
            for sheet in pricing_sheets:
                if 'patterns' in sheet:
                    for col, stats in sheet['patterns'].items():
                        if 'margin' in col.lower():
                            metrics['average_margin'] = stats['mean']
                            
        return metrics
        
    def _calculate_quality_score(self, sheets_data: Dict) -> float:
        """Calculate data quality score (0-100)"""
        scores = []
        
        for sheet in sheets_data.values():
            if 'summary_stats' in sheet:
                completeness = 1 - (sheet['summary_stats'].get('null_percentage', 0) / 100)
                scores.append(completeness)
                
            anomaly_penalty = len(sheet.get('anomalies', [])) * 0.05
            scores.append(max(0, 1 - anomaly_penalty))
            
        return round(np.mean(scores) * 100, 1) if scores else 0
        
    def _get_summary_stats(self, df: pd.DataFrame, key_columns: Dict) -> Dict:
        """Get summary statistics for the sheet"""
        stats = {
            'null_percentage': round((df.isnull().sum().sum() / df.size) * 100, 2),
            'unique_products': len(df[key_columns['product_id']].unique()) if 'product_id' in key_columns else 0
        }
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats['numeric_columns'] = len(numeric_cols)
            
        return stats
        
    def _generate_insights(self, sheets_data: Dict) -> List[Dict]:
        """Generate actionable insights from analysis"""
        insights = []
        
        quality_scores = [s.get('summary_stats', {}).get('null_percentage', 0) 
                         for s in sheets_data.values()]
        avg_nulls = np.mean(quality_scores) if quality_scores else 0
        
        if avg_nulls > 10:
            insights.append({
                'type': 'data_quality',
                'priority': 'high',
                'title': 'Data Quality Issues Detected',
                'description': f"Average {avg_nulls:.1f}% missing data across sheets",
                'recommendation': 'Implement data validation rules and automated cleaning'
            })
            
        if len(sheets_data) > 10:
            insights.append({
                'type': 'organization',
                'priority': 'medium',
                'title': 'Complex Workbook Structure',
                'description': f"Workbook contains {len(sheets_data)} sheets",
                'recommendation': 'Consider consolidating related data for easier analysis'
            })
            
        return insights

excel_processor = ExcelIntelligenceEngine()
