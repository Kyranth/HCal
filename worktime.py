# This program calculates hours for a week
# from a file as input using the datetime library

from datetime import datetime

class Worktime:
    """ This program calculates hours for an entire week including break time
    in 12 hour format
    """
    # constructor
    def __init__(self, path:str) -> None:
        """Initiates attributes to save data then
        reads from the file and parses data into a dictionary.

        Args:
            path (str): file path as a string
        """
        self.data = []
        self.week = dict()
        self.read_from_file(path)
        self.parse_data()

    def read_from_file(self, file_path:str) -> None:
        """Reads data from a file and saves into the class attribute @data

        Args:
            file_path (str): given file path as a string
        """
        try:
            # Using readlines()
            self.given_file = open(file_path, 'r')
            self.data = self.given_file.readlines()
            for i in range(len(self.data)):
                self.data[i] = self.data[i].split()
        
        except FileNotFoundError as e:
            print(f"{file_path} not found")

    def print_output(self):
        for i in range(1, 8):
            print(f"\t{self.data[i][0]} : {self.data[i][1:]}")
        print()

    def parse_data(self):
        """ Converts data to an dictionary
        days as keys
        times information as values, which is an array
        """
        for i in range(1, 8):
            self.week[self.data[i][0]] = self.data[i][1:]
    
    def convert_hours(self, time:str):
        """Converts 12 hour time into 24 hour

        Args:
            time (str): time as string

        Returns:
            str: returns 24 hour time
        """
        # Checking if last two elements of time
        # is AM and first two elements are 12
        if time[-2:] == "am" and time[:2] == "12":
            return "00" + time[2:-2]
            
        # remove the AM
        elif time[-2:] == "am":
            return time[:-2]
        
        # Checking if last two elements of time
        # is PM and first two elements are 12
        elif time[-2:] == "pm" and time[:2] == "12":
            return time[:-2]
            
        else:
            # add 12 to hours and remove PM
            return str(int(time[:2]) + 12) + time[2:5]

    def calculate_hours(self):
        """Calculates hours for a given week

        Returns:
            int: number of hours
        """
        print(f"Week info:")
        self.print_output()

        total = 0

        print("Week Breakdown:")
        for key, val in self.week.items():
            if (len(val) == 0):
                continue
            start_time = val[0]
            end_time = val[1]
            break_time = val[2]

            # creates datetime object to calculate time differences
            starttime = datetime.strptime(self.convert_hours(start_time), "%H:%M")
            endtime = datetime.strptime(self.convert_hours(end_time), "%H:%M")

            # get hours without break
            unweighed_hours = endtime - starttime
            # get time with break in seconds and convert back to hours
            weighed_hours = (unweighed_hours.total_seconds() - (int(break_time) * 60)) / 3600
            
            # Week breakdown
            print(f"\t{key} : ({end_time} - {start_time}) = {weighed_hours} hours")
            total += weighed_hours
        
        # print total hours
        print(f"Total hours: {total}")


if __name__ == '__main__':
    calculator = Worktime("worktime.csv")
    calculator.calculate_hours()
