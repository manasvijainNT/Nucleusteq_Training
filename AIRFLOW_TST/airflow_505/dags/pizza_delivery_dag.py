from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

from airflow.utils.trigger_rule import TriggerRule

def receive_order(**context):

    ti = context["ti"]

    order_id = "PIZZA_101"
    toppings = ["cheese", "onion", "capsicum"]

    ti.xcom_push(
        key="order_id",
        value=order_id
    )

    ti.xcom_push(
        key="toppings",
        value=toppings
    )

    ti.log.info("New pizza order received")
    ti.log.info(f"Order ID: {order_id}")
    ti.log.info(f"Toppings: {toppings}")

def check_stock(**context):

    ti = context["ti"]

    order_id = ti.xcom_pull(
        task_ids="receive_order",
        key="order_id"
    )

    toppings = ti.xcom_pull(
        task_ids="receive_order",
        key="toppings"
    )

    ti.log.info(f"Checking stock for toppings: {order_id}")
    ti.log.info(f"Checking stock for toppings: {toppings}")

    available_toppings = [
        "capsicum",
        "onion",
        "oregano",
        "cheese",
        "mushroom",
    ]

    unavailable_toppings = [
        topping for topping in toppings
        if topping not in available_toppings
    ]

    if unavailable_toppings :
        ti.log.warning("Unavailable toppings for %s : %s", order_id, unavailable_toppings)
        return "skip_preparation"

    ti.log.info("All toppings are available for order %s", order_id)
    return "prepare_pizza"


def skip_preparation(**context):
    ti = context["ti"]
    order_id = ti.xcom_pull(
        task_ids="receive_order",
        key="order_id"
    )

    toppings = ti.xcom_pull(
        task_ids="receive_order",
        key="toppings"
    )

    ti.log.info(f"Checking stock for toppings: {order_id}")
    ti.log.info(f"Checking stock for toppings: {toppings}")


def prepare_pizza(**context):

    ti = context["ti"]

    order_id = ti.xcom_pull(
        task_ids="receive_order",
        key="order_id"
    )

    toppings = ti.xcom_pull(
        task_ids="receive_order",
        key="toppings"
    )

    ti.log.info(f"Preparing pizza for {order_id}")
    ti.log.info(f"Adding toppings: {toppings}")
    ti.log.info("Pizza preparation completed")

def quality_check(**context):
    ti = context["ti"]

    order_id = ti.xcom_pull(
        task_ids="receive_order",
        key="order_id"
    )
    ti.log.info(f"Quality check started for {order_id}")
    ti.log.info("Pizza passed quality check")

def pack_order(**context):

    ti = context["ti"]

    order_id = ti.xcom_pull(
        task_ids="receive_order",
        key="order_id"
    )
    ti.log.info(f"Packing order {order_id}")
    ti.log.info("Pizza packed successfully")


def dispatch_order(**context):
    ti = context["ti"]
    order_id = ti.xcom_pull(
        task_ids="receive_order",
        key="order_id"
    )
    ti.log.info(f"Dispatching order {order_id}")
    ti.log.info("Order dispatched successfully")


default_args = {
    "owner": "Manasvi",
    "retries": 0
}

with DAG(

    dag_id="pizza_delivery_pipeline",
    default_args=default_args,
    description="Pizza delivery pipeline",
    start_date=datetime(2026, 8, 18),
    schedule="0 12,19 * * *",
    catchup=False
) as dag:


    receive_order_task = PythonOperator(
        task_id="receive_order",
        python_callable=receive_order
    )

    check_stock_task = BranchPythonOperator(
        task_id="check_stock",
        python_callable=check_stock
    )

    skip_preparation_task = PythonOperator(
        task_id="skip_preparation",
        python_callable=skip_preparation
    )

    prepare_pizza_task = PythonOperator(
        task_id="prepare_pizza",
        python_callable=prepare_pizza
    )

    bake_pizza_task = BashOperator(

        task_id="bake_pizza",
        bash_command=(
            "echo 'Oven is preheating'; "
            "echo 'Pizza is baking'; "
            "echo 'Pizza baking completed'"
        )

    )

    quality_check_task = PythonOperator(
        task_id="quality_check",
        python_callable=quality_check
    )

    pack_order_task = PythonOperator(
        task_id="pack_order",
        python_callable=pack_order,
        trigger_rule=(
            TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
        )

    )

    dispatch_order_task = PythonOperator(
        task_id="dispatch_order",
        python_callable=dispatch_order,
        trigger_rule=(
            TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
        )

    )

    receive_order_task >> check_stock_task
    check_stock_task >> [skip_preparation_task , prepare_pizza_task]
    prepare_pizza_task >> bake_pizza_task
    bake_pizza_task >> quality_check_task
    quality_check_task >> pack_order_task
    pack_order_task >> dispatch_order_task