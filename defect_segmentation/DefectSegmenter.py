from Utils.ConfigProvider import ConfigProvider
from defect_segmentation.DiffSegmenter import DiffSegmenter
from defect_segmentation.BlurredDiffSegmenter import BlurredDiffSegmenter
from defect_segmentation.LowDiffFarFromEdgeSegmenter import LowDiffFarFromEdgeSegmenter
from defect_segmentation.ThreadDefectSegmenter import ThreadDefectSegmenter
from defect_segmentation.DefectSegmentationRefineer import DefectSegmentationRefiner

import numpy as np
from Utils.plotting.plot_utils import plot_image


class DefectSegmenter(object):
    def __init__(self):
        self._config = ConfigProvider.config()
        self._refiner = DefectSegmentationRefiner()

        self._defect_segmenters = [
            DiffSegmenter(),
            BlurredDiffSegmenter(),
            LowDiffFarFromEdgeSegmenter(),
            ThreadDefectSegmenter()
        ]

    def segment_defects(self, inspected, warped, warp_mask):
        focused_defect_mask = self._detect_defects(inspected, warp_mask, warped)
        segmentation_result = self._refiner.refine_segmentation(focused_defect_mask, inspected, warped, warp_mask)
        return segmentation_result

    def _detect_defects(self, inspected, warp_mask, warped):
        total_defect_mask = np.zeros(inspected.shape, dtype='uint8')
        for seg in self._defect_segmenters:
            seg_mask = seg.detect(inspected, warped, warp_mask)
            total_defect_mask = np.logical_or(total_defect_mask, seg_mask)

        plot_image(total_defect_mask, "total_defect_mask")
        return total_defect_mask
