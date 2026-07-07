#renv::install("ellmer")
library(ellmer)
chat <- chat_groq(model="openai/gpt-oss-120b")
chat$chat("Tell me three jokes about statisticians")

protocol <- content_pdf_file("../POLYFIX-DCM Protocol v2.0-30May22 FINAL clean.pdf")
protocol <- readLines("../POLYFIX DCM Protocol 2.0-30May22 FINAL clean.txt")
prompt <- " Extract and write the Administrative Information section for a
    comprehensive Statistical Analysis Plan (SAP) based on the clinical trial protocol.


    Instructions:

    Please identify and clearly present the following administrative elements based on the content of the protocol:

    Full trial title

    Trial registration details (registry name, registration number, and registration date). This will be either ISRCTN or ClinicalTrials.gov. Do not include details of other registrations.

    Protocol number and version (including version date)

    Names, and affiliations of:

    Chief investigator / Principal investigator
    Trial statistician(s)

    Do not include addresses for investigators or statisticians. Examples of sufficient infomration would be:

    Chief Investigator: Dr. Ben Carter, Kings College London Clinical Trials Unit, Institute of Psychiatry, Psychology and Neuroscience, King's College London

    Write this section in a clear and detailed format suitable for inclusion in the SAP.
    Use paragraphs or bullet points as appropriate.
    Focus only on administrative and contributor-related information—do not extract study objectives,
    endpoints, methodology, or statistical methods in this prompt.
"
chat <- chat_groq(model="openai/gpt-oss-20b", prompt)
chat$chat(protocol)


chat <- chat_google_gemini( prompt)
chat$chat(protocol)
