from src.menu.MenuConsts import MenuConsts as menuConsts
from src.settings.Setting import Setting
from src.simulationElements import Shop, ProfitCalculator, Queue
from src.simulationElements.Time import Time
from src.simulationElements.Queue import Queue
from src.simulationElements.Customer import Client
from src.simulationElements.Shop import Shop
from src.simulationElements.Employee import Employee
from src.simulationElements.ProfitCalculator import ProfitCalculator
import os
import random
import numpy as np
import matplotlib.pyplot as plt

class Menu:
    def __init__(self):
        self.settings = Setting()
        self.shop = None
        self.time = Time()
        self.profit_calculator = None
        self.potential_profit_lost = 0;
        self.queue = Queue()
        self.employees = []
        self.option = 0
        self.shouldExit = False
        self.days = []
        self.profit = []
        self.loss = []

    # ... [inne metody klasy]

    def simulate_day(self):
        # Losowanie sklepu zgodnie z poleceniem 1.
        self.shop = self.create_random_shop()
        self.profit_calculator = ProfitCalculator(self.shop)
        # Symulacja zmian zgodnie z poleceniem 2.
        for shift in range(1, 3):
            start_time = (6) if shift == 1 else (14)
            for employee in self.employees:
                # Rozwiązanie tymczasowe
                if shift == 1:
                    employee.start_shift(start_time)
            self.run_shift(shift)
        # Podsumowanie dnia
        self.profit.append(self.profit_calculator.calculate_daily_profit())
        self.loss.append(self.profit_calculator.calculate_daily_loss())

    def create_random_shop(self):
        # Należy dodać opcje tworzenia losowego sklepu lub tego zaincjalizowanego przez user-a
        # Losuj liczbę pracowników, kas normalnych i samoobsługowych
        num_employees = random.randint(1, 10)  # przykładowy zakres
        num_regular_checkouts = random.randint(1, 5)
        num_self_service_checkouts = random.randint(1, 5)

        # Tworzenie pracowników
        self.employees = [Employee(i, f'Pracownik_{i}') for i in range(num_employees)]

        # Tworzenie sklepu
        shop = Shop()
        shop.setWorkerNumber(num_employees)
        shop.setRegularCheckoutsNumber(num_regular_checkouts)
        shop.setSelfServiceCheckoutsNumber(num_self_service_checkouts)
        return shop

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

    def generate_customers(self):
        # Generowanie klientów z krzywej gaussa, z najwyższym punktem około godziny 15
        mean = 15 - self.time.current_time  # przesunięcie średniej
        num_customers = int(abs(np.random.normal(mean, 1)) * 10)  # przykładowe wartości
        return [Client() for _ in range(num_customers)]

    def process_customers_queue(self):
        if self.shop is None or self.profit_calculator is None:
            raise ValueError("Simulation error!")
        # Przetwarzanie kolejki klientów
        while not self.queue.is_empty() and self.shop.is_open(self.time):
            for employee in self.employees:
                if employee.is_on_shift(self.time.current_time):
                    # Obsłuż klientów, zakładając, że każdy pracownik może obsłużyć około 3 klientów na minutę
                    customers_to_process = min(self.queue.get_length(), employee.process_customers(1))
                    for _ in range(customers_to_process):
                        customer = self.queue.remove_customer(0)
                        if customer is not None:
                            self.profit_calculator.add_profit(customer.get_spent_money())
                    # Sprawdź, czy klienci nie oczekiwali zbyt długo
                    self.queue.remove_long_waiting_customers(30)  # 30 minut

    # Metoda sprawdzająca, czy klasa jest pusta (potrzebna dla procesowania kolejki)
    def is_empty(self):
        return len(self.clients) == 0

    # Metoda do usuwania klientów czekających zbyt długo
    def remove_long_waiting_customers(self, max_waiting_time):
        # Usuń klientów, którzy czekają dłużej niż max_waiting_time
        self.clients = [customer for customer in self.clients if customer.waiting_time < max_waiting_time]
        # Potencjalnie utracony zysk dla tych, którzy odeszli
        self.potential_profit_lost += sum(customer.spent_money for customer in self.clients if customer.waiting_time >= max_waiting_time)
    # Method runs the main menu till shouldExit variable of object is changed to True
    def mainMenuRunner(self):
        while not self.shouldExit:
            self.printMainMenu()
            self.setOption(self.inputController(menuConsts.mainMenuLowerBounderie, menuConsts.mainMenuHigherBounderie))
            self.mainMenuControler()
            self.clearTerminal()
    # Metoda pobiera długoś symulacji i ją wykonuje
    def simmulationRunner(self):
        print("How long should simmulation run")
        daysToRun = self.readInput()
        currentDay = 1
        for currentDay in range(1,daysToRun):
            self.simulate_day()
            self.days.append(currentDay)

    # Print main menu with options
    def printMainMenu(self):
        print("Main menu of shop simulation")
        print("1. Print simulation settings")
        print("2. Set simulation settings")
        print("3. Print chart from the simulation")
        print("4. Print results")
        print("5. Save to file")
        print("6. Run simulation")
        print("7. Exit application")
        print("Enter number related to the option")

    # Method controles and validates the input from the user
    def inputController(self, lowerLimit, higherLimit):
        isInputCorrect = False  
        tmp = 0
        while not isInputCorrect:
            tmp = self.inputFromUser()
            isInputCorrect = self.handleUserInput(tmp, lowerLimit, higherLimit)  
        return int(tmp) 
                 

    # Method takes input from the user and tries to convert it to number. In case of exception method returns 0
    def inputFromUser(self):
        tmp = input("> ")
        try:
            number = int(tmp)
            return  number
        except(ValueError, TypeError):
            print("Option must be a number")
            return 0

    # Checks if the input of user which is an argument is correct value from the range of numbers
    def handleUserInput(self, input, lowerLimit, higherLimit):
        if lowerLimit > int(input) or higherLimit < int(input):
            return False
        else:
           return True

    # Controler of main menu, who based on the option invokes next operations
    def mainMenuControler(self):
        if menuConsts.printSimulationSettings == self.getOption():
            self.printSimulationSettings()
        elif menuConsts.setSimulationSettings == self.getOption():
            self.printChart()
        elif menuConsts.printResults == self.getOption():
            self.printResults()
        elif menuConsts.saveToFile == self.getOption():
            self.saveToFile()
        elif menuConsts.runSim == self.getOption():
            self.startSimulation()
        elif menuConsts.exitApp == self.getOption():
            self.exitApp()


    def printSimulationSettings(self):
        self.settings.printAllSettings()
    def simulationSettings(self):
        self.settings.settingMenuRunner(2)
    def printChart(self):
        # Utwórz nową figurę o numerze 0 i rozdzielczości 120 dpi
        plt.figure(0,dpi=120)
        plt.plot(self.days,self.profit,'o',label="Profit")
        plt.plot(self.days,self.loss,'o',label="Loss")
        plt.legend()
        # Pojawia się okienko z wykresem
        plt.show()
        return
    def printResults(self):
        if self.profit_calculator:
            daily_profit = self.profit_calculator.daily_profit 
            potential_profit_lost = self.profit_calculator.get_potential_profit_lost()
            print(f"Daily profit: {daily_profit}")
            print(f"Potential profit lost: {potential_profit_lost}")
        else:
            print("No results available. Please run the simulation first.")
    #
    def saveToFile(self):
        print("Save file")
        return 
    # Funkcja zaczyna symulacje
    def startSimulation(self):
        self.simmulationRunner()
        return
    def exitApp(self):
        self.shouldExit = True
        return 

    # Method takes input from the user and tries to convert it to number. In case of exception method returns 0
    def readInput(self):
        tmp = input("> ")
        try:
            number = int(tmp)
            return  number
        except(ValueError, TypeError):
            print("Option must be a number")
            return 0

    # Functions clears terminal after any key was pressed
    def clearTerminal(self):
        input("Press any key...")
        # 'clear' jest niedostępne dla Windowsa jeżeli nie wykonuje się poprawnie wykonaj 'cls' odpowiednik w Windowsie
        status = os.system('clear')
        if status != 0:
            os.system('cls')

    # Checks if the input of user which is an argument is correct value from the range of numbers
    def handleInput(self, input, lowerLimit, higherLimit):
        if lowerLimit > int(input) or higherLimit < int(input):
            return False
        else:
            return True


# GETTERS AND SETTERS
    def getOption(self):
        return self.option
    def setOption(self, option):
        self.option = option
 
        
