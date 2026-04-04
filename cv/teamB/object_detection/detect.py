import cv2
import numpy as np
import scipy.io as sio
from pathlib import Path
import json
import time

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
BASE_DIR      = Path(__file__).resolve().parent.parent  # cv/teamB/
RAW_DIR       = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

CLASSES  = ["fish", "fly", "honeybee", "seagull"]
MIN_AREA = 5
MAX_AREA = 500


# ─────────────────────────────────────────────
# LOAD GROUND TRUTH (.mat)
# ─────────────────────────────────────────────
def load_mat_bbox(mat_path):
    try:
        mat  = sio.loadmat(str(mat_path))
        keys = [k for k in mat.keys() if not k.startswith("_")]
        if not keys:
            return []
        data = mat[keys[0]]
        if data.dtype == object:
            data = np.vstack([b for b in data.flat if b.size > 0])
        return data.tolist()
    except Exception as e:
        print(f"  [WARN] {mat_path.name}: {e}")
        return []


# ─────────────────────────────────────────────
# DETECT OBJECTS IN ONE IMAGE
# ─────────────────────────────────────────────
def detect_objects(image_path):
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Cannot read: {image_path}")

    gray    = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh  = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=11, C=2
    )
    kernel  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opened  = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detections = []
    annotated  = img.copy()

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if not (MIN_AREA <= area <= MAX_AREA):
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy     = x + w // 2, y + h // 2
        detections.append({
            "x": int(x), "y": int(y),
            "w": int(w), "h": int(h),
            "area": float(area),
            "cx": int(cx), "cy": int(cy)
        })
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.circle(annotated, (cx, cy), 2, (0, 0, 255), -1)

    return detections, annotated


# ─────────────────────────────────────────────
# COMPUTE METRICS vs GROUND TRUTH
# ─────────────────────────────────────────────
def compute_metrics(detections, gt_boxes, iou_thresh=0.3):
    def iou(a, b):
        ax1, ay1, ax2, ay2 = a[0], a[1], a[0]+a[2], a[1]+a[3]
        bx1, by1, bx2, by2 = int(b[0]), int(b[1]), int(b[0])+int(b[2]), int(b[1])+int(b[3])
        ix    = max(0, min(ax2, bx2) - max(ax1, bx1))
        iy    = max(0, min(ay2, by2) - max(ay1, by1))
        inter = ix * iy
        if inter == 0:
            return 0.0
        union = (ax2-ax1)*(ay2-ay1) + (bx2-bx1)*(by2-by1) - inter
        return inter / union if union > 0 else 0.0

    matched = set()
    TP = 0
    for det in detections:
        box     = [det["x"], det["y"], det["w"], det["h"]]
        best, j = 0.0, -1
        for i, gt in enumerate(gt_boxes):
            if i in matched:
                continue
            s = iou(box, gt)
            if s > best:
                best, j = s, i
        if best >= iou_thresh and j >= 0:
            TP += 1
            matched.add(j)

    FP = len(detections) - TP
    FN = len(gt_boxes)   - TP
    P  = TP / (TP + FP) if (TP + FP) > 0 else 0.0
    R  = TP / (TP + FN) if (TP + FN) > 0 else 0.0
    return {"TP": TP, "FP": FP, "FN": FN,
            "precision": round(P, 4),
            "recall":    round(R, 4)}


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────
def run():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    summary = []

    for cls in CLASSES:
        img_dir  = RAW_DIR / cls / "img"
        bbox_dir = RAW_DIR / cls / "gt-bbox"
        out_dir  = PROCESSED_DIR / cls
        out_dir.mkdir(parents=True, exist_ok=True)

        if not img_dir.exists():
            print(f"[SKIP] {cls} - folder not found")
            continue

        images = sorted(img_dir.glob("*.jpg")) + sorted(img_dir.glob("*.png"))
        if not images:
            print(f"[SKIP] {cls} - no images found")
            continue

        print(f"\n{'='*50}")
        print(f"  Class: {cls}  ({len(images)} images)")
        print(f"{'='*50}")

        results                        = []
        total_det                      = 0
        total_tp = total_fp = total_fn = 0

        for img_path in images:
            # detect
            try:
                detections, annotated = detect_objects(img_path)
            except Exception as e:
                print(f"  [ERROR] {img_path.name}: {e}")
                continue

            # load GT
            gt_boxes  = []
            img_index = "".join(filter(str.isdigit, img_path.stem))
            if bbox_dir.exists():
                for mf in sorted(bbox_dir.glob("*.mat")):
                    if img_index and img_index in mf.stem:
                        gt_boxes = load_mat_bbox(mf)
                        break

            # metrics
            metrics = compute_metrics(detections, gt_boxes) if gt_boxes else {}
            if metrics:
                total_tp += metrics["TP"]
                total_fp += metrics["FP"]
                total_fn += metrics["FN"]
            total_det += len(detections)

            # save annotated image
            cv2.imwrite(str(out_dir / f"det_{img_path.name}"), annotated)

            results.append({
                "image":      img_path.name,
                "detections": len(detections),
                "gt_boxes":   len(gt_boxes),
                "metrics":    metrics,
                "boxes":      detections
            })

            print(f"  {img_path.name:30s} | det={len(detections):3d}  "
                  f"gt={len(gt_boxes):3d}  "
                  f"P={metrics.get('precision', '-')}  "
                  f"R={metrics.get('recall', '-')}")

        # save per-class results
        with open(out_dir / "results.json", "w") as f:
            json.dump(results, f, indent=2)

        # class summary
        P  = total_tp/(total_tp+total_fp) if (total_tp+total_fp) > 0 else 0
        R  = total_tp/(total_tp+total_fn) if (total_tp+total_fn) > 0 else 0
        F1 = 2*P*R/(P+R) if (P+R) > 0 else 0
        summary.append({
            "class": cls, "images": len(results),
            "total_detections": total_det,
            "TP": total_tp, "FP": total_fp, "FN": total_fn,
            "precision": round(P, 4),
            "recall":    round(R, 4),
            "f1":        round(F1, 4)
        })

    # final summary
    print(f"\n{'='*60}")
    print("  FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"{'Class':<12} {'Imgs':>5} {'Dets':>6} {'P':>7} {'R':>7} {'F1':>7}")
    print("-" * 60)
    for row in summary:
        print(f"{row['class']:<12} {row['images']:>5} "
              f"{row['total_detections']:>6} "
              f"{row['precision']:>7} {row['recall']:>7} {row['f1']:>7}")

    with open(PROCESSED_DIR / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Annotated images -> {PROCESSED_DIR}")
    print(f"  Summary          -> {PROCESSED_DIR / 'summary.json'}")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    t0 = time.time()
    run()
    print(f"\n  Done in {time.time() - t0:.1f}s")