import numpy as np
import io

import matplotlib.pyplot as plt


def get_binary_figure(build_summary):
    N = len(build_summary)
    passed = [i["pass"] for i in build_summary]
    failed = [i["fail"] for i in build_summary]

    ind = np.arange(N)
    plt.figure(figsize=(8, 4.5))

    p1 = plt.bar(ind, passed, color="green")
    p2 = plt.bar(ind, failed, bottom=passed, color="red")

    plt.ylabel('Number of cases')
    plt.title('Build Trend')
    plt.xticks(ind, ["#%s" % build_summary[i]["number"]
                     for i in range(N)],  rotation='vertical')

    plt.legend((p1[0], p2[0]), ('Pass', 'Fail'))

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()
