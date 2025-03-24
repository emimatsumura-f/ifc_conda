import os
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'ifc_app.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads'),
        MAX_CONTENT_LENGTH=100 * 1024 * 1024,  # 最大100MB
        # タイムアウトとバッファサイズの設定を追加
        PERMANENT_SESSION_LIFETIME=1800,  # 30分
        MAX_BUFFER_SIZE=100 * 1024 * 1024  # アップロード用バッファサイズ
    )

    # CSRFプロテクションを初期化
    csrf = CSRFProtect()
    csrf.init_app(app)

    # セッションの設定
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30分

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(test_config)

    # インスタンスフォルダとアップロードディレクトリの作成
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError as e:
        print(f"Error creating directories: {str(e)}")

    # データベース初期化
    from ifc_app import db
    db.init_app(app)
    
    # ログイン管理の設定
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'このページにアクセスするにはログインが必要です。'
    login_manager.init_app(app)

    from ifc_app.models import User
    @login_manager.user_loader
    def load_user(id):
        return User.get(id)
    
    # Blueprintの登録
    from ifc_app import auth
    app.register_blueprint(auth.bp)
    
    from ifc_app import views
    app.register_blueprint(views.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app

# アプリケーションインスタンスの作成
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)