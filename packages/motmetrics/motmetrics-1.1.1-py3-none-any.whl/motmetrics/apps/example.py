"""py-motmetrics - metrics for multiple object tracker (MOT) benchmarking.

Christoph Heindl, 2017
https://github.com/cheind/py-motmetrics
"""

import motmetrics as mm
import numpy as np

if __name__ == '__main__':

    # Create an accumulator that will be updated during each frame
    acc = mm.MOTAccumulator(auto_id=True)

    # Each frame a list of ground truth object / hypotheses ids and pairwise distances
    # is passed to the accumulator. For now assume that the distance matrix given to us.

    # 2 Matches, 1 False alarm
    acc.update(
        ['a', 'b'],                 # Ground truth objects in this frame
        [1, 2, 3],                  # Detector hypotheses in this frame
        [[0.1, np.nan, 0.3],        # Distances from object 'a' to hypotheses 1, 2, 3
         [0.5,  0.2,   0.3]]        # Distances from object 'b' to hypotheses 1, 2, 
    )
    print(acc.events)

    # 1 Match, 1 Miss
    df = acc.update(
        ['a', 'b'],
        [1],
        [[0.2], [0.4]]
    )
    print(df)

    # 1 Match, 1 Switch
    df = acc.update(
        ['a', 'b'],
        [1, 3],
        [[0.6, 0.2],
         [0.1, 0.6]]
    )
    print(df)
    
    # Compute metrics

    mh = mm.metrics.create()
    summary = mh.compute(acc, metrics=['num_frames', 'mota', 'motp'], name='acc')
    print(summary)

    summary = mh.compute_many(
        [acc, acc.events.loc[0:1]], 
        metrics=['num_frames', 'mota', 'motp'], 
        names=['full', 'part'])    
    print(summary)


    strsummary = mm.io.render_summary(
        summary, 
        formatters={'mota' : '{:.2%}'.format}, 
        namemap={'mota': 'MOTA', 'motp' : 'MOTP'}
    )
    print(strsummary)


    summary = mh.compute_many(
        [acc, acc.events.loc[0:1]], 
        metrics=mm.metrics.motchallenge_metrics, 
        names=['full', 'part'])
    strsummary = mm.io.render_summary(
        summary, 
        formatters=mh.formatters, 
        namemap=mm.io.motchallenge_metric_names
    )
    print(strsummary)