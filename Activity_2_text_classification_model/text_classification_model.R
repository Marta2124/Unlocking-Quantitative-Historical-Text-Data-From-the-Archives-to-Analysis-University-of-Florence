

library(shiny)
library(jsonlite)

# Load your CSV (replace with your actual file)
df <- read.csv("/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/sample_1870_1920_ner_people_100_rows_session_3.csv", stringsAsFactors = FALSE)

# The values we want to classify:
entities <- df$tailored_entities


# 2. SHINY APP FOR CLASSIFYING TAILORED ENTITIES

ui <- fluidPage(
  titlePanel("Social Group Classification of Tailored Entities"),
  
  sidebarLayout(
    sidebarPanel(
      h4("Choose the social group:"),
      radioButtons("label_type", "Label:",
                   choices = c("aristocracy", 
                               "clergy", 
                               "public officials", 
                               "royals",
                               "military",
                               "untitled", 
                               "other")),
      
      actionButton("save_label", "Save Label"),
      actionButton("next_entity", "Next Entity"),
      hr(),
      downloadButton("download_data", "Save Labeled Data")
    ),
    
    mainPanel(
      h4("Entity to Label:"),
      textOutput("current_entity", container = pre),
      hr(),
      h4("Labeled Entities:"),
      tableOutput("annotations")
    )
  )
)


server <- function(input, output, session) {
  
  rv <- reactiveValues(
    index = 1,
    annotations = data.frame(
      entity = character(),
      label = character(),
      stringsAsFactors = FALSE
    )
  )
  
  # Show current entity
  output$current_entity <- renderText({
    entities[rv$index]
  })
  
  # Save label
  observeEvent(input$save_label, {
    rv$annotations <- rbind(rv$annotations, data.frame(
      entity = entities[rv$index],
      label = input$label_type,
      stringsAsFactors = FALSE
    ))
  })
  
  # Move to next entity
  observeEvent(input$next_entity, {
    if (rv$index < length(entities)) {
      rv$index <- rv$index + 1
    } else {
      showNotification("All entities labeled!", type = "message")
    }
  })
  
  # Show table of annotations
  output$annotations <- renderTable({
    rv$annotations
  })
  
  # Save labeled CSV
  output$download_data <- downloadHandler(
    filename = function() {
      paste0("entity_labels_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write.csv(rv$annotations, file, row.names = FALSE)
    }
  )
}

# Run the Shiny app
shinyApp(ui, server)



# 3. CONVERT LABELED ENTITIES TO SPACY TEXTCAT JSONL


convert_textcat_jsonl <- function(df, 
                                  text_col = "entity", 
                                  label_col = "label",
                                  output_file = "textcat_entities.jsonl") {
  
  df[[label_col]] <- as.character(df[[label_col]])
  
  data_list <- lapply(1:nrow(df), function(i) {
    text <- df[[text_col]][i]
    label <- df[[label_col]][i]
    
    list(
      text = text,
      cats = setNames(list(1), label)
    )
  })
  
  jsonlines <- sapply(data_list, jsonlite::toJSON, auto_unbox = TRUE)
  writeLines(jsonlines, output_file)
  
  message("Saved JSONL to: ", output_file)
}


# 4. RUN AFTER LABELING

# Example:
annotations <- read.csv("/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/output/entity_labels_2025-11-20.csv", stringsAsFactors = FALSE)
convert_textcat_jsonl(annotations, output_file = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/output/textcat_entities_train.jsonl")
