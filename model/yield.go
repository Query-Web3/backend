package model

import (
	"encoding/json"

	"github.com/Query-Web3/backend/model/dbgen"
)

func Yields(page, size int) (string, int64, error) {
	if page < 1 {
		page = 1
	}
	if size < 1 {
		size = 10
	}
	list := []dbgen.FullTable{}
	result := DB.Limit(size).Offset((page - 1) * size).Find(&list)
	if result.Error != nil {
		return "", 0, result.Error
	}

	var count int64
	result = DB.Model(&dbgen.FullTable{}).Count(&count)
	if result.Error != nil {
		return "", 0, result.Error
	}

	jsonStr, err := json.Marshal(list)
	if err != nil {
		return "", 0, err
	}
	return string(jsonStr), count, nil
}
