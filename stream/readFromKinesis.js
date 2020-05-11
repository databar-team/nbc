// To run (use command AWS_PROFILE=nbc node readFromKinesis.js):

const AWS = require ('aws-sdk')  //aws library
const fs = require('fs')      

AWS.config.update({region:process.env.AWS_REGION || "us-east-1"})  //Set region

const kinesis = new AWS.Kinesis() //Make new constructor for kinesis

function catcher(err){
    console.log("ERROR")
    console.dir(err)
}

const allRecords = [];
const iteratedShards = [];

function getRecords(iter){
    if(iter && !(iter in iteratedShards)){
        iteratedShards.push(iter)
        return kinesis.getRecords({
            ShardIterator: iter,
        }).promise().then(records =>{
            records.Records.forEach(record => {
                const data = Buffer.from(record.Data, "base64").toString()
                console.log(data)
                try{
                    console.log("test")
                    const r = JSON.parse(data)
                    allRecords.push(r)
                    fs.appendFile("nekifajl.txt", JSON.stringify(r,null,2), (err)=>{
                        if(err) throw err
                    })
                }catch(e){
                    fs.appendFile("nekifajl.txt", JSON.stringify(data), (err)=>{
                        if(err) throw err
                    })
                }
            });
            if(records.MillisBehindLatest > 0) {
                return getRecords(records.NextShardIterator)
            }
        })
        
    }
}

const StreamName = "Foo";  //Try diferent stream names for diferent results


async function run() {
  return await kinesis.describeStream({
    StreamName
  }).promise().then(async shards => {
    shards.StreamDescription.Shards.forEach(async shard => {
      return await kinesis.getShardIterator({
        StreamName,
        ShardId: shard.ShardId,
        ShardIteratorType: "AT_TIMESTAMP",
        Timestamp: 1587329400
      }).promise().then(iter => getRecords(iter.ShardIterator)).catch(catcher);
    });
  }).catch(catcher);
  
}
run();