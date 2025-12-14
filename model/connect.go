package model

import (
	"fmt"
	"os"

	"github.com/Query-Web3/backend/model/dbgen"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var DB *gorm.DB

// initialize db connection
func InitializeDB() {
	dsn := os.Getenv("DB_DSN")
	if dsn == "" {
		dsn = "dev:123456@tcp(127.0.0.1:30306)/dev?charset=utf8mb4&parseTime=True&loc=Local"
	}

	var err error
	DB, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic(fmt.Errorf("open mysql %q fail: %w", dsn, err))
	}

	CreateTableIfNotExists(DB, &dbgen.TokenExt{})
}

// CreateTableIfNotExists 表不存在则创建
func CreateTableIfNotExists(db *gorm.DB, model interface{}) error {
	if !CheckTableExists(db, model) {
		err := db.AutoMigrate(model)
		if err != nil {
			return err
		}
		return nil
	}
	return nil
}

// CheckTableExists 判断指定模型对应的表是否存在
func CheckTableExists(db *gorm.DB, model interface{}) bool {
	// 获取当前数据库的Migrator（适配不同数据库）
	migrator := db.Migrator()
	// 判断表是否存在
	return migrator.HasTable(model)
}
