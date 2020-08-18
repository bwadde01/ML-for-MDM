import random
import numpy as np
import pandas as pd
from pydbgen import pydb


# randomly sets fields to NULL
def random_null(value, threshold):
    a = random.random()
    if a < threshold:
        return ""
    else:
        return value
        
def perturb_name(name, threshold):
    
    def random_swap(name):
        if len(name) < 2:
            return name
        else:
            swap_pos = int(random.uniform(0,len(name)-2))
            list_name = list(name)
            temp = list_name[swap_pos]
            list_name[swap_pos] = list_name[swap_pos+1]
            list_name[swap_pos+1] = temp
            return "".join(list_name)
    
    a = random_null(name,threshold)
    if a == "":
        return a
    else:
        # 35% will be same
        # 15% will be first name last initial
        # 15% will be first initial last name
        # 10% will be typographical error in last name
        # 10% will be typographical error in first name
        # 10% will be just first name
        # 5% will be swapped first and last
        b = random.random()
        if b < .35: 
            return name
        elif b < .50:
            return name.split(" ")[0] + " " + list(name.split(" ")[1])[0]
        elif b < .65:
            return list(name.split(" ")[0])[0] + " " + name.split(" ")[1]
        elif b < .75:
            return name.split(" ")[0] + " " + random_swap(name.split(" ")[1])
        elif b < .85:
            return random_swap(name.split(" ")[0]) + " " + name.split(" ")[1]
        elif b < .95:
            return name.split(" ")[0]
        else: 
            return name.split(" ")[1] + " " + name.split(" ")[0]

def perturb_bday(bday, threshold):

    def change_format(bday):
        bday_items = list(map(str,bday.split(" ")))
        random.shuffle(bday_items)
        return "-".join(bday_items)
    
    a = random_null(bday,threshold)
    if a == "":
        return a
    else: 
        b = random.random()
        if b < .15:
            return change_format(bday)
        else: return bday
        
def perturb_ssn(ssn, threshold=.15):
    return random_null(ssn,threshold)

def perturb_rssd_id(rssd, threshold=.4):
    return random_null(rssd,threshold)    
    
def perturb_duns(duns, threshold=.4):
    return random_null(duns,threshold)    
    
def perturb_country(country, threshold=.2):
    return random_null(country,threshold)

def perturb_city(city, threshold=.3):
    return random_null(city,threshold)
    
def perturb_state(state, threshold=.3):
    return random_null(state,threshold)

def perturb_zip(zip,threshold=.4):
    
    def gen_rand_zip():
        return "".join(list(map(str,np.random.randint((9,9,9,9,9)))))
    
    a = random_null(zip,threshold)
    if a == "":
        return a
    else: 
        b = random.random()
        if b < .05:
            return gen_rand_zip()
        else: 
            return zip    


def perturb_phone(phone,threshold=.5):
    
    def gen_rand_phone():
        return "".join(list(map(str,np.random.randint((9,9,9,9,9,9,9,9,9,9)))))
    
    a = random_null(phone,threshold)
    if a == "":
        return a
    else: 
        b = random.random()
        if b < .05:
            return gen_rand_phone()
        else: 
            return phone    


def perturb_address(address,threshold=.3):
        
    def reference_abbrevs(address_final_part):
        abbrevs = pd.read_excel("address_abbrevs.xlsx")
        filtered = abbrevs[abbrevs['Formal']==address_final_part.upper()]
        if len(filtered) > 0:
            all_abbrevs = filtered['Abbreviation'].values
            rand_index = int(random.randint(0,len(all_abbrevs)-1))
            return all_abbrevs[rand_index]
        else:
            return address_final_part
    
    address = " ".join(address.split(" ")[:-1]) + " " + reference_abbrevs(address.split(" ")[-1])
    
    a = random_null(address,threshold)
    if a == "":
        return a
    else: 
        # 35% -> same
        # 15% -> just part 1
        # 15% -> just part 2
        # 15% -> just part 3
        # 5% -> random address same
        
        if len(address.split(" "))<3:
            return address
        else:
            b = random.random()
            if b < .5:
                return address
            elif b < .65: 
                return address.split(" ")[0] 
            elif b < .8: 
                return address.split(" ")[1] 
            elif b < .95: 
                return address.split(" ")[2] 
            else:
                return "8876 Heather Ave."
        
if __name__ == '__main__':
    myDB = pydb()
    df = pd.DataFrame()
    data = myDB.gen_dataframe(10000,['name','date','ssn','country','street_address','city','state','zipcode','company','phone_number_full'])
    df = pd.concat([df,data])
    
    for i in range(4):
        df = pd.concat([df,data.sample(9000)])
    
    df.sort_index(inplace=True)

    df['duns']=df['ssn'].apply(lambda x: 1+int("".join(x.split("-"))))
    df['rssd_id']=df['ssn'].apply(lambda x: 2+int("".join(x.split("-"))))
    
    df['perturbed_name'] = df['name'].apply(perturb_name,threshold=.05)
    df['perturbed_bday'] = df['date'].apply(perturb_bday,threshold=.4)
    df['perturbed_ssn'] = df['ssn'].apply(perturb_ssn)
    df['perturbed_rssd_id'] = df['rssd_id'].apply(perturb_rssd_id)
    df['perturbed_duns'] = df['duns'].apply(perturb_duns)
    df['perturbed_country'] = df['country'].apply(perturb_country)
    df['perturbed_city'] = df['city'].apply(perturb_city)
    df['perturbed_state'] = df['state'].apply(perturb_state)
    df['perturbed_zip'] = df['zipcode'].apply(perturb_zip)
    df['perturbed_phone'] = df['phone_number_full'].apply(perturb_phone)
    df['perturbed_address'] = df['street_address'].apply(perturb_address)
    

    df.to_csv("perturbed_MDM_data.csv")
    





