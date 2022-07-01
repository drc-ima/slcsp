import csv
import collections
import sys


def get_silver_rates_by_rate_area(plans_path: str):

    try:
        # open plans.csv file
        plans = open(plans_path, mode="r")
        # variable to hold the state by rate area and their corresponding rate
        silver_rates_by_rate_area = collections.defaultdict(set)
        print(silver_rates_by_rate_area['happy'].add(123))

        for row in csv.DictReader(plans):
            # check for only Silver plan
            if row["metal_level"] == "Silver":
                # concat state and rate area to get label
                state_rate_label = row["state"] + " " + row["rate_area"]
                silver_rates_by_rate_area[state_rate_label].add(float(row["rate"]))
    except Exception as e:
        print("Something bad happened here.")
        raise e
    return silver_rates_by_rate_area


def get_rate_areas_by_zipcode(zips_path: str):

    try:
        # import zip file
        zips = open(zips_path, mode="r")
        # variable to hold the zipcodes and their corresponding state and rate area
        rate_areas_by_zipcode = collections.defaultdict(set)

        # looping through the zip file to update the rate_areas_by_zipcode dict
        for row in csv.DictReader(zips):
            # concat state and rate area to get zipcode label
            rate_areas_by_zipcode[row["zipcode"]].add(row["state"] + " " + row["rate_area"])
    except Exception as e:
        print("Error occured somewhere")
        raise e
    return rate_areas_by_zipcode


def get_slcsp_by_zipcode(zipcode: str, silver_rates_by_rate_area: dict, rate_areas_by_zipcode: dict):

    try:
        # parse zipcode item as list to access them by index
        rate_area = list(rate_areas_by_zipcode[zipcode])[0]
        
        # rate output for each zipcode
        rate_output = ""
        # check if the zipcode appears onces in the rate_areas_by_zipcode and the rate area is in the silver_rates_by_rate_area
        if len(rate_areas_by_zipcode[zipcode]) == 1 and rate_area in silver_rates_by_rate_area:
            # checking if the rate area per zipcode is more than or equals to two to be able to access the second lowest rate
            if len(silver_rates_by_rate_area[rate_area]) >= 2:
                # sort the list by converting set to a sorted list
                sorted_rates = sorted(silver_rates_by_rate_area[rate_area])
                # formatting for fixed 2 decimal places
                rate_output = "{:.2f}".format(sorted_rates[1])
    except Exception as e:
        print("Error occured somewhere")
        raise e
    return rate_output


def output(slcsp_path: str, rate_areas_by_zipcode: dict, silver_rates_by_rate_area: dict):

    try:
        # output the slcsp file
        slcsp = open(slcsp_path, mode="r")
        for row in csv.DictReader(slcsp):
            # using the get_slcsp_by_zipcode() function to to get the rate output per zipcode
            rate = get_slcsp_by_zipcode(row["zipcode"], silver_rates_by_rate_area, rate_areas_by_zipcode)
            # stdout to console
            sys.stdout.write(f'{row["zipcode"]},{rate}\n')
            
    except Exception as e:
        print("Error occured somewhere")
        raise e
    return


if __name__ == "__main__":

    silver_rates_by_rate_area = get_silver_rates_by_rate_area('plans.csv')

    rates_area_by_zipcode = get_rate_areas_by_zipcode('zips.csv')

    output('slcsp.csv', rates_area_by_zipcode, silver_rates_by_rate_area)

