# CCD Astrophysics — CCD Synthetic Noise Modeling

A computational astrophysics project for testing astronomical source-detection performance using real CCD imaging data and synthetic star injection.

## Overview

This project uses real astronomical CCD data stored in FITS format and performs an injection-recovery experiment to evaluate how effectively sources can be detected in an astronomical image.

Synthetic stars are modeled using elliptical Moffat point-spread functions and injected directly into a real CCD image. The resulting image is then processed with a simple threshold-based source-detection algorithm. Known injected sources are matched against detected sources to estimate the source-detection efficiency.

The goal is to study how well astronomical sources can be recovered under realistic image conditions.

## Method

The current pipeline consists of the following steps:

1. **Load a real FITS image**

   * Reads astronomical CCD data using `Astropy`.
   * Converts the image data to floating-point values for analysis.

2. **Inject synthetic stars**

   * Generates stars at random positions within the image.
   * Models each source using an elliptical Moffat profile.
   * Randomizes source amplitude, spatial scale, and Moffat shape parameter.

3. **Add detector artifacts**

   * Simulates cosmic-ray-like events by adding high-intensity pixels.

4. **Apply detector saturation**

   * Applies a full-well limit to simulate CCD saturation.

5. **Generate ground truth**

   * Records the known locations of all injected sources.

6. **Detect sources**

   * Estimates the background statistics using sigma-clipped statistics.
   * Applies a threshold of `median + 5σ`.
   * Identifies connected regions above the detection threshold.

7. **Perform injection-recovery matching**

   * Compares detected source positions against the known injected positions.
   * A detection is considered a match when it falls within a specified pixel tolerance.

8. **Calculate detection efficiency**

   * Computes the fraction of injected sources successfully recovered.

## Example Result

The program reports:

```text
===================================
Injected stars: 50
Detected sources: ...
Matched stars: ...
Detection efficiency: ...%
===================================
```

It also produces a three-panel visualization showing:

* The original astronomical image
* The image after synthetic source injection
* The detected sources compared with the known injected sources

## Requirements

Python 3.x with:

```text
numpy
matplotlib
astropy
scipy
```

Install the dependencies with:

```bash
pip install numpy matplotlib astropy scipy
```

## Usage

Place your FITS image in an accessible location and update the input path in the script:

```python
with fits.open("path/to/your/image.fits") as hdul:
    real_image = hdul[0].data.astype(float)
```

Then run:

```bash
python your_script.py
```

## Data

The code is designed to operate on FITS-format astronomical imaging data.

The repository does not necessarily contain the original observational data. Users should provide their own FITS image or obtain the relevant dataset from its appropriate source.

## Citation

If you use this software in academic research, please cite this repository.

The recommended citation is provided in [`CITATION.cff`](CITATION.cff), which can also be used by GitHub to generate citation formats.

## Author

**Austin Jang**

Physics undergraduate student and researcher at UC Berkeley..

## License

This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for details.


If you use this software in academic work, please cite this repository:

> Jang, A. (2026). CCD Synthetic Noise Modeling. GitHub.
> https://github.com/austinjang12/ASTRAL-Lick-Observatory-CCD-Modeling

A machine-readable citation is also provided in `CITATION.cff`.
