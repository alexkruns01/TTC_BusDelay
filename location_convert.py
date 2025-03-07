from geopy.geocoders import ArcGIS
import geopy.geocoders
import csv
import ssl
import certifi

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_
ssl_context = ctx


def main():
    my_geocode = ArcGIS()
    with open('ttc-bus-delay-data-2024.csv', newline='') as csvfile:
        delay_reader = csv.reader(csvfile)
        next(delay_reader)
        g = 0
        for line in delay_reader:
            g += 1
            n = my_geocode.geocode(f"{line[4]}, Toronto")
            print(my_geocode.geocode(n))
            print(n[::])
            if g == 100:
                break



if __name__ == '__main__':
    main()
