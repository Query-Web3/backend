package model

import (
	"fmt"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var DB *gorm.DB

// initialize db connection
func InitializeDB() {
	dsn := "dev:123456@tcp(127.0.0.1:31006)/dev?charset=utf8mb4&parseTime=True&loc=Local"
	var err error
	DB, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic(fmt.Errorf("open mysql %q fail: %w", dsn, err))
	}
}
