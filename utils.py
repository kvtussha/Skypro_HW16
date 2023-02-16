import json


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def to_dict(class_name):
    if class_name.__tablename__ == 'user':
        return {
            "id": class_name.id,
            "first_name": class_name.first_name,
            "last_name": class_name.last_name,
            "age": class_name.age,
            "email": class_name.email,
            "role": class_name.role,
            "phone": class_name.phone
            }
    elif class_name.__tablename__ == 'order':
        return {
            "id": class_name.id,
            "name": class_name.name,
            "description": class_name.description,
            "start_date": class_name.start_date,
            "end_date": class_name.end_date,
            "address": class_name.address,
            "price": class_name.price,
            "customer_id": class_name.customer_id,
            "executor_id": class_name.executor_id
            }
    return {
        "id": class_name.id,
        "order_id": class_name.order_id,
        "executor_id": class_name.executor_id
    }
