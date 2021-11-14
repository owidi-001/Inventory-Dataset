import csv
from datetime import date


def full_inventory(inventory_list):
    with open('FullInventory.csv', 'w', newline='') as fullinventory:
        fieldnames = ['ID', 'manufacturer_name', 'item_type', 'price', 'service_date', 'is_damaged']
        fullinventory = csv.DictWriter(fullinventory, fieldnames=fieldnames)

        fullinventory.writeheader()
        for item in inventory_list:
            fullinventory.writerow(item)


def item_type(inventory_list):
    items = []
    for inventory in inventory_list:
        if inventory['item_type'] not in items:
            items.append(inventory['item_type'])
    for item in items:
        with open(f'{item}Inventory.csv', 'w', newline='') as itemInventory:
            fieldnames = ['ID', 'manufacturer_name', 'price', 'service_date', 'is_damaged']
            itemInventory = csv.DictWriter(itemInventory, fieldnames=fieldnames)

            itemInventory.writeheader()
            for row in inventory_list:
                if row['item_type'] == item:
                    row = {key: val for key, val in row.items() if key != 'item_type'}
                    itemInventory.writerow(row)


def past_service_date(inventory_list):
    now_date = date.today()
    with open('PastServiceDateInventory.csv', 'w', newline='') as pastservicedate:
        fieldnames = ['ID', 'manufacturer_name', 'item_type', 'price', 'service_date', 'is_damaged']
        pastservicedate = csv.DictWriter(pastservicedate, fieldnames=fieldnames)

        pastservicedate.writeheader()
        for item in inventory_list:
            service_date = item['service_date'].split('/')
            if len(service_date[0]) == 1:
                service_date[0] = '0'+service_date[0]
            if len(service_date[1]) == 1:
                service_date[1] = '0'+service_date[1]
            service_date[0], service_date[1], service_date[2] = service_date[2], service_date[0], service_date[1]
            service_date = '-'.join(service_date)
            service_date = date.fromisoformat(service_date)
            if service_date > now_date:
                pastservicedate.writerow(item)


def damaged_inventory(inventory_list):
    with open('DamagedInventory.csv', 'w', newline='') as damagedinventory:
        fieldnames = ['ID', 'manufacturer_name', 'item_type', 'price', 'service_date']
        damagedinventory = csv.DictWriter(damagedinventory, fieldnames=fieldnames)

        damagedinventory.writeheader()
        for row in inventory_list:
            if row['is_damaged'] == 'damaged':
                row = {key: val for key, val in row.items() if key != 'is_damaged'}
                damagedinventory.writerow(row)


if __name__ == '__main__':
    inventory_list = []

    with open('ManufacturerList .csv', 'r') as manufacturer_list:
        manufacturer_list = csv.reader(manufacturer_list)

        for manufacturer in manufacturer_list:
            inventory = {'ID': manufacturer[0], 'manufacturer_name': manufacturer[1],
                         'item_type': manufacturer[2],
                         'is_damaged': manufacturer[3]}

            inventory_list.append(inventory)

    with open('PriceList.csv', 'r') as price_list:
        price_list = csv.reader(price_list)

        price_list = dict(price_list)

        for inventory in inventory_list:
            inventory_id = inventory['ID']
            if inventory_id in price_list:
                inventory['price'] = price_list[inventory_id]

    with open('ServiceDatesList .csv', 'r') as service_dates:
        service_dates = csv.reader(service_dates)

        service_dates = dict(service_dates)

        for inventory in inventory_list:
            inventory_id = inventory['ID']
            if inventory_id in service_dates:
                inventory['service_date'] = service_dates[inventory_id]

    full_inventory(inventory_list)
    item_type(inventory_list)
    past_service_date(inventory_list)
    damaged_inventory(inventory_list)
