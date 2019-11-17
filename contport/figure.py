import numpy as np
import matplotlib.pyplot as plt
import io

build_trend = [
    {
        "number": 1,
        "pass": 1,
        "fail": 3
    },
    {
        "number": 2,
        "pass": 1,
        "fail": 3
    },
    {
        "number": 3,
        "pass": 1,
        "fail": 3
    },
    {
        "number": 4,
        "pass": 1,
        "fail": 3
    },
    {
        "number": 5,
        "pass": 0,
        "fail": 4
    },
    {
        "number": 6,
        "pass": 0,
        "fail": 4
    },
    {
        "number": 7,
        "pass": 0,
        "fail": 4
    }
    ]

def get_binary_figure():
    N = len(build_trend)
    passed = [i["pass"] for i in build_trend]
    failed = [i["fail"] for i in build_trend]
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, passed)
    p2 = plt.bar(ind, failed, bottom=passed)

    plt.ylabel('Number of cases')
    plt.title('Build Trend')
    plt.xticks(ind, ["#%s" % (i+1) for i in range(N)])
    #  plt.yticks(np.arange(0, 81, 10))
    plt.legend((p1[0], p2[0]), ('Pass', 'Fail'))

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    return buf.read()

    #plt.savefig('build_trend_image.png')