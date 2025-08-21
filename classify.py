from processor_regex import classify_with_regex
from processor_bert import classify_with_bert
from processor_llm import classify_with_llm
import pandas as pd

def classify(logs):
    labels = []
    for source, log_msg in logs:
        label = classify_log(source, log_msg)
        labels.append(label)
    return labels


def classify_log(source, log_message):
    if source == 'LegacyCRM':
        label = classify_with_llm(log_message)
    else:
        label = classify_with_regex(log_message)
        if label is None:
            label = classify_with_bert(log_message)
    return label


def classify_csv(input_file):
    df = pd.read_csv(input_file)
    
    df.columns = df.columns.str.strip()
    
    df["log_message"] = df["log_message"].str.strip().str.strip('"').str.strip("'")
    df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

    output_file = "resources/output.csv"
    df.to_csv(output_file, index=False)



if __name__ == "__main__":
    classify_csv("resources/test.csv")

    logs = [
    #    ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
        ("BillingSystem", "User User12345 logged in."),
      #  ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
       # ("AnalyticsEngine", "Backup completed successfully."),
        #("ModernHR", "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1"" Return code: 200 len: 1893 time: 0.2676129"),
        #("ModernHR", "Admin access escalation detected for user 9429"),
        #("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support"),
        #("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax"),
        #("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaign'"),
        #("LegacyCRM", " The 'ReportGenerator' module will be retired in version 4"),
    ]
    classified_logs = classify(logs)
    print(classified_logs)

    