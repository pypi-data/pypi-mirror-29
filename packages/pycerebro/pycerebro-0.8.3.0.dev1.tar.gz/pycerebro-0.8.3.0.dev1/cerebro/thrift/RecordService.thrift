// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

namespace py cerebro.RecordService
namespace cpp recordservice
namespace java com.cloudera.recordservice.thrift

//
// This file contains the service definition for the RecordService which consists
// of two thrift services: RecordServicePlanner and RecordServiceWorker.
//

// Version used to negotiate feature support between the server and client. Both
// clients and servers need to maintain backwards compatibility.
typedef string TProtocolVersion

// 128-bit GUID.
struct TUniqueId {
  1: required i64 hi
  2: required i64 lo
}

// Network address which specifies the machine, typically used to schedule where
// tasks run.
struct TNetworkAddress {
  1: required string hostname
  2: required i32 port
}

struct TServerVersion {
  1: optional string version
  2: optional string build_time
  3: optional string build_hash
}

// Types support by the RecordService.
enum TTypeId {
  // Boolean, true or false
  BOOLEAN,

  // 1-byte (signed) integer.
  TINYINT,

  // 2-byte (signed) integer.
  SMALLINT,

  // 4-byte (signed) integer.
  INT,

  // 8-byte (signed) integer.
  BIGINT,

  // ieee floating point number
  FLOAT,

  // ieee double precision floating point number
  DOUBLE,

  // Variable length byte array.
  STRING,

  // Variable length byte array with a restricted maximum length.
  VARCHAR,

  // Fixed length byte array.
  CHAR,

  // Fixed point decimal value.
  DECIMAL,

  // Timestamp with nanosecond precision.
  TIMESTAMP_NANOS,
}

// Type specification, containing the enum and any additional parameters the type
// may need.
struct TColumnType {
  1: required TTypeId type_id

  // Only set if id == DECIMAL
  2: optional i32 precision
  3: optional i32 scale

  // Only set if id == VARCHAR or CHAR
  4: optional i32 len
}

// A description for a column in the schema.
struct TColumnDesc {
  1: required TColumnType type
  2: required string name

  // If true, this column is a partitioning column
  3: optional bool is_partitioning_col

  // If true, this column is not accessible to this user
  4: optional bool hidden

  5: optional string comment
}

// Representation of a RecordServiceSchema.
struct TSchema {
  1: required list<TColumnDesc> cols
  2: required bool is_count_star = false
}

// Record serialization formats.
enum TRecordFormat {
  // Serialized columnar data. Each column is a contiguous byte buffer to minimize
  // serialization costs.
  // The serialization is optimized for little-endian machines:
  //   BOOLEAN - Encoded as a single byte.
  //   TINYINT, SMALLINT, INT, BIGINT - Encoded as little endian,
  //        2's complement in the size of this type.
  //   FLOAT, DOUBLE - Encoded as IEEE
  //   STRING, VCHAR - Encoded as a INT followed by the byte data.
  //   CHAR - The byte data.
  //   DECIMAL - Encoded as the unscaled 2's complement little-endian value.
  //   TIMESTAMP_NANOS - Encoded as a BIGINT (8 bytes) millis since epoch followed
  //        by INT(4 byte) nanoseconds offset.
  // Serialized data excludes NULLs. Values are serialized back to back.
  Columnar,

  // Similar to `Columnar` but optimized to allow cheaper deserialization from numpy.
  // The differences are:
  // 1. Values are dense. NULLs are included in the serialized data. The value
  //    for those bytes is undefined. For example if that data was [1,NULL,2],
  //    with Columnar, the serialized data is just [1,2] for a total of 2 bytes.
  //    With ColumnarNumPy it is [1, undefined byte, 2] for a total fo 3 bytes.
  // 2. String serialization is different. In this version, all string lengths
  //    are encoded at the start of the data buffer, followed by all the
  //    string data back to back. The lengths are also dense. For example,
  //    if the data was ['hello', NULL, 'world']:
  //       Columnar: 5hello,4,world
  //       ColumnarNumPy: 5(undefined 4 bytes)4helloworld
  ColumnarNumPy,
}

struct TColumnData {
  // One byte for each value.
  1: required binary is_null
  2: required binary data
}

// List of column data for the Columnar record format. This is 1:1 with the
// schema. i.e. cols[0] is the data for schema.cols[0].
struct TColumnarRecords {
  1: required list<TColumnData> cols
}

// The type of request specified by the client. Clients can specify read
// requests in multiple ways.
enum TRequestType {
  Sql,
  Path,
}

struct TPathRequest {
  // The URI to read.
  1: required string path

  // Optional query (for predicate push down). The query must be valid SQL with
  // __PATH__ used instead of the table.
  2: optional string query

  // The schema for the files at 'path'. The client can set this if it wants the
  // server to interpret the data with this schema, otherwise the server will infer
  // the schema
  3: optional TSchema schema

  // Only valid if schema is set. Specifies the field delimiter to use for the files
  // in 'path'. Only applicable to some file formats.
  4: optional byte field_delimiter
}

enum TLoggingLevel {
  // The OFF turns off all logging.
  OFF,

  // The ALL has the lowest possible rank and is intended to turn on all logging.
  ALL,

  // The FATAL level designates very severe error events that will presumably lead the
  // application to abort.
  FATAL,

  // The ERROR level designates error events that might still allow the application
  // to continue running.
  ERROR,

  // The WARN level designates potentially harm
  WARN,

  // The INFO level designates informational messages that highlight the progress of the
  // application at coarse-grained level.
  INFO,

  // The DEBUG Level designates fine-grained informational events that are most useful
  // to debug an application.
  DEBUG,

  // The TRACE Level designates finer-grained informational events than the DEBUG
  TRACE,
}

// Log messages return by the RPCs. Non-continuable errors are returned via
// exceptions in the RPCs. These messages contain either warnings or additional
// diagnostics.
struct TLogMessage {
  // User facing message.
  1: required string message

  // Additional detail (e.g. stack trace, object state)
  2: optional string detail

  // Level corresponding to this message.
  3: required TLoggingLevel level

  // The number of times similar messages have occurred. It is up to the service to
  // decide what counts as a duplicate.
  4: required i32 count = 1
}

struct TRequestOptions {
  // If true, fail tasks if an corrupt record is encountered, otherwise, those records
  // are skipped (and warning returned).
  1: optional bool abort_on_corrupt_record = false
}

struct TPlanRequestParams {
  // The version of the client
  1: required TProtocolVersion client_version = "1.0"

  2: required TRequestType request_type

  // Optional arguments to the plan request.
  3: optional TRequestOptions options

  // Only one of the below is set depending on request type
  4: optional string sql_stmt
  5: optional TPathRequest path

  // Username for the connecting user. On a secure cluster, this is ignored and
  // instead the authenticated user used.
  6: optional string user

  // A hint for the maximum number of tasks this request will generate. If not
  // set, the server will pick a default. If this value is smaller than the
  // number ofnatural task splits (e.g. HDFS blocks), the server will combine tasks.
  // The combined tasks will have multiple blocks, for example.
  7: optional i32 max_tasks

  // If set, this is the user to run the request as. Note that this can be different
  // than the connected user for proxy access. For example, the connected user can
  // be the userid of the server application, and the requesting user can be the
  // end user.
  8: optional string requesting_user

  // If true, generate only a single task per recordservice worker.
  9: optional bool single_task_per_worker

  // If true, this will return tasks where each tasks contains data that is only
  // for a single partition. It is possible to have many tasks for the same partition
  // (i.e. if the partition is big and should split) but no task will contain data
  // that spans partitions.
  10: optional bool preserve_partitions
}

struct TTask {
  // The list of hosts where this task can run locally.
  1: required list<TNetworkAddress> local_hosts

  // An opaque blob that is produced by the RecordServicePlanner and passed to
  // the RecordServiceWorker.
  2: required binary task

  // Unique ID generated by the planner. Used only for diagnostics (e.g. server
  // log messages).
  3: required TUniqueId task_id

  // If true, the records returned by this task are ordered, meaning in the case
  // of failures, the client can continue from the current record. If false, the
  // client needs to recompute from the beginning.
  4: required bool results_ordered

  // A unit-less estimate of the computation required to execute the task. This
  // should only be used to compare task sizes returned from a single PlanRequest()
  // to give an estimate of how large tasks are. Within a single request if the
  // size of one task is 3x bigger than another task, we expect it to take 3 times
  // as long.
  5: required i64 task_size = 1

  // Only set if preserve_partitions is set to true in TPlanRequestParams, in which
  // case it contains the partitions values for this task as formatted in storage.
  // e.g. year=2001/month=2/day=1. This does *not* include the base dir.
  6: optional string partition_path
}

struct TPlanRequestResult {
  1: required list<TTask> tasks
  2: required TSchema schema

  // Unique ID generated by the planner. Used only for diagnostics (e.g. server
  // log messages).
  3: required TUniqueId request_id

  // The list of all hosts running workers.
  4: required list<TNetworkAddress> hosts

  // List of warnings generated during planning the request. These do not have
  // any impact on correctness.
  5: required list<TLogMessage> warnings

  // The wire formats the server supports when returning records. If unset,
  // the server only supports the default, TRecordFormat.Columnar.
  6: optional set<TRecordFormat> supported_result_formats
}

struct TGetSchemaResult {
  1: required TSchema schema
  2: required list<TLogMessage> warnings
}

struct TExecTaskParams {
  // This is produced by the RecordServicePlanner and must be passed to the worker
  // unmodified.
  1: required binary task

  // Logging level done by the service the service Service level logging for this task.
  2: optional TLoggingLevel logging_level

  // Maximum number of records that can be returned per fetch. The server can return
  // fewer. If unset, service picks default.
  3: optional i32 fetch_size

  // The format of the records to return. Only the corresponding field is set
  // in TFetchResult. If unset, the server picks the default.
  4: optional TRecordFormat record_format

  // The memory limit for this task in bytes. If unset, the service manages it
  // on its own.
  5: optional i64 mem_limit

  // The offset to start returning records. This is only valid for tasks where
  // results_ordered is true. This can be used to improve performance when there
  // are failures. The client can run the task against another daemon with the
  // offset set to the number of records already seen.
  // The offset is the record ordinal, that is, the first offset records are not
  // returned to the client.
  6: optional i64 offset

  // The maximum number of records to return for this task.
  7: optional i64 limit
}

struct TExecTaskResult {
  1: required TUniqueId handle

  // Schema of the records returned from Fetch().
  2: required TSchema schema
}

struct TFetchParams {
  1: required TUniqueId handle
}

struct TFetchResult {
  // If true, all records for this task have been returned. It is still valid to
  // continue to fetch, but they will return 0 records.
  1: required bool done

  // The approximate completion progress [0, 1]
  2: required double task_progress

  // The number of records in this batch.
  3: required i32 num_records

  // The encoding format.
  4: required TRecordFormat record_format

  // TRecordFormat.Columnar
  5: optional TColumnarRecords columnar_records
}

struct TStats {
  // [0 - 1]
  1: required double task_progress

  // The number of records read before filtering.
  2: required i64 num_records_read

  // The number of records returned to the client.
  3: required i64 num_records_returned

  // The number of records that were skipped (due to data errors).
  4: required i64 num_records_skipped

  // Time spent in the record service serializing returned results.
  5: required i64 serialize_time_ms

  // Time spent in the client, as measured by the server. This includes
  // time in the data exchange as well as time the client spent working.
  6: required i64 client_time_ms

  //
  // HDFS specific counters
  //

  // Time spent in decompression.
  7: optional i64 decompress_time_ms

  // Bytes read from HDFS
  8: optional i64 bytes_read

  // Bytes read from the local data node.
  9: optional i64 bytes_read_local

  // Throughput of reading the raw bytes from HDFS, in bytes per second
  10: optional double hdfs_throughput
}

struct TTaskStatus {
  1: required TStats stats

  // Errors due to invalid data
  2: required list<TLogMessage> data_errors

  // Warnings encountered when running the task. These should have no impact
  // on correctness.
  3: required list<TLogMessage> warnings
}

enum TErrorCode {
  // The request is invalid or unsupported by the Planner service.
  INVALID_REQUEST,

  // The handle is invalid or closed.
  INVALID_HANDLE,

  // The task is malformed.
  INVALID_TASK,

  // Service is busy and not unable to process the request. Try later.
  SERVICE_BUSY,

  // The service ran out of memory processing the task.
  OUT_OF_MEMORY,

  // The task was cancelled.
  CANCELLED,

  // Internal error in the service.
  INTERNAL_ERROR,

  // The server closed this connection and any active requests due to a timeout.
  // Clients will need to reconnect.
  CONNECTION_TIMED_OUT,

  // Error authenticating.
  AUTHENTICATION_ERROR,
}

exception TRecordServiceException {
  1: required TErrorCode code

  // The error message, intended for the client of the RecordService.
  2: required string message

  // The detailed error, intended for troubleshooting of the RecordService.
  3: optional string detail
}

// TODO: argument this response with the description, units, etc.
struct TMetricResponse {
  // Set if the metric is defined. This is the human readable string of the value.
  1: optional string metric_string
}

// Serialized delegation token.
struct TDelegationToken {
  // Identifier/password for authentication. Do not log the password.
  // Identifier is opaque but can be logged.
  1: required string identifier
  2: required string password

  // Entire serialized token for cancel/renew. Do not log this. It contains
  // the password.
  3: required binary token
}

typedef list<string> TDatabaseName

struct TDatabase {
  1: TDatabaseName name
}

struct TTable {
  1: required string name
  9: optional TDatabaseName db

  2: optional string owner
  3: optional TSchema schema

  // Description attached to table
  4: optional string description

  // Time this dataset was created, in unix time
  5: optional i64 created_time_unix_epoch

  // Time ddl was executed on this dataset.
  7: optional i64 last_ddl_time_unix_epoch

  // Information string on the primary storage system for this table. This is
  // not interpreted and just presented to the user. Examples are "hdfs', 'kinesis'.
  6: optional string primary_storage

  // If this is an external view, the view string for this table
  8: optional string view_string

  // If set, the path in the storage system where this table is located.
  10: optional string location

  // If set, this dataset is invalid for some reason and could not be fully loaded.
  11: optional string loading_error_msg
}

struct TPartition {
  1: required list<string> partition_values
}

// Returns the databases in the catalog
struct TGetDatabasesParams {
  1: optional string filter
  2: optional string requesting_user
}

struct TGetDatabasesResult {
  1: required list<TDatabase> databases
}

// Returns the tables in the catalog
struct TGetTablesParams {
  1: required TDatabaseName database

  // Only one of name or filter can be set.
  // - If name is set, returns the details of this dataset.
  // - If filter is set, returns basic metadata about all the datasets with
  //   name that match filter (i.e. matches with SQL 'LIKE' semantics)
  2: optional string name
  3: optional string filter

  4: optional string requesting_user
}

struct TGetTablesResult {
  1: required list<TTable> tables
}

struct TGetPartitionsParams {
  1: required TDatabaseName database
  2: required string table
  3: optional string requesting_user
}

struct TGetPartitionsResult {
  1: optional list<TPartition> partitions
}

// This service is responsible for planning requests.
service RecordServicePlanner {
  // Returns the version of the server. Throws exception if there are too
  // many connections for the planner.
  TProtocolVersion GetProtocolVersion() throws(1:TRecordServiceException ex)

  // Returns the version information of the server.
  TServerVersion GetServerVersion() throws(1:TRecordServiceException ex)

  // Sets the name of the application.
  void SetApplication(1:string app) throws(1:TRecordServiceException ex)

  // Plans the request. This generates the tasks and the list of machines
  // that each task can run on.
  TPlanRequestResult PlanRequest(1:TPlanRequestParams params)
      throws(1:TRecordServiceException ex);

  // Returns the schema for a plan request.
  TGetSchemaResult GetSchema(1:TPlanRequestParams params)
      throws(1:TRecordServiceException ex);

  // Queries the server for a metric by key.
  TMetricResponse GetMetric(1:string key)

  // Returns the databases in the catalog.
  TGetDatabasesResult GetDatabases(1:TGetDatabasesParams params)
      throws(1:TRecordServiceException ex);

  // Returns the tables in this database.
  TGetTablesResult GetTables(1:TGetTablesParams params)
      throws(1:TRecordServiceException ex);

  // Returns the partitions in this table.
  TGetPartitionsResult GetPartitions(1:TGetPartitionsParams params)
      throws(1:TRecordServiceException ex);

  // Gets a delegation for user. This creates a token if one does not already exist
  // for this user. renewer, if set, is the user than can renew this token (in addition
  // to the 'user').
  // Returns an opaque delegation token which can be subsequently used to authenticate
  // with the RecordServicePlanner and RecordServiceWorker services.
  TDelegationToken GetDelegationToken(1:string user, 2:string renewer)
      throws(1:TRecordServiceException ex);

  // Cancels the delegation token.
  void CancelDelegationToken(1:TDelegationToken delegation_token)
      throws(1:TRecordServiceException ex);

  // Renews the delegation token. Duration set by server configs.
  void RenewDelegationToken(1:TDelegationToken delegation_token)
      throws(1:TRecordServiceException ex);
}

// This service is responsible for executing tasks generated by the RecordServicePlanner
service RecordServiceWorker {
  // Returns the version of the server. Throws exception if there are too
  // many connections for the worker.
  TProtocolVersion GetProtocolVersion() throws(1:TRecordServiceException ex)

  // Returns the version information of the server.
  TServerVersion GetServerVersion() throws(1:TRecordServiceException ex)

  // Sets the name of the application.
  void SetApplication(1:string app) throws(1:TRecordServiceException ex)

  // Begin execution of the task in params. This is asynchronous.
  TExecTaskResult ExecTask(1:TExecTaskParams params)
      throws(1:TRecordServiceException ex);

  // Returns the next batch of records
  TFetchResult Fetch(1:TFetchParams params)
      throws(1:TRecordServiceException ex);

  // Closes the task specified by handle. If the task is still running, it is
  // cancelled. The handle is no longer valid after this call.
  void CloseTask(1:TUniqueId handle);

  // Returns status for the task specified by handle. This can be called for tasks that
  // are not yet closed (including tasks in flight).
  TTaskStatus GetTaskStatus(1:TUniqueId handle)
      throws(1:TRecordServiceException ex);

  // Queries the server for a metric by key.
  TMetricResponse GetMetric(1:string key)
}

