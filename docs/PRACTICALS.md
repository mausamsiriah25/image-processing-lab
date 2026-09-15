# Practicals Map — extracted from Image_Processing_lab.md

Course: **Image Processing Lab** — Course Code **N-PECCS502P**

This is the canonical field-level mapping from the source Markdown to the
application's content schema (see `CLAUDE.md` §6). It must stay in sync with
`content/practicals/*.json`.

---

## practical-01 — Python & IDE Setup (Prelab)

- **Category:** Setup / Fundamentals
- **requiresImage:** false
- **Aim:** Introduce Python and set up the development environment for image
  processing (PyCharm/Jupyter/Colab), installing OpenCV, NumPy, Pandas,
  Scikit-learn, Matplotlib.
- **Theory covers:** Python overview, what an IDE is, role of NumPy, Pandas,
  Scikit-learn, Matplotlib, OpenCV in image processing.
- **Content includes:** install steps for PyCharm, Google Colab, and Jupyter
  Notebook; a basic "read + display + wait + close" OpenCV syntax block;
  a minimal read/display code sample.
- **Special handling:** This practical has no image transformation to run.
  UI shows theory + install steps + the syntax/code reference, with **no**
  "Run Experiment" workspace — replaced by a setup checklist. No parameters,
  no outputs, no report image sections (report still includes aim/theory/
  conclusion text).

---

## practical-02 — Image I/O, Colour Conversion, Arithmetic & Bitwise Ops

- **Category:** Fundamentals
- **requiresImage:** true (2 images for arithmetic/bitwise sub-operations)
- **Aim:** Convert images between formats (RGB/Grayscale) and perform
  arithmetic and bitwise operations using OpenCV.
- **Theory covers:** pixels, RGB image, grayscale image, `cv2.imread`,
  `cv2.imshow`, `cv2.waitKey`, `cv2.destroyAllWindows`, `cv2.imwrite`,
  BGR↔RGB conversion, BGR→Gray conversion, arithmetic ops (`cv2.add`,
  `cv2.addWeighted`, `cv2.subtract`), bitwise ops (`cv2.bitwise_and/or/xor/not`).
- **Parameters:**
  - `operation`: select — `grayscale | bgr2rgb | add | addWeighted | subtract | bitwise_and | bitwise_or | bitwise_xor | bitwise_not`
  - `weight1`, `weight2`, `gamma` (only for `addWeighted`)
- **Outputs:** original, converted/result image; for two-image ops, both
  inputs plus the combined result.
- **Special handling:** second image uploader appears only when the
  selected operation needs two images.

---

## practical-03 — 2D Geometric Transformations

- **Category:** Geometric Transformations
- **requiresImage:** true
- **Aim:** Apply 2D geometric transformations: Translation, Reflection,
  Rotation, Scaling (shrink/enlarge), Cropping, Shearing (X and Y axis).
- **Algorithm/operations present in source code:**
  1. Translation (matrix `[[1,0,tx],[0,1,ty]]` via `cv2.warpAffine`)
  2. Reflection along X-axis
  3. Rotation (`cv2.getRotationMatrix2D` + `cv2.warpAffine`)
  4. Shrink (scale down, `cv2.resize`)
  5. Enlarge (scale up, `cv2.resize`)
  6. Crop (array slicing)
  7. Shearing — X-axis matrix
  8. Shearing — Y-axis matrix
- **Parameters:**
  - `operation`: select — one of the 8 above
  - `tx`, `ty` (translation)
  - `angle` (rotation, degrees)
  - `scale` (shrink/enlarge factor)
  - `x1,y1,x2,y2` (crop box)
  - `shearFactor` (X or Y shear)
- **Outputs:** original + transformed image for the selected operation (or,
  as an "all transforms" mode, one output per transformation).

---

## practical-04 — Spatial Domain Image Enhancement

- **Category:** Image Enhancement
- **requiresImage:** true
- **Aim:** Study/implement Histogram Equalization, Spatial Filtering
  (smoothing/sharpening), and Thresholding for spatial-domain enhancement.
- **Operations present in source code:**
  1. Negative image (`255 - pixel`)
  2. Brightness & contrast (`cv2.convertScaleAbs`, alpha/beta)
  3. Brightness & contrast via manual scaling
  4. Sharpening (kernel convolution, `cv2.filter2D`)
  5. Laplacian filtering/sharpening (`cv2.Laplacian`)
  6. Median filtering (`cv2.medianBlur`)
  7. Histogram equalization (`cv2.equalizeHist`) + histogram plot
     (Matplotlib) before/after
  8. Thresholding — 5 types: `THRESH_BINARY`, `THRESH_BINARY_INV`,
     `THRESH_TRUNC`, `THRESH_TOZERO`, `THRESH_TOZERO_INV`
- **Parameters:**
  - `operation`: select from the 8 above
  - `alpha` (contrast), `beta` (brightness)
  - `medianKernel` (odd int)
  - `thresholdValue` (0–255), `thresholdType` (one of the 5)
- **Outputs:** processed image; for histogram equalization, also the
  before/after histogram chart; for thresholding, can show all 5 variants
  side by side.

---

## practical-05 — Spatial Domain Filters

- **Category:** Filtering
- **requiresImage:** true
- **Aim:** Apply Averaging, Box, Gaussian, Median, and Bilateral filters.
- **Operations:**
  1. Averaging filter (`cv2.blur`)
  2. Box filter (`cv2.boxFilter`)
  3. Gaussian filter (`cv2.GaussianBlur`)
  4. Median filter (`cv2.medianBlur`)
  5. Bilateral filter (`cv2.bilateralFilter`)
- **Parameters:**
  - `filter`: select from the 5 above
  - `kernelSize` (odd int, e.g. 3/5/7)
  - `sigmaX` (Gaussian)
  - `diameter`, `sigmaColor`, `sigmaSpace` (bilateral)
- **Outputs:** original + filtered image; "compare all filters" mode shows
  one output per filter.

---

## practical-06 — Image Restoration (Inpainting & Denoising)

- **Category:** Restoration
- **requiresImage:** true
- **Aim:** Restore damaged image regions via inpainting (Telea &
  Navier-Stokes methods) and reduce noise via denoising filters.
- **Operations present in source code:**
  1. Automatic damage-mask creation (threshold near-black pixels) +
     `cv2.inpaint(..., cv2.INPAINT_TELEA)`
  2. Predefined-mask inpainting + `cv2.inpaint(..., cv2.INPAINT_NS)`
  3. Gaussian blur denoising
  4. Median filter denoising
  5. Non-local means denoising (`cv2.fastNlMeansDenoising`, params `h`,
     `templateWindowSize`, `searchWindowSize`)
  6. Synthetic damaged/noisy image generators (Gaussian noise, salt &
     pepper noise, scratches) used in the source to create demo inputs
- **Parameters:**
  - `mode`: select — `inpaint_telea | inpaint_ns | denoise_gaussian | denoise_median | denoise_nlm`
  - `maskThreshold` (auto mask sensitivity)
  - `inpaintRadius`
  - `nlmH`, `templateWindowSize`, `searchWindowSize`
- **Outputs:** mask preview, restored/denoised image(s); when both Telea and
  NS are run, both results shown side by side.
- **Special handling:** manual mask drawing is **out of scope for V1**
  (documented as future extension — see ARCHITECTURE.md §6). V1 uses
  automatic mask detection only. A "generate a synthetic damaged demo image"
  option can substitute for upload, since the source code demonstrates this
  pattern.

---

## practical-07 — Lossless Image Compression

- **Category:** Compression
- **requiresImage:** true
- **Aim:** Implement a coding technique for lossless compression and compare
  original vs compressed sizes.
- **Operations present in source code:**
  1. Lossy JPEG vs lossless PNG size/quality comparison + compression ratio
  2. RLE (Run-Length Encoding) encode/decode + lossless reconstruction check
     + approximate compressed size
  3. LZW compression/decompression + lossless reconstruction check +
     approximate compressed size
- **Parameters:**
  - `method`: select — `jpeg_vs_png | rle | lzw`
  - `jpegQuality` (for the JPEG comparison path)
- **Outputs (non-standard — numeric/table heavy):**
  - `type: "value"` — original size, compressed size, compression ratio
  - `type: "table"` — method-by-method comparison
  - `type: "image"` — reconstructed image (to visually confirm lossless
    reconstruction matches the original)
- **Special handling:** this practical's primary output is data, not a
  transformed image — `ProcessingResult` must use `value`/`table` output
  types alongside a single confirmation image, per CLAUDE.md §5.

---

## practical-08 — Morphological Operations

- **Category:** Morphological Operations
- **requiresImage:** true
- **Aim:** Perform Erosion, Dilation, Opening, and Closing on binary images
  and study effects on shapes/noise.
- **Operations:**
  1. Binarization (thresholding to create the binary image)
  2. Erosion (`cv2.erode`)
  3. Dilation (`cv2.dilate`)
  4. Opening (`cv2.morphologyEx`, `MORPH_OPEN`)
  5. Closing (`cv2.morphologyEx`, `MORPH_CLOSE`)
  6. Object area analysis per operation (contour/area calculation)
- **Parameters:**
  - `binarizeThreshold`
  - `kernelSize`, `kernelShape` (rect/ellipse/cross if present)
  - `iterations`
- **Outputs:** binary image + one output per morphological operation +
  a `type: "table"` output of object areas per operation.

---

## practical-09 — Object Detection Using Correlation Principle

- **Category:** Object Detection
- **requiresImage:** true
- **multiImage:** true — needs a **template image** and a **target/scene
  image**
- **Aim:** Detect an object in an image using the correlation principle
  (OpenCV template matching).
- **Operations:** `cv2.matchTemplate` (normalized correlation) +
  thresholding the match score (source uses `0.8`) + drawing a bounding
  rectangle on the best match.
- **Parameters:**
  - `matchThreshold` (default `0.8`)
  - `matchMethod` (fixed to the normalized-correlation method used in the
    source unless the Markdown implies otherwise)
- **Outputs:** target image annotated with the detection rectangle (or a
  "not detected" message/output if below threshold) + numeric match score.

---

## postlab-02 — Colour Space Conversion

- **Category:** Colour Processing
- **requiresImage:** true
- **Aim:** Convert images between RGB, HSV, YCrCb, and Lab colour spaces and
  analyze how colour information is encoded in each.
- **Operations present in source code:**
  1. Grayscale read/display
  2. BGR channel split — display Blue, Green, Red channels individually
  3. BGR → YCrCb
  4. BGR → HSV
  5. BGR → Lab
  6. Combined view converting to multiple colour spaces at once
- **Parameters:**
  - `targetSpace`: select — `grayscale | channels | ycrcb | hsv | lab | all`
- **Outputs:** one image per selected space/channel; `all` mode returns all
  of them together.

---

## postlab-03 — Edge Detection: Canny vs Sobel vs Prewitt

- **Category:** Edge Detection
- **requiresImage:** true
- **Aim:** Detect edges using Canny and compare against Sobel and Prewitt
  operators.
- **Operations present in source code:**
  1. Gaussian blur pre-processing + `cv2.Canny` (low/high thresholds)
  2. Sobel gradients (x, y) → gradient magnitude → 8-bit conversion
  3. Prewitt kernels (custom convolution via `cv2.filter2D`) → gradient
     magnitude → 8-bit conversion
  4. Side-by-side comparison of all three
- **Parameters:**
  - `cannyLow`, `cannyHigh`
  - `gaussianKernel` (pre-blur for Canny)
- **Outputs:** Canny edge map, Sobel magnitude map, Prewitt magnitude map,
  and a combined comparison output.

---

## Cross-Practical Notes

- **Multiple outputs** are the norm, not the exception: practicals 03, 04,
  05, 06, 07, 08, and postlab-02/03 all naturally produce more than one
  result. The `ProcessingResult.outputs` list design (CLAUDE.md §5) is
  required, not optional polish.
- **Charts/histograms** are needed for: practical-04 (histogram
  equalization), practical-07 (size/ratio comparison table, optionally a
  bar chart), practical-08 (area comparison table).
- **Parameter-heavy practicals:** 02, 03, 04, 05, 06, 08, postlab-02,
  postlab-03. **Fixed/no-parameter:** 01 (no processing at all), 09 (mostly
  fixed threshold, exposed as one tunable number).
- **Two-image practicals:** 02 (conditionally, for arithmetic/bitwise), 09
  (always — template + target).
- **No-image practical:** 01 only.
