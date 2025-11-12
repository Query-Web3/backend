version: "0.1"
database:
  dsn : "dev:123456@tcp(127.0.0.1:30306)/dev?charset=utf8mb4&parseTime=True&loc=Local"
  db  : "mysql"
  outPath :  "./gen"
  outFile :  ""
  withUnitTest  : true
  modelPkgName  : "dbgen"
  fieldNullable : true
  onlyModel : true
  tables :
    - "full_table"
    - "token_ext"
  fieldWithIndexTag : false
  fieldWithTypeTag  : false