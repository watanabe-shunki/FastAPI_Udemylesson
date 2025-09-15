from sqlalchemy import create_engine # データベースとPythonを繋ぐ接続オブジェクト
from sqlalchemy.ext.declarative import declarative_base # declarative_baseを継承してモデルクラス（テーブル定義）を作成
from sqlalchemy.orm import sessionmaker # セッション：データベースへの操作（読み書き）を行うためのオブジェクト

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" # 接続するデータベースのURLを定義

engine= create_engine( # データベースエンジンを作成
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # connect_args={"check_same_thread"：複数スレッドからアクセスを許可するために必要
)

# データベース操作用のセッションを作成するためのクラスを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORMモデルの親クラスを作成
Base = declarative_base()