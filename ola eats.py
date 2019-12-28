import mysql.connector
import datetime


class olaeats:
            def __init__(self):
                self.conn=mysql.connector.connect(host="127.0.0.1",user="root",password="",database="zomato")
                self.mycursor=self.conn.cursor()
                self.program_menu()

            def program_menu(self):
                program_input=input(""" WELCOME TO OLA-EATS
                1.Enter 1 to login for registered users
                2.Enter 2 to register for new users
                3.Enter anything to exit \n""")
                if program_input=="1":
                    self.login()
                elif program_input=="2":
                    self.register()
                else:
                    print("Thanks for coming here visit again .......")

            def register(self):
                print("Welcome")
                print("Register to use the service")
                name=input("Enter name :")
                email=input("Enter email :")
                phone_num=int(input("Enter phone number :"))
                area=input("Enter your location manually :")


                self.mycursor.execute("""INSERT INTO `users` (`name`, `email`,`phone_num`,`area`)
                 VALUES ('{}', '{}','{}','{}') """.format(name,email,phone_num,area))

                self.conn.commit()
                print("Registered successfully")
                self.program_menu()

            def login(self):
                email=input("Enter the email : ")
                phone_num=input("Enter the phone number : ")
                self.mycursor.execute("""SELECT * FROM `users` WHERE `email`
                    LIKE '{}' AND `phone_num` LIKE '{}'""".format(email,phone_num))
                user_list=self.mycursor.fetchall()


                # print(user_list)
                if len(user_list) > 0:
                    print("LOGIN SUCCESSFULL")
                    self.current_user_id = user_list[0][0]
                    self.user_menu()
                else:
                    print("Incorrect")
                    self.program_menu()

            def user_menu(self):
                
                self.mycursor.execute("""SELECT * FROM `feedback` """.format(self.current_user_id))
                feedback=self.mycursor.fetchall()
                rating=0
                count=0
                for i in feedback:
                    rating=rating+i[2]
                    count=count+1
                rate=rating/count
                    
                print("Ola-eats is rated ",rate,"/5  by the users")        
                user_input = input("""How would you like to proceed
                                    1.Enter 1 to select your restaurant and order food
                                    2.Anything else to logout \n """)


                if user_input=="1":
                    self.viewall_restaurant()
                else:
                    self.logout()

            def viewall_restaurant(self):
                self.mycursor.execute("""SELECT * FROM `restaurant` """.format(self.current_user_id))
                all_users=self.mycursor.fetchall()
                for i in all_users:
                    print("-->",i[1],"|","Rating=",i[2],"|","Area=",i[3])
                    print("----------------------------------------")
                self.restaurant_id=int(input("Enter the restaurant you want to choose to see for the food menu : "))
                
                
                    
                print("\nFood Menu: ")
                self.mycursor.execute("""SELECT * FROM `food` """.format(self.current_user_id))
                food_ordered = self.mycursor.fetchall()
                for i in food_ordered:
                    print(i)
                    print("----------------------------------------")
                self.food_id=int(input("Enter the food item you want to choose : "))
                self.quantity=int(input("Enter how much quantity do you want : "))
                if self.quantity>20:
                    print("Sorry that much quantity not available")
                for i in food_ordered:
                    if(self.food_id==i[0]):
                        print(i[1],"|",i[2])
                        print("----------------------------------------")


                user_input_1= input("""Hi how would you like to proceed
                                    1.Enter 1 to Order the food
                                    2.Anything else to logout\n""")


                if user_input_1=="1":
                    self.order_food()
                else:
                    self.logout()

            def order_food(self):
                print("---------------------INVOICE RECEIPT---------------------")
                print("Restaurant")

                self.mycursor.execute("""SELECT * FROM `restaurant` """.format(self.current_user_id))
                all_users=self.mycursor.fetchall()

                for i in all_users:
                    if(self.restaurant_id==i[0]):
                        print(i[1],"|","Rating=",i[2],"|","Area=",i[3],"\n")

                self.mycursor.execute("""INSERT INTO `order_history` (`food_id`,`restaurant_id`,`user_id`)
                VALUES ('{}','{}','{}') """.format(self.food_id,self.restaurant_id,self.current_user_id))
                self.conn.commit()

                datetime.datetime.now()
                                   
                print(" Order ID Food item        Price      Quantity          Amount\n")
                
                self.mycursor.execute("""SELECT * FROM `food` """.format(self.current_user_id))
                food_ordered = self.mycursor.fetchall()
                for i in food_ordered:
                    if(self.food_id==i[0]):
                        price=i[2]
                        print(i[0],"\t",i[1],"\t",i[2],"\t    ",self.quantity,"\t   ",price*self.quantity)
                        print("----------------------------------------")
                        print("THE PAYMENT MUST BE MADE AT THE TIME OF THE DELIVERY ")
                        print("Thanks for choosing us ")
                self.rating=float(input("Please rate our service out of 5 : "))
                self.mycursor.execute("""INSERT INTO `feedback` (`user_id`,`rating`)
                VALUES ('{}','{}') """.format(self.current_user_id,self.rating))
                self.conn.commit()
                
                self.user_menu()
                
                
                
           


            def logout(self):
                self.current_user_id=0
                print("LOGOUT SUCESSFULLY \n")
                

obj1=olaeats()
