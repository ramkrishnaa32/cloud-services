import boto3
from pyspark.sql import SparkSession
from lib import constants, utils

def main():
    # Initialize Spark Session
    spark = utils.initiating_spark_session("CSVtoParquetS3")

    # Reading CSV
    inputPath = f"{constants.S3_BUCKET}/athena-input/"
    students_df = spark.read \
                       .format('csv') \
                       .option("header", "true") \
                       .option("inferSchema", "true") \
                       .csv(inputPath)

    print(f"Read CSV from {inputPath}, records: {students_df.count()}")

    # Writing parquet
    outputPath = f"{constants.S3_BUCKET}/students/"
    students_df.write \
            .format('parquet') \
            .mode('overwrite') \
            .partitionBy('subject') \
            .save(outputPath)

    print(f"Written Parquet to {outputPath}")

if __name__ == "__main__":
    main()