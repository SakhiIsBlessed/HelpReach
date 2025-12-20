import os
from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, NGO, Donation
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = config.SECRET_KEY

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.form or request.json or {}
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        if not name or not email or not password:
            return jsonify({'error':'Missing fields'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error':'Email exists'}), 409
        user = User(name=name, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return jsonify({'ok':True,'user_id':user.id})

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.form or request.json or {}
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error':'Missing'}), 400
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error':'Invalid'}), 401
        session['user_id'] = user.id
        return jsonify({'ok':True,'user_id':user.id})

    @app.route('/api/logout', methods=['POST','GET'])
    def logout():
        session.pop('user_id', None)
        return jsonify({'ok':True})

    @app.route('/api/donations', methods=['GET','POST'])
    def donations():
        if request.method == 'GET':
            items = Donation.query.order_by(Donation.created_at.desc()).limit(200).all()
            out = []
            for d in items:
                out.append({
                    'id': d.id,
                    'title': d.title,
                    'description': d.description,
                    'quantity': d.quantity,
                    'images': d.images,
                    'donor_id': d.donor_id,
                    'status': d.status,
                    'pickup_info': d.pickup_info,
                    'created_at': d.created_at.isoformat()
                })
            return jsonify({'ok':True,'donations':out})

        # POST
        if 'user_id' not in session:
            return jsonify({'error':'Unauthorized'}), 401
        title = request.form.get('title') or request.json.get('title')
        description = request.form.get('description') or request.json.get('description')
        quantity = request.form.get('quantity') or request.json.get('quantity')
        pickup = request.form.get('pickup_info') or request.json.get('pickup_info')

        images_list = []
        # handle file uploads
        if 'photos' in request.files:
            files = request.files.getlist('photos')
            for f in files:
                if f and f.filename:
                    filename = secure_filename(f.filename)
                    dest = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    f.save(dest)
                    images_list.append(filename)

        images_csv = ','.join(images_list) if images_list else None
        donation = Donation(title=title, description=description, quantity=quantity, pickup_info=pickup, images=images_csv, donor_id=session['user_id'])
        db.session.add(donation)
        db.session.commit()
        return jsonify({'ok':True,'donation_id':donation.id})

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
