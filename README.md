# Calculator_OSAGO
The program performs calculations based on data about the driver and the vehicle, such as the driver’s experience, the driver’s age, the bonus-malus coefficient (KBM), engine power, vehicle type, seasonal use of the vehicle, registration of the vehicle in another country, and so on. These parameters determine the values of the following coefficients:
1. Driver’s experience coefficient (KE),
2. Driver’s age coefficient (KA),
3. Bonus-malus coefficient (KBM),
4. Engine power coefficient (KP),
5. Vehicle type coefficient (KT),
6. Seasonal use coefficient (KSE),
7. Registration in another country coefficient (KRC).

**Functional Description**

The calculator accepts data about the driver and the vehicle, retrieves the necessary coefficients from the database, and applies them to the base cost of the policy to calculate the final amount.

**How It Works**

1. The program asks for data about the driver and the vehicle.
2. For each parameter (experience, age, power, and others), it finds the corresponding coefficients in the database.
3. Then, the calculator uses these coefficients to calculate the OSAGO cost and outputs the final amount for the user.

**Input Structure**

To correctly calculate the policy, the program requires the following data:
1. Driver’s experience (in years)
2. Driver’s age (in years)
3. Bonus-malus coefficient (KBM)
4. Engine power (in horsepower)
5. Vehicle type (e.g., passenger car, truck, etc.)
6. Seasonal use of the vehicle (yes/no)
7. Registration of the vehicle in another country (yes/no)

**Technical Requirements**

To run the calculator, the following is required:
1. Python 3.x
2. Installed libraries: sqlalchemy, pandas, IPython, functools, operator, time
3. Database with the following tables: AlBabkinaKvs, AlBabkinaKbm, AlBabkinaKm, AlBabkinaKs, AlBabkinaKp, AlBabkinaKt
