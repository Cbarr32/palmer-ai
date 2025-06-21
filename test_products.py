import pandas as pd

# Create sample product data
products = pd.DataFrame({
    'name': [
        '3/4 inch Ball Valve',
        'Industrial Temperature Sensor',
        '5HP Electric Motor',
        'Safety Gloves Cut Level 5',
        'LED High Bay Light 150W'
    ],
    'sku': ['BV-750-SS', 'TS-IND-420', 'MTR-5HP-3P', 'GLV-CUT5-L', 'LED-HB-150'],
    'manufacturer': ['FlowTech', 'SensorPro', 'PowerDrive', 'SafetyFirst', 'BrightLux'],
    'category': ['Valves', 'Sensors', 'Motors', 'PPE', 'Lighting'],
    'description': [
        'Stainless steel ball valve',
        'Temperature sensor for industrial use',
        'Three phase motor',
        'Cut resistant work gloves',
        'High efficiency LED light'
    ],
    'specifications': [
        'Material: 316 SS, Pressure: 1000 PSI',
        'Range: -40 to 400°F, Output: 4-20mA',
        'Voltage: 230/460V, RPM: 1800',
        'ANSI Cut Level 5, Nitrile coating',
        'Lumens: 20000, Color: 5000K'
    ],
    'price': ['$89.99', '$149.99', '$899.99', '$24.99', '$299.99'],
    'industry': ['plumbing', 'industrial', 'industrial', 'safety', 'electrical']
})

products.to_excel('test_products.xlsx', index=False)
print("Created test_products.xlsx with 5 sample products")
