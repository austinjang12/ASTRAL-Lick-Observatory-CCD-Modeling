import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.ndimage import label, center_of_mass
from astropy.stats import sigma_clipped_stats

# -------------------------------
# 1. LOAD REAL FITS IMAGE
# -------------------------------
with fits.open("data/d145.fits") as hdul:
    real_image = hdul[0].data.astype(float)

image = real_image.copy()
ny, nx = image.shape

# -------------------------------
# 2. STAR INJECTION FUNCTIONS
# -------------------------------
def add_star_moffat_elliptical(image, x0, y0, amplitude,
                               alpha_x, alpha_y, beta):
    y, x = np.indices(image.shape)
    r2 = ((x - x0)**2 / alpha_x**2 +
          (y - y0)**2 / alpha_y**2)
    star = amplitude * (1 + r2)**(-beta)
    image += star

true_stars = []

for _ in range(50):
    x0 = np.random.randint(20, nx-20)
    y0 = np.random.randint(20, ny-20)

    amplitude = np.random.uniform(2000, 8000)

    alpha_x = np.random.uniform(1.5, 3.0)
    alpha_y = np.random.uniform(1.5, 3.0)

    beta = np.random.uniform(2.0, 4.0)

    add_star_moffat_elliptical(image, x0, y0,
                               amplitude,
                               alpha_x, alpha_y,
                               beta)

    true_stars.append((x0, y0))
# -------------------------------
# 3. ADD COSMIC RAYS
# -------------------------------
for _ in range(20):
    x = np.random.randint(0, nx)
    y = np.random.randint(0, ny)
    image[y, x] += np.random.uniform(8000, 20000)

# -------------------------------
# 4. APPLY SATURATION
# -------------------------------
full_well = 60000
image = np.clip(image, 0, full_well)

# -------------------------------
# 5. CREATE GROUND TRUTH MASK
# -------------------------------
true_mask = np.zeros_like(image)

for x0, y0 in true_stars:
    true_mask[y0-3:y0+4, x0-3:x0+4] = 1

# -------------------------------
# 6. SIMPLE DETECTION ALGORITHM
# -------------------------------
mean, median, std = sigma_clipped_stats(image, sigma=3.0)

threshold = median + 5 * std
binary = image > threshold

labeled, num_features = label(binary)

detected_centers = center_of_mass(binary, labeled, range(1, num_features+1))

# -------------------------------
# 7. MATCH DETECTIONS TO TRUE STARS
# -------------------------------
matched = 0
tolerance = 5  # pixels

for tx, ty in true_stars:
    for cy, cx in detected_centers:
        if np.sqrt((tx - cx)**2 + (ty - cy)**2) < tolerance:
            matched += 1
            break

print("===================================")
print(f"Injected stars: {len(true_stars)}")
print(f"Detected sources: {len(detected_centers)}")
print(f"Matched stars: {matched}")
print(f"Detection efficiency: {matched/len(true_stars)*100:.2f}%")
print("===================================")

# -------------------------------
# 8. PLOT EVERYTHING SIDE-BY-SIDE
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# -------------------------------
# 1️⃣ Original real image
# -------------------------------
vmin0 = np.percentile(real_image, 5)
vmax0 = np.percentile(real_image, 99)

axs[0].imshow(real_image, cmap='gray', origin='lower',
              vmin=vmin0, vmax=vmax0)
axs[0].set_title("Original FITS Image")

# -------------------------------
# 2️⃣ Injected image
# -------------------------------
vmin1 = np.percentile(image, 5)
vmax1 = np.percentile(image, 99)

axs[1].imshow(image, cmap='gray', origin='lower',
              vmin=vmin1, vmax=vmax1)
axs[1].set_title("Real Image + Injected Stars")

# -------------------------------
# 3️⃣ Detection overlay
# -------------------------------
axs[2].imshow(image, cmap='gray', origin='lower',
              vmin=vmin1, vmax=vmax1)
axs[2].set_title("Detection Results")

# Plot true stars (green)
for i, (x0, y0) in enumerate(true_stars):
    if i == 0:
        axs[2].plot(x0, y0, 'go', markersize=5, label="True Stars")
    else:
        axs[2].plot(x0, y0, 'go', markersize=5)

# Plot detected stars (red)
for i, (cy, cx) in enumerate(detected_centers):
    if i == 0:
        axs[2].plot(cx, cy, 'r+', markersize=8, label="Detected")
    else:
        axs[2].plot(cx, cy, 'r+', markersize=8)

axs[2].legend()

plt.tight_layout()
plt.show()

print(real_image.shape)
print(np.min(real_image), np.max(real_image))
