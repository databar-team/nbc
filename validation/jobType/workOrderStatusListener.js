"use strict";

require("promise.allsettled").shim();

const logging = require("./logger");
const AWS = require("aws-sdk");
const { buildStatusMessage } = require("./utils/statusMessage");
const { KinesisClient } = require("./utils/kinesisClient");

function updateMaterialRequested(db, workOrderId, jobId) {
  const params = {
    TableName: process.env.WORKORDER_TABLE,
    Key: {
      workOrderId: workOrderId
    },
    UpdateExpression: "SET materialRequested=:jobId, validated=:n",
    ExpressionAttributeValues: {
      ":jobId": jobId,
      ":n": null
    }
  };
  return db.update(params).promise();
}

function updateMaterialRetrieval(db, workOrderId, jobId) {
  const params = {
    TableName: process.env.WORKORDER_TABLE,
    Key: {
      workOrderId: workOrderId
    },
    UpdateExpression: "SET materialRetrieval=:jobId",
    ExpressionAttributeValues: {
      ":jobId": jobId
    },
    ConditionExpression: "materialRequested = :jobId"
  };
  return db.update(params).promise();
}

function updateValidated(db, workOrderId, validated) {
  const params = {
    TableName: process.env.WORKORDER_TABLE,
    Key: {
      workOrderId: workOrderId
    },
    UpdateExpression: "SET validated=:val",
    ExpressionAttributeValues: {
      ":val": validated
    }
  };
  return db.update(params).promise();
}

function deleteWorkOrder(db, workOrderId) {
  const params = {
    TableName: process.env.WORKORDER_TABLE,
    Key: {
      workOrderId: workOrderId
    }
  };
  return db.delete(params).promise();
}

function isJobCompletedStatus(payload) {
  const jobTypes = [
    "JobScheduler",
    "JobSubmission",
    "cp-JobSubmission",
    "cp-jsCreate",
    "cp-jsRemove",
    "cp-jsTrigger",
    "DynamicStepFunction",
    "cp-Validation"
  ];
  return (
    ((payload.jobType === "cp-jsRemove" && payload.jobStatus === "Done") ||
      (jobTypes.includes(payload.jobType) && payload.jobStatus === "Error")) &&
    payload.workOrderId &&
    payload.workOrderId.length !== 0 &&
    payload.cpId &&
    payload.cpId.length !== 0
  );
}

function isRequestedStatus(payload) {
  return (
    payload.jobType === "WorkOrderBacklog" &&
    payload.statusMessage === "materialRequested" &&
    payload.jobId &&
    payload.jobId.length !== 0
  );
}

function isRetrievalStatus(payload) {
  return (
    payload.requester === "WorkOrderBacklog" &&
    payload.jobType === "Material" &&
    payload.jobStatus === "Done"
  );
}

function isValidationStatus(payload) {
  return (
    payload.jobType === "cp-Validation" &&
    payload.statusMessage === "materialsValid" &&
    ["Done", "Error"].indexOf(payload.jobStatus) > -1
  );
}

function logDbComplete(log, context, data) {
  log.info(`DB operation performed ${JSON.stringify(data)}`, context);
}

function logDbError(log, context, e) {
  log.error(`DB operation errored: ${e.message}`, context);
}

module.exports.handler = async (event, ctx) => {
  logging.resetContext(event, ctx);
  const dynamodb = new AWS.DynamoDB.DocumentClient();
  const log = logging.createLogger("workOrderStatusListener");
  try {
    log.info("begin lambda");
    const promises = [];
    for (const record of event.Records) {
      const payload = Buffer.from(record.kinesis.data, "base64").toString(
        "utf8"
      );
      let parsedPayload = undefined;
      try {
        parsedPayload = JSON.parse(payload);
        if (
          parsedPayload &&
          parsedPayload.workOrderId &&
          parsedPayload.workOrderId.length !== 0
        ) {
          let promise = undefined;
          const logContext = {
            WOId: parsedPayload.workOrderId,
            cpId: parsedPayload.cpId,
            jobId: parsedPayload.jobId
          };
          if (isValidationStatus(parsedPayload)) {
            promise = updateValidated(
              dynamodb,
              parsedPayload.workOrderId,
              parsedPayload.jobStatus === "Done"
            );
          } else if (isRetrievalStatus(parsedPayload)) {
            promise = updateMaterialRetrieval(
              dynamodb,
              parsedPayload.workOrderId,
              parsedPayload.jobId
            );
          } else if (isRequestedStatus(parsedPayload)) {
            promise = updateMaterialRequested(
              dynamodb,
              parsedPayload.workOrderId,
              parsedPayload.jobId
            );
          } else if (isJobCompletedStatus(parsedPayload)) {
            promise = deleteWorkOrder(dynamodb, parsedPayload.workOrderId);
            const client = new KinesisClient();
            const doneMessage = buildStatusMessage(
              parsedPayload,
              "Done",
              null,
              [],
              `Workorder Cleared from Backlog.`,
              null,
              "Translator",
              parsedPayload.cpId
            );
            log.info(doneMessage, logContext);
            promises.push(
              client.putRecord(parsedPayload.workOrderId, doneMessage)
            );
          }
          if (promise) {
            log.info(
              "Found relevant event: " + JSON.stringify(parsedPayload),
              logContext
            );
            const success = logDbComplete.bind(null, log, logContext);
            const error = logDbError.bind(null, log, logContext);
            promises.push(promise.then(success).catch(error));
          }
        }
      } catch (e) {
        const context = !parsedPayload
          ? {}
          : {
              WOId: parsedPayload.workOrderId,
              cpId: parsedPayload.cpId,
              jobId: parsedPayload.jobId
            };
        log.info(`Invalid record ${e.message}`, context);
      }
    }
    await Promise.allSettled(promises);
  } finally {
    log.info("end lambda");
  }
};
