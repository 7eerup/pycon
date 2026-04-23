import json
import time

EPSILON = 1e-9

# =========================
# 유틸 함수
# =========================

def normalize_label(label: str) -> str:
    label = label.strip().lower()
    if label in ['+', 'cross']:
        return 'Cross'
    elif label in ['x']:
        return 'X'
    return 'UNKNOWN'


# =========================
# 입력 처리
# =========================

def read_matrix(n: int):
    matrix = []

    for _ in range(n):
        while True:
            row = input().strip().split()

            if len(row) != n:
                print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                continue

            try:
                row = [float(x) for x in row]
                matrix.append(row)
                break
            except ValueError:
                print("숫자만 입력해야 합니다.")

    return matrix


# =========================
# MAC 연산
# =========================

def mac_operation(pattern, filt):
    n = len(pattern)
    result = 0.0

    for i in range(n):
        for j in range(n):
            result += pattern[i][j] * filt[i][j]

    return result


# =========================
# 점수 비교
# =========================

def compare_scores(score_cross, score_x):
    if abs(score_cross - score_x) < EPSILON:
        return "UNDECIDED"
    return "Cross" if score_cross > score_x else "X"


# =========================
# 성능 측정
# =========================

def benchmark(pattern, filt, repeat=10):
    start = time.perf_counter()

    for _ in range(repeat):
        mac_operation(pattern, filt)

    end = time.perf_counter()

    avg_time = (end - start) / repeat * 1000
    return avg_time


# =========================
# 모드 1
# =========================

def run_mode_1():
    print("\n#----------------------------------------")
    print("# [1] 필터 입력")
    print("#----------------------------------------")

    print("필터 A (3줄 입력)")
    filter_a = read_matrix(3)

    print("\n필터 B (3줄 입력)")
    filter_b = read_matrix(3)

    print("\n#----------------------------------------")
    print("# [2] 패턴 입력")
    print("#----------------------------------------")

    print("패턴 (3줄 입력)")
    pattern = read_matrix(3)

    print("\n#----------------------------------------")
    print("# [3] MAC 결과")
    print("#----------------------------------------")

    score_a = mac_operation(pattern, filter_a)
    score_b = mac_operation(pattern, filter_b)

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")

    avg_time = benchmark(pattern, filter_a)
    print(f"연산 시간(평균/10회): {avg_time:.6f} ms")

    result = compare_scores(score_a, score_b)

    if result == "UNDECIDED":
        print("판정: 판정 불가 (|A-B| < 1e-9)")
    else:
        print(f"판정: {result}")


# =========================
# JSON 로드
# =========================

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


# =========================
# 필터 로드
# =========================

def load_filters(data):
    filters = {}

    print("\n#----------------------------------------")
    print("# [1] 필터 로드")
    print("#----------------------------------------")

    for key, value in data["filters"].items():
        size = int(key.split("_")[1])

        filters[size] = {
            "Cross": value.get("cross"),
            "X": value.get("x")
        }

        print(f"✓ size_{size} 필터 로드 완료 (Cross, X)")

    return filters


# =========================
# 패턴 분석
# =========================

def analyze_patterns(data, filters):
    results = []

    print("\n#----------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#----------------------------------------")

    for key, value in data["patterns"].items():
        print(f"\n--- {key} ---")

        size = int(key.split("_")[1])
        pattern = value["input"]
        expected = normalize_label(value["expected"])

        # 크기 검증
        valid = True
        if size not in filters:
            valid = False

        if valid:
            if len(pattern) != size or any(len(row) != size for row in pattern):
                valid = False

        if not valid:
            print("FAIL: 크기 불일치")
            results.append({
                "id": key,
                "result": "FAIL",
                "reason": "크기 불일치"
            })
            continue

        cross_filter = filters[size]["Cross"]
        x_filter = filters[size]["X"]

        score_cross = mac_operation(pattern, cross_filter)
        score_x = mac_operation(pattern, x_filter)

        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")

        predicted = compare_scores(score_cross, score_x)

        if predicted == "UNDECIDED":
            result = "FAIL"
            reason = "동점 처리"
        elif predicted == expected:
            result = "PASS"
            reason = ""
        else:
            result = "FAIL"
            reason = "예측 불일치"

        print(f"판정: {predicted} | expected: {expected} | {result}")

        results.append({
            "id": key,
            "result": result,
            "reason": reason
        })

    return results


# =========================
# 성능 분석
# =========================

def performance_analysis(filters):
    print("\n#----------------------------------------")
    print("# [3] 성능 분석 (평균/10회)")
    print("#----------------------------------------")

    print("크기       평균 시간(ms)    연산 횟수")
    print("-------------------------------------")

    sizes = [3, 5, 13, 25]

    for size in sizes:
        # 더미 데이터 생성
        pattern = [[1.0]*size for _ in range(size)]
        filt = [[1.0]*size for _ in range(size)]

        avg_time = benchmark(pattern, filt)

        print(f"{size}×{size:<5} {avg_time:<15.6f} {size*size}")


# =========================
# 결과 요약
# =========================

def summarize(results):
    print("\n#----------------------------------------")
    print("# [4] 결과 요약")
    print("#----------------------------------------")

    total = len(results)
    passed = sum(1 for r in results if r["result"] == "PASS")
    failed = total - passed

    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")

    if failed > 0:
        print("\n실패 케이스:")
        for r in results:
            if r["result"] == "FAIL":
                print(f"- {r['id']}: {r['reason']}")


# =========================
# 모드 2
# =========================

def run_mode_2():
    data = load_json("data.json")

    filters = load_filters(data)
    results = analyze_patterns(data, filters)
    performance_analysis(filters)
    summarize(results)


# =========================
# 메인
# =========================

def main():
    print("=== Mini NPU Simulator ===\n")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    choice = input("선택: ").strip()

    if choice == '1':
        run_mode_1()
    elif choice == '2':
        run_mode_2()
    else:
        print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()