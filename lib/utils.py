from pyspark.sql import SparkSession

def initiating_spark_session(appName):
    spark = SparkSession.builder \
                        .appName(appName) \
                        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.11.1026") \
                        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
                        .getOrCreate()

    return spark