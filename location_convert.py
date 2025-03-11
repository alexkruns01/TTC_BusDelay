from geopy.geocoders import ArcGIS
import geopy.geocoders
import csv
import ssl
import certifi

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


def date_format(date: str):
    """
    change string <date> format from DD-MM-YY to YY-MM-DD
    :param date:
    :return: str
    """
    d = date.split('-')
    return f"{d[2]}-{d[1]}-{d[0]}"


def print_outlier(address):
    """
    return True if address is inaccurate.
    By inaccurate, if coordinate is not in the vicinity of GTA
    :param address:
    :return Bool:
    """
    return "Ontario" not in address.address or not (43.428982 < address.latitude < 44.037264
                                                    and -79.878022 < address.longitude < -79.022919)


def geocode_address(csv_read, csv_write):
    """
    read location from <csv_file>, and write data with full address
    with coordinates on a new csv file <csv_write>
    """
    my_geocode = ArcGIS()

    header = next(csv_read)
    csv_write.writerow(header + ["Latitude", "Longitude", "Address"])

    address_dict = {}
    for line in csv_read:
        # To improve speed only search through geocode if new location(not in dict key) is searched
        if line[4] not in address_dict:
            address = my_geocode.geocode(f"{line[4]}, Ontario, Canada")

            # if address is inaccurate, then print the inaccurate address and retry geocoding
            if print_outlier(address):
                print(address.latitude, address.longitude, address.address)
                address = my_geocode.geocode(f"{line[4]}, Toronto, Canada")
                print(address.latitude, address.longitude, address.address, line[4], '\n')

            address_dict[line[4]] = address

        lat = [address_dict[line[4]].latitude]
        long = [address_dict[line[4]].longitude]
        address = [address_dict[line[4]].address]

        date = [date_format(line[0])]

        csv_write.writerow(date + line[1:] + lat + long + address)


def main():
    my_geocode = ArcGIS()
    with open("ttc-bus-delay-data-2024.csv", newline='') as csvfile:
        with open("final_ttc_bus_delay_2024.csv", 'w', newline='') as new_csv:
            write = csv.writer(new_csv)
            reader = csv.reader(csvfile)

            geocode_address(reader, write)


if __name__ == '__main__':
    main()
