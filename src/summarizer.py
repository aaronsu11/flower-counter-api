from statistics import mean, stdev
from scipy import stats


def summarize(results):
    summary = dict()

    if results:
        # Number of data
        SIZE = len(results)
        summary["size"] = SIZE

        # Sum
        # summary["sum"] = 0
        # for result in results:
        #     summary["sum"] = summary["sum"] + result

        # Mean
        MEAN = mean(results)
        summary["mean"] = MEAN

        # Maximun
        MAX = max(results)
        summary["max"] = MAX

        # Minimum
        MIN = min(results)
        summary["min"] = MIN

        if SIZE > 1:
            # Following only valid for more than 1 sample point
            # Standard Deviation
            STDEV = stdev(results)
            summary["stdev"] = STDEV

            #  Variance
            # VAR = variance(results)
            # summary["var"] = VAR
            # Variation
            VART = STDEV * 100 / MEAN

            # Best sample size
            # TINV(0.05,SIZE-1)^2*VART^2/15^2
            # Studnt, n=999, p<0.05, 2-tail
            # equivalent to Excel TINV(0.05,999)
            # stats.t.ppf(1-0.025, 999)
            TOL = 15  # 15% Tolerance
            BSS = (stats.t.ppf(1 - 0.025, SIZE - 1) * VART / TOL) ** 2
            # Round up or down
            # to specify strict up or down, use math.ceil() or math.floor()
            summary["bss"] = round(BSS, 0)
        else:
            summary["stdev"] = "N/A"
            # summary["var"] = "N/A"
            summary["bss"] = "N/A"
            summary["message"] = "not enough samples"
    else:
        summary["message"] = "result is empty"

    return summary
