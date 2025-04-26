import elo as e
def test_elo():
    corr = 0
    exp_corr = 0
    inc = 0
    exp_inc = 0
    for i in range(2000, 2026):
        tcorr, texp_corr, tinc, texp_inc = e.main(print_rankings=False, year=i)
        corr += tcorr
        exp_corr += texp_corr
        inc += tinc
        exp_inc += texp_inc
    total = corr + inc
    if total > 0:
        acc = (corr / total) * 100
        exp_acc = (exp_corr / (exp_corr + exp_inc)) * 100
        print(f"Correct Predictions: {corr}")
        print(f"Incorrect Predictions: {inc}")
        print(f"Accuracy: {acc:.2f}%")
        print(f"Expected Accuracy: {exp_acc:.2f}%")
    else:
        print("No confident predictions made yet.")

if __name__ == "__main__":
    test_elo()
    # m.main()