from .ElementsConst import ElementsConst as  CONST
import random
class Client: 

    # Consturcotr of client class
    def __init__(self):
        self.__shopingTime = CONST.DEF_SHOPING_TIME
        self.__averageCartCost = CONST.DEF_AVG_CART_COST
        self.__actual_cart_cost = random.normalvariate(self.__averageCartCost,10) # Na podstawie średniej wartości wyznacza losową liczbę, 10 to odchylenie std
        self.__shopingTimeAbounde = CONST.DEF_SHOPING_TIME_ABOUNDE
        self.__satisfactionLevel = random.randint(5,20) 
        self.__time_waited = 0


    # Function prints the option for client class
    def printOptions(self):
        print("Choose client variable to print/set")
        for i in range(len(CONST.CLINET_OPTIONS)): 
            print(i+1, CONST.CLINET_OPTIONS[i])
        print("Enter relevant number: ")
    

    # Function prints specified settings of a client based on the user input
    def printControler(self, usrInput):
        if (usrInput == CONST.SHOPING_TIME):
            print("Current shoping time: ",self.getShopingTime()) 
        elif (usrInput == CONST.CART_VALUE):
            print("Current average cart value: ", self.getAverageCartCost())
        elif (usrInput == CONST.ABOUNDE_TIME):
            print("Current time after which clients will leave the shop: ", self.getShopingTimeAbounde())
        elif (usrInput == CONST.SATISFACTION_LEVEL):
            print("Current basic satisfaction level: ", self.getSatisfactionLevel())
        elif (usrInput == CONST.ALL_CLIENT):
                self.printCustomerSettings()


    # Function sets settings of a client based on the user input
    def setController(self, usrInput):
        if (usrInput == CONST.SHOPING_TIME):
            print("Enter shoping time: ")
            self.setShopingTime(self.readInput())
        elif (usrInput == CONST.CART_VALUE):
            print("Enter average cost of shpoing: ")
            self.setAverageCartCost(self.readInput())
        elif (usrInput == CONST.ABOUNDE_TIME):
            print("Enter time after which the client wil leave the shop: ")
            self.setShopingTimeAbounde(self.readInput())
        elif (usrInput == CONST.SATISFACTION_LEVEL):
            print("Enter satisfaction level of clients: ")
            self.setSatisfactionLevel(self.readInput())
        elif (usrInput == CONST.ALL_CLIENT):
            self.setSettings()


    # Function prints current settings for client
    def printCustomerSettings(self):
        print("Shoping time: ", self.getShopingTime())
        print("Average cost of shoping cart: ", self.getAverageCartCost())
        print("Shoping time abounde: ", self.getShopingTimeAbounde())
        print("Basic satisfaction level: ", self.getSatisfactionLevel())


    # Function sets all of the client fileds by user
    def setSettings(self):
        print("WARTNING! In case of incorrect input data value of field will remain as deafult")
        print("Enter shoping time: ")
        self.setShopingTime(self.readInput())
        print("Enter average cost of shoping cart: ")
        self.setAverageCartCost(self.readInput())
        print("Enter time after clinet will aboundon shop: ")
        self.setShopingTimeAbounde(self.readInput())
        print("Enter the starting satisfaction level of clients: ")
        self.setSatisfactionLevel(self.readInput())


    # Function reads input of a usre. Input should be provided as a number. In other case function will return 0
    def readInput(self):
        tmp = input("> ")
        try:
            number = int(tmp)
            return  number
        except(ValueError, TypeError):
            return 0


    # Function increase time waited by the customer
    def increase_time_waited(self,time_amount):
        self.__time_waited += time_amount


    # Function decrease satisfaction level of a customer    
    def decrease_satisfaction_level(self):
        self.__satisfactionLevel -= 1
    
    # GETTERS
    def getShopingTime(self):
        return self.__shopingTime
    def getAverageCartCost(self):
        return self.__averageCartCost
    def getShopingTimeAbounde(self):
        return self.__shopingTimeAbounde
    def getSatisfactionLevel(self):
        return self.__satisfactionLevel
    def get_spent_money(self):
        return self.__actual_cart_cost
    def time_in_queue(self):
        return self.__time_waited

    # SETTERS
    def setShopingTime(self, shopingTime):
        if ( shopingTime > 0):
            self.__shopingTime = shopingTime
    def setAverageCartCost(self, avgCartCost) :
        if ( avgCartCost > 0):
            self.__averageCartCost= avgCartCost 
    def setShopingTimeAbounde(self, abounde):
        if ( abounde > 0):
            self.__shopingTimeAbounde = abounde 
    def setSatisfactionLevel(self, satisfactionLevel):
        if (satisfactionLevel >= 0 and satisfactionLevel <= 20):
            self.__satisfactionLevel = satisfactionLevel


