package model

import (
	"encoding/json"

	"github.com/Query-Web3/backend/model/dbgen"
)

func Yields() (string, error) {
	list := []dbgen.MultipleYield{}
	result := DB.Find(&list)
	if result.Error != nil {
		return "", result.Error
	}

	jsonStr, err := json.Marshal(list)
	if err != nil {
		return "", err
	}
	return string(jsonStr), nil
}

type YieldItem struct {
	Token string  `json:"token"`
	Apy   float64 `json:"apy"`
	Tvl   float64 `json:"tvl"`
	Price float64 `json:"price"`
}
