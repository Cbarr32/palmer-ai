import pandas as pd

products = pd.DataFrame({
   'name': [
       'Industrial Pressure Sensor 0-100 PSI',
       'Heavy Duty Safety Gloves Cut Level 5',
       'Variable Frequency Drive 10HP',
       'LED High Bay Light 200W',
       'Pneumatic Cylinder 2 inch Bore'
   ],
   'sku': ['PS-100', 'SG-HD5', 'VFD-10', 'LED-200', 'PC-2B'],
   'manufacturer': ['SensorTech', 'SafetyPro', 'DriveMax', 'IllumiTech', 'AirPower'],
   'category': ['Sensors', 'PPE', 'Motor Controls', 'Lighting', 'Pneumatics'],
   'description': [
       'Pressure sensor',
       'Work gloves',
       'Motor drive',
       'LED light',
       'Air cylinder'
   ],
   'specifications': [
       '0-100 PSI, 4-20mA output',
       'ANSI Cut Level 5, Nitrile palm',
       '10HP, 480V 3-phase',
       '200W, 28000 lumens, 5000K',
       '2" bore, 12" stroke'
   ],
   'price': ['$149.99', '$34.99', '$1,299.99', '$389.99', '$219.99'],
   'industry': ['industrial'] * 5
})

products.to_excel('test_products.xlsx', index=False)
print("Created test_products.xlsx")
