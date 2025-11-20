library(shiny)
library(jsonlite)

# Step 1: Read the CSV and sample 200 rows
# Step 1: Read CSV

cc_1870_1920 <- read.csv("/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Session 2/Activity_4_Creating_a_Tailored_Spacy_Model/sample_1870_1920_ner_people_regex_existing_spacy.csv")

set.seed(123)  # For reproducibility

# Step 2: Sample 50 rows from each year
#sample_1870 <- cc_1870_1920[cc_1870_1920$Year == 1870, ]
#sample_1920 <- cc_1870_1920[cc_1870_1920$Year == 1920, ]

#sample_50_1870 <- sample_1870[sample(nrow(sample_1870), 50), ]
#sample_50_1920 <- sample_1920[sample(nrow(sample_1920), 50), ]

## Step 3: Combine into one data frame
#sample_100 <- rbind(sample_50_1870, sample_50_1920)

# Step 4: Save to CSV
# write.csv(sample_100,"/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Session 2/sample_1870_1920_ner_people_100_rows.csv",
 #         row.names = FALSE)


# remember to label consistently and keep it simple so that it's easier for the model to recognise it

# Optional: reload to check
sample_100 <- read.csv("/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Session 2/Activity_4_Creating_a_Tailored_Spacy_Model/sample_1870_1920_ner_people_100_rows.csv")

# Step 2: Extract the text column (replace 'text' with the actual column name if different)
texts <- sample_100$text

# Step 3: Shiny App UI
ui <- fluidPage(
  tags$head(
    tags$script(HTML("
      document.addEventListener('mouseup', function() {
        var selectedText = window.getSelection().toString();
        Shiny.setInputValue('selected_text', selectedText);
      });
    "))
  ),
  titlePanel("NER Labeling App"),
  sidebarLayout(
    sidebarPanel(
      radioButtons("label_type", "Choose label:",
                   choices = c("PERSON")),
      actionButton("save_label", "Save Label"),
      actionButton("next_sentence", "Next Sentence"),
      hr(),
      downloadButton("download_data", "Save Labeled Data")
    ),
    mainPanel(
      h4("Text to Label:"),
      textOutput("current_text"),
      hr(),
      h4("Labeled Entities:"),
      tableOutput("annotations")
    )
  )
)

# Step 4: Shiny App Server
server <- function(input, output, session) {
  rv <- reactiveValues(
    index = 1,
    annotations = data.frame(
      text = character(),
      entity = character(),
      label = character(),
      stringsAsFactors = FALSE
    )
  )
  
  output$current_text <- renderText({
    texts[rv$index]
  })
  
  observeEvent(input$save_label, {
    if (!is.null(input$selected_text) && nchar(input$selected_text) > 0) {
      rv$annotations <- rbind(rv$annotations, data.frame(
        text = texts[rv$index],
        entity = input$selected_text,
        label = input$label_type,
        stringsAsFactors = FALSE
      ))
    } else {
      showNotification("Please highlight some text first!", type = "error")
    }
  })
  
  observeEvent(input$next_sentence, {
    if (rv$index < length(texts)) {
      rv$index <- rv$index + 1
    } else {
      showNotification("All sentences labeled!", type = "message")
    }
  })
  
  output$annotations <- renderTable({
    rv$annotations
  })
  
  output$download_data <- downloadHandler(
    filename = function() {
      paste0("ner_labels_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write.csv(rv$annotations, file, row.names = FALSE)
    }
  )
}

# Step 5: Run Shiny App
shinyApp(ui, server)

# --- Step 6: Convert labeled CSV to spaCy JSONL ---

# Load labeled CSV
annotations <- read.csv("/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Session 2/Activity_4_Creating_a_Tailored_Spacy_Model/output/annotations.csv", stringsAsFactors = FALSE)

# Function to convert CSV -> spaCy JSONL
convert_to_jsonl <- function(df, output_file = "ner_annotations.jsonl") {
  data_list <- lapply(split(df, df$text), function(group) {
    text <- unique(group$text)
    entities <- lapply(1:nrow(group), function(i) {
      entity <- group$entity[i]
      start <- regexpr(entity, text)[1]
      end <- start + nchar(entity)
      list(start, end, group$label[i])
    })
    list(text = text, entities = entities)
  })
  
  jsonlines <- sapply(data_list, toJSON, auto_unbox = TRUE)
  writeLines(jsonlines, output_file)
}

# Example: convert your labeled CSV
convert_to_jsonl(annotations)
