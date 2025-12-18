package main

import (
	"os"
	"path/filepath"
	"testing"
)

// TestIsFileExists 测试文件存在性检查函数
func TestIsFileExists(t *testing.T) {
	// 测试不存在的文件
	exists := IsFileExists("/nonexistent/file/path/that/should/not/exist")
	if exists {
		t.Error("不存在的文件应该返回false")
	}

	// 测试存在的文件（使用当前目录的go.mod文件）
	goModPath := filepath.Join("../", "go.mod")
	exists = IsFileExists(goModPath)
	if !exists {
		t.Errorf("go.mod文件应该存在，路径: %s", goModPath)
	}

	// 测试当前目录
	currentDir, err := os.Getwd()
	if err == nil {
		exists = IsFileExists(currentDir)
		// 目录存在时，IsFileExists可能返回true或false，取决于实现
		// 这里我们只验证函数不会panic
		_ = exists
	}

	// 测试空字符串
	exists = IsFileExists("")
	// 空字符串通常会导致错误，应该返回false
	if exists {
		t.Error("空字符串路径应该返回false")
	}
}

// TestIsFileExistsWithTempFile 使用临时文件测试
func TestIsFileExistsWithTempFile(t *testing.T) {
	// 创建临时文件
	tmpFile, err := os.CreateTemp("", "test_file_*.txt")
	if err != nil {
		t.Fatalf("创建临时文件失败: %v", err)
	}
	defer os.Remove(tmpFile.Name()) // 清理
	tmpFile.Close()

	// 测试临时文件存在
	exists := IsFileExists(tmpFile.Name())
	if !exists {
		t.Errorf("临时文件应该存在: %s", tmpFile.Name())
	}

	// 删除文件后测试
	os.Remove(tmpFile.Name())
	exists = IsFileExists(tmpFile.Name())
	if exists {
		t.Errorf("已删除的文件应该返回false: %s", tmpFile.Name())
	}
}

