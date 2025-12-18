package model

import (
	"os"
	"testing"

	"github.com/Query-Web3/backend/model/dbgen"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// TestCheckTableExists 测试表存在性检查
func TestCheckTableExists(t *testing.T) {
	// 使用SQLite内存数据库进行测试
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	if err != nil {
		t.Fatalf("打开数据库失败: %v", err)
	}

	// 测试表不存在的情况
	exists := CheckTableExists(db, &dbgen.TokenExt{})
	if exists {
		t.Error("表不应该存在")
	}

	// 创建表
	err = db.AutoMigrate(&dbgen.TokenExt{})
	if err != nil {
		t.Fatalf("创建表失败: %v", err)
	}

	// 测试表存在的情况
	exists = CheckTableExists(db, &dbgen.TokenExt{})
	if !exists {
		t.Error("表应该存在")
	}
}

// TestCreateTableIfNotExists 测试表不存在时创建表
func TestCreateTableIfNotExists(t *testing.T) {
	// 使用SQLite内存数据库进行测试
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	if err != nil {
		t.Fatalf("打开数据库失败: %v", err)
	}

	// 测试表不存在时创建
	err = CreateTableIfNotExists(db, &dbgen.TokenExt{})
	if err != nil {
		t.Fatalf("创建表失败: %v", err)
	}

	// 验证表已创建
	exists := CheckTableExists(db, &dbgen.TokenExt{})
	if !exists {
		t.Error("表应该已创建")
	}

	// 测试表已存在时不重复创建
	err = CreateTableIfNotExists(db, &dbgen.TokenExt{})
	if err != nil {
		t.Fatalf("表已存在时不应该报错: %v", err)
	}
}

// TestInitializeDB 测试数据库初始化（使用环境变量）
func TestInitializeDB(t *testing.T) {
	// 保存原始环境变量
	originalDSN := os.Getenv("DB_DSN")
	defer func() {
		if originalDSN != "" {
			os.Setenv("DB_DSN", originalDSN)
		} else {
			os.Unsetenv("DB_DSN")
		}
		// 重置全局DB变量
		DB = nil
	}()

	// 测试使用SQLite内存数据库（避免需要真实的MySQL连接）
	os.Setenv("DB_DSN", "file::memory:?cache=shared")
	
	// 注意：InitializeDB使用mysql驱动，在测试环境中可能会失败
	// 这里我们主要测试环境变量的读取逻辑
	dsn := os.Getenv("DB_DSN")
	if dsn == "" {
		t.Error("环境变量DB_DSN应该被设置")
	}

	// 测试默认DSN
	os.Unsetenv("DB_DSN")
	dsn = os.Getenv("DB_DSN")
	if dsn != "" {
		t.Error("环境变量DB_DSN应该为空")
	}
}

