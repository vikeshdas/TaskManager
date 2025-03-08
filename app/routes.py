from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import Task

api_bp = Blueprint('api', __name__)


@api_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400

        new_task = Task(
            title=data.get('title'),
            description=data.get('description', ''), 
            completed=False,
            user_id=user_id
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            'message': 'Task created successfully',
            'task': {
                'id': new_task.id,
                'title': new_task.title,
                'description': new_task.description,
                'completed': new_task.completed,
                'user_id': new_task.user_id
            }
        }), 201

    except Exception as e:
        db.session.rollback()

        print(f"Error creating task: {e}")

        return jsonify({'error': 'An error occurred while creating the task'}), 500



from flask import url_for

@api_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        tasks = Task.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'tasks': [{'id': task.id, 'title': task.title, 'completed': task.completed} for task in tasks.items],
            'total': tasks.total,
            'pages': tasks.pages,
            'current_page': tasks.page,
            'next_page': url_for('api.get_tasks', page=tasks.next_num, per_page=per_page, _external=True) if tasks.has_next else None,
            'prev_page': url_for('api.get_tasks', page=tasks.prev_num, per_page=per_page, _external=True) if tasks.has_prev else None
        })

    except SQLAlchemyError:
        return jsonify({'error': 'Database error occurred'}), 500

    except Exception:
        return jsonify({'error': 'An unexpected error occurred'}), 500


@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    try:
        user_id=get_jwt_identity()
       
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        if task.user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed,'user':task.user_id})

    except Exception as e:
        return jsonify({'error': 'An error occurred while retrieving the task'}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    try:
        task = Task.query.get(task_id)
        user_id=get_jwt_identity()

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        if task.user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON request'}), 400

        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)

        db.session.commit()
        return jsonify({'message': 'Task updated successfully'})

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        user_id=get_jwt_identity()

        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        if task.user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500
