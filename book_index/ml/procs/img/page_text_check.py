# -*- coding: utf-8 -*-
import torch
from torch.autograd import Variable

import cv2
import numpy as np
from collections import OrderedDict

from imutils.object_detection import non_max_suppression

from ml.procs.img.craft_utils import craft, imgproc, craft_utils
from ml.procs.img.craft_utils.craft import CRAFT

def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict

def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")


class PageTxtChecker():

    trained_model = 'model/craft_mlt_25k.pth'
    canvas_size = 1280
    text_threshold = 0.7
    low_text = 0.4
    link_threshold = 0.4
    mag_ratio = 1.5
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    poly = False
    show_time = False
    refine = False

    def __init__(self):
        print('-'*50)
        print(' '*21 + self.device)
        print('-'*50)
        self.network = CRAFT()

        # -----------------
        # load_weights
        self._load_weights()

        pass

    def draw_txt_bboxes(self, img):

        orig = img.copy()
        bboxes = self._test_net(self.network, img, self.text_threshold, self.link_threshold, self.low_text,
                                      self.poly)
        rects = self._refine_bboxes(bboxes)

        for (startX, startY, endX, endY) in rects:
            cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

        return orig

    def _load_weights(self):
        self.network.to(self.device)
        self.network.load_state_dict(copyStateDict(torch.load(self.trained_model, map_location=torch.device(self.device))))
        self.network.eval()
        pass

    def _refine_bboxes(self, bboxes):

        rects = []
        for bbox in bboxes:
            start = tuple((np.round(bbox[0])).astype(np.int32))
            end = tuple((np.round(bbox[2])).astype(np.int32))

            rects.append(np.array(start + end))

        rects = non_max_suppression(np.array(rects))

        return rects

    def _test_net(self, net, img, text_threshold, link_threshold, low_text, poly):

        # resize
        img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(img, self.canvas_size,
                                                                              interpolation=cv2.INTER_LINEAR,
                                                                              mag_ratio=self.mag_ratio)
        ratio_h = ratio_w = 1 / target_ratio

        # preprocessing
        x = imgproc.normalizeMeanVariance(img_resized)
        x = torch.from_numpy(x).permute(2, 0, 1)  # [h, w, c] to [c, h, w]
        x = Variable(x.unsqueeze(0))  # [c, h, w] to [b, c, h, w]

        x = x.to(self.device)

        # forward pass
        y, feature = net(x)

        # make score and link map
        score_text = y[0, :, :, 0].cpu().data.numpy()
        score_link = y[0, :, :, 1].cpu().data.numpy()

        # Post-processing
        boxes, polys = craft_utils.getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text, poly)

        # coordinate adjustment
        boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)

        return boxes