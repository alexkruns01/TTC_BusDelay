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
    if len(d[0]) == 1:
        d[0] = f"0{d[0]}"

    month_dict = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }
    d[1] = month_dict[d[1]]

    return f"20{d[2]}-{d[1]}-{d[0]}"


def is_outlier(address):
    """
    return True if address is inaccurate.
    By inaccurate, if coordinate is not in the vicinity of GTA
    :param address:
    :return Bool:
    """
    return not (43.550789 < address.latitude < 43.920318
                and -79.90089 < address.longitude < -78.948069)


def get_gta_address(address):
    """
    return full address from incomplete str address <address>
    :param address:
    :return str:
    """
    my_geocode = ArcGIS()
    full_address = my_geocode.geocode(f"{address}, Toronto, Canada")

    # if address is inaccurate, then print the inaccurate address and retry geocoding
    while is_outlier(full_address):
        print(f"REPEAT, {address}, {full_address}", end='', flush=True)
        full_address = my_geocode.geocode(f"{address}, Toronto, Canada")
        if not is_outlier(full_address):
            return full_address
        full_address = my_geocode.geocode(f"{address}, York, Canada")
        if not is_outlier(full_address):
            return full_address
        full_address = my_geocode.geocode(f"{address}, Scarborough, Canada")
        if not is_outlier(full_address):
            return full_address
        full_address = my_geocode.geocode(f"{address}, Etobicoke, Canada")
        if not is_outlier(full_address):
            return full_address

    return full_address


def geocode_address(csv_read, csv_write):
    """
    read location from <csv_file>, and write data with full address
    with coordinates on a new csv file <csv_write>
    """
    header = next(csv_read)
    csv_write.writerow(header + ["Latitude", "Longitude", "Address"])

    address_dict = {}
    for line in csv_read:
        print('-', flush=True)
        # To improve speed only search through geocode if new location(not in dict key) is searched
        if line[4] not in address_dict:
            address_dict[line[4]] = get_gta_address(line[4])
        else:
            print('_', flush=True)

        lat = [address_dict[line[4]].latitude]
        long = [address_dict[line[4]].longitude]
        address = [address_dict[line[4]].address]

        date = [date_format(line[0])]

        csv_write.writerow(date + line[1:] + lat + long + address)


def main():
    # my_geocode = ArcGIS()
    # print(my_geocode.geocode("VICTORIA PARK, Toronto, Canada"))

    with open("ttc-bus-delay-data-2024.csv", newline='') as csvfile:
        with open("final_ttc_bus_delay_2024.csv", 'w', newline='') as new_csv:
            write = csv.writer(new_csv)
            reader = csv.reader(csvfile)

            geocode_address(reader, write)


if __name__ == '__main__':
    main()
