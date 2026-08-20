# Pizza Delivery Pipeline — Apache Airflow

### 1. Overview
 - This project implements a pizza delivery workflow using Apache Airflow.
 - The DAG contains 8 tasks and uses PythonOperator, BashOperator, XCom, logging, and a cron-based schedule.
---

### 2. Folder Structure
```text
AIRFLOW_TST/
│
├── airflow_505/
|    |
|    ├── dags/
│    |     └── pizza_delivery_dag.py
|    ├── logs
|    ├── plugins
|    ├── airflow.cfg 
|    └── webserver_config.py
|
├── docker-compose.yaml
│
├── screenshots/
|    ├── Flow1.png
|    ├── Flow2.png
|    ├── Swagger1.png
|    ├── Swagger2.png
|    └── Xcom.png
|
├── README.md
```
---

### 3. Task Flow
```
receive_order
      ↓
check_stock
      ↓
skip_preparation
      ↓
prepare_pizza
      ↓
bake_pizza
      ↓
quality_check
      ↓
pack_order
      ↓
dispatch_order
```

- receive_order – Receives the order and stores order details in XCom.
- check_stock – Checks whether the required toppings are available.
- skip_preparation – Checks the ingredient availability and skips preparation if an ingredient is unavailable.
- prepare_pizza – Prepares the pizza.
- bake_pizza – Simulates baking using BashOperator.
- quality_check – Performs the pizza quality check.
- pack_order – Packs the pizza.
- dispatch_order – Dispatches the order for delivery.
---

### 4. XCom
XCom is used to pass data between tasks.
The receive_order task passes:
```
• order_id.
• toppings.
```
The check_stock task also passes ingredients_available to skip_preparation.
![image](screenshots/Xcom.png)
---

### 5. Skip Condition
Ingredient availability is stored using True and False values:
```
available_items = {
    "cheese": True,
    "onion": True,
    "capsicum": False
}
```
 - If a required ingredient is unavailable, ingredients_available becomes False.
 - The ShortCircuitOperator then returns False, causing the pizza preparation task to be skipped.
---

### 6. Schedule
- The DAG uses: 0 12,19 * * *
- It runs at 12:00 PM and 7:00 PM, representing the lunch and dinner rush.
---

### 7. Logging
Airflow’s task logger is used to record important events such as:

- Order details.
- Ingredient availability.
- Pizza preparation.
- Baking.
- Quality check.
- Packing and dispatch.
- Reason for skipping a task.
---
### 8. DAG Graph Screenshot
![image](screenshots/Flow1.png)
![image](screenshots/Flow2.png)
---

### 9. Airflow API Trigger Screenshot

The DAG was triggered using the Airflow REST API through Swagger.

![image](screenshots/Swagger1.png)
![image](screenshots/Swagger2.png)

---

### 10. Conclusion

The pipeline automates the pizza order-to-delivery process and demonstrates task dependencies, XCom communication, Bash and Python operators, logging, and conditional task skipping in Apache Airflow.

---
## Author 

## Manasvi Jain
