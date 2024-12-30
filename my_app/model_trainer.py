import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 데이터 로드
def load_data():
    """
    CSV 파일에서 데이터를 로드합니다.
    """
    # 절대 경로 사용
    base_dir = os.path.dirname(__file__)  # 현재 파일(model_trainer.py)의 디렉터리
    csv_file = os.path.join(base_dir, 'match_data.csv')  # match_data.csv 경로 설정
    
    # 파일 존재 여부 확인
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"{csv_file} 파일이 존재하지 않습니다.")
    
    df = pd.read_csv(csv_file)
    df = df[["home_team", "away_team", "home_score", "away_score", "winner"]]

    # 타겟 변수 생성
    df["target"] = df.apply(
        lambda row: 0 if row["winner"] == row["home_team"] else (2 if row["winner"] == row["away_team"] else 1),
        axis=1
    )
    return df

# 데이터 전처리
def preprocess_data(df):
    X = df[["home_score", "away_score"]].to_numpy()  # Numpy 배열로 변환해 피처 이름 제거
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# 모델 학습
def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

# 모델 평가
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print("모델 정확도:", accuracy_score(y_test, y_pred))
    print("분류 리포트:")
    print(classification_report(y_test, y_pred))

# 모델 저장
def save_model(model):
    base_dir = os.path.dirname(__file__)
    output_file = os.path.join(base_dir, 'match_predictor.pkl')
    joblib.dump(model, output_file)
    print(f"모델이 {output_file}에 저장되었습니다.")

# 실행
if __name__ == "__main__":
    df = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(df)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    save_model(model)