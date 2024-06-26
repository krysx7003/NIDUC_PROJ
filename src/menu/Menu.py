from src.menu.MenuConsts import MenuConsts as menuConsts
from src.settings.Setting import Setting
from src.simulationElements.Time import Time #import Customer as Client, Time, Employee,  ProfitCalculator, Queue
from src.simulationElements.Customer import Client 
from src.simulationElements.Employee import Employee 
from src.simulationElements.Queue import Queue 
from src.simulationElements.ProfitCalculator import ProfitCalculator 
from src.simulationElements.Result import Result 
import os
import random
import platform 
import numpy as np
import matplotlib.pyplot as plt

class Menu:
    def __init__(self):
        self.settings = Setting()  # I have reamoved the shop variable because the settings variable already containes the shop object so there is no point to do so
        self.time =  Time()
        self.profit_calculator = None
        self.potential_profit_lost = 0;
        self.queue = Queue()
        self.employees = []
        self.option = 0
        self.shouldExit = False
        self.days = []
        self.result = Result()

    # Method simualtes a working day in the store
    def simulate_day(self, dataSource):
        self.settings.setShop(self.create_random_shop(dataSource))
        self.profit_calculator = ProfitCalculator(self.settings.getShop())
        for shift in range(1, 3):
            start_time = (6) if shift == 1 else (14)
            for employee in self.employees:
                # Rozwiązanie tymczasowe
                if shift == 1:
                    employee.start_shift(start_time)
            self.run_shift(shift)
        # Podsumowanie dnia
        self.result.getProfit().append(self.profit_calculator.calculate_daily_profit())
        self.result.getLoss().append(self.profit_calculator.calculate_daily_loss())

    # Method creates or fetches shop from the user options and creates new employees for that
    def create_random_shop(self, dataSource):
        shop = self.settings.getShop()
        if (dataSource == 2): 
            shop.setWorkerNumber(random.randint(1,10))
            shop.setRegularCheckoutsNumber(random.randint(1,5))
            shop.setSelfServiceCheckoutsNumber(random.randint(1,5))
        self.employees = [Employee(i, f'Pracownik_{i}') for i in range(shop.getWorkerNumber())]
        return shop

    # Method runnes the shift of the employees
    def run_shift(self, shift):
        # Ustaw czas początku i końca zmiany
        start_time, end_time = (6, 14) if shift == 1 else (14, 22)

        # Przetwarzanie klientów dla każdej godziny zmiany
        for hour in range(start_time, end_time):
            self.time.current_time = hour
            clients_this_hour = self.generate_customers()
            for client in clients_this_hour:
                self.queue.add_customer(client)
            self.process_customers_queue()
            self.queue.tick_time(1)
            self.queue.descreseClientsSatisfactionLevel();

    # Method generates the customers for the simulation
    def generate_customers(self):
        # Generowanie klientów z krzywej gaussa, z najwyższym punktem około godziny 15
        mean = 15 - self.time.current_time  # przesunięcie średniej
        num_customers = int(abs(np.random.normal(mean, 1)) * 10)  # przykładowe wartości
        return [Client() for _ in range(num_customers)]

    # Method process the customer queue
    def process_customers_queue(self):
        if self.settings.getShop() is None or self.profit_calculator is None:
            raise ValueError("Simulation error!")
        # Przetwarzanie kolejki klientów
        numRemovedClients = 0
        while not self.queue.is_empty() and self.settings.getShop().is_open(self.time):
            for employee in self.employees:
                if not employee.is_on_shift(self.time.current_time):
                    continue
                customers_to_process = min(self.queue.get_length(), employee.process_customers(random.randint(1, 3)))
                for _ in range(customers_to_process):
                    customer = self.queue.remove_customer(0)
                    if customer is None:
                        continue
                    self.result.updatedSatisfactionScore(customer.getSatisfactionLevel())
                    self.profit_calculator.add_profit(customer.get_spent_money())
                numRemovedClients = self.queue.remove_long_waiting_customers()  
                self.result.updatedLostClients(numRemovedClients)

    # Method runs the main menu till shouldExit variable of object is changed to True
    def mainMenuRunner(self):
        while not self.shouldExit:
            self.printMainMenu()
            self.setOption(self.inputController(menuConsts.mainMenuLowerBounderie, menuConsts.mainMenuHigherBounderie))
            self.mainMenuControler()
            self.clearTerminal()

    # Method takes the time and process of the simulation 
    def simulationRunner(self, dataSource):
        print("How long should simmulation run")
        daysToRun = self.readInput()
        currentDay = 1
        modulo = daysToRun/10
        for currentDay in range(1,daysToRun):
            self.simulate_day(dataSource)
            self.days.append(currentDay)
            if not currentDay % modulo:
                print(f"Results of simulation after {currentDay} days:\n")
                self.printResults()
                print("\n")

    # Print main menu with options
    def printMainMenu(self):
        print("Main menu of shop simulation")
        print("1. Print simulation settings")
        print("2. Set simulation settings")
        print("3. Print chart from the simulation")
        print("4. Print results")
        print("5. Save to file")
        print("6. Run simulation")
        print("7. Open file with results")
        print("8. Exit application")
        print("Enter number related to the option")


    # Controler of main menu, who based on the option invokes next operations
    def mainMenuControler(self):
        if menuConsts.printSimulationSettings == self.getOption():
            self.settings.printAllSettings()
        elif menuConsts.setSimulationSettings == self.getOption():
            self.settings.setAllSettings()
        elif menuConsts.printChart == self.getOption():
            self.printChart()
        elif menuConsts.printResults == self.getOption():
            self.printResults()
        elif menuConsts.saveToFile == self.getOption():
            self.saveToFile()
        elif menuConsts.runSim == self.getOption():
            self.simulationRunner(self.determinDataSource())
        elif menuConsts.openResultFile == self.getOption():
            self.openResultFile()
        elif menuConsts.exitApp == self.getOption():
            self.exitApp()

    # Function determines the source of options for the simulation
    def determinDataSource(self):
        print(f"What should be source of data for simulation?")
        print(f"1. Saved in options")
        print(f"2. Randomly generated")
        return self.inputController(1,2)

    # Method controles and validates the input from the user
    def inputController(self, lowerLimit, higherLimit):
        isInputCorrect = False  
        tmp = 0
        while not isInputCorrect:
            tmp = self.readInput()
            isInputCorrect = self.handleInput(tmp, lowerLimit, higherLimit)  
        return int(tmp) 

    # Method takes input from the user and tries to convert it to number. In case of exception method returns 0
    def readInput(self):
        tmp = input("> ")
        try:
            number = int(tmp)
            return  number
        except(ValueError, TypeError):
            print("Option must be a number")
            return 0

    # Checks if the input of user which is an argument is correct value from the range of numbers
    def handleInput(self, input, lowerLimit, higherLimit):
        if lowerLimit > int(input) or higherLimit < int(input):
            return False
        else:
            return True

    # Method creates the chart which represent the simulation runned
    def printChart(self):
        plt.figure(0,dpi=120)
        plt.plot(self.days,self.result.getProfit(),'o',label="Profit")
        plt.plot(self.days,self.result.getLoss(),'o',label="Loss")
        plt.legend()
        plt.show()
        return

    # Method prints the current result of simulation to the default output stream
    def printResults(self):
        if not self.profit_calculator:
            print("No results available. Please run the simulation first.")
            return 
        daily_profit = self.profit_calculator.daily_profit 
        potential_profit_lost = self.profit_calculator.get_potential_profit_lost()
        avgSatisfactionLevel = self.result.calculateAvgSatisfactionLevel()
        print(f"Daily profit: {daily_profit}")
        print(f"Potential profit lost: {potential_profit_lost}")
        print(f"Average satisfaction level of customers: {avgSatisfactionLevel}")
        print("Number of served clients: ", self.result.getProccessedClients())
        print("Number of lost clients: ", self.result.getLostClients())
    
    # Method returns to the user content of the file with result of the simulation current and previous one 
    def openResultFile(self):
        try: 
            with open('simulationResult.txt','r') as file:
                file_content = file.read()
                print(f"Content of result file: \n")
                print(file_content)
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Premission denied. Please check your permission.")
        except Exception as e:
            print(f"An unexpected error occured: {e}")

    # Method chcecks if the simulation was runned and if there was a simulation function saves the results to simulationResult.txt file 
    def saveToFile(self):
        if self.profit_calculator is None:
            print("No results available. Please run the simulation first.")
            return
        with open('simulationResult.txt','a') as file:
            file.write("---------------------------------------------------------------------\n")
            file.write("Daily profit: " + str(self.profit_calculator.daily_profit)  + "\n")
            file.write("Potential profit lost: " + str(self.profit_calculator.get_potential_profit_lost()) + "\n")
            file.write("---------------------------------------------------------------------\n")
        return 
    

    # Functions clears terminal after any key was pressed
    def clearTerminal(self):
        input("Press any key...")
        current_os = platform.system()
        if current_os == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    # Function sets the shouldExit option on true
    def exitApp(self):
        self.shouldExit = True
        return 

# GETTERS AND SETTERS
    def getOption(self):
        return self.option
    def setOption(self, option):
        self.option = option
 
        
