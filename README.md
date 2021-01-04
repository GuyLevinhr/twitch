# twitch

the project's target:

  Research and follow top users on the twitch site.

Code:

  Regularly switch to the currently leading 1,000 live streams - and get parameters like the user, the amount of live viewers and more.
  For each stream add information about the game name and more.
    Send the records to kinesis.

In the AWS environment:

  Using the Kinesis firehouse to convert records from Json to parquet and save to S3 storage.

  And through Athena conduct research and find the top users, the growth rate of their live viewers and find the most popular games.
