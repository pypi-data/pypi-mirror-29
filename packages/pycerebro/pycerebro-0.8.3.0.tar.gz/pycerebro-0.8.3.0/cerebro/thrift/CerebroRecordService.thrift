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

namespace py cerebro.CerebroRecordService
namespace cpp recordservice
namespace java com.cerebro.recordservice.ext.thrift

include "RecordService.thrift"

// Requests access permissions for tables
struct TGetAccessPermissionsParams {
  // The users (or groups) to query access permissions for.
  1: required list<string> users_or_groups

  // Database to request permissions on
  2: required string database

  // Filter to apply to tables within the database
  3: optional string filter

  // User making the request, if not set, will use the connected user
  4: optional string requesting_user
}

enum TAccessPermissionLevel {
  ALL,
  READ,
  WRITE,
}

struct TAccessPermission {
  // The list of users/groups that have this access.
  1: required list<string> users_or_groups

  // For each user/group, the role that granted them this access. Note that it is
  // possible multiple roles granted them this, this returns just one of them.
  2: required list<string> roles

  3: required TAccessPermissionLevel level
  4: required bool has_grant
  5: required string database
  6: required string table

  // The projection that is accessible
  7: optional list<string> projection
}

struct TGetAccessPermissionsResult {
  1: required list<TAccessPermission> permissions
}

struct TExecDDLParams {
  1: required string ddl

  // User running the request
  2: optional string requesting_user

  // If set, the default db to use when executing the ddl statement. If not
  // set, the default db is 'default'
  3: optional string defaultdb
}

// Result for a DDL statement. Note that none of the fields need to be set for
// DDL that does not return a result (e.g. create table).
struct TExecDDLResult {
  // Set if the result is tabular. col_names is the headers of the table
  // and tabular_result contain the resutls row by row.
  1: optional list<string> col_names
  2: optional list<list<string>> tabular_result

  // Set if the result is not tabular and should just be output in fixed-width font.
  3: optional string formatted_result
}

struct TGetRoleProvenanceParams {
  // The user to query role provenance for
  1: optional string user
}

struct TRoleProvenance {
  // The name of the role
  1: required string role
  // The list of groups granting this role
  2: required list<string> provenance
}

struct TGetRoleProvenanceResult {
  // The requesting user
  1: required string user
  // The groups this user belongs to
  2: required list<string> groups
  // The roles and provenance this user belongs to
  3: required list<TRoleProvenance> roles

  // Return a list of groups which have access to datasets where this user is admin.
  4: optional set<string> groups_administered
}

struct TGetAuthenticatedUserResult {
  // Returns the authenticated user name
  1: required string user

  // If set, the credentials used to authenticate this user will expire in
  // this number of milliseconds.
  // If not set, the credentials will not expire.
  2: optional i64 expires_in_ms
}

struct TGetDatasetsParams {
  // The user running the request. Can be unset if this should just be the connected
  // user.
  1: optional string requesting_user

  // Returns datasets only in this database
  2: required list<string> databases

  // If set, only return datasets where the requesting user has these levels of
  // access.
  3: optional list<TAccessPermissionLevel> access_levels

  // If set, only match datasets which contain this string
  4: optional string filter

  // If true, also return the schema for the dataset
  5: optional bool with_schema

  // If set, the set of groups to return permissions for. This means that for each dataset
  // returned, the server will return the groups in this list that have some access to
  // those datasets.
  // If not set, the server does not return any group related access information.
  6: optional set<string> groups_to_return_permissions_for

  // Offset and count for pagination. The first `offset` datasets are skipped (after
  // matching filters) and at most `count` are returned. Not that this is not 
  // transactional, if datasets get added or removed while paging through them, results
  // will be inconsistent
  7: optional i32 offset
  8: optional i32 count

  // Returns the total matched datasets. This is expected to be used with pagination
  // to return the total count.
  9: optional bool return_total
}

struct TGetDatasetsResult {
  1: required list<RecordService.TTable> datasets

  // If 'groups_to_return_permissions_for' is specified in the request, for each 
  // dataset in 'datasets', the list of groups with some access to the dataset.
  // i.e. 'groups_with_access[i]' are the groups that have access to 'datasets[i]'
  3: optional list<set<string>> groups_with_access

  // For each dataset in `datasets`, true, if this user is admin on it.
  5: optional list<bool> is_admin

  // List of datasets that failed to load. The server returns as many of the fields
  // as possible, but some may be unset as they could not load.
  // This list is always disjoint with `datasets.
  2: optional list<RecordService.TTable> failed_datasets

  // Map of databases that failed to load to the error.
  4: optional map<string, RecordService.TRecordServiceException> failed_databases

  // Set if `return_total` was set in the request.
  6: optional i32 total_count
}

// This currently just contains the fields to make this compatible with hive.
struct TUdf {
  1: required string database
  2: required string fn_signature
  3: required string class_name

  // The list of resources required to run this UDF. This can be for example, the list
  // of jars that need to be added that are required for the UDF.
  4: optional list<string> resource_uris
}

struct TGetUdfsParams {
  // List of databases to return UDFs for. If not set, returns it for all databases.
  1: optional list<string> databases
}

struct TGetUdfsResult {
  1: list<TUdf> udfs
}

// Cerebro extensions to the RecordServicePlanner API
service CerebroRecordServicePlanner extends RecordService.RecordServicePlanner {
  // Returns the access permissions for tables.
  TGetAccessPermissionsResult GetAccessPermissions(1: TGetAccessPermissionsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns role provenance for a user
  TGetRoleProvenanceResult GetRoleProvenance(1: TGetRoleProvenanceParams params)
    throws(1:RecordService.TRecordServiceException ex);

  // Executes a ddl command against the server, returning the results (if it produces
  // results).
  list<string> ExecuteDDL(1:TExecDDLParams ddl)
      throws(1:RecordService.TRecordServiceException ex);

  TExecDDLResult ExecuteDDL2(1:TExecDDLParams ddl)
      throws(1:RecordService.TRecordServiceException ex);

  // This will register aliases for 'user'. When the 'user' access path, it will
  // resolve to 'table'. If view is non-empty, a view will created for the user and
  // whenever the user access 'path' or 'table', it will resolve to the view.
  string RegisterAlias(1:string user, 2:string table, 3:string path, 4:string view)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the authenticated user from the user's token.
  TGetAuthenticatedUserResult AuthenticatedUser(1:string token)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the datasets. This is similar to RecordServicePlanner.GetTables() but
  // version2, which matches more advanced usage patterns better.
  TGetDatasetsResult GetDatasets(1:TGetDatasetsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the UDFs that have been registered. Note that this does not include
  // builtins, only functions explicilty registered by the user.
  TGetUdfsResult GetUdfs(1:TGetUdfsParams params)
      throws(1:RecordService.TRecordServiceException ex);
}
