try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    
from datetime import datetime
from django.db import transaction
from ..models import GenerationReport, Unit


class ExcelImporter:
    """Service class for importing Excel files into the database"""
    
    REQUIRED_COLUMNS = [
        'date', 'unit_number', 'generation_kwh', 'operating_hours',
        'availability_hours', 'forced_outage_hours', 'scheduled_outage_hours'
    ]
    
    def __init__(self, uploaded_file):
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas is required for Excel import. Install with: pip install pandas")
        
        self.uploaded_file = uploaded_file
        self.plant = uploaded_file.plant
        self.errors = []
    
    def process(self):
        """Main processing method"""
        df = self._read_excel()
        self._validate_columns(df)
        self._validate_data(df)
        
        if self.errors:
            raise ValueError(f"Validation errors: {'; '.join(self.errors)}")
        
        records_imported = self._import_data(df)
        return records_imported
    
    def _read_excel(self):
        """Read Excel file into pandas DataFrame"""
        try:
            # Try reading the file
            df = pd.read_excel(self.uploaded_file.file.path, sheet_name=0)
            
            # Check if first row might be a title/header row
            # If first column contains text like "National Power Corporation", skip it
            if df.shape[0] > 0:
                first_cell = str(df.iloc[0, 0]).lower()
                if 'national' in first_cell or 'power' in first_cell or 'corporation' in first_cell:
                    # Skip the first row and re-read with next row as header
                    df = pd.read_excel(self.uploaded_file.file.path, sheet_name=0, header=1)
            
            # Normalize column names - handle various formats
            df.columns = (df.columns
                         .astype(str)
                         .str.lower()
                         .str.strip()
                         .str.replace(' ', '_')
                         .str.replace('-', '_')
                         .str.replace('__', '_'))
            
            # Remove any unnamed columns or columns that are mostly empty
            df = df.loc[:, ~df.columns.str.contains('^unnamed')]
            
            # Print columns for debugging
            print(f"Excel columns after normalization: {list(df.columns)}")
            print(f"First few rows:\n{df.head()}")
            
            return df
        except Exception as e:
            raise ValueError(f"Error reading Excel file: {str(e)}")
    
    def _validate_columns(self, df):
        """Validate that all required columns are present"""
        missing_columns = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing_columns:
            found_columns = list(df.columns)
            self.errors.append(
                f"Missing required columns: {', '.join(sorted(missing_columns))}. "
                f"Found columns: {', '.join(found_columns) if found_columns else 'None'}. "
                f"Required columns are: {', '.join(sorted(self.REQUIRED_COLUMNS))}"
            )
    
    def _validate_data(self, df):
        """Validate data types and values"""
        # Check for null values in required columns
        for col in self.REQUIRED_COLUMNS:
            if col in df.columns and df[col].isnull().any():
                null_rows = df[df[col].isnull()].index.tolist()
                self.errors.append(f"Null values found in column '{col}' at rows: {null_rows}")
        
        # Validate date format
        if 'date' in df.columns:
            try:
                df['date'] = pd.to_datetime(df['date'])
            except Exception as e:
                self.errors.append(f"Invalid date format: {str(e)}")
        
        # Validate numeric columns
        numeric_columns = ['generation_kwh', 'operating_hours', 'availability_hours', 
                          'forced_outage_hours', 'scheduled_outage_hours']
        for col in numeric_columns:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    try:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except:
                        self.errors.append(f"Column '{col}' contains non-numeric values")
                
                # Check for negative values
                if (df[col] < 0).any():
                    self.errors.append(f"Column '{col}' contains negative values")
        
        # Validate hours (0-24)
        hour_columns = ['operating_hours', 'availability_hours', 'forced_outage_hours', 'scheduled_outage_hours']
        for col in hour_columns:
            if col in df.columns and ((df[col] < 0) | (df[col] > 24)).any():
                self.errors.append(f"Column '{col}' contains values outside 0-24 range")
    
    @transaction.atomic
    def _import_data(self, df):
        """Import validated data into database"""
        records_imported = 0
        
        # Get all units for this plant
        units = {unit.unit_number: unit for unit in Unit.objects.filter(plant=self.plant)}
        
        for idx, row in df.iterrows():
            unit_number = int(row['unit_number'])
            
            # Check if unit exists
            if unit_number not in units:
                self.errors.append(f"Row {idx}: Unit {unit_number} not found for plant {self.plant.code}")
                continue
            
            unit = units[unit_number]
            report_date = row['date'].date() if isinstance(row['date'], pd.Timestamp) else row['date']
            
            # Check for duplicates
            existing = GenerationReport.objects.filter(
                plant=self.plant,
                unit=unit,
                report_date=report_date
            ).first()
            
            if existing:
                # Update existing record
                existing.generation_kwh = row['generation_kwh']
                existing.operating_hours = row['operating_hours']
                existing.availability_hours = row['availability_hours']
                existing.forced_outage_hours = row.get('forced_outage_hours', 0)
                existing.scheduled_outage_hours = row.get('scheduled_outage_hours', 0)
                existing.remarks = row.get('remarks', '')
                existing.uploaded_file = self.uploaded_file
                existing.save()
            else:
                # Create new record
                GenerationReport.objects.create(
                    plant=self.plant,
                    unit=unit,
                    report_date=report_date,
                    uploaded_file=self.uploaded_file,
                    generation_kwh=row['generation_kwh'],
                    operating_hours=row['operating_hours'],
                    availability_hours=row['availability_hours'],
                    forced_outage_hours=row.get('forced_outage_hours', 0),
                    scheduled_outage_hours=row.get('scheduled_outage_hours', 0),
                    remarks=row.get('remarks', '')
                )
            
            records_imported += 1
        
        if self.errors:
            raise ValueError(f"Import errors: {'; '.join(self.errors)}")
        
        return records_imported
