from geopy.geocoders import ArcGIS
import geopy.geocoders
import csv
import ssl
import certifi

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


def new_csv_address(csv_file, csv_write):
    """
    return a dictionary of incomplete address as key and complete address and value from <csv_file>
    """
    my_geocode = ArcGIS()
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        address_dict = {}
        with open(csv_write, 'w', newline='') as new_data:
            write = csv.writer(new_data)
            for line in reader:
                if line[4] not in address_dict:
                    address = my_geocode.geocode(f"{line[4]}, Ontario")
                    address_dict[line[4]] = address
                line[4] = address_dict[line[4]]
                write.writerow(line)


def main():
    new_csv_address('ttc-bus-delay-data-2024.csv', "final_ttc_bus_delay_2024.csv")


if __name__ == '__main__':
    main()
