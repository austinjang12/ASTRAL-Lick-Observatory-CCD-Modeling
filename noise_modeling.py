import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label, center_of_mass

ny, nx = 200, 200 
base_signal = 1000  

flat = np.ones((ny, nx)) * base_signal

def add_star(image, x0, y0, amplitude, fwhm, beta=3.5):
    y, x = np.indices(image.shape)
    
    alpha = fwhm / (2 * np.sqrt(2**(1/beta) - 1))
    
    r2 = (x - x0)**2 + (y - y0)**2
    star = amplitude * (1 + r2 / alpha**2)**(-beta)

    fwhm = np.random.uniform(2.0, 4.0) 
    
    image += star

star_locations = []

for _ in range(20):
    x0 = np.random.uniform(15, nx-15)
    y0 = np.random.uniform(15, ny-15)
    amplitude = np.random.uniform(500, 2500)
    sigma = np.random.uniform(0.8, 1.5)  
    star_locations.append((x0, y0, amplitude, sigma)) 
    add_star(flat, x0, y0, amplitude, sigma)

print("Star locations and properties (x, y, amplitude, sigma):")
for i, (x, y, amp, s) in enumerate(star_locations, 1):
    print(f"Star {i}: x={x}, y={y}, amplitude={amp:.1f}, sigma={s:.2f}")

plt.imshow(flat, cmap='gray', origin='lower')
plt.colorbar(label='Electrons')
plt.title('Perfect Flat (no noise)')
plt.show()

############# Dark Current ##################

exposure_time = 100

dark_current_rate = 0.2  #e-/sec/pixel

dark_signal = dark_current_rate * exposure_time

flat_with_dark = flat + dark_signal

hot_pixel_map = np.zeros((ny, nx))

for _ in range(100):
    y = np.random.randint(0, ny)
    x = np.random.randint(0, nx)
    hot_pixel_map[y, x] = np.random.uniform(1, 5)  # e-/sec

dark_map = dark_current_rate + hot_pixel_map
dark_signal = dark_map * exposure_time

flat_with_dark = flat + dark_signal

plt.imshow(flat_with_dark, cmap='gray', origin='lower')
plt.colorbar(label='Electrons')
plt.title('Flat with Dark Current')
plt.show()

########### shot noise #############
shot_noise_flat = np.random.poisson(flat_with_dark)

plt.imshow(shot_noise_flat, cmap='gray', origin='lower')
plt.colorbar(label='Electrons')
plt.title('Flat with Shot Noise')
plt.show()

########## read noise ############
read_noise_sigma = 20  # electrons

flat_with_noise = shot_noise_flat + np.random.normal(0, read_noise_sigma, (ny, nx))

plt.imshow(flat_with_noise, cmap='gray', origin='lower')
plt.colorbar(label='Electrons')
plt.title('Flat with Shot Noise + Read Noise')
plt.show()

############# Saturation ###############
full_well = 5000

saturated_flat = np.clip(flat_with_noise, 0, full_well)

plt.imshow(saturated_flat, cmap='gray', origin='lower')
plt.colorbar(label='Electrons')
plt.title('Flat with Noise + Saturation')
plt.show()

mean_pixel = saturated_flat.mean()
std_pixel = saturated_flat.std()

print(f"Mean pixel: {mean_pixel:.2f}")
print(f"Std pixel: {std_pixel:.2f}")




####################################################
####################################################
####################################################
####################################################


# -----------------------------
# Estimate background and noise
# -----------------------------
# Use pixels below a high threshold to avoid stars
background = np.median(saturated_flat)
noise = np.std(saturated_flat[saturated_flat < background + 3*20])  # 20 is your read_noise_sigma

print(f"Estimated background: {background:.2f} e-")
print(f"Estimated noise: {noise:.2f} e-")

# threshold to detect stars - Anything significantly above background is considered a star
threshold = background + 5*noise
star_pixels = saturated_flat > threshold

###connected regions
labeled_array, num_features = label(star_pixels)
print(f"Detected {num_features} stars")

##star properties##
star_info = []

for i in range(1, num_features+1):
    mask = labeled_array == i
    total_flux = np.sum(saturated_flat[mask] - background)
    y_center, x_center = center_of_mass(mask)
    peak = np.max(saturated_flat[mask])
    star_info.append({
        "id": i,
        "x": x_center,
        "y": y_center,
        "peak": peak,
        "total_flux": total_flux
    })

for star in star_info[:25]:
    print(f"Star {star['id']}: x={star['x']:.1f}, y={star['y']:.1f}, peak={star['peak']:.1f}, total_flux={star['total_flux']:.1f}")

plt.imshow(saturated_flat, cmap='gray', origin='lower')
plt.contour(labeled_array, colors='red', linewidths=0.5)  # outlines each star
plt.title("Detected Stars (red contours)")
plt.colorbar(label='Electrons')
plt.show()
