# -----------------------------
# Load libraries
# -----------------------------
library(RSelenium)   # Automate browser actions
library(netstat)     # Find free ports
library(rvest)       # Optional, for parsing HTML
library(tidyverse)   # Optional, for data manipulation

# -----------------------------
# Start RSelenium with Firefox
# -----------------------------
rD <- rsDriver(
  browser = "firefox",
  port = netstat::free_port(),  # pick a free port
  phantomver = NULL             # skip PhantomJS
)

# Get the browser client
driver <- rD$client

# -----------------------------
# Navigate to the webpage
# -----------------------------
url <- "https://example.com"    # replace with your target URL
driver$navigate(url)

# -----------------------------
# Find an element by XPath
# -----------------------------
# Replace 'copy_your_xpath' with the actual XPath of the element
element <- driver$findElement(using = "xpath", "copy_your_xpath")

# Get text content
text_value <- element$getElementText()[[1]]
print(text_value)

# -----------------------------
# Click an element (e.g., a button)
# -----------------------------
# Replace 'copy_your_xpath_for_button' with actual XPath
button <- driver$findElement(using = "xpath", "copy_your_xpath_for_button")
button$clickElement()

# -----------------------------
# Optional: get another element after clicking
# -----------------------------
new_element <- driver$findElement(using = "xpath", "copy_new_xpath")
new_text <- new_element$getElementText()[[1]]
print(new_text)

# -----------------------------
# Close RSelenium session
# -----------------------------
driver$close()
rD$server$stop()
