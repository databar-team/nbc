// To run:
// AWS_PROFILE=saml node readFromKinesis.js

// const AWS = require("aws-sdk");
const AWS = require('/usr/local/lib/node_modules/aws-sdk');

AWS.config.update({ region: process.env.AWS_REGION || "us-east-1" });
const kinesis = new AWS.Kinesis();
function catcher(err) {
  console.log("ERRROR")
  console.dir(err)
}
const allRecords = [];
const iteratedShards = [];
const fs = require('fs')
function getRecords(iter) {
  if(iter && !(iter in iteratedShards)) {
    iteratedShards.push(iter);
    return kinesis.getRecords({
      ShardIterator: iter,
    }).promise().then(records => {
      records.Records.forEach(record => {
        const data = Buffer.from(record.Data, "base64").toString();
        try {
          const r = JSON.parse(data);
          allRecords.push(r);
          console.log("\n==========================================\n");
          console.log(JSON.stringify(r, null, 2));
          fs.appendFile('status.txt', JSON.stringify(r, null, 2), (err) =>{
            if(err) throw err;
            // console.log('File has been written successfully')
          })
        } catch(e) {
          console.log("Failed to parse: ", data);
          fs.appendFile('status.txt', data, (err) =>{
            if(err) throw err;
            console.log('Error has been made')
          })
        }
      });
      if(records.MillisBehindLatest > 0) {
        return getRecords(records.NextShardIterator)
      }
    });
  }
}

// const StreamName = "cp-pr-44-bf5c7-validation";
const StreamName = "cp-status-pr-44-bf5c7";


async function run() {
  return await kinesis.describeStream({
    StreamName
  }).promise().then(async shards => {
    shards.StreamDescription.Shards.forEach(async shard => {
      const seq = shard.SequenceNumberRange.StartingSequenceNumber;
      // console.dir(shard)
      return await kinesis.getShardIterator({
        StreamName,
        ShardId: shard.ShardId,
        // ShardIteratorType: "LATEST",
        // ShardIteratorType: "TRIM_HORIZON",
        ShardIteratorType: "AT_TIMESTAMP",
        Timestamp: 1587329400
        // ShardIteratorType: "AFTER_SEQUENCE_NUMBER",
        // StartingSequenceNumber: seq
      }).promise().then(iter => getRecords(iter.ShardIterator)).catch(catcher);
    });
  }).catch(catcher);
}
run();
