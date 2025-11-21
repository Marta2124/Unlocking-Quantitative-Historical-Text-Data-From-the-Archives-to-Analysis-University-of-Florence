library(dplyr)
library(tidyr)
library(ggplot2)
library(sf)
library(rnaturalearth)
library(readr)

# 1. Load CSV

df <- read_csv("/Users/martapagnini/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_4_plotting_spatial_data_in_a_map/uk_geocoded_social_groups.csv") %>%
  filter(!is.na(lat) & !is.na(lng)) %>%
  separate_rows(space_extracted, sep="\\|") %>%
  mutate(space_extracted = trimws(space_extracted))



# Calculate % of social groups for 1870 and 1920
social_group_percentages <- df %>%
  filter(Year %in% c(1870, 1920)) %>%            # keep only 1870 and 1920
  group_by(Year, predicted_label) %>%            # group by year & social group
  summarise(n = n(), .groups = "drop") %>%       # count rows
  group_by(Year) %>%
  mutate(percentage = n / sum(n) * 100)          # convert to %

social_group_percentages

# 2. Count social groups per city/year
df_summary <- df %>%
  group_by(Year, space_extracted, predicted_label) %>%
  summarise(count = n(), .groups = "drop")

df <- df %>%
  left_join(df_summary, by = c("Year", "space_extracted", "predicted_label"))

# 3. Convert to sf points

df_sf <- st_as_sf(df, coords = c("lng", "lat"), crs = 4326)

# 4. Load UK map
uk <- ne_countries(country = "United Kingdom", scale = "medium", returnclass = "sf")

# 5. Plot with scaled points but real counts in legend

# Use a transformation for point sizes (sqrt) for better visualization
# but keep legend labels as actual counts
max_count <- max(df_sf$count)

p <- ggplot() +
  geom_sf(data = uk, fill = "lightgrey", color = "black") +
  geom_sf(data = df_sf, aes(color = predicted_label, size = count), alpha = 0.7) +
  scale_size_continuous(
    range = c(1,8),
    breaks = c(1, round(max_count/4), round(max_count/2), max_count),
    labels = c(1, round(max_count/4), round(max_count/2), max_count)
  ) +
  facet_wrap(~Year) +
  coord_sf(xlim = c(-10, 2), ylim = c(49, 60)) +
  labs(title = "Social Groups by City in UK",
       color = "Social Group",
       size = "Number of entries") +
  theme_minimal()

# -------------------------------
# 6. Save as PDF
# -------------------------------
output_pdf <- "/Users/martapagnini/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_4_plotting_spatial_data_in_a_map/uk_social_groups_map.pdf"
ggsave(filename = output_pdf, plot = p, width = 10, height = 12)
