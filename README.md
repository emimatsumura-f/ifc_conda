# IFC Converter

IFCファイルから部材情報を抽出し、CSVファイルとして出力できるWebアプリケーションです。

## 機能

- ユーザー認証（登録・ログイン）
- IFCファイルのアップロード（最大100MB）
- 部材情報の抽出と表示
  - 部材種別
  - 部材名
  - 断面性能
  - 重量
  - 長さ
- 変換履歴の管理
- CSVファイルのダウンロード

## 技術スタック

- **バックエンド**: Python (Flask)
- **フロントエンド**: HTML, CSS (Bootstrap), JavaScript
- **データベース**: SQLite
- **IFC処理**: IfcOpenShell
- **その他**:
  - Flask-Login（認証管理）
  - Flask-WTF（フォーム処理・CSRF保護）

## 環境構築

1. Conda環境の作成と依存パッケージのインストール:
```bash
conda env create -f environment.yml
conda activate ifc_env
```

2. アプリケーションの起動:
```bash
flask run
```

デフォルトでは http://localhost:5000 でアプリケーションが起動します。

## セキュリティ機能

- CSRF保護
- セキュアなセッション管理
- パスワードハッシュ化
- ファイルアップロードの制限
- 認証済みユーザーのみアクセス可能

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。