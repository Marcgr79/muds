import csv
from dataclasses import dataclass

@dataclass
class Population:
    borough: str
    nta_name: str
    nta_code: str
    population: int
    year: str

@dataclass
class School:
    nta_code: str
    nta_name: str
    location_category_description: str
    borough: str = ''

def create_dict(file_path):

    data_dict = []

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_dict.append(row)

    return data_dict

population_dict = create_dict('population.csv')
schools_dict = create_dict('school.csv')

population = [Population(**entry) for entry in population_dict]
school = [School(**entry) for entry in schools_dict]
        
def percentage_borough(borough):
    borough_entries = [entry for entry in population if entry.borough == borough]
    population_borough = sum(int(entry.population) for entry in borough_entries)
    total_population = sum(int(entry.population) for entry in population)
    
    percentage = (population_borough / total_population) * 100
    
    print(f"Porcentaje de poblacion en {borough}: {percentage:.2f}%")
    
def percentage_schools(borough):
    schools_borough = sum(1 for school in school if school.borough == borough)
    total_schools = len(school)
    
    percentage2 = (schools_borough / total_schools) * 100
    print(f"Porcentaje de escuelas en {borough}: {percentage2:.2f}%") 

def distribution_schools(location_category_description):
    total_cateogry = sum(1 for entry in school if entry.location_category_description == location_category_description)
    total_schools = len(school)
    
    percentage_type = (total_cateogry / total_schools) * 100
    print(f"Porcentaje de escuelas del tipo {location_category_description}: {percentage_type:.2f}%")
    
def ratio_schools(borough):
    borough_entries = [entry for entry in school if entry.borough == borough]
    
    schools_borough = len(borough_entries)
    population_borough = sum(int(entry.population) for entry in population)
    
    ratio = (schools_borough / population_borough) * 10000
    print(f"{borough} tiene {ratio:.2f} escuelas por cada 10.000 habitantes")
    
def hello_word():
    print('successful')

#percentage_schools('Brooklyn')
#percentage_schools('Queens')
#percentage_schools('Bronx')
#percentage_schools('Manhattan')
#percentage_schools('Staten Island')

#percentage_borough('Brooklyn')
#percentage_borough('Queens')
#percentage_borough('Bronx')
#percentage_borough('Manhattan')
#percentage_borough('Staten Island')

#ratio_schools('Brooklyn')
#ratio_schools('Queens')
#ratio_schools('Bronx')
#ratio_schools('Manhattan')
#ratio_schools('Staten Island')
