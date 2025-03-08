from geopy.geocoders import ArcGIS
import geopy.geocoders
import csv
import ssl
import certifi

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


def new_csv_address(csv_file, csv_write):
    """
    read location from <csv_file>, and write data with full address
    with coordinates on a new csv file <csv_write>
    """

    my_geocode = ArcGIS()
    with open(csv_file, newline='') as csvfile:
        with open(csv_write, 'w', newline='') as new_data:
            write = csv.writer(new_data)
            reader = csv.reader(csvfile)

            header = next(reader)
            # Remove Location header as lat, long, ad will be appended to end of the line
            header.pop(4)
            write.writerow(header + ["Latitude", "Longitude", "Address"])

            address_dict = {}
            for line in reader:
                # To improve speed only search through geocode if new location(not in dict key) is searched
                if line[4] not in address_dict:
                    address = my_geocode.geocode(f"{line[4]}, Ontario")
                    address_dict[line[4]] = address
                lat = [address_dict[line[4]].latitude]
                long = [address_dict[line[4]].longitude]
                address = [address_dict[line[4]].address]

                # Remove partial address on index 4 of the line. Does not change <csv_file>
                line.pop(4)
                write.writerow(line + lat + long + address)


def main():
    new_csv_address('ttc-bus-delay-data-2024.csv', "final_ttc_bus_delay_2024.csv")


if __name__ == '__main__':
    main()
