import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 데이터 로드
def load_data(csv_file):
    """
    CSV 파일에서 데이터를 로드합니다.
    """
    df = pd.read_csv(csv_file)

    # 필요한 열만 추출
    df = df[["home_team", "away_team", "home_score", "away_score", "winner"]]

    # 타겟 변수 생성 (0: 홈 승, 1: 무승부, 2: 원정 승)
    df["target"] = df.apply(
        lambda row: 0 if row["winner"] == row["home_team"] else (2 if row["winner"] == row["away_team"] else 1),
        axis=1
    )


    return df

# 데이터 전처리
def preprocess_data(df):
    """
    데이터를 학습에 적합한 형태로 전처리합니다.
    """
    # 입력 변수 (Features) 및 타겟 변수 (Target) 분리
    X = df[["home_score", "away_score"]]
    y = df["target"]

    # 학습 데이터와 테스트 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# 모델 학습
def train_model(X_train, y_train):
    """
    Random Forest 모델을 학습합니다.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

# 모델 평가
def evaluate_model(model, X_test, y_test):
    """
    학습된 모델을 평가합니다.
    """
    y_pred = model.predict(X_test)
    print("모델 정확도:", accuracy_score(y_test, y_pred))
    print("분류 리포트:")
    print(classification_report(y_test, y_pred))

# 모델 저장
def save_model(model, output_file):
    """
    학습된 모델을 파일로 저장합니다.
    """
    joblib.dump(model, output_file)
    print(f"모델이 {output_file}에 저장되었습니다.")

# 실행
if __name__ == "__main__":
    # 데이터 로드
    csv_file = "match_data.csv"
    df = load_data(csv_file)

    # 데이터 전처리
    X_train, X_test, y_train, y_test = preprocess_data(df)

    # 모델 학습
    model = train_model(X_train, y_train)

    # 모델 평가
    evaluate_model(model, X_test, y_test)

    # 모델 저장
    save_model(model, "match_predictor.pkl")
